#!venv/bin/python
from app import db, models
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from datetime import datetime
import os.path
import json
import pdb

snipf = {
    'title': 'Class Definition',
    "des": """
        <p>Classes are used to create user defined datatypes.</p>
        <ul class='snippetDesStyle'>
            <li>By convention, they are capitalized.</li>
            <li>A class is a python object, and is a template used to create class instances. A class instance is created by instantiation <em>(inst = class()</em>).</li>
            <li>Classes can have docstrings.</li>
            <li>Use the <em>pass</em> statement to define a null class.</li>
        </ul>
""",
    "code": """
#class Dog:
#\"\"\" This is a docstring for the Dog class. \"\"\"
#pass
#<pre class='snippetCommandStyle'>
#>>> d = Dog()
#>>> Dog.__doc__
#>>> ' This is a docstring for the Dog class. '
"""
}

snipe = {
    'title': 'Class Variables',
    "des": """
        <p>Class variables in python are shared among all of the class instances.</p>
        <ul>
            <li>If you change the class variable with the class object (class.attr = value), the value is changed in all existing and future class instances <em>(Dog.sound = 'yip')</em>.
            <li>If you change the variable through a class instance <em>(big_dog.sound = 'growl')</em> a local variable is created for that instance and added to the instance's dictionary.</li>
        </ul>
""",
    "code": """
class Dog:
sound = 'bark'
            <pre class="snippetCommandStyle">
>>> print Dog.sound
bark
>>> big_dog = Dog()
>>> small_dog = Dog()
>>> print big_dog.sound, small_dog.sound 
bark bark
>>> Dog.sound = 'yip'
>>> print big_dog.sound, small_dog.sound 
yip yip
>>> big_dog.sound = 'growl'
>>> print big_dog.sound, small_dog.sound 
growl yip</pre>
"""
}

snipd = {
    'title': 'Built-in Class Attributes',
    "des": """
        <ul>
            <li>__dict__ Dictionary containing the class's namespace</li>
            <li>__doc__ The docstring - set to <em>None</em> if undefined</li>
            <li>__name__ Class name</li>
            <li>__module__ Module name in which the class is defined - is "__main__" in interactive mode</li>
            <li>__bases__ A tuple containing the base classes</li>
        </ul>
""",
    "code": ''
}

snipc = {
    'title': 'Built-in Instance Attributes',
    "des": """
        <ul class="snippetTextAlone">
            <li>__dict__ Dictionary containing the instances's namespace</li>
            <li>__class__ Name of the instance's class</li>
        </ul>
""",
    "code": ''
}

snipb = {
    'title': 'Instance Variables/Methods, Ctor/Dtor',
    "des": '',
    "code": ''
}

snipa = {
    'title': 'Inheritance, Public/Private Attrs',
    "des": '',
    "code": ''
}

snipt = {
    'title': 'Class Definition',
    "des": """
""",
    "code": """
"""
}
snippets = [snipa, snipb, snipc, snipd, snipe, snipf]

def cs():
    """ Create a snippet """

def create_db():
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

jfb = {'fb_id': '100002423206916', 'name':'JohnMarksJr', 'email': 'johnmarksjr@gmail.com', 'role':models.ROLE_USER}
jgoog = {'google_id': '106697488228998596996', 'name':'John', 'email': 'johnmarksjr@gmail.com', 'role':models.ROLE_USER}
jtwit = {'twitter_id': '1860746486', 'name':'jettagozoom', 'email': None, 'role':models.ROLE_USER}
users = [jfb, jgoog, jtwit]

def add_users():
    u = None
    for user in users:
        if 'fb_id' in user:
            u = models.User(fb_id=user['fb_id'], name=user['name'], email=user['email'], role=user['role'])
            db.session.add(u)

            # Add the 'General' topic for the user
            topic = models.Topic(topic = 'General', author = u)
            db.session.add(topic)
        elif 'google_id' in user:
            u.google_id = user['google_id']
        elif 'twitter_id' in user:
            u = models.User(twitter_id=user['twitter_id'], name=user['name'], role=user['role'])
            db.session.add(u)

            # Add the 'General' topic for the user
            topic = models.Topic(topic = 'General', author = u)
            db.session.add(topic)

        db.session.commit()


def add_snips():
    # Get the 'General' topic
    gt = models.Topic.query.first()

    # Create and add the snippets
    for snip in snippets:
        #pdb.set_trace()
        s = models.Snippet(title = snip['title'], description = snip['des'], code = snip['code'],
                           timestamp = datetime.utcnow(),
                           topic=gt, public=True)
        db.session.add(s)
    db.session.commit()

def delete_snips():
    snips = qsnips()
    for snip in snips:
        db.session.delete(snip)
    db.session.commit()

def populate_db():
    create_db()
    add_users()
    add_snips()

def qusers():
    """ Find all users """
    users = models.User.query.all()
    return users
def qtopics():
    """ Find all topics """
    topics = models.Topic.query.all()
    return topics
def qsnips():
    """ Find all of a user's snippets (particular user) - order by timestamp """
    """ This requires a join """
    user = models.User.query.first()
    topic = user.topics.filter_by(topic='General').first()
    snips = topic.snippets.all()
    for snip in snips:
        print '*****************'
        print snip
    return snips
def qsnips2():
    """ Find all snippets in db (all users) - no ordering """
    snips = models.Snippet.query.all()
    return snips
def qsnips3():
    """ Find all snippets in db (all users) - order by timestamp """
    snips = models.Snippet.query.order_by(models.Snippet.timestamp.desc()).all()
    return snips

def jsonify_snips():
    """ Create JSON of the snippets """
    snips = models.Snippet.query.all()
    reply = {}
    reply['found'] = 'found'
    for i, snip in enumerate(snips):
        #pdb.set_trace()
        d = dict(title=snip.title, description=snip.description, code=snip.code)
        reply[i] = d
    return json.dumps(reply)
