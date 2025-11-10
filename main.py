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

@app.get("/demontazh-peregorodok-v-saratove", response_class=HTMLResponse)
def serve_demontazh_peregorodok_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/demontazh-peregorodok-v-saratove.html", {"request": request})

@app.get("/vozvedenie-peregorodok-v-saratove", response_class=HTMLResponse)
def serve_vozvedenie_peregorodok_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/vozvedenie-peregorodok-v-saratove.html", {"request": request})

@app.get("/stjazhka-pola-v-saratove", response_class=HTMLResponse)
def serve_stjazhka_pola_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/stjazhka-pola-v-saratove.html", {"request": request})

@app.get("/vyravnivanie-sten-v-saratove", response_class=HTMLResponse)
def serve_vyravnivanie_sten_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/vyravnivanie-sten-v-saratove.html", {"request": request})

@app.get("/shumoizolyaciya-uteplenie-v-saratove", response_class=HTMLResponse)
def serve_shumoizolyaciya_uteplenie_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/shumoizolyaciya-uteplenie-v-saratove.html", {"request": request})

@app.get("/malyarnie-raboty-v-saratove", response_class=HTMLResponse)
def serve_malyarnie_raboty_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/malyarnie-raboty-v-saratove.html", {"request": request})

@app.get("/pokleyka-oboev-v-saratove", response_class=HTMLResponse)
def serve_pokleyka_oboev_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/pokleyka-oboev-v-saratove.html", {"request": request})

@app.get("/ukladka-plitki-v-saratove", response_class=HTMLResponse)
def serve_ukladka_plitki_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/ukladka-plitki-v-saratove.html", {"request": request})

@app.get("/natyazhnie-potolki-v-saratove", response_class=HTMLResponse)
def serve_natyazhnie_potolki_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/natyazhnie-potolki-v-saratove.html", {"request": request})

@app.get("/santekhnicheskie-raboty-v-saratove", response_class=HTMLResponse)
def serve_santekhnicheskie_raboty_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/santekhnicheskie-raboty-v-saratove.html", {"request": request})

@app.get("/elektromontazhnye-raboty-v-saratove", response_class=HTMLResponse)
def serve_elektromontazhnye_raboty_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/elektromontazhnye-raboty-v-saratove.html", {"request": request})

@app.get("/shtukaturnye-raboty-v-saratove", response_class=HTMLResponse)
def serve_shtukaturnye_raboty_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/shtukaturnye-raboty-v-saratove.html", {"request": request})

@app.get("/ukladka-laminata-parketa-linoleuma-v-saratove", response_class=HTMLResponse)
def serve_ukladka_laminata_parketa_linoleuma_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/ukladka-laminata-parketa-linoleuma-v-saratove.html", {"request": request})

@app.get("/ustanovka-kondicionerov-v-saratove", response_class=HTMLResponse)
def serve_ustanovka_kondicionerov_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/ustanovka-kondicionerov-v-saratove.html", {"request": request})

@app.get("/montazh-otopleniya-v-saratove", response_class=HTMLResponse)
def serve_montazh_otopleniya_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/montazh-otopleniya-v-saratove.html", {"request": request})

@app.get("/montazh-ventilyacii-v-saratove", response_class=HTMLResponse)
def serve_montazh_ventilyacii_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/montazh-ventilyacii-v-saratove.html", {"request": request})

@app.get("/zalivka-fundamenta-v-saratove", response_class=HTMLResponse)
def serve_zalivka_fundamenta_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/zalivka-fundamenta-v-saratove.html", {"request": request})

@app.get("/betonnye-raboty-v-saratove", response_class=HTMLResponse)
def serve_betonnye_raboty_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/betonnye-raboty-v-saratove.html", {"request": request})

@app.get("/kladka-kirpicha-i-gazobetona-v-saratove", response_class=HTMLResponse)
def serve_kladka_kirpicha_i_gazobetona_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/kladka-kirpicha-i-gazobetona-v-saratove.html", {"request": request})

@app.get("/monolitnye-konstrukcii-v-saratove", response_class=HTMLResponse)
def serve_monolitnye_konstrukcii_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/monolitnye-konstrukcii-v-saratove.html", {"request": request})

@app.get("/dizajn-i-3d-vizualizaciya-v-saratove", response_class=HTMLResponse)
def serve_dizajn_i_3d_vizualizaciya_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/dizajn-i-3d-vizualizaciya-v-saratove.html", {"request": request})

@app.get("/montazh-dverei-i-okon-v-saratove", response_class=HTMLResponse)
def serve_montazh_dverei_i_okon_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/montazh-dverei-i-okon-v-saratove.html", {"request": request})

@app.get("/mebel-i-vstroennye-konstrukcii-v-saratove", response_class=HTMLResponse)
def serve_mebel_i_vstroennye_konstrukcii_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/mebel-i-vstroennye-konstrukcii-v-saratove.html", {"request": request})

@app.get("/landshaftnye-raboty-v-saratove", response_class=HTMLResponse)
def serve_landshaftnye_raboty_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/landshaftnye-raboty-v-saratove.html", {"request": request})

@app.get("/remont-pod-klyuch-v-saratove", response_class=HTMLResponse)
def serve_remont_pod_klyuch_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/remont-pod-klyuch-v-saratove.html", {"request": request})

@app.get("/kapitalnyi-remont-v-saratove", response_class=HTMLResponse)
def serve_kapitalnyyi_remont_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/kapitalnyi-remont-v-saratove.html", {"request": request})

@app.get("/kosmeticheskiy-remont-v-saratove", response_class=HTMLResponse)
def serve_kosmeticheskiy_remont_v_saratove(request: Request):
    return templates.TemplateResponse("services-pages/kosmeticheskiy-remont-v-saratove.html", {"request": request})

@app.post("/submit-application")
async def submit_application(
    phone: str = Form(...),
    comment: str = Form(None) 
):
    try:
        save_application(phone.strip(), comment.strip() if comment else None)
        return JSONResponse({"status": "success", "message": "Заявка успешно отправлена"})
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Ошибка сервера"})
