import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.connection import CONN, CURSOR
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Drop tables (optional, for a clean setup)
Article.drop_table()
Author.drop_table()
Magazine.drop_table()

# Create tables
Author.create_table()
Magazine.create_table()
Article.create_table()

print("Database setup complete.")