import sys
import os

# Ajouter le dossier parent au PYTHONPATH pour que les imports fonctionnent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def setup_database():
    """Initialize the database with tables"""
    with get_connection() as conn:
        with open(os.path.join(os.path.dirname(__file__), '..', 'lib', 'db', 'schema.sql')) as f:
            conn.executescript(f.read())
    print("Database tables created successfully.")

def seed_database():
    """Add sample data to the database"""
    # Create authors
    author1 = Author.create("John Doe")
    author2 = Author.create("Jane Smith")
    author3 = Author.create("Bob Johnson")

    # Create magazines
    magazine1 = Magazine.create("Tech Today", "Technology")
    magazine2 = Magazine.create("Science Weekly", "Science")
    magazine3 = Magazine.create("Business Insights", "Business")

    # Create articles
    Article.create("Python ORM Guide", author1, magazine1)
    Article.create("Machine Learning Trends", author2, magazine1)
    Article.create("Quantum Computing", author2, magazine2)
    Article.create("Startup Funding", author3, magazine3)
    Article.create("AI Ethics", author1, magazine1)
    Article.create("Blockchain Revolution", author3, magazine1)
    Article.create("Data Privacy", author1, magazine2)
    Article.create("Cloud Computing", author2, magazine1)

    print("Sample data seeded successfully.")

if __name__ == "__main__":
    setup_database()
    seed_database()
