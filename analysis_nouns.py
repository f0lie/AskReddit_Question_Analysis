import collections
import find_nouns

import datetime
from find_nouns import Sentence, Noun
from typing import List, Dict, Set, Counter

CountNouns = Counter[str]
DAY_LENGTH = 86400
WEEK_LENGTH = 604800

class NounCount:
    def __init__(self, sentences: List[Sentence], nouns: List[Noun], length: int, remove_words=None):

        # The mininum timestamp for all of the sentences, used for grouping them by time
        self.start_time = min(int(sentence[2]) for sentence in sentences)
        self.sentences = sentences # Contains all of the sentence data
        self.nouns = nouns # Contains all of the found nouns in the sentences

        self.update_sentences(length) # Creates self.group_sentences and self.length
        self.count_nouns(remove_words) # Creates self.group_count_nouns
    
    def update_sentences(self, length: int):
        # Updates groups_sentences with new groups of sentences seperated by a timespan of length
        # Length should a timeperiod in seconds such as the length of a day in seconds, 86400
        self.group_sentences: Dict[int, List[str]] = collections.defaultdict(list)
        self.length = length
        for row_id, _, created_utc in self.sentences:
            offset = (int(created_utc)-self.start_time)//self.length
            self.group_sentences[offset].append(row_id)
    
    def count_nouns(self, remove_words: Set[str]=None):
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
        self.group_count_nouns: Dict[int, Counter] = collections.defaultdict(collections.Counter)
        for group, sentences in self.group_sentences.items():
            for sentence in sentences:
                self.group_count_nouns[group].update(noun_lookup[sentence])
 
    def print_count(self, n=10):
        # Prints out the top N most common words in a group
        for group in sorted(self.group_count_nouns):
            # Convert the groups into readable timestamps
            print(datetime.date.fromtimestamp(self.start_time + group*self.length))
            for noun, count in self.group_count_nouns[group].most_common(n):
                print('\t', noun, ":", count)

if __name__ == "__main__":
    sentences = find_nouns.read_sentences("data/askreddit_titles_entire_month.csv", n=None)
    nouns = find_nouns.read_nouns("data/found_nouns_all.csv")
    print("found sentences:", len(sentences), ", found nouns:", len(nouns))

    sentence_count = NounCount(sentences, nouns, WEEK_LENGTH)
    common_words = set(["reddit", "redditor", "people", "life", "story", "time", "person", "thing", "way"])

    print("Results with common words")
    sentence_count.print_count()
    print("Results without common words")
    sentence_count.count_nouns(common_words)
    sentence_count.print_count()
    print("Daily results")
    sentence_count.update_sentences(DAY_LENGTH)
    sentence_count.print_count()
 
