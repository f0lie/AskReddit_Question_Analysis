import collections
import find_nouns

import datetime
from find_nouns import Title, Noun
from typing import List, Dict, Set, Counter

CountNouns = Counter[str]
DAY_LENGTH = 86400
WEEK_LENGTH = 604800

def group_titles(titles: List[Title], start_time: int, length: int=WEEK_LENGTH) -> Dict[int, List[str]]:
    # Group titles by created_utc. Does this in chunks of length, defaults to week length. start_time should be the smallest timestamp
    # Returns a dict with keys as the group and the value as a list of row_ids in that group
    group_titles = collections.defaultdict(list)
    for row_id, _, created_utc in titles:
        # Subtract start_time from created_utc and divded by length to create offsets that are the groups
        offset = (int(created_utc)-start_time)//length
        group_titles[offset].append(row_id)
    return group_titles

def group_count_nouns(group_titles: Dict[int, List[str]], nouns: List[Noun], common_words: Set[str]=None) -> Dict[int, CountNouns]:
    # Takes in grouped titles and counts all of the nouns with Counter. If a noun is in common_words, then it's removed from count.
    # Returns a dict with keys as the group and the values as Counters of that group
    if not common_words:
        common_words = set()

    # Create dict to quickly lookup the nouns that a question has
    noun_lookup = collections.defaultdict(list)
    for row_id, noun in nouns:
        if noun.lower() not in common_words:
            noun_lookup[row_id].append(noun.lower())

    # Create a dict to quickly add counts to a grouping
    group_count: Dict[int, CountNouns] = collections.defaultdict(collections.Counter)
    for group, titles in group_titles.items():
        for title in titles:
            group_count[group].update(noun_lookup[title])
    return group_count
    
def print_count_nouns(group_counter: Dict[int, CountNouns], start_time: int, length: int=WEEK_LENGTH, n: int=10) -> None :
    # Prints most common nouns from bins. Length and start_time need to match the ones that created the group countings.
    for group in sorted(group_counter):
        # Convert the groups into readable timestamps
        print(datetime.date.fromtimestamp(start_time + group*length))
        for noun, count in group_counter[group].most_common(n):
            print('\t', noun, ":", count)

if __name__ == "__main__":
    titles = find_nouns.read_titles("data/askreddit_titles_entire_month.csv", n=None)
    nouns = find_nouns.read_nouns("data/found_nouns_all.csv")
    print("found titles:", len(titles), ", found nouns:", len(nouns))

    # This is used to create offsets for the groupings. Allows for very fast grouping.
    start_time = min(int(title[2]) for title in titles)
    weekly_titles = group_titles(titles, start_time)

    # These words show up very often in the result and don't say much so I removed them here.
    common_words = set(["reddit", "redditor", "people", "life", "story", "time", "person", "thing", "way"])
    no_common_count = group_count_nouns(weekly_titles, nouns, common_words)
    all_count = group_count_nouns(weekly_titles, nouns)

    print("Results with common words.")
    print_count_nouns(all_count, start_time)
    print("Results without common words.")
    print_count_nouns(no_common_count, start_time)

    print("Results with daily bins")
    daily_titles = group_titles(titles, start_time, length=DAY_LENGTH)
    daily_count = group_count_nouns(daily_titles, nouns)

    print_count_nouns(daily_count, start_time, length=DAY_LENGTH)