import spacy
import pandas

if __name__ == "__name__":
    spacy.prefer_gpu()
    # Don't need NER pipeline
    nlp = spacy.load("en_core_web_md", disable=['ner'])

    title_df = pandas.read_csv("data/askreddit_titles_2019_08.csv")

    # Consist of tuples of (row_id, noun lemma) so it's possible to find sentence the noun is from
    found_nouns = []

    for row_id, title in title_df.itertuples():
        doc = nlp(title)
        for token in doc:
            if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
                found_nouns.append((row_id, token.lemma_))

    nouns_df = pandas.DataFrame(found_nouns, columns=['id', 'noun'])
    nouns_df.to_csv("data/found_nouns.csv", index=False)
