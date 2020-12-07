# AskReddit Question Analysis

The main idea of this project is to find out what people on reddit is talking about. This is mainly done through finding nouns.

## Setup for project

```python
pip install pandas

# Directly from spacy's website
python -m venv .env
.env\Scripts\activate
pip install -U spacy

# For some reason numpy has a glitch that breaks downloading things
pip uninstall numpy
pip install numpy==1.19.3

python -m spacy download en_core_web_sm
```

## Running the project

`find_nouns.py` outputs nouns that spacy finds from the reddit dataset.