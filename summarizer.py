# -*- coding: utf-8 -*-
 
import re
import nltk
from nltk import * 

count=0
final_summary=""
final_text=""

def summary(text):
    global final_text,final_summary,count
    final_summary=""
    full_content=""
    word_freq={}
    sent_score={}


    full_content=text
    
    #Text cleaning using regular expressions
    
    text_content=re.sub(r'\[[0-9]*\]',' ',full_content)
    final_text=re.sub(r'\s+',' ',text_content)
    final_text=re.sub(r'\[[a-zA-Z]*\]',' ',final_text)
    final_text=re.sub(r'\s+',' ',final_text)
    final_text=re.sub(r'\(([^)]*)\)',' ',final_text)
    final_text=re.sub(r'\s+',' ',final_text)
    

    #Sentence tokenizations & Word tokenization
    
    sentences_text=nltk.sent_tokenize(final_text)
    words_text=nltk.word_tokenize(final_text)
    
    #Stop words Removal & Calculatin the word frequency
    
    sw=corpus.stopwords.words("english")
    
    for word in words_text:
         if word not in sw:
             if word not in word_freq.keys():
                  word_freq[word]=1
             else:
                 word_freq[word]+=1
    
    word_freq_max= max(word_freq.values())
    
    
    for word in word_freq.keys():
            word_freq[word]=(word_freq[word]/word_freq_max)
            
    # Generating the Relevant and important sentences
            
    for sentence in sentences_text:
        if len(sentence.split(" ")) < 25:
            for word in nltk.word_tokenize(sentence.lower()):
                if word not in word_freq.keys():
                    pass;
                else:
                    if sentence not in sent_score.keys():
                        sent_score[sentence]=word_freq[word]
                    else:
                        sent_score[sentence]+=word_freq[word]
    
    
    #final_summary=heapq.nlargest(5,sent_score,key=sent_score.get)
    
    #setting a threshold for considering the important sentences
    threshold=(max(sent_score.values()))/2
    
    for sentence in sent_score.keys():
        if(sent_score[sentence]>=threshold):
            final_summary += sentence
            count +=1
    

    
    #Returing the final Summary to UI
    
    return final_summary

def compare():
    original_sent = nltk.sent_tokenize(final_text)
    original_words = nltk.word_tokenize(final_text)
    original_read_time = len(original_words)/200           #on average an adult reads 200- 250 words per minute
    
    return original_sent,original_words,original_read_time
                               
    