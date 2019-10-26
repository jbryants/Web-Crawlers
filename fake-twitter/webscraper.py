from bs4 import BeautifulSoup
import requests
import json

# Set the url, pass a get request giving url as param, based on the response recieved parse the html doc
url = 'http://ethans_fake_twitter_site.surge.sh/'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

# Initializing tweetArr for storing dict having scraped data
tweetArr = []

# Storing the contents of two div containers having different class names.
tweet_cont = content.findAll('div', attrs={"class": "tweetcontainer"})
tweet_hDiv = content.findAll('div', attrs={"class": "horizontalDivider"})

# Iterating over the contents to get the sub elements separately.
for t_cont, hDiv in zip(tweet_cont, tweet_hDiv):
    # Obtaining the html element-wise content separately and storing them in a dict
    tweetObject = {
            "author": t_cont.find('h2', attrs={"class": "author"}).text.encode('utf-8').decode('utf-8'),
            "date": t_cont.find('h5', attrs={"class": "dateTime"}).text.encode('utf-8').decode('utf-8'),
            "tweet": t_cont.find('p', attrs={"class": "content"}).text.encode('utf-8').decode('utf-8')
    }
    tweetObject["likes"] = hDiv.find('p', attrs={"class": "likes"}).text.encode('utf-8').decode('utf-8')
    tweetObject["shares"] = hDiv.find('p', attrs={"class": "shares"}).text.encode('utf-8').decode('utf-8')
    
    # Appending the dict content obtained to tweetArr
    tweetArr.append(tweetObject)

# Saving the data in json format.
with open('twitterData.json', 'w') as outfile:
    json.dump(tweetArr, outfile)
