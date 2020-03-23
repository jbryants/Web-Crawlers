#! python3
# lucky.py - Opens several Google search results.
  
import webbrowser
import bs4
import requests
import sys
 
def my_func(search_str) :
    print('Googling...') # display text while downloading the Google page
    res = requests.get('http://google.com/search?source=' + ' '.join(search_str))
    print(res.raise_for_status())
  
    # Retreive top search result links.
    soup = bs4.BeautifulSoup(res.text, "html.parser")
  
    # Open a browser tab for each result
    linkElems = soup.select('.r a')
    numOpen = min(5, len(linkElems))
    for i in range(numOpen):
        webbrowser.open('http://google.com' + linkElems[i].get('href'))
 
def test_it():
    my_func(sys.argv[1:])

test_it()
