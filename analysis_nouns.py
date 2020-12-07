import collections
import find_nouns
import datetime

#peusdo_stem_words = set(["reddit", "redditor", "people", "life", "story", "time", "person", "thing", "way"])

def time_bin(titles, start_time, bin_length=86400):
    # Bins titles by created_utc. Does this in chunks of bin_length which is utc in day_length by default
    # Returns a dict with a list of row_id in that bin_length
    # Keys are ints showcasing how far that bin is from start_time
    bin = collections.defaultdict(list)
    for row_id, _, created_utc in titles:
        day = (int(created_utc)-start_time)//bin_length
        bin[day].append(row_id)
    return bin

def counter_bin(titles_bin, nouns):
    # Takes in titles binned and counts all the nouns in the titles
    # Returns a dict with count of all of the nouns
    # Keys are the same as the bin key in titles_bin
    noun_lookup = collections.defaultdict(list)
    for row_id, noun in nouns:
        #if noun.lower() not in peusdo_stem_words:
        noun_lookup[row_id].append(noun.lower())

    bin_count = collections.defaultdict(collections.Counter)
    for bin, titles in titles_bin.items():
        for title in titles:
            bin_count[bin].update(noun_lookup[str(title)])
    return bin_count
    
def print_day_common_nouns(counter_bin, start_time, n=5):
    # Prints most common nouns from bins
    for day, counter in counter_bin.items():
        print(datetime.date.fromtimestamp(start_time + day*86400))
        for noun, count in counter.most_common(n):
            print('\t', noun, ":", count)

if __name__ == "__main__":
    titles = find_nouns.read_titles(n=None)
    nouns = find_nouns.read_nouns("data/found_nouns_all.csv")

    start_time = min(int(title[2]) for title in titles)
    titles_bin = time_bin(titles, start_time)

    counter_bin = counter_bin(titles_bin, nouns)

    print_day_common_nouns(counter_bin, start_time)