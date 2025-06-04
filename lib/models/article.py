
from db.connection import CURSOR, CONN

class Article:
    all = {}

    def __init__(self, title, author_id, magazine_id ,article_id = None):
        self.article_id = article_id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return (
            f"<Article ID ({self.article_id}): {self.title} " +
            f"Author ID ({self.author_id}), Magazine ID ({self.magazine_id})>"
        )

    @classmethod
    #Creating the articles table
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
                article_id INTEGER PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(author_id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    #Deleting the articles table
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS articles;
        """
        CURSOR.execute(sql)
        CONN.commit()

    #Inserting a new row into the articles table
    def save(self):
        sql = """
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id))
        CONN.commit()

        self.article_id = CURSOR.lastrowid
        
        #Adds the article instance to the dictionary
        type(self).all[self.article_id] = self

    @classmethod
    def instance_from_db(cls, row):

        #Checking for exitsing article instance using the row id
        article = cls.all.get(row[0])

        if article:
            article.title = row[1]
            article.author_id = row[2]
            article.magazine_id = row[3]
        else:
            article = cls(row[1], row[2], row[3], article_id=row[0])
            cls.all[article.article_id] = article
        return article
    
    @classmethod
    def get_all(cls):
        """Return a list containing a Article object per row in the table"""
        sql = """
            SELECT *
            FROM articles
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, article_id):
        sql = """
            SELECT * FROM articles
            WHERE article_id = ?
        """
        row = CURSOR.execute(sql, (article_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    
    @classmethod
    def find_by_title(cls, title):
        sql = """
           SELECT * FROM articles
           WHERE title = ?
        """
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    #Creating a new article record
    def create(cls, title, author_id, magazine_id):
        article = cls(title, author_id, magazine_id)
        article.save()
        return article
    
    #Updating an existing article record
    def update(self):
        sql = """
            UPDATE articles
            SET title = ?, author_id = ?, magazine_id = ?
            WHERE article_id = ?
        """
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id, self.article_id))
        CONN.commit()

    #Deleting an article record
    def delete(self):
        sql = """
            DELETE FROM articles
            WHERE article_id = ?
        """
        CURSOR.execute(sql, (self.article_id,))
        CONN.commit()

        del type(self).all[self.article_id]

        self.article_id = None
