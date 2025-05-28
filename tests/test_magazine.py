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
    author1 = Author.create("Author 1")
    author2 = Author.create("Author 2")
    magazine = Magazine.create("Test Magazine", "Test Category")
    Article.create("Article 1", author1, magazine)
    Article.create("Article 2", author1, magazine)
    Article.create("Article 3", author2, magazine)
    Article.create("Article 4", author2, magazine)
    Article.create("Article 5", author2, magazine)
    
    yield
    
    # Clean up
    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")

def test_magazine_creation():
    magazine = Magazine.find_by_name("Test Magazine")
    assert magazine is not None
    assert magazine.name == "Test Magazine"
    assert magazine.category == "Test Category"

def test_magazine_articles():
    magazine = Magazine.find_by_name("Test Magazine")
    articles = magazine.articles()
    assert len(articles) == 5
    assert {a.title for a in articles} == {f"Article {i}" for i in range(1, 6)}

def test_magazine_contributors():
    magazine = Magazine.find_by_name("Test Magazine")
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert {c.name for c in contributors} == {"Author 1", "Author 2"}

def test_magazine_article_titles():
    magazine = Magazine.find_by_name("Test Magazine")
    titles = magazine.article_titles()
    assert len(titles) == 5
    assert set(titles) == {f"Article {i}" for i in range(1, 6)}

def test_magazine_contributing_authors():
    magazine = Magazine.find_by_name("Test Magazine")
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Author 2"

def test_magazine_top_publisher():
    # Create another magazine with fewer articles
    Magazine.create("Other Magazine", "Other Category")
    top_magazine = Magazine.top_publisher()
    assert top_magazine.name == "Test Magazine"