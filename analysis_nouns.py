import pandas
import collections

if __name__ == "__main__":
    nouns_df = pandas.read_csv("data/found_nouns.csv")
    counter = collections.Counter()

    for noun in nouns_df['noun']:
        counter[str(noun).lower()] += 1
    
    print(counter.most_common(100))
    