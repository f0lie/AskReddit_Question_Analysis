import spacy
import csv

def read_titles(file_name: str, n=100000) -> [(str,str,str)]:
    # Read titles from a csv file at file_name.
    # n is the number of rows to return. Passing n=None reads the entire file
    # Returns list of (row_id, title, created_utc)
    titles = []
    i = 0
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for title, created_utc in csv_reader:
            if i == n:
                break
            titles.append((str(i), title, created_utc))
            i += 1
    return titles[1:]

def read_nouns(file_name: str) -> [(str,str)]:
    # Read nouns from a csv file at file_name
    # Returns a list of (row_id, noun). Row_id refers to the original sentence the noun was found at.
    nouns = []
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row_id, noun in csv_reader:
            nouns.append((row_id, noun))
    return nouns

def find_nouns(nlp, titles: [(str,str,str)], file_name: str) -> None:
    # Takes in spacy pipeline, titles, and writes to a csv file at file_name
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['row_id', 'noun'])
        for row_id, title, _ in titles:
            doc = nlp(title)
            for token in doc:
                if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
                    writer.writerow((row_id, token.lemma_))

if __name__ == "__main__":
    spacy.prefer_gpu()
    # Don't need NER pipeline
    nlp = spacy.load("en_core_web_md", disable=['ner'])

    print('Reading titles')
    titles = read_titles("data/askreddit_titles_entire_month.csv", n=None) 
    print("Titles loaded")

    print("Finding nouns")
    find_nouns(nlp, titles, "data/found_nouns_all.csv")
    print("Nouns found")
