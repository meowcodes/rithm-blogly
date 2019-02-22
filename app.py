"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def show_index():
    """Redirect to list of users"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('index.html', posts=posts)

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

    first_name = request.form.get('first_name') or None
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
    
    return render_template('user_details.html', user=user, posts=user.posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_detail_edit_form(user_id):
    """Show the edit page for a user."""
    user = User.query.get(user_id)
    
    return render_template('user_details_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_detail(user_id):
    """Show the edit page for a user."""
    updated_user = User.query.get(user_id)

    updated_user.first_name = request.form.get('first_name') or None
    updated_user.last_name = request.form.get('last_name') or None
    updated_user.image_url = request.form.get('image_url') or None

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
    tags = Tag.query.all()

    return render_template('new_post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts', methods=['POST'])
def add_post(user_id):
    """ Add post to database """

    title = request.form.get('title')
    content = request.form.get('content')
    tag_ids = request.form.getlist('tag')
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)

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
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Update post in database """

    post = Post.query.get(post_id)

    post.title = request.form.get('title')
    post.content = request.form.get('content')

    tag_ids = request.form.getlist('tag')
    post.tags= Tag.query.filter(Tag.id.in_(tag_ids)).all()

#     db.session.commit()
    
# #     import pdb; pdb.set_trace()

#     for tag_id in tag_ids:
#         post.posts_tags.append(PostTag(tag_id=tag_id))

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

@app.route('/tags')
def show_tags():
    """Lists all tags, with links to the tag detail page"""

    tags = Tag.query.all()

    return render_template('tag_listing.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show detail about a tag. Have links to edit form and to delete"""

    tag = Tag.query.get(tag_id)

    return render_template('tag_detail_page.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form(tag_id):
    """Shows a form to add a new tag"""

    tag = Tag.query.get(tag_id)

    return render_template('new_tag.html', tag=tag)

@app.route('/tags', methods=['POST'])
def add_tag(tag_id):
    """process add form, adds tag, and redirecting to tag list"""

    name = request.form.get('name')

    new_tag = Tag(name=name, tag_id=tag_id)

    db.session.add(new_tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """ Update tag in database """

    tag = Tag.query.get(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """process edit tag form, edit tag, and redirects to the tags list"""

    tag = Tag.query.get('tag_id')

    tag.name = request.form.get('name')

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """delete a tag"""
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.commit()

    return redirect('/tags')