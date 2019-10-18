from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# Your local Craigslist directory show go below in the BASE_URL position

BASE_URL = 'https://flagstaff.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    # Get the content of the search bar, what is being posted
    search = request.POST.get('search')
    # add the search to the list of searches in teh database
    models.Search.objects.create(search=search)
    # quote plus automatically adds "+" to searches with spaces
    search_url = BASE_URL.format(quote_plus(search))
    response = requests.get(search_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    # result elements
    listings = soup.find_all('li', {'class': 'result-row'})

    final_results = []

    for post in listings:
        title = post.find(class_='result-title').text
        url = post.find('a').get('href')
        if post.find(class_='result-price'):
            price = post.find(class_='result-price').text
        else:
            price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            # get first portion of original image result url, which has "1:" in front, drop to get
            # image tag
            image_url = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            image = BASE_IMAGE_URL.format(image_url)
        else:
            image = 'https://craigslist.org/images/peace.jpg'


        final_results.append((title, url, price, image))

    search_content = {
        'search': search,
        'final_results': final_results,
    }
    # Return the search content
    return render(request, 'myapp/new_search.html', search_content)