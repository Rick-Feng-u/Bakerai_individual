import flickrapi
import xml.etree.ElementTree as ET
import webbrowser

api_key = u'bfe22e378803fa7d7b232ce46eabaf06'
api_secret = u'5e079964800bd252'

def show_image(tag):
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    photos = flickr.photos.search(text=tag, per_page='10')['photos']['photo'][1]

    url = "http://farm" + str(photos["farm"]) + ".staticflickr.com/" + photos["server"] + "/" + photos["id"] + "_" +photos["secret"] + ".jpg"

    webbrowser.open(url=url)