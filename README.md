# News Snap

News Snap ([newssnap.press]( http://newssnap.press)) is an auto-curated daily news briefing provider designed to become an alternative to current human-generated daily news briefings (e.g. “The Skimm”, NY Times “Evening Briefing”, …). The current services tend to suffer from the inevitable political bias of the human curator, their news source or both. News Snap is intended to solve this problem by using a variety of news sources across the political spectrum and automatically identifying the main topics dominating the news. It does so by using the assumption that the number of articles written on a specific news event is a reliable indicator of how “important” the event is.

### Repository Structure

- `runapp.py`: main application
- `flaskapp`: application module
    - `__init__.py`
    - `views.py`: primary Flask function for generating web app
    - `main.py`: contains the main function (findTopics) for identifying the important topics within a corpus of news articles
    - `functions.py`: contains the auxiliary functions called by views.py and main.py
    - `templates`: contains the HTML files for the different pages (tabs) within website
    - `static`: contains the standard Bootstrap files website layout
    
### Data

The dataset used is a corpus of ~60,000 New York Times articles publised between March 15th 2016 and February 5th 2017.


### Algorithm overview

The algorithm used by News Snap starts by converting all the news articles available on a specific date into high-dimensional vectors by taking their [TF-IDF]( https://en.wikipedia.org/wiki/Tf-idf) vector representation. Content resemblance between any two articles can then be assessed by [cosine similarity]( https://en.wikipedia.org/wiki/Cosine_similarity) between their TF-IDF vectors. The cosine similarity measure is used as a distance metric in order to cluster together articles about similar topics using [hierarchical clustering]( https://en.wikipedia.org/wiki/Hierarchical_clustering). The largest clusters found are assumed to correspond to the important topics dominating the news. 
Each “important topic” is labeled with 5 keywords, identified as the 5 main dimensions (or terms, in TF-IDF space) represented in the cluster’s vectors. Also, for each important topic, News Snap returns the corresponding list of articles sorted by relevance. Relevance is determined by the average distance between a given article and all other articles in the cluster. Articles with shorter average distances are defined as more relevant, or more representative of the cluster/topic as a whole. 


### About the current version

For reasons related to access to past news data, News Snap in its current version uses The New York Times as its unique news source. This version is meant as a proof of concept to show that the underlying algorithm is indeed effective at automatically identifying major news events in the past. 
However, News Snap is really meant to work by sourcing articles from a variety of politically diverse news outlets. The adjustment needed to include other news sources is only a matter of obtaining access to the material published daily by other news outlets; only very minimal modifications to News Snap current algorithm should be necessary.  
