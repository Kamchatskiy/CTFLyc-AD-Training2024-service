from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, make_response, jsonify
import jwt
from .login import load_data, save_data
from config import SECRET_KEY

create_note_route = Blueprint("create_note_route", __name__)

NOTES_FILE = "app/service/database/notes.json"


def verify_jwt_cookie():
    jwt_token = request.cookies.get('jwt_token')
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            return username
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None


@create_note_route.route('/create_note', methods=["GET", 'POST'])
def create_note():
    if request.method == "POST":
        username = verify_jwt_cookie()
        if not username:
            return redirect(url_for('auth_route.login'))

        title = request.form.get('title')
        content = request.form.get('content')
        visibility = request.form.get('visibility', 'private')
        author = username  # Используем имя пользователя из JWT
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_ = str(int(datetime.now().timestamp() * 1000))
        notes = load_data(NOTES_FILE)

        new_note = {
            "id": id_,
            'title': title,
            'content': content,
            'visibility': "public",
            'author': author,
            'timestamp': timestamp
        }
        notes[new_note["id"]] = new_note
        save_data(notes, NOTES_FILE)

        return redirect(url_for("view_note_route.view_note", note_id=id_))

    username = verify_jwt_cookie()
    if not username:
        return redirect(url_for('auth_route.login'))

    return render_template("notes/create_note.html")
