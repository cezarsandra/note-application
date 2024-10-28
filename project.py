"""module providing a server application using Python, 
handling HTTP requests, serving content from database"""
import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, render_template, request, send_from_directory, jsonify


app = Flask (__name__)

class Cofigs():
    """Cofigs representing the app configs"""
    def __init__(self, file_path):
        if not load_dotenv(file_path):
            print("cannot read .env file")
            exit(1)
        
        self.db_user = os.getenv("my_user") if os.getenv("my_user") else "root"
        self.db_password = os.getenv("my_password") if os.getenv("my_password") else "abc"
        self.db_name = os.getenv("my_db") if os.getenv("my_db") else "db"
        self.port = os.getenv("my_port") if os.getenv("my_port") else 2000
        self.db_host = os.getenv(my_host) if os.getenv(my_host) else "localhost"

        print("These are my configs:")
        print("User:", self.db_user)
        print("Password:", self.db_password)
        print("Database:", self.db_name)
        print("Port:", self.port)

class Note():
    """Class representing the Notes values"""
    def __init__(self, title, note):
        self.title = title
        self.note = note

#route for css
@app.route("/css/<path:filename>")
def send_css(filename):

    return send_from_directory("static/css/", filename)

#route for js
@app.route("/js/<path:filename>")
def send_js(filename):

    return send_from_directory("static/js/", filename)

@app.route("/")
def get():

    connection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes ")
    result_query = cursor.fetchall()
    values = []
    for row in result_query:
        notes_object = Notes(row[0], row[1],)
        values.append(notes_object)

    return render_template("home.html", result = values)

@app.route("/post", methods = ["GET", "POST"])
def post_note():

    if request.method == "GET":
        return render_template("post_note.html")
    elif request.method == "POST":
        post_object = Notes(
            title = request.form.get("Title"),
            note = request.form.get("Note")
        )
        query = """INSERT INTO notes (Title, Note) VALUES (%s, %s)"""
        connection.connect()
        cursor = connection.cursor()
        cursor.execute(query, (post_object.title, post_object.note))

        connection.commit()
        connection.close()
        cursor.close()
        return "The note has been added "

@app.route("/update/<titleNote>", methods=["GET", "PUT"])
def update_note(titleNote):

    if request.method == "GET":
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM notes WHERE Title = %s", (titleNote,))
        value = cursor.fetchone()
        result = []
        val_object = Notes(value[0], value[1])
        result.append(val_object)

        cursor.close()
        connection.close()
        return render_template("update.html", values=result)


    elif request.method == "PUT":
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        send_object = Notes(titleNote, data.get("note"))
        print(send_object.note)

        connection.connect()
        cursor = connection.cursor()
        cursor.execute("""UPDATE notes SET Note = %s WHERE Title = %s""",
                        (send_object.note, titleNote))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message" :"The Note has been updated"})


@app.route("/delete/<titleNote>", methods=["DELETE"])
def delte_note(titleNote):

    query="""DELETE FROM notes WHERE Title = %s"""
    connection.connect()
    cursor = connection.cursor()
    cursor.execute(query, (titleNote,))

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify({"message": f"The {titleNote } Note has been deleted"})


@app.route("/search/")
def search():

    return render_template ("search.html")

@app.route("/searchnotes", methods=["GET"])
def search_notes():

    title = request.args.get("TitleNotes")
    connection.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM notes")
    result_query = cursor.fetchall()
    title_notes=[]
    for column in result_query:
        title_notes.append(column[0])

    if title in title_notes:
        cursor.execute("SELECT * FROM notes WHERE Title = %s", (title,))
        my_note = cursor.fetchone()
        return f"This is your Note:<br><br> Title: {my_note[0]} <br> Notes: {my_note[1]}"
    else:
        return "We can t find your Note"


def DB_connection(cfg):
    try:    
        connection = mysql.connector.connect(
            host=cfg.db_host,
            user=cfg.db_user,
            password=cfg.db_password,
            database=cfg.db_name
        )
        print("Connected to database successfully")
    except mysql.connector.Error as err:
        print("Cannot connect to database")

def main():
    cfg = Configs("./.env")
    conn = DB_connection(cfg)

    app.run(port = cfg.port)

if __name__ == "__main__":
    main()

