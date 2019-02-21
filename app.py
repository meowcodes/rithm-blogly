"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def show_index():
    """Redirect to list of users"""
    return redirect("/users")

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template("user_listing.html",
        users = users)

@app.route('/users/new')
def show_new_user_form():
    """Show an add form for users"""
    return render_template("new_user_form.html")

@app.route('/users', methods=['POST'])
def post_new_user():
    """Process the add form, adding a new user and going back to /users"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url') or None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show information about the given user."""
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_detail_edit_form(user_id):
    """Show the edit page for a user."""
    user = User.query.get(user_id)
    
    return render_template('user_details_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_detail(user_id):
    """Show the edit page for a user."""
    updated_user = User.query.get(user_id)

    updated_user.first_name = request.form.get('first_name')
    updated_user.last_name = request.form.get('last_name')
    updated_user.image_url = request.form.get('image_url') or None


    db.session.add(updated_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_detail(user_id):
    """delete user."""
    deleted_user = User.query.get(user_id)
    db.session.delete(deleted_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """ Show add post form """

    user = User.query.get(user_id)

    return render_template('new_post_form.html', user=user)

@app.route('/users/<int:user_id>/posts', methods=['POST'])
def add_post(user_id):
    """ Add post to database """

    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """ Show post details """

    post = Post.query.get(post_id)

    return render_template('post_detail_page.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """ Show update post form """

    post = Post.query.get(post_id)

    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Update post in database """

    post = Post.query.get(post_id)

    post.title = request.form.get('title')
    post.content = request.form.get('content')

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ Delete post in database """

    post = Post.query.get(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")