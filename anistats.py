import tweepy
from mal import AnimeSearch
import urllib.request
import time

CONSUMER_KEY = 'F0IKzzEmB4lVn6vIdh8uTKR77'
CONSUMER_SECRET = 'VD14stheIqUNyT8nh0vei2yZhwspiE2SuB31v9Nqx3i0OjRpOw'
ACCESS_KEY = '1341981535407403008-LEeyVm5nplsPJUV2LyoyczxZJ1IjJc'
ACCESS_SECRET = 'E5rsKP2xRYV61R92bpM6TPIfkDeM3hNErhTTKT6qL72ZT'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

last = retrieve_last_seen_id('last.txt')
mentions = api.mentions_timeline(last)
mentions.reverse()

def action():
    print('Actuating')
    for mention in mentions:
        if len(mention.text) > 12:
            anime = mention.text[11:]
            search = AnimeSearch(anime)
            if len(search.results) > 0:
                
                ret = search.results[0].title + '\n' + str(search.results[0].score) + '\n' + search.results[0].synopsis
                img = search.results[0].image_url
                urllib.request.urlretrieve(img, 'img.jpg')
                media = api.media_upload('img.jpg')
                media_array = [media.media_id_string]
                api.update_status('@' + mention.user.screen_name + ' ' + ret, mention.id, media_ids=media_array)
            else:
                api.update_status('@' + mention.user.screen_name + ' Anime not found!', mention.id)
        else:
            api.update_status('@' + mention.user.screen_name + ' Hello!', mention.id)
        store_last_seen_id(mention.id, 'last.txt')

while True:
    action()
    time.sleep(5)

