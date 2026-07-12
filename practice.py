import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo(
    id INTEGER PRIMARY KEY,
    name TEXT)
""")
conn.commit()

class Todo(BaseModel):
    name: str

@app.get("/")
def root():
    return {"message": "SQLite connected successfully"}

@app.post("/todo")
def add_todo(todo: Todo):
    cursor.execute("INSERT INTO todo (name) VALUES (?)", (todo.name,))
    conn.commit()
    return {"message": "Todo added", "name": todo.name}