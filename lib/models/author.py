from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @classmethod
    def create_table(cls):
        """Create the authors table in the database"""
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

    def save(self):
        """Insert or update the author in the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )

    @classmethod
    def create(cls, name):
        """Create and save a new author instance"""
        author = cls(name)
        author.save()
        return author

    @classmethod
    def find_by_id(cls, id):
        """Find an author by their ID"""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM authors WHERE id = ?", 
                (id,)
            ).fetchone()
            if row:
                return cls(row['name'], row['id'])
            return None

    @classmethod
    def find_by_name(cls, name):
        """Find an author by their name"""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM authors WHERE name = ?", 
                (name,)
            ).fetchone()
            if row:
                return cls(row['name'], row['id'])
            return None

    def articles(self):
        """Return all articles written by this author"""
        from lib.models.article import Article
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (self.id,)
            ).fetchall()
            return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                    for row in rows]

    def magazines(self):
        """Return all unique magazines this author has written for"""
        from lib.models.magazine import Magazine
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT magazines.* 
                FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
            """, (self.id,)).fetchall()
            return [Magazine(row['name'], row['category'], row['id']) 
                    for row in rows]

    def add_article(self, magazine, title):
        """Create and save a new article for this author in a magazine"""
        from lib.models.article import Article
        return Article.create(title, self, magazine)

    def topic_areas(self):
        """Return all unique magazine categories this author has written for"""
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT category 
                FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
            """, (self.id,)).fetchall()
            return [row['category'] for row in rows]

    @classmethod
    def all(cls):
        """Return all authors in the database"""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM authors").fetchall()
            return [cls(row["name"], row["id"]) for row in rows]
