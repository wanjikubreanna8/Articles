from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name} ({self.category})>"

    @classmethod
    def create_table(cls):
        """Create the magazines table"""
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS magazines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            """)

    def save(self):
        """Save the magazine to the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )

    @classmethod
    def create(cls, name, category):
        """Create and save a new magazine"""
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID"""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM magazines WHERE id = ?", 
                (id,)
            ).fetchone()
            if row:
                return cls(row['name'], row['category'], row['id'])
            return None

    @classmethod
    def find_by_name(cls, name):
        """Find a magazine by name"""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM magazines WHERE name = ?", 
                (name,)
            ).fetchone()
            if row:
                return cls(row['name'], row['category'], row['id'])
            return None

    @classmethod
    def all(cls):
        """Return all magazines from the database"""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM magazines").fetchall()
            return [cls(row["name"], row["category"], row["id"]) for row in rows]

    def articles(self):
        """Get all articles published in this magazine"""
        from lib.models.article import Article
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (self.id,)
            ).fetchall()
            return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                   for row in rows]

    def contributors(self):
        """Get all authors who have written for this magazine"""
        from lib.models.author import Author
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT authors.*
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
            """, (self.id,)).fetchall()
            return [Author(row['name'], row['id']) for row in rows]

    def article_titles(self):
        """Get all article titles published in this magazine"""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT title FROM articles WHERE magazine_id = ?",
                (self.id,)
            ).fetchall()
            return [row['title'] for row in rows]

    def contributing_authors(self):
        """Get authors with more than 2 articles in this magazine"""
        from lib.models.author import Author
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING article_count > 2
            """, (self.id,)).fetchall()
            return [Author(row['name'], row['id']) for row in rows]

    @classmethod
    def top_publisher(cls):
        """Find the magazine with the most articles"""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT magazines.*, COUNT(articles.id) as article_count
                FROM magazines
                LEFT JOIN articles ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
                ORDER BY article_count DESC
                LIMIT 1
            """).fetchone()
            if row:
                return cls(row['name'], row['category'], row['id'])
            return None
