# News Snap

News Snap is 
a web app located at [http://newssnap.press]() 

### Repository Structure

- `runapp.py`: main application
- `flaskapp`: application module
    - `__init__.py`
    - `views.py`: primary flask function for generating web app
    - `main.py`: contains mian functions (findTopics) for extracting the main topics from a corpus of news articles
    - `functions.py`: contains simple auxiliary functions called by views.py and main.py
    - `static`: contains standard bootstrap files for creating the website
    - `templates`: contains the HTML files for the different pages (tabs) within website
    
### Data

Here is a rough overview of the database structure for reference, since access to the database is not provided.

