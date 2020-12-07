import collections
import find_nouns

def most_common_nouns(nouns, n=100):
    counter = collections.Counter()

    for _, noun in nouns:
        counter[str(noun).lower()] += 1
    
    for noun, count in counter.most_common(n):
        print(noun, '\t', count)

def time_bin(titles, bin_length=86400):
    # Bins titles by created_utc. Does this in chunks of bin_length which is utc in day_length by default
    start_time = min(int(title[2]) for title in titles)
    bin = collections.defaultdict(list)
    for row_id, _, created_utc in titles:
        day = (int(created_utc)-start_time)//bin_length
        bin[day].append(row_id)
    return bin

if __name__ == "__main__":
    titles = find_nouns.read_titles()

    print(time_bin(titles))