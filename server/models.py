from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        if value == "" or key == None:
            raise ValueError("requires author to have a name.")
        elif value in [author.name for author in Author.query.all()]:
            raise ValueError("requires author to have a unique name.")
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("requires each phone number to be exactly ten digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Content too short. Less than 250 chars.")
        return value
    
    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Summary too long. More than 250 chars.")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if value != "Fiction" and value != "Non-Fiction":
            raise ValueError("Incorrect category.")
        return value
    
    @validates('title')
    def validate_name(self, key, value):
        click_baits = ["Won't Believe", "Secret", "Top", "Guess"]
        for element in click_baits:
            if element in value:
                return value
        raise ValueError("No clickbait validator for title.")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
