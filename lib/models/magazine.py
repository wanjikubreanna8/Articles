from db.connection import CURSOR, CONN

class Magazine:
    all = {}

    def __init__(self, name, category, magazine_id = None):
        self.magazine_id = magazine_id
        self.name = name 
        self.category = category
    
    def __repr__(self):
        return f"Magazine ID ({self.magazine_id}): {self.name} -- {self.category}"

    @classmethod
    #Creating the magazines table
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
                magazine_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    #Deleting the magazines table
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS magazines;
        """
        CURSOR.execute(sql)
        CONN.commit()

    #Inserting a new row into the magazines table
    def save(self):
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()

        self.magazine_id = CURSOR.lastrowid
            
        #Adds the magazine instance to the dictionary
        type(self).all[self.magazine_id] = self

    @classmethod
    def instance_from_db(cls, row):

        #Checking for exitsing magazine instance using the row id
        magazine = cls.all.get(row[0])

        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2], magazine_id=row[0])
            cls.all[magazine.magazine_id] = magazine
        return magazine
    
    @classmethod
    def get_all(cls):
        """Return a list containing a Magazine object per row in the table"""
        sql = """
            SELECT *
            FROM magazines
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, magazine_id):
        sql = """
            SELECT * FROM magazines
            WHERE magazine_id = ?
        """
        row = CURSOR.execute(sql, (magazine_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM magazines
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_category(cls, category):
        sql = """
            SELECT * FROM magazines
            WHERE category = ?
        """
        row = CURSOR.execute(sql, (category,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def get_all_by_category(cls, category):
        sql = """
            SELECT * FROM magazines
            WHERE category = ?
        """
        rows = CURSOR.execute(sql, (category,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def with_multiple_authors(cls):
        sql = """
            SELECT m.*
            FROM magazines m
            JOIN articles a ON m.magazine_id = a.magazine_id
            GROUP BY m.magazine_id
            HAVING COUNT(DISTINCT a.author_id) >= 2
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def article_counts(cls):
        sql = """
            SELECT m.name, COUNT(a.article_id) AS article_count
            FROM magazines m
            LEFT JOIN articles a ON m.magazine_id = a.magazine_id
            GROUP BY m.magazine_id
        """
        rows = CURSOR.execute(sql).fetchall()
        return [{'name': row[0], 'article_count': row[1]} for row in rows]
    
    @classmethod
    def most_articles_written(cls):
        sql = """
            SELECT a.*, COUNT(ar.article_id) AS article_count
            FROM authors a
            JOIN articles ar ON a.author_id = ar.author_id
            GROUP BY a.author_id
            ORDER BY article_count DESC
            LIMIT 1
        """
        row = CURSOR.execute(sql).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    #Creating a new magazine record
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine
    
    #Updating an existing magazine record
    def update(self):
        sql = """
            UPDATE magazines
            SET name = ?, category = ?
            WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (self.name, self.category, self.magazine_id))
        CONN.commit()

    #Deleting an magazine record
    def delete(self):
        sql = """
            DELETE FROM magazines
            WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (self.magazine_id,))
        CONN.commit()

        del type(self).all[self.magazine_id]

        self.magazine_id = None

    def contributors(self):
        sql = """
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles a ON au.author_id = a.author_id
            WHERE a.magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.magazine_id,)).fetchall()
        from lib.models.author import Author
        return [Author.instance_from_db(row) for row in rows]

    def article_titles(self):
        sql = "SELECT title FROM articles WHERE magazine_id = ?"
        rows = CURSOR.execute(sql, (self.magazine_id,)).fetchall()
        return [row[0] for row in rows]

    def contributing_authors(self):
        sql = """
            SELECT au.*, COUNT(a.article_id) as article_count
            FROM authors au
            JOIN articles a ON au.author_id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.author_id
            HAVING article_count > 2
        """
        rows = CURSOR.execute(sql, (self.magazine_id,)).fetchall()
        from lib.models.author import Author
        return [Author.instance_from_db(row) for row in rows]

    def articles(self):
        #Return all the articles associated with the current Magazine instance
        from lib.models.article import Article
        sql = """
            SELECT * FROM articles
            WHERE magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.magazine_id,)).fetchall()

        return [Article.instance_from_db(row) for row in rows]
    
    def authors(self):
        from lib.models.author import Author
        sql = """
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles ar ON au.author_id = ar.author_id
            WHERE ar.magazine_id = ?
        """
        rows = CURSOR.execute(sql, (self.magazine_id,)).fetchall()
        return [Author.instance_from_db(row) for row in rows]

    