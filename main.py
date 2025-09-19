from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключаем папку static для css/js
app.mount("/static", StaticFiles(directory="static"), name="static")

# Отдаём index.html
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
