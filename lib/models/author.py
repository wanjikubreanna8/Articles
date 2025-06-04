from db.connection import CURSOR, CONN

class Author:
    all = {}

    def __init__(self, name, author_id = None):
        self.author_id = author_id
        self.name = name 
    
    def __repr__(self):
        return f"Author ID ({self.author_id}): {self.name}"
    
    @property
    def id(self):
        return self.author_id

    @classmethod
    #Creating the authors table
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
                author_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
        ...

    @classmethod
    #Deleting the authors table
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS authors;
        """
        CURSOR.execute(sql)
        CONN.commit()

    #Inserting a new row into the authors table
    def save(self):
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.author_id = CURSOR.lastrowid

        #Adds the author instance to the dictionary
        type(self).all[self.author_id] = self

    @classmethod
    def instance_from_db(cls, row):

        #Checking for exitsing author instance using the row id
        author = cls.all.get(row[0])

        if author:
            author.name = row[1]
        else:
            author = cls(row[1], author_id=row[0])
            cls.all[author.author_id] = author
        return author
    
    @classmethod
    def get_all(cls):
        """Return a list containing a Author object per row in the table"""
        sql = """
            SELECT *
            FROM authors
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, author_id):
        sql = """
            SELECT * FROM authors
            WHERE author_id = ?
        """
        row = CURSOR.execute(sql, (author_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM authors
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    #Creating a new author record
    def create(cls, name):
        author = cls(name)
        author.save()
        return author
    
    @classmethod
    def add_with_articles(cls, name, articles_data):
        try:
            with CONN:
                CURSOR.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (name,)
                )
                author_id = CURSOR.lastrowid

                for article in articles_data:
                    CURSOR.execute(
                        "INSERT INTO articles (name, title, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                        (article['name'], article['title'], author_id, article['magazine_id'])
                    )
            return cls.find_by_id(author_id)
        except Exception as e:
            print(f"Transaction failed: {e}")
            return None

    
    #Updating an existing author record
    def update(self):
        sql = """
            UPDATE authors
            SET name = ?
            WHERE author_id = ?
        """
        CURSOR.execute(sql, (self.name, self.author_id))
        CONN.commit()

    #Deleting an author record
    def delete(self):
        sql = """
            DELETE FROM authors
            WHERE author_id = ?
        """
        CURSOR.execute(sql, (self.author_id,))
        CONN.commit()

        del type(self).all[self.author_id]

        self.author_id = None

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author_id=self.author_id, magazine_id=magazine.magazine_id)
        article.save()
        return article

    def topic_areas(self):
        sql = """
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.magazine_id = a.magazine_id
            WHERE a.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.author_id,)).fetchall()
        return [row[0] for row in rows]
    
    @classmethod
    def top_author(cls):
        sql = """
            SELECT a.author_id, a.name, COUNT(ar.article_id) AS article_count
            FROM authors a
            JOIN articles ar ON a.author_id = ar.author_id
            GROUP BY a.author_id
            ORDER BY article_count DESC
            LIMIT 1
        """
        row = CURSOR.execute(sql).fetchone()
        if row:
            # row[0] = author_id, row[1] = name
            return cls.find_by_id(row[0])
        return None

    def articles(self):
        #Return a list of articles associated with the current author
        from lib.models.article import Article
        sql = """
            SELECT * FROM articles
            WHERE author_id = ?
        """
        rows = CURSOR.execute(sql, (self.author_id,)).fetchall()

        return [Article.instance_from_db(row) for row in rows]
    
    def magazines(self):
        from lib.models.magazine import Magazine
        sql = """
            SELECT DISTINCT m.*
            FROM magazines m
            JOIN articles a ON m.magazine_id = a.magazine_id
            WHERE a.author_id = ?
        """
        rows = CURSOR.execute(sql, (self.author_id,)).fetchall()
        return [Magazine.instance_from_db(row) for row in rows]