from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Определение модели данных для запроса
class Post(BaseModel):
    title: str | None = None
    content: str
    author: str | None = None

# Настройка CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Создание таблицы, если она не существует
def init_db():
    con = sqlite3.connect("main.db")
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT NOT NULL,
        author TEXT
    );""")
    con.commit()
    con.close()

init_db()  # Инициализация базы данных при запуске сервера

# Зависимость для подключения к базе данных
def get_db():
    con = sqlite3.connect("main.db")
    try:
        yield con
    finally:
        con.close()

# Эндпоинт для получения всех постов
@app.get('/')
async def home(db: sqlite3.Connection = Depends(get_db)):
    c = db.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    c.close()
    return posts

# Эндпоинт для добавления поста
@app.post('/add_post')
async def add_post(post: Post, db: sqlite3.Connection = Depends(get_db)):
    c = db.cursor()
    c.execute("INSERT INTO posts (title, content, author) VALUES (?,?,?)", (post.title, post.content, post.author))
    db.commit()
    c.close()
    return {"status": "Post added successfully"}
