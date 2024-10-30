import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post')

    def __str__(self):
        return self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __str__(self):
        return self.content[:20]
    

def db_init():
    post1 = Post(title='Python Frameworks', content='There are many, like Flask, Django, and FastAPI')
    post2 = Post(title='Front End', content='Learn HTML, CSS, and JavaScript')
    post3 = Post(title='Database for the Web', content='Any DBMS will do, like MySQL, Postgres, or MongoDB')

    comment1 = Comment(content='I prefer Flask', post=post1)
    comment2 = Comment(content='Can we use frameworks', post=post2)
    comment3 = Comment(content='React is my choice', post_id=2)
    comment4 = Comment(content='Which one is better?', post_id=1)
    comment5 = Comment(content='Depends on your project', post_id=1)


    db.session.add_all([post1, post2, post3])
    db.session.add_all([comment1, comment2, comment3, comment4, comment5])

    db.session.commit()
    

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>/')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    database_file = Path(os.path.join(basedir, 'blog.db'))
    if database_file.is_file():
        print("DB found at ", str(database_file))
    else: 
        with app.app_context():
            db.create_all()
            db_init()
        print("DB created")
    app.run(debug=True)