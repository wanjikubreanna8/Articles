from .connection import get_connection
from lib.models import Author, Article, Magazine

def clear_tables(cursor):
    """Clear all data from tables"""
    tables = ["articles", "authors", "magazines"]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

def create_authors():
    """Return list of sample authors"""
    return [
        Author("J.K. Rowling"),
        Author("Stephen King"),
        Author("Margaret Atwood"),
        Author("Neil Gaiman"),
        Author("Ursula K. Le Guin")
    ]

def create_magazines():
    """Return list of sample magazines"""
    return [
        Magazine("Fantasy Quarterly", "Fantasy"),
        Magazine("Horror Today", "Horror"),
        Magazine("Literary Review", "Literature"),
        Magazine("Sci-Fi Chronicles", "Science Fiction")
    ]

def create_articles(authors, magazines):
    """Return list of sample articles"""
    return [
        Article("The Philosopher's Stone", authors[0].id, magazines[0].id),
        Article("The Shining", authors[1].id, magazines[1].id),
        Article("The Handmaid's Tale", authors[2].id, magazines[2].id),
        Article("Fantastic Beasts", authors[0].id, magazines[0].id),
        Article("It", authors[1].id, magazines[1].id),
        Article("American Gods", authors[3].id, magazines[3].id),
        Article("A Wizard of Earthsea", authors[4].id, magazines[0].id)
    ]

def seed_database():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        clear_tables(cursor)
        authors = create_authors()
        magazines = create_magazines()
        for author in authors:
            author.save()
        for magazine in magazines:
            magazine.save()
        articles = create_articles(authors, magazines)
        for article in articles:
            article.save()
        conn.commit()
        print("✅ Database seeded successfully!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    seed_database()
    print("Seeding database...")
    seed_database()