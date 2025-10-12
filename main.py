from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from database import init_db, save_application

app = FastAPI()

# Инициализируем базу данных при запуске
init_db()

# Подключаем папку static для css/js
app.mount("/static", StaticFiles(directory="static"), name="static")

# Отдаём index.html
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/privacy", response_class=HTMLResponse)
def serve_privacy():
    with open("privacy.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/submit-application")
async def submit_application(
    name: str = Form(...),
    phone: str = Form(...),
    comment: str = Form(None)  # <--- Новое поле, необязательное
):
    try:
        save_application(name.strip(), phone.strip(), comment.strip() if comment else None)
        return JSONResponse({"status": "success", "message": "Заявка успешно отправлена"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Ошибка сервера"})
