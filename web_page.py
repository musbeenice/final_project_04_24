
# используемые библиотеки
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# создание объекта app на основе класса Flask
app = Flask(__name__)

# указание URI базы данных, которую будем использовать для подключения (sqlite) и название создаваемой БД (blog.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# создание объекта на основе класса SQLAlchemy
db = SQLAlchemy(app)


# создание класса - таблицы, в которой будут храниться записи создаваемых статей
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Article %r' % self.id

# отслеживание определенного url-адреса
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/mgs_1')
def mgs_1():
    return render_template('mgs_1.html')


@app.route('/mgs_2')
def mgs_2():
    return render_template('mgs_2.html')


@app.route('/mgs_3')
def mgs_3():
    return render_template('mgs_3.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        if not article.title or not article.intro or not article.text:
            return 'Не все поля заполнены'

        try:
            db.session.commit()
            return redirect(f'/posts/{id}')
        except:
            return 'При редактировании статьи произошла ошибка'

    else:
        return render_template('post_update.html', article=article)


# список методов, какие может принимать функция;
# чтобы функция могла обрабатывать данные из форм, необходим метод POST
@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        if not title or not intro or not text:
            return 'Не все поля заполнены'

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'

    else:
        return render_template('create_post.html')


if __name__ == '__main__':
    app.run(debug=True)
