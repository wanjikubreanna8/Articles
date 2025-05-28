import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_database():
    """Setup database for each test that needs it"""
    # Setup tables and schema
    with get_connection() as conn:
        with open('lib/db/schema.sql') as f:
            conn.executescript(f.read())

    # Create test data (one author, one magazine, one article)
    author = Author.create("Test Author")
    magazine = Magazine.create("Test Magazine", "Test Category")
    article = Article.create("Test Article", author, magazine)

    yield article

    # Clean up after test
    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        # Reset SQLite autoincrement counters
        conn.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'articles'")
        conn.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'authors'")
        conn.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'magazines'")
