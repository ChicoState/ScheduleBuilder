import nltk
import re
import os
import datetime
from collections import Counter
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


class assignment_parser:
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.stop_words_path = "core\custom_stopwords.txt"
        self.word_count = None
        self.class_name = ""
        self.assignment_title = file_name
        self.word_tokens = ""
        self.assignment_description = ""
        self.due_date = ""
        self.parsed_elements = []

    def read_and_tokenize_words(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            self.word_tokens = nltk.word_tokenize(text)
            tokens_filtered = [word.lower() for word in self.word_tokens if word.isalpha()]
            return tokens_filtered

    def remove_stop_words(self, tokens):
        with open(self.stop_words_path, 'r', encoding='utf-8') as stop_word_file:
            stop_words = set(line.strip() for line in stop_word_file)
            return [word for word in tokens if word not in stop_words]

    def count_words(self):
        tokens_filtered = self.read_and_tokenize_words()
        tokens_filtered = self.remove_stop_words(tokens_filtered)
        self.word_count = Counter(tokens_filtered)
        
    def extract_class_name_from_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            class_name_pattern = r'\b[a-z]{4} \d{3}\b'
            match = re.search(class_name_pattern, text, re.IGNORECASE)
            if match:
                self.class_name = match.group()
                self.parsed_elements.append(self.class_name)
                
    def extract_description_from_file(self):
        #unfinished, weird formatting from how we tokenize sentences from the text. 
        bullet_pattern = r'^\s*[\u2022*\-+]\s+'
        word_freq = self.word_count
        max_freq = word_freq.most_common(1)[0][1]
        word_freq = {word: word_freq[word] / max_freq for word in word_freq}
        sent_scores = {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            sent_tokens = nltk.sent_tokenize(text)
            sent_filtered = [sent.lower() for sent in sent_tokens]
            for sent in sent_tokens:
                if any(element in sent for element in self.parsed_elements):
                    continue
                if len(sent.split(' ')) < 30:
                    sent = re.sub(bullet_pattern, '', sent)
                    sent = re.sub(r'http\S+', '', sent)
                    sent = re.sub(r'\x0c', 'fi', sent)
                    for word in nltk.word_tokenize(sent):
                        if word in word_freq:
                            if sent not in sent_scores.keys():
                                sent_scores[sent] = word_freq[word]
                            else:
                                sent_scores[sent] += word_freq[word]
        top_sents = Counter(sent_scores).most_common(5)               
        assignment_description = ' '.join(sent.strip() for sent, _ in top_sents)
        self.assignment_description = assignment_description
        
    def standardize_date_format(self):
        _date = parse(self.due_date)
        time = _date.time()
        if (time.hour == 0 and time.minute == 0 and time.second == 0):
            self.due_date = _date + relativedelta(hour=23,minute=59)
        else:
            self.due_date = _date
        
    def extract_due_date_from_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            due_date_pattern = r'Due:? ([Bb]y)?(.*?)\n'
            match = re.search(due_date_pattern, text, re.DOTALL)
            if match:
                self.due_date = match.group(2).strip()
        
    def get_parsed_contents(self):
        return {
            'class_name': self.class_name,
            'assignment_title': self.assignment_title,
            'assignment_description': self.assignment_description,
            'due_date': self.due_date,
            'word_count': self.word_count
        }
                    
    def process_assignment(self):
        self.extract_class_name_from_file()
        self.extract_due_date_from_file()
        self.count_words()
        self.extract_description_from_file()
