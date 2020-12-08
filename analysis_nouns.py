import collections
import find_nouns

import datetime
from find_nouns import Title, Noun
from typing import List, Dict, Set, Counter

CountNouns = Counter[str]
DAY_LENGTH = 86400
WEEK_LENGTH = 604800

def group_titles(titles: List[Title], start_time: int, length: int=WEEK_LENGTH) -> Dict[int, List[str]]:
    # Group titles by created_utc. Does this in chunks of length which is utc in day by default
    # Returns a dict with a list of row_id in that bin_length
    # Keys are ints showcasing how far that bin is from start_time
    bin = collections.defaultdict(list)
    for row_id, _, created_utc in titles:
        day = (int(created_utc)-start_time)//length
        bin[day].append(row_id)
    return bin

def group_count_nouns(titles_bin: Dict[int, List[str]], nouns: List[Noun], common_words: Set[str]=None) -> Dict[int, CountNouns]:
    # Takes in titles binned and counts all the nouns in the titles
    # Returns a dict with count of all of the nouns
    # Keys are the same as the bin key in titles_bin
    if not common_words:
        common_words = set()

    noun_lookup = collections.defaultdict(list)
    for row_id, noun in nouns:
        if noun.lower() not in common_words:
            noun_lookup[row_id].append(noun.lower())

    bin_count: Dict[int, CountNouns] = collections.defaultdict(collections.Counter)
    for bin, titles in titles_bin.items():
        for title in titles:
            bin_count[bin].update(noun_lookup[title])
    return bin_count
    
def print_count_nouns(counter_bin: Dict[int, CountNouns], start_time: int, length: int=WEEK_LENGTH, n: int=10) -> None :
    # Prints most common nouns from bins. Start_time and length is there to correctly output dates
    for bin in sorted(counter_bin):
        print(datetime.date.fromtimestamp(start_time + bin*length))
        for noun, count in counter_bin[bin].most_common(n):
            print('\t', noun, ":", count)

if __name__ == "__main__":
    titles = find_nouns.read_titles("data/askreddit_titles_entire_month.csv", n=None)
    nouns = find_nouns.read_nouns("data/found_nouns_all.csv")

    start_time = min(int(title[2]) for title in titles)
    titles_bin = group_titles(titles, start_time)

    common_words = set(["reddit", "redditor", "people", "life", "story", "time", "person", "thing", "way"])
    no_common_counter_bin = group_count_nouns(titles_bin, nouns, common_words)
    all_counter_bin = group_count_nouns(titles_bin, nouns)

    print("Results without common words.")
    print_count_nouns(no_common_counter_bin, start_time)
    print("Results with common words.")
    print_count_nouns(all_counter_bin, start_time)

    print("Results with daily bins")
    titles_bin = group_titles(titles, start_time, length=DAY_LENGTH)
    count_week = group_count_nouns(titles_bin, nouns)

    print_count_nouns(count_week, start_time, length=DAY_LENGTH)