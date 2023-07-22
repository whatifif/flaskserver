from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
import os

# Load environment variables from .env file
load_dotenv()

# Get the database path from the environment variable
db_path = os.getenv('SQLALCHEMY_DATABASE_URI').replace('sqlite:///', '')

# Convert to absolute path if it's not already
if not os.path.isabs(db_path):
    db_path = os.path.join(os.getcwd(), db_path)

# Get the directory part of the path
db_dir = os.path.dirname(db_path)

# Check if the directory exists
if not os.path.exists(db_dir):
    # If the directory does not exist, create it
    os.makedirs(db_dir)

# Check if the database file exists
if not os.path.exists(db_path):
    # If the database file does not exist, create it
    open(db_path, 'w').close()

# Update the SQLALCHEMY_DATABASE_URI environment variable to the absolute path
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
api = Api(app)
db = SQLAlchemy(app)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    owner = db.Column(db.String(50))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

group_ns = api.namespace('group', description='Group operations')

@group_ns.route('/')
class GroupList(Resource):
    def get(self):
        groups = Group.query.all()
        return [{'id': group.id, 'name': group.name, 'owner': group.owner, 'createdAt': group.createdAt.isoformat()} for group in groups]

    def post(self):
        name = request.json['name']
        owner = request.json['owner']
        new_group = Group(name, owner)
        db.session.add(new_group)
        db.session.commit()
        return {'id': new_group.id, 'name': new_group.name, 'owner': new_group.owner, 'createdAt': new_group.createdAt.isoformat()}

@group_ns.route('/<int:id>')
class GroupAPI(Resource):
    def get(self, id):
        group = Group.query.get(id)
        return {'id': group.id, 'name': group.name, 'owner': group.owner, 'createdAt': group.createdAt.isoformat()}

    def put(self, id):
        group = Group.query.get(id)
        name = request.json['name']
        owner = request.json['owner']
        group.name = name
        group.owner = owner
        db.session.commit()
        return {'id': group.id, 'name': group.name, 'owner': group.owner, 'createdAt': group.createdAt.isoformat()}

    def delete(self, id):
        group = Group.query.get(id)
        db.session.delete(group)
        db.session.commit()
        return {'result': 'group deleted'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
