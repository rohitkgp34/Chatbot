import numpy as np 
import tensorflow as tf
import time
import re

lines = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

# Creating a dictionary that maps each line and its id
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]

# Create a list of all of the conversations' lines' ids.
conversations_ids =[]
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations_ids.append(_conversation.split(','))
    
# Sort the sentences into questions (inputs) and answers (targets)
questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])

# Just for checking
print(len(conversations_ids))
print(conversation[0])
print(id2line[conversation[0]])

# Compare lengths of questions and answers
print(len(questions))
print(len(answers))

# Clean text by removing unnecessary characters and altering the format of words
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "that is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"n'", "ng", text)
    text = re.sub(r"'bout", "about", text)
    text = re.sub(r"'til", "until", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    return text

# Cleaning of questions
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))
    
# Cleaning of answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))

# Create a dictionary for the frequency of the each word in que and ans
word2count = {}
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
# Creating two dictionaries that map the questions words and the answers words to a unique integer
threshold = 20
questionswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number += 1
answerswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        answerswords2int[word] = word_number
        word_number += 1
  
# Check      
if (questionswords2int == answerswords2int):
    print('true')
else:
    print('false')
    
# Adding the last tokesn to the above dictinary
tokens = ['<PAD>','<EOS>','<OUT>','SOS']
for token in tokens:
    questionswords2int[token] = len(questionswords2int) + 1
for token in tokens:
    answerswords2int[token] = len(answerswords2int) + 1

# Creating the inverse dict of answerswords2int
answersint2words = {w_i : w for w, w_i in answerswords2int.items()}

# Adding the EOS token to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'
    
# Translating all the ques and ans list int o integers and
# Replacing the all the filtered out words with <EOS> token
questions_into_int = []
for question in clean_questions:
    ints = []
    for word in question:
        if word not in questionswords2int:
            ints.append(questionswords2int['<EOS>'])
        else:
            ints.append(questionswords2int[word])
    questions_into_int.append(ints)
            
answers_into_int = []
for answer in clean_answers:
    ints = []
    for word in answer:
        if word not in answerswords2int:
            ints.append(answerswords2int['<EOS>'])
        else:
            ints.append(answerswords2int[word])
    answers_into_int.append(ints)
    
# Sorting the que and qns a/c to the lenght of question
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 25+1):
    for i in enumerate(questions_into_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_into_int[i[0]])
            sorted_clean_answers.append(answers_into_int[i[0]])
