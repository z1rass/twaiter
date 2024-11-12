from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
app = FastAPI()

class Post(BaseModel):
    title: str | None = None
    content: str
    author: str | None = None

con = sqlite3.connect("main.db")
c = con.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT NOT NULL,
    author TEXT
);
""")
con.commit()
c.close()





@app.get('/')
async def home():
    con = sqlite3.connect("main.db")
    c = con.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    con.commit()
    c.close()
    return posts



@app.post('/add_post')
async def add_post(post: Post):
    con = sqlite3.connect("main.db")
    c = con.cursor()
    c.execute("INSERT INTO posts (title, content, author) VALUES (?,?,?)", (post.title, post.content, post.author))
    con.commit()
    c.close()
    return 200