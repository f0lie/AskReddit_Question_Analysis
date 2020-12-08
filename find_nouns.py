import spacy
import csv
from typing import List, Tuple

Sentence = Tuple[str,str,str]
Noun = Tuple[str,str]

def read_sentences(file_name: str, n=100000) -> List[Sentence]:
    # Read sentences from a csv file at file_name.
    # n is the number of rows to return. Passing n=None reads the entire file
    # Returns list of (row_id, sentence, created_utc)
    sentences = []
    i = 0
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for sentence, created_utc in csv_reader:
            if i == n:
                break
            sentences.append((str(i), sentence, created_utc))
            i += 1
    return sentences[1:]

def read_nouns(file_name: str) -> List[Noun]:
    # Read nouns from a csv file at file_name
    # Returns a list of (row_id, noun). Row_id refers to the original sentence the noun was found at.
    nouns = []
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row_id, noun in csv_reader:
            nouns.append((row_id, noun))
    return nouns

def find_nouns(nlp, sentences: List[Sentence], file_name: str) -> None:
    # Takes in spacy pipeline, sentences, and writes to a csv file at file_name
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['row_id', 'noun'])
        for row_id, sentence, _ in sentences:
            doc = nlp(sentence)
            for token in doc:
                if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
                    writer.writerow((row_id, token.lemma_))

if __name__ == "__main__":
    spacy.prefer_gpu()
    # Don't need NER pipeline
    nlp = spacy.load("en_core_web_md", disable=['ner'])

    print('Reading sentences')
    sentences = read_sentences("data/askreddit_sentences_entire_month.csv", n=None) 
    print("Sentences loaded")

    print("Finding nouns")
    find_nouns(nlp, sentences, "data/found_nouns_all.csv")
    print("Nouns found")
