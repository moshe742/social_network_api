import logging
import random
import string

import requests

import bot_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.num_of_users = bot_config.NUMBER_OF_USERS
        self.max_posts_per_user = bot_config.MAX_POSTS_PER_USER
        self.max_likes_per_user = bot_config.MAX_LIKES_PER_USER
        self.url = 'http://localhost:8000/api/'
        self.users = {}
        self.posts = {}

    def create_users(self):
        logger.info('creating users')
        usernames = []
        num = 1
        for _ in range(self.num_of_users):
            username = f'moshegrey+{num}'
            num += 1
            while username in usernames:
                username = get_random_string(random.randint(5, 10))
            usernames.append(username)
            user = {
                'username': username,
                'email': f'{username}@gmail.com',
                'password': get_random_string(random.randint(8, 12)),
                'posts': [],
                'posts_without_likes': []
            }
            self.users[username] = user

    def signup_all_users(self):
        logger.info('signup all users')
        for user in self.users.values():
            logger.info(f'signing in {user["username"]}')
            res = requests.post(f'{self.url}signup/', json=user)
            res_json = res.json()
            if 'error' in res_json:
                logger.error(res_json)
                exit()

    def login_user(self, user):
        res = requests.post(f'{self.url}login/', json=user)
        res_json = res.json()
        if 'error' in res_json:
            logger.error(res_json)
            exit()
        user['token'] = res_json['token']

    def create_posts(self, user):
        num_of_posts = random.randint(1, bot_config.MAX_POSTS_PER_USER)
        for _ in range(num_of_posts):
            content = get_random_string(random.randint(10, 100))
            res = requests.post(f'{self.url}posts/',
                                headers={'Authorization': user['token']},
                                json={'content': content})
            res_json = res.json()
            if 'error' in res_json:
                logger.error(res_json['error'])
                exit()
            user['posts'].append(res_json['id'])
            user['posts_without_likes'].append(res_json['id'])
            self.posts[res_json['id']] = {
                'user': res_json['user']['username'],
                'num_of_likes': 0
            }

    def like_posts(self):
        logger.info('doing likes')
        users = sorted(self.users, key=lambda user_name: len(self.users[user_name]['posts']), reverse=True)
        posts_with_likes = 0
        for user in users:
            logger.info(f'{user}')
            num_of_likes = 0
            posts = dict(self.posts)
            while num_of_likes < bot_config.MAX_LIKES_PER_USER:
                if not posts:
                    break

                post_id = random.choice(list(posts.keys()))
                post_dict = posts.pop(post_id)
                logger.info(f'{post_id}, {post_dict["user"]}')
                if post_id not in self.users[user]['posts'] and \
                        self.users[post_dict['user']]['posts_without_likes']:
                    res = requests.patch(f'{self.url}posts/{post_id}/',
                                         headers={'Authorization': self.users[user]['token']},
                                         json={'like': 'like'})
                    res_json = res.json()
                    if 'error' in res_json:
                        logger.error(res_json['error'])
                        exit()
                    num_of_likes += 1
                    if post_dict['num_of_likes'] == 0:
                        posts_with_likes += 1
                        if posts_with_likes == len(self.posts):
                            return
                    post_dict['num_of_likes'] += 1

    def login_and_post(self):
        logger.info('login users and posting posts')
        for user in self.users.values():
            self.login_user(user)
            self.create_posts(user)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def main():
    bot = Bot()
    bot.create_users()
    bot.signup_all_users()
    bot.login_and_post()
    bot.like_posts()


if __name__ == '__main__':
    main()
