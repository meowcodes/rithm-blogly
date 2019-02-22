from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name='Whiskey', last_name='The Dog')
spike = User(first_name='Spike', last_name='The Porcupine')

# Add posts
post1 = Post(title='Woof!', content='I love snacks!', user_id=1)
post2 = Post(title='Hi!', content='I love snacks!', user_id=2)

# Add tags
tag1 = Tag(name='awesome')
tag2 = Tag(name='fun')

# Add posts-tags
pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=2)
pt3 = PostTag(post_id=2, tag_id=2)

db.session.add(whiskey)
db.session.add(spike)
db.session.add(post1)
db.session.add(post2)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(pt1)
db.session.add(pt2)
db.session.add(pt3)

# Commit--otherwise, this never gets saved!
db.session.commit()