from datetime import datetime
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    intro = db.Column(db.String(300), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
         return '<Article %r>' % self.id

@app.route("/")
@app.route("/home")
def hello_world():
    return render_template("home.html")
   
@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/user/<string:name>/<int:age>")
def user(name, age):
    if age < 13:
        return f"{name} your age is small"
    else:
        return f" Your name is {name} \n And your age - {age}"


@app.route("/create-article", methods = ['POST', 'GET'])
def create_article():
    if request.method == "POST":
        try:
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']

            article = Article(title = title, intro = intro, text = text)

            db.session.add(article)
            db.session.commit()
            return redirect("/posts")
        except:
            return "Произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles = articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article = article)
    


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "Произошла ошибка"
    

@app.route("//posts/<int:id>/update", methods = ['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/posts")
        except:
            return "Произошла ошибка"
    else:
        return render_template("post_update.html", article = article)



if __name__ == '__main__':
	app.run()