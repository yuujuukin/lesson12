from flask import Flask, request, render_template, send_from_directory
from functions import load_posts, find_post
from pathlib import Path
import json


app = Flask(__name__)

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"
posts = load_posts(POST_PATH)

#Путь к хранению загруженных картинок
UPLOAD_FOLDER = "../uploads/images/"

#Форматы картинок, которые можно загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route("/")
def page_index():
    return render_template('index.html')


@app.route("/post_list")
def page_tag():
    s = request.args['s']
    items = find_post(s, posts)
    return render_template("post_list.html", s=s, search_posts=items)


@app.route("/post_form", methods=["GET", "POST"])
def page_post_form():
    return render_template('post_form.html')


@app.route("/post_uploaded", methods=["POST"])
def page_post_upload():
    if request.files.get("pic") and request.form["content"]:
        picture = request.files.get("pic")
        content = request.form["content"]
        filename = picture.filename
        extension = filename.split(".")[-1]
        if extension in ALLOWED_EXTENSIONS:
            picture.save(f"./uploads/images/{filename}")
            path = Path('posts.json')
            data = json.loads(path.read_text(encoding='utf-8'))
            data.append({'pic': f'{UPLOAD_FOLDER}{filename}', 'content': content})
            path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8', )
            return render_template("post_uploaded.html", pic=f"./uploads/images/{filename}", content=content)
        return f"Тип файлов {extension} не поддерживается"
    return f"Вы забыли загрузить картинку или текст"


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


app.run()



