import collections
import find_nouns

peusdo_stem_words = set(["reddit", "redditor", "people", "life", "story", "time", "person", "thing", "way"])

def time_bin(titles, start_time, bin_length=86400):
    # Bins titles by created_utc. Does this in chunks of bin_length which is utc in day_length by default
    bin = collections.defaultdict(list)
    for row_id, _, created_utc in titles:
        day = (int(created_utc)-start_time)//bin_length
        bin[day].append(row_id)
    return bin

def counter_bin(titles_bin, nouns):
    noun_lookup = collections.defaultdict(list)
    for row_id, noun in nouns:
        if noun.lower() not in peusdo_stem_words:
            noun_lookup[row_id].append(noun.lower())

    bin_count = collections.defaultdict(collections.Counter)
    for bin, titles in titles_bin.items():
        for title in titles:
            bin_count[bin].update(noun_lookup[str(title)])
    return bin_count
    

if __name__ == "__main__":
    titles = find_nouns.read_titles()
    nouns = find_nouns.read_nouns()


    start_time = min(int(title[2]) for title in titles)
    titles_bin = time_bin(titles, start_time)

    counter_bin = counter_bin(titles_bin, nouns)

    for day, counter in counter_bin.items():
        print(day, counter.most_common(10))