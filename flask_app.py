import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Selamat datang di situs saya menggunakan Flash'


app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Ini halaman utama</h1>
<p>Halaman web Rest API dengan Python Flask.</p>
<p><a href="http://sukasate.pythonanywhere.com/books/all">GET All</a>'''


@app.route('/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@app.route('book/create', methods=['POST','GET'])
def tambah():
    query_parameters = request.get_json()
    val1 = query_parameters["author"]
    val2 = query_parameters["first_sentence"]
    val3 = query_parameters["id"]
    val4 = query_parameters["published"]
    val5 = query_parameters["title"]
    query = "INSERT INTO books(author,first_sentence,id,published,title) VALUES (val1,val2,val3,val4,val5);"


    conn = sqlite3.connect('boooks.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query).fetchall()
    return jsonify(results)

app.run()