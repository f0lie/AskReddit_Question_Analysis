import spacy
import pandas
import csv

def read_titles(file_name='data/askreddit_titles_entire_month.csv', n=100000):
    # Read titles from CSV file
    # n is the number of rows
    titles = []
    i = 0
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for title, created_utc in csv_reader:
            if i == n:
                break
            titles.append((i, title, created_utc))
            i += 1
    return titles[1:]

def read_nouns(file_name='data/found_nouns.csv'):
    # Read nouns from noun file
    nouns = []
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row_id, noun in csv_reader:
            nouns.append((row_id, noun))
    return nouns


def write_nouns(found_nouns, file_name='data/found_nouns.csv'):
    # Write found nouns into a file
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['row_id', 'noun'])
        writer.writerows(found_nouns)

if __name__ == "__main__":
    spacy.prefer_gpu()
    # Don't need NER pipeline
    nlp = spacy.load("en_core_web_md", disable=['ner'])

    print('Reading titles')
    titles = read_titles(n=None) 
    print("Titles loaded")

    # Consist of tuples of (row_id, noun lemma) so it's possible to find sentence the noun is from
    found_nouns = []

    print("Finding nouns")
    with open("data/found_nouns_all.csv", 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['row_id', 'noun'])
        for row_id, title, _ in titles:
            doc = nlp(title)
            for token in doc:
                if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
                    writer.writerow((row_id, token.lemma_))
    print("Nouns found")
