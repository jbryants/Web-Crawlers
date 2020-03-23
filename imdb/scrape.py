from time import time, sleep
from requests import get
from random import randint
from IPython.core.display import clear_output
from bs4 import BeautifulSoup
import re
import pandas as pd

# Redeclaring the lists to store data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
pages = []

# Setting up values for headers, pages and years_url
headers = {"Accept-Language": "en-US, en;q=0.5"}
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2018,2020)]

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# Regex patterns we will need to clean the data
yearRegex = re.compile('\d{4}')
m_scoreRegex = re.compile('\d{1,3}')

# For every year in the interval specified
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page, headers = headers)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_ = 'inline-block ratings-metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
                try:
                    year = yearRegex.search(year).group()
                    print(year)
                    years.append(year)
                except:
                    print("Year match not found.")

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('div', class_='inline-block ratings-metascore').text
                try:
                    m_score = m_scoreRegex.search(m_score).group()
                    metascores.append(int(m_score))
                except:
                    print("Metascore match not found.")

                # Scrape the number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))


# Examining the scraped data
movie_ratings = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes
})
print(movie_ratings.info())
print(movie_ratings.head(10))
print(movie_ratings.tail(10))

movie_ratings.to_csv('movie_ratings.csv')
