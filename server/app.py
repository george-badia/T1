from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'HFVWQEYFEYGBHERWGM47583495UFUEF[EWPKF]'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    entries = db.relationship('Entry', backref='user', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('Photo', backref='entry', lazy=True)
    tags = db.relationship('Tag', secondary='entry_tag', backref=db.backref('entries', lazy='dynamic'))

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

entry_tag = db.Table('entry_tag',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# Helper functions
def entry_to_dict(entry):
    return {
        'id': entry.id,
        'location': entry.location,
        'date': entry.date.isoformat(),
        'description': entry.description,
        'created_at': entry.created_at.isoformat(),
        'tags': [tag.name for tag in entry.tags]
    }

# Routes
@app.route('/api/entries', methods=['GET'])
@jwt_required()
def get_entries():
    user_id = get_jwt_identity()
    entries = Entry.query.filter_by(user_id=user_id).all()
    return jsonify([entry_to_dict(entry) for entry in entries])

@app.route('/api/entries', methods=['POST'])
@jwt_required()
def create_entry():
    user_id = get_jwt_identity()
    data = request.json
    new_entry = Entry(
        location=data['location'],
        date=datetime.fromisoformat(data['date']),
        description=data['description'],
        user_id=user_id
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(entry_to_dict(new_entry)), 201

@app.route('/api/entries/<int:id>', methods=['GET'])
@jwt_required()
def get_entry(id):
    entry = Entry.query.get_or_404(id)
    return jsonify(entry_to_dict(entry))

@app.route('/api/entries/<int:id>', methods=['PUT'])
@jwt_required()
def update_entry(id):
    entry = Entry.query.get_or_404(id)
    data = request.json
    entry.location = data['location']
    entry.date = datetime.fromisoformat(data['date'])
    entry.description = data['description']
    db.session.commit()
    return jsonify(entry_to_dict(entry))

@app.route('/api/entries/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_entry(id):
    entry = Entry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return '', 204

@app.route('/api/entries/<int:id>/photos', methods=['GET'])
@jwt_required()
def get_entry_photos(id):
    entry = Entry.query.get_or_404(id)
    photos = [{'id': photo.id, 'url': photo.url} for photo in entry.photos]
    return jsonify(photos)

# @app.route('/api/entries/<int:id>/photos', methods=['POST'])
# @jwt_required()
# def upload_photo(id):
#     entry = Entry.query.get_or_404(id)
#     if 'photo' not in request.files:
#         return jsonify({'error': 'No photo provided'}), 400
#     photo = request.files['photo']
#     if photo.filename == '':
#         return jsonify({'error': 'No photo selected'}), 400
#     if photo:
#         filename = f"{datetime.now().timestamp()}_{photo.filename}"
#         photo.save(os.path.join('uploads', filename))
#         new_photo = Photo(url=f"/uploads/{filename}", entry_id=entry.id)
#         db.session.add(new_photo)
#         db.session.commit()
#         return jsonify({'id': new_photo.id, 'url': new_photo.url}), 201

@app.route('/api/entries/<int:id>/photos', methods=['POST'])
@jwt_required()
def upload_photo(id):
    entry = Entry.query.get_or_404(id)
    data = request.json
    if 'url' not in data:
        return jsonify({'error': 'No photo URL provided'}), 400
    new_photo = Photo(url=data['url'], entry_id=entry.id)
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({'id': new_photo.id, 'url': new_photo.url}), 201

@app.route('/api/tags', methods=['GET'])
@jwt_required()
def get_tags():
    tags = Tag.query.all()
    return jsonify([{'id': tag.id, 'name': tag.name, 'created_at': tag.created_at.isoformat()} for tag in tags])

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/users/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    })

@app.route('/api/users/reset-password', methods=['POST'])
def reset_password():
    # In a real application, you would send an email with a reset link
    # For this example, we'll just return a success message
    return jsonify({'message': 'Password reset email sent'}), 200

@app.route('/api/tags', methods=['POST'])
@jwt_required()
def create_tag():
    data = request.json
    existing_tag = Tag.query.filter_by(name=data['name']).first()
    if existing_tag:
        return jsonify({"id": existing_tag.id, "name": existing_tag.name})
    new_tag = Tag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"id": new_tag.id, "name": new_tag.name}), 201

@app.route('/api/entries/<int:entry_id>/tags', methods=['POST'])
@jwt_required()
def add_tag_to_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    data = request.json
    tag = Tag.query.get_or_404(data['tag_id'])
    if tag not in entry.tags:
        entry.tags.append(tag)
        db.session.commit()
    return jsonify({"message": "Tag added successfully"}), 200

@app.route('/api/entries/<int:entry_id>/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def remove_tag_from_entry(entry_id, tag_id):
    entry = Entry.query.get_or_404(entry_id)
    tag = Tag.query.get_or_404(tag_id)
    if tag in entry.tags:
        entry.tags.remove(tag)
        db.session.commit()
    return '', 204

@app.route('/api/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)