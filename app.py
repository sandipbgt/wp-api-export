import requests
import json
from collections import OrderedDict
import os
import subprocess
from pprint import pprint

BASE_API = 'http://shoutmeloudblog.com/wp-json/wp/v2'

def get_posts(category_id):
    posts = []
    rows = requests.get(BASE_API + "/posts?_embed&per_page=20&categories=" + str(category_id)).json()
    for row in rows:
        post = OrderedDict([
            ('id', row['id']),
            ('date', row['date'].replace('T', ' ')),
            ('modified', row['modified'].replace('T', ' ')),
            ('slug', row['slug']),
            ('link', row['link']),
            ('title', row['title']['rendered']),
            ('content', row['content']['rendered']),
            ('excerpt', row['excerpt']['rendered']),
            ('thumbnail', row['_embedded']['wp:featuredmedia'][0]['media_details']['sizes']['thumbnail']['source_url']),
            ('featured_image', row['_embedded']['wp:featuredmedia'][0]['media_details']['sizes']['medium']['source_url']),
        ])
        posts.append(post)
    return posts

def get_categories():
    categories = []
    rows = requests.get(BASE_API + "/categories" ).json()
    for row in rows:
        posts = get_posts(row['id'])
        category = OrderedDict([
            ('id', row['id']),
            ('name', row['name']),
            ('slug', row['slug']),
            ('count', row['count']),
            ('posts', posts)
        ])
        categories.append(category)
    return categories

def export_to_json(filename):
    categories = get_categories()
    with open(filename + '.json', 'w') as f:
        f.write(json.dumps(categories, indent=4))

def push_to_github(path, commit_message):
    print("Pushing to GitHub")
    os.chdir(path)
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', commit_message])
    subprocess.call(['git', 'push', 'origin', 'gh-pages'])
    print("Pushed to GitHub")

def main():
    export_to_json('/home/bgt/temp/api')
    push_to_github("/home/bgt/temp/", "updated")

if __name__ == "__main__":
    main()
