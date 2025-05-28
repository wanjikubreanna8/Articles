import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def setup_sample_data():
    """Initialize the database with sample data"""
    with get_connection() as conn:
        schema_path = os.path.join(os.path.dirname(__file__), 'db', 'schema.sql')
        with open(schema_path) as f:
            conn.executescript(f.read())
    
    # Create authors
    author1 = Author.create("John Doe")
    author2 = Author.create("Jane Smith")
    
    # Create magazines
    magazine1 = Magazine.create("Tech Today", "Technology")
    magazine2 = Magazine.create("Science Weekly", "Science")
    
    # Create articles
    Article.create("Python ORM Guide", author1, magazine1)
    Article.create("Machine Learning Trends", author2, magazine1)
    Article.create("Quantum Computing", author2, magazine2)
    
    print("\n Sample data created successfully.\n")

def display_all():
    """Display authors, magazines, and articles"""
    print(" Authors:")
    for author in Author.all():
        print(f" - {author.name}")

    print("\n Magazines:")
    for magazine in Magazine.all():
        print(f" - {magazine.name}")

    print("\n Articles:")
    for article in Article.all():
        print(f" - {article.title} (Author: {article.author().name}, Magazine: {article.magazine().name})")

if __name__ == "__main__":
    setup_sample_data()
    display_all()
