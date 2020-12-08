import collections
import find_nouns

import datetime
from find_nouns import Title, Noun
from typing import List, Dict, Set, Counter

CountNouns = Counter[str]
DAY_LENGTH = 86400
WEEK_LENGTH = 604800

class TitleCount:
    def __init__(self, titles, nouns, length, remove_words=None):
        self.start_time = min(int(title[2]) for title in titles)
        self.titles = titles
        self.nouns = nouns

        self.update_titles(length)
        self.count_nouns(remove_words)
    
    def update_titles(self, length):
        # Updates groups_titles with new groups of a timespan of length
        # Length should a timeperiod in seconds such as the length of a day in seconds, 86400
        self.group_titles = collections.defaultdict(list)
        self.length = length
        for row_id, _, created_utc in self.titles:
            offset = (int(created_utc)-self.start_time)//self.length
            self.group_titles[offset].append(row_id)
    
    def count_nouns(self, remove_words=None):
        # Updates group_count_nouns with new counts of nouns within that group
        # Remove_words is a set of words to remove from the count. Meant for very common words
        if not remove_words:
            remove_words = set()
        
        # Create noun lookup
        noun_lookup = collections.defaultdict(list)
        for row_id, noun in self.nouns:
            if noun.lower() not in remove_words:
                noun_lookup[row_id].append(noun.lower())

        # Create a dict to quickly add counts to a grouping
        self.group_count_nouns = collections.defaultdict(collections.Counter)
        for group, titles in self.group_titles.items():
            for title in titles:
                self.group_count_nouns[group].update(noun_lookup[title])
 
    def print_count(self, n=10):
        # Prints out the top N most common words in a group
        for group in sorted(self.group_count_nouns):
            # Convert the groups into readable timestamps
            print(datetime.date.fromtimestamp(self.start_time + group*self.length))
            for noun, count in self.group_count_nouns[group].most_common(n):
                print('\t', noun, ":", count)

if __name__ == "__main__":
    titles = find_nouns.read_titles("data/askreddit_titles_entire_month.csv", n=None)
    nouns = find_nouns.read_nouns("data/found_nouns_all.csv")
    print("found titles:", len(titles), ", found nouns:", len(nouns))

    title_count = TitleCount(titles, nouns, WEEK_LENGTH)
    common_words = set(["reddit", "redditor", "people", "life", "story", "time", "person", "thing", "way"])

    print("Results with common words")
    title_count.print_count()
    print("Results without common words")
    title_count.count_nouns(common_words)
    title_count.print_count()
    print("Daily results")
    title_count.update_titles(DAY_LENGTH)
    title_count.print_count()
 
