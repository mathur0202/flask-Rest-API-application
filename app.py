from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:farcry1234@localhost/articles"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ARTICLES = [

]


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))

    def __init__(self, title, description):
        self.title = title
        self.description = description


@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>Welcome To the home page we have created rest api and checked it against postman</h1>"


@app.route("/add", methods=["POST"])
def add_article():
    req_data = request.get_json()
    title = req_data['title']
    description = req_data['description']

    article = Articles(title=title, description=description)
    db.session.add(article)
    db.session.commit()
    new_article = {
        'title': req_data['title'],
        'description': req_data['description']
    }
    ARTICLES.append(new_article)
    return jsonify(req_data)


@app.route("/get/<string:title>", methods=["GET"])
def get_article(title):
    for article in ARTICLES:
        if article['title'] == title:
            return jsonify(article)


@app.route("/update/<int:id>", methods=["PUT"])
def update_article(id):
    curr_article = Articles.query.filter_by(id=id).first()
    req_data = request.get_json()
    curr_article.title = req_data['title']
    curr_article.description = req_data['description']
    db.session.commit()

    return {req_data['title']: req_data['description']}


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_article(id):
    curr_article = Articles.query.filter_by(id=id).first()
    db.session.delete(curr_article)
    db.session.commit()
    return {curr_article.title: curr_article.description}

