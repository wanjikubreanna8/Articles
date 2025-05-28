from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

    @classmethod
    def create_table(cls):
        """Create the articles table"""
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    magazine_id INTEGER NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
                    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
                )
            """)

    def save(self):
        """Save the article to the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.id)
                )

    @classmethod
    def create(cls, title, author, magazine):
        """Create and save a new article"""
        article = cls(title, author.id, magazine.id)
        article.save()
        return article

    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID"""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM articles WHERE id = ?", 
                (id,)
            ).fetchone()
            if row:
                return cls(row['title'], row['author_id'], row['magazine_id'], row['id'])
            return None

    def author(self):
        """Get the author of this article"""
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        """Get the magazine this article was published in"""
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def all(cls):
        """Get all articles"""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles").fetchall()
            return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                   for row in rows]# ... existing code ...

        # ... existing code ...

        @classmethod
        def all(cls):
            """Get all articles"""
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM articles")
                rows = cursor.fetchall()
                if rows:
                    return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                        for row in rows]
                return []