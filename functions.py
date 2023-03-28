import json
from Class import Search

path = 'posts.json'


def load_posts(path: str) -> list[Search]:
    post = []
    with open(path, 'r', encoding='UTF-8') as file:
        data = json.load(file)

    for item in data:
        pic = item['pic']
        content = item['content']
        post.append(Search(pic, content))

    return post


def find_post(s: str, post: list[Search]) -> list[Search]:
    search = []
    for item in post:
        if s.lower() in item.content.lower():
            search.append(item)
    return search


