import collections
import find_nouns

def most_common_nouns(nouns, n=100):
    counter = collections.Counter()

    for _, noun in nouns:
        counter[str(noun).lower()] += 1
    
    for noun, count in counter.most_common(n):
        print(noun, '\t', count)

if __name__ == "__main__":
    nouns = find_nouns.read_nouns()

    most_common_nouns(nouns)
    