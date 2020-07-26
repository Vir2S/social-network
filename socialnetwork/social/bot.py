import json
import random
import requests
from social.models import Post, SocialUser
from django.http import JsonResponse
from socialnetwork.settings import BASE_URL


def start_bot(request):

    with open('bot_rules.json', 'r') as read_file:
        bot = json.load(read_file)

    def bot_user_create():
        url_user = BASE_URL + 'create_user/'
        user_data = {
            "username": 'bot-{}'.format(''.join(['{}'.format(random.randrange(0, 101, 1)) for _ in range(5)])),
            "password": ''.join(['{}'.format(random.randrange(0, 101, 1)) for _ in range(8)]),
            "first_name": 'bot_username'
        }
        usr = requests.post(url_user, data=user_data)
        print('r', usr)

    def bot_post_create(last_user, headers):
        url = BASE_URL + 'post_create/'
        postdata = {
            "post_text": "post text by robot",
            "post_user": last_user.id
        }
        r = requests.post(url, headers=headers, data=postdata)
        print('r', r)

    def bot_like_create(last_user, headers):
        all_posts = Post.objects.all()
        random_post_id = random.choice([i.id for i in all_posts])
        url_like = BASE_URL + 'post/{}/{}/like/'.format(random_post_id, last_user.id)
        like_data = {
            "like_user": last_user.id,
            "like_post": random_post_id,
            "like": 1
        }
        l = requests.post(url_like, headers=headers, data=like_data)
        print('r', l)

    for i in range(bot['number_of_users']):
        bot_user_create()
        last_user = StarnaviUser.objects.all().last()
        headers = {'Authorization': 'Token {}'.format(last_user.auth_token.key)}

        for _ in range(bot['max_posts_per_user']):
            bot_post_create(last_user, headers)

        for _ in range(bot['max_likes_per_user']):
            bot_like_create(last_user, headers)

    return JsonResponse(bot, safe=True)
