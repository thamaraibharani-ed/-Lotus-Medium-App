from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("lotus.db")

# ---------- LOGIN ----------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/home')
    return render_template('login.html')

# ---------- NEXT PAGE ----------
@app.route('/home')
def home():
    return render_template('home.html')

# ---------- SHOW ALL BLOGS ----------
@app.route('/blogs')
def blogs():
    con = db()
    blogs = con.execute("SELECT * FROM blogs").fetchall()
    return render_template('blogs.html', blogs=blogs)

# ---------- CREATE ----------
@app.route('/add', methods=['POST'])
def add():
    con = db()
    con.execute(
        "INSERT INTO blogs (title, content) VALUES (?,?)",
        (request.form['title'], request.form['content'])
    )
    con.commit()
    return redirect('/blogs')

# ---------- UPDATE ----------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    con = db()
    if request.method == 'POST':
        con.execute(
            "UPDATE blogs SET title=?, content=? WHERE id=?",
            (request.form['title'], request.form['content'], id)
        )
        con.commit()
        return redirect('/blogs')

    blog = con.execute("SELECT * FROM blogs WHERE id=?", (id,)).fetchone()
    return render_template('edit.html', blog=blog)

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete(id):
    con = db()
    con.execute("DELETE FROM blogs WHERE id=?", (id,))
    con.commit()
    return redirect('/blogs')

# ---------- API ----------
@app.route('/api/blogs')
def api_blogs():
    con = db()
    blogs = con.execute("SELECT * FROM blogs").fetchall()
    return jsonify(blogs)

if __name__ == '__main__':
    con = db()
    con.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    """)
    con.commit()
    app.run(debug=True)
