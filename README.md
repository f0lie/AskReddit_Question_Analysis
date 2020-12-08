# AskReddit Question Analysis

The main idea of this project is to find out what people on reddit is talking about. This is mainly done through counting the nouns in every question of AskReddit.

## Setup for project

```python
# Directly from spacy's website
python -m venv .env
.env\Scripts\activate
pip install -U spacy

# For some reason numpy has a glitch that breaks downloading things
pip uninstall numpy
pip install numpy==1.19.3

python -m spacy download en_core_web_md
```

## Running the project

You need a file csv file of two columns that contains the text itself and the UNIX timestamp of it's creation. `askreddit_titles_entire_month.csv` contains all of the questions on AskReddit for the month of August 2019 since that's what BigQuery had.

Running `python find_nouns.py` outputs a csv file to `data` that contains all of the nouns in the Reddit data csv file. This will take a long time. For the included dataset, it took around 30 minutes to completely run.

Running `python analysis_nouns.py` outputs to the terminal the count of nouns over timespan. You need to make sure that the noun file and the Reddit data file together since to output things correctly, the algorithm uses both files. It is possible to just run `analysis_nouns.py` because I included all of the data in the github itself. But if you want to use a new set of data, you need to keep this in mind.

Output looks something like this:

```txt
2019-07-31
         reddit : 16464
         people : 11624
         thing : 9777
         life : 5512
         time : 4492
         story : 3355
         way : 3078
         redditor : 2752
         movie : 2744
         person : 2398
2019-08-07
         reddit : 17672
         people : 12930
         thing : 10179
         life : 5304
         time : 4272
         story : 3486
         redditor : 3225
         way : 2734
         movie : 2604
         game : 2599
2019-08-14
         reddit : 17419
         people : 12207
         thing : 10047
         life : 5111
         time : 4382
         story : 3287
         way : 3034
         redditor : 2943
         movie : 2644
         game : 2427
2019-08-21
         reddit : 14058
         people : 11243
         thing : 9426
         life : 5719
         time : 4256
         way : 3115
         ....
```