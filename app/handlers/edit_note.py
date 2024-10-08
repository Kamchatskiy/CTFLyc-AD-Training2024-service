from flask import Blueprint, request, render_template, redirect, url_for, make_response
from .login import load_data, save_data
from .create_note import verify_jwt_cookie

edit_note_route = Blueprint("edit_note_route", __name__)

NOTES_FILE = "app/database/notes.json"


@edit_note_route.route('/note/edit/<note_id>', methods=["GET", "POST"])
def edit_note(note_id):
    username = verify_jwt_cookie()
    can_edit = request.cookies.get("can_edit_note")

    if not username:
        return redirect(url_for('auth_route.register'))

    notes = load_data(NOTES_FILE)
    note = notes.get(note_id)

    if not note:
        return render_template('errors/404.html')

    if can_edit == "0":
        return render_template('errors/403.html')

    if request.method == "POST":
        new_title = request.form.get('title')
        new_content = request.form.get('content')
        new_visibility = request.form.get('visibility', 'private')

        note['title'] = new_title
        note['content'] = new_content
        note['visibility'] = new_visibility

        save_data(notes, NOTES_FILE)

        return redirect(url_for("view_note_route.view_note", note_id=note_id))

    response = make_response(render_template("notes/edit_note.html", note=note, current_user=username))
    response.delete_cookie("can_edit_note")

    return response
