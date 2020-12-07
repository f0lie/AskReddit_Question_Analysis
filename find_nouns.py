import spacy
import pandas
import csv

def read_titles(file_name='data/askreddit_titles_entire_month.csv', n=100000):
    titles = []
    i = 0
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for title, created_utc in csv_reader:
            if i == n:
                break
            titles.append((i, title, created_utc))
            i += 1
    return titles

def write_nouns(found_nouns, file_name='data/found_nouns.csv'):
    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['row_id', 'noun'])
        writer.writerows(found_nouns)

    

if __name__ == "__main__":
    spacy.prefer_gpu()
    # Don't need NER pipeline
    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    titles = read_titles(n=10) 

    # Consist of tuples of (row_id, noun lemma) so it's possible to find sentence the noun is from
    found_nouns = []

    for row_id, title, _ in titles:
        doc = nlp(title)
        for token in doc:
            if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
                found_nouns.append((row_id, token.lemma_))

    write_nouns(found_nouns)
        