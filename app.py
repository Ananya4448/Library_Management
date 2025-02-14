from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ananya@2002'
app.config['MYSQL_DB'] = 'library_db'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    published_date = request.form['published_date']
    publication = request.form['publication']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO books (title, author, published_date, publication) VALUES (%s, %s, %s, %s)", 
                (title, author, published_date, publication))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        published_date = request.form['published_date']
        publication = request.form['publication']
        
        cur.execute("UPDATE books SET title=%s, author=%s, published_date=%s, publication=%s WHERE id=%s", 
                    (title, author, published_date, publication, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cur.fetchone()
    cur.close()
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    book = None
    if request.method == 'POST':
        book_id = request.form['book_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s", (book_id,))
        book = cur.fetchone()
        cur.close()
    
    return render_template('search.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)