from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import init_db, save_application

app = FastAPI()

# Инициализируем базу данных при запуске
init_db()

# Подключаем папку static для css/js
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настраиваем шаблонизатор
templates = Jinja2Templates(directory="templates")

# Отдаём index.html
@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/privacy", response_class=HTMLResponse)
def serve_privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.post("/submit-application")
async def submit_application(
    name: str = Form(...),
    phone: str = Form(...),
    comment: str = Form(None) 
):
    try:
        save_application(name.strip(), phone.strip(), comment.strip() if comment else None)
        return JSONResponse({"status": "success", "message": "Заявка успешно отправлена"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Ошибка сервера"})
