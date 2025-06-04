-- Drop existing tables if they exist (for reinitialization)
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS magazines;

-- Create authors table
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create magazines table
CREATE TABLE magazines (
    magazine_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);

-- Create articles table
CREATE TABLE articles (
    article_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER,
    magazine_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(author_id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id)
);