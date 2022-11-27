import spacy
import re
import json
from tqdm import tqdm
import pandas as pd

## 다음처럼 spacy에서 내가 원하는 언어의 모델을 가져오고,
nlp = spacy.load('en_core_web_sm')

MULTIPLE_SPACES = re.compile(' {2,}', re.UNICODE)
NON_ENGLISH = re.compile('[^a-zA-Z]', re.UNICODE)


# Sample text
text = """Success isn't easy, and that's a good thing - at least in business. If it was easy, everybody would be doing it and your competition would be outrageous!"""
# returns doc container with many attributes.
doc = nlp(text)
lemmatizer = nlp.get_pipe("lemmatizer")
print([token.lemma_ for token in doc])


# loop through doc and return tokens with .text attribute
# using list comprehension
sentence_seg = [sent.text for sent in doc.sents]
sentence_seg = [sent.text for sent in filtered_sentence.sents]
tokenized = [token.text for token in doc]

from spacy.lang.en.stop_words import STOP_WORDS
# Create list of word tokens after removing stopwords
filtered_sentence =[]

for word in tokenized:
    lexeme = nlp.vocab[word]
    if lexeme.is_stop == False:
        filtered_sentence.append(word)

filtered_sentence = ' '.join(filtered_sentence)
filtered_sentence = nlp(filtered_sentence)
filtered_sentence = re.sub(NON_ENGLISH, ' ', filtered_sentence)
filtered_sentence = re.sub(MULTIPLE_SPACES, ' ', filtered_sentence)
filtered_sentence = filtered_sentence.strip()
filtered_sentence = nlp(filtered_sentence)

lemma_word1 = [token.lemma_ for token in filtered_sentence]



def average_sent_len(document):
    """
    Average sentence length calculator
    :param sentence_seg: list containing segregated sentences
    :return: mean value of sentence length in a document
    """
    sents = nlp(document).sents
    sent_seg = [sent.text for sent in sents]
    word_list, sent_list = [], []

    for sent in sent_seg:
        sent = re.sub(NON_ENGLISH, ' ', sent)
        sent = re.sub(MULTIPLE_SPACES, ' ', sent)
        sent = sent.strip()
        word_list.extend(sent.split())
        sent_list.append(sent.split())

    word_count, sent_count = len(word_list), len(sent_list)

    return float(word_count/sent_count)

with open('./data/factcheckorg.json') as f:
    factcheckorg_dict = json.load(f)
url_list = [factcheckorg_dict[str(i)]['url'] for i in range(len(factcheckorg_dict))]
date_list = [factcheckorg_dict[str(i)]['date'] for i in range(len(factcheckorg_dict))]
author_list = [', '.join(factcheckorg_dict[str(i)]['author']) for i in range(len(factcheckorg_dict))]
issue_list = [', '.join(factcheckorg_dict[str(i)]['issue']) for i in range(len(factcheckorg_dict))]
title_list = [factcheckorg_dict[str(i)]['title'] for i in range(len(factcheckorg_dict))]
content_list = [factcheckorg_dict[str(i)]['content'] for i in range(len(factcheckorg_dict))]

df_factcheckorg = pd.DataFrame({'url': url_list, 'date': date_list, 'author': author_list, 'issue': issue_list, 'title': title_list, 'content': content_list})
df_factcheckorg.to_csv('factcheckorg.csv', index=False)
df_factcheckorg = pd.DataFrame()

with open('./politifact.json') as f:
    politifact_dict = json.load(f)

url_list = [politifact_dict[str(i)]['url'] for i in range(len(politifact_dict))]
date_list = [politifact_dict[str(i)]['date'] for i in range(len(politifact_dict))]
author_list = [', '.join(politifact_dict[str(i)]['author']) for i in range(len(politifact_dict))]
issue_list = [', '.join(politifact_dict[str(i)]['category']) for i in range(len(politifact_dict))]
title_list = [politifact_dict[str(i)]['title'] for i in range(len(politifact_dict))]
content_list = [politifact_dict[str(i)]['content'] for i in range(len(politifact_dict))]
df_politifact = pd.DataFrame({'url': url_list, 'date': date_list, 'author': author_list, 'issue': issue_list, 'title': title_list, 'content': content_list})
df_politifact.to_csv('politifact.csv', index=False)

content_list = [factcheckorg_dict[str(i)]['content'] for i in tqdm(range(factcheckorg_dict_len))]
mean_sent_len = [average_sent_len(content) for content in tqdm(content_list)]
mean_sent_len

from textstat import automated_readability_index

processed_content = []
for i in tqdm(range(factcheckorg_dict_len)):
    text = factcheckorg_dict[str(i)]['content']
    text = nlp(text)
    text = [token.lemma_ for token in text]
    filtered = []
    for word in text:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered.append(word)
    text = ' '.join(text).lower()
    text = re.sub(NON_ENGLISH, ' ', text)
    text = re.sub(MULTIPLE_SPACES, ' ', text)
    text = text.strip()
    processed_content.append(text)

automated_readability_index(processed_content[0])

automated_readability_index(factcheckorg_dict['0']['content'])

ari = [automated_readability_index(content) for content in processed_content]
ari_new = [automated_readability_index(factcheckorg_dict[str(i)]['content']) for i in range(len(factcheckorg_dict))]

import math

ari_new

