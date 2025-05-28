import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_database():
    """Setup database for each test"""
    with get_connection() as conn:
        with open('lib/db/schema.sql') as f:
            conn.executescript(f.read())
    
    # Create test data
    author = Author.create("Test Author")
    magazine1 = Magazine.create("Magazine 1", "Category 1")
    magazine2 = Magazine.create("Magazine 2", "Category 2")
    Article.create("Article 1", author, magazine1)
    Article.create("Article 2", author, magazine1)
    Article.create("Article 3", author, magazine2)
    
    yield
    
    # Clean up
    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")

def test_author_creation():
    author = Author.find_by_name("Test Author")
    assert author is not None
    assert author.name == "Test Author"

def test_author_articles():
    author = Author.find_by_name("Test Author")
    articles = author.articles()
    assert len(articles) == 3
    assert {a.title for a in articles} == {"Article 1", "Article 2", "Article 3"}

def test_author_magazines():
    author = Author.find_by_name("Test Author")
    magazines = author.magazines()
    assert len(magazines) == 2
    assert {m.name for m in magazines} == {"Magazine 1", "Magazine 2"}

def test_author_topic_areas():
    author = Author.find_by_name("Test Author")
    categories = author.topic_areas()
    assert len(categories) == 2
    assert set(categories) == {"Category 1", "Category 2"}

def test_author_add_article():
    author = Author.find_by_name("Test Author")
    magazine = Magazine.find_by_name("Magazine 1")
    new_article = author.add_article(magazine, "New Article")
    
    assert new_article is not None
    assert new_article.title == "New Article"
    assert len(author.articles()) == 4