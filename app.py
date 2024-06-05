from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

database = 'database.db'
def add_comment(name, comment):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('INSERT INTO comments (name, comment) VALUES (?, ?)', (name, comment))
    conn.commit()
    conn.close()

def get_comments():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT * FROM comments')
    comments = c.fetchall()
    conn.close()
    return comments

def format_comments(comments):
    var = [f'{name}: {comment}' for id, name, comment, datetime in comments]
    return var


@app.route('/')
def index():
    comments = get_comments()
    comments = format_comments(comments)
    return render_template('index.html', comments=comments)

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        add_comment(name, comment)
        return redirect('/')
    comments = get_comments()
    comments = format_comments(comments)
    return comments