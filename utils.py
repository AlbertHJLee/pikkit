"""
Utils for scraping Instagram
"""

import requests
import json
import numpy as np
from PIL import Image
from io import BytesIO

import time
import sys, select



def getUserPage(user):

    """
    Get json of user page data
    """

    page = requests.get('https://www.instagram.com/'+user+'/media/')
    content = page.content
    struct = json.loads(content)

    return page, struct




def getImage(userpage, index):

    struct = json.loads(page.content)

    imgurl = struct['items'][index]['images']['standard_resolution']['url']
    code = struct['items'][index]['code']

    image = Image.open(BytesIO(requests.get(imgurl).content))

    return image




def getImagesOld(userpage):

    struct = json.loads(page.content)

    imgurls = []
    codes = []
    images = []

    for post in struct['items']:
        imgurls += [post['images']['standard_resolution']['url']]
        codes += [post['code']]
        images += [Image.open(BytesIO(requests.get(imgurls[-1]).content))]

    return imgurls,codes,images





def getPosts(userpage):

    struct = json.loads(userpage.content)

    posts = []

    for post in struct['items']:
        id = post['id']
        code = post['code']
        imgurl = post['images']['standard_resolution']['url']
        image = Image.open(BytesIO(requests.get(imgurl).content))
        caption = post['caption']['text']
        userid = post['user']['id']
        username = post['user']['username']
        likes = post['likes']['count']
        comments = post['comments']['count']
        posts += [{'id':id, 'code':code, 'imgurl':imgurl, 'image':image,
                  'caption':caption, 'userid':userid, 'username':username,
                  'likes':likes, 'comments':comments}]

    return posts





def img2numpy(image):

    array = numpy.array(image.getdata()).reshape(image.size[0], image.size[1], 3)

    return array




def search(term):

    page = requests.get('https://www.instagram.com/explore/tags/'+term+'/')
    content = page.content

    sharedData = content.split('<script type="text/javascript">window._sharedData = ')
    substrings = sharedData[1].split('}, {')
    struct = []

    i=0
    length = len(substrings)
    print str(length) + ' results'

    for string in substrings[1:(length-10)]:

        #print i
        #i += 1
        struct += [json.loads('{'+string+'}')]

    return struct




def searchLoop(term, verbose=1):

    struct = []
    interrupt = False
    
    while not interrupt:

        struct += search(term)
        
        with open('data/posts.json','w') as outfile:
            if verbose >= 1:
                print "Saving posts..."
                json.dump(struct,outfile)

        #time.sleep(20)
        rout, wout, exout = select.select( [sys.stdin], [], [], 20 )

        if (rout):
            interrupt = True

    print "Done (keyboard interrupt)"

    return struct

