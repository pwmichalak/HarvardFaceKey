#!/usr/bin/python3
import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import face_recognition


# from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



files = os.listdir('people')
known_face_encodings = []
known_face_names = []
if '.DS_Store' in files:
    files.remove('.DS_Store')

print(files)

for file in files:
    image = face_recognition.load_image_file('people/' + file)
    known_face_encodings.append(face_recognition.face_encodings(image)[0])
    known_face_names.append(file.replace('.jpg',''))

name = "Unknown"

@app.route("/")
def index():
    return redirect("/upload")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload a picture"""
    global name
    if request.method == "POST":
        image = request.files["image"]
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
        file = face_recognition.load_image_file('image.jpg')
        encoding = face_recognition.face_encodings(file)[0]

        matches = face_recognition.compare_faces(known_face_encodings, encoding)

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            print("matched")
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            return redirect("/welcome")

        os.remove('image.jpg')
        print(name)
        print("hi")
        return render_template("index.html")

    return render_template("index.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html", name=name)

#
# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
