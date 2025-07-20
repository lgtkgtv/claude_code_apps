from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from nicegui import app as nicegui_app, ui
from pathlib import Path
import shutil
from fastapi.responses import RedirectResponse

# ---------- Setup FastAPI ----------
app = FastAPI(
    title="Photo Upload API",
    docs_url="/api/docs",             # Swagger UI
    redoc_url="/api/redoc",           # ReDoc
    openapi_url="/openapi.json",
)

# Allow cross-origin if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # during dev
        # "https://your-frontend-domain.com",  # production frontend
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

# Upload folder setup
upload_dir = Path("static/uploads")
upload_dir.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile):
    dest = upload_dir / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

# Serve uploaded files statically
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------- Setup NiceGUI ----------
@ui.page("/")
def show_ui():
    ui.label("📸 Photo Uploader")

    image = ui.image()

    def handle_upload(e):
        file = e.files[0]
        with open(file["content"], "rb") as f:
            import requests
            res = requests.post("http://localhost:8080/upload", files={"file": (file["name"], f)})
            filename = res.json()["filename"]
            image.set_source(f"/static/uploads/{filename}")

    picker = ui.upload(on_upload=handle_upload)
    picker.label = "Upload Image"


# ---------- Mount NiceGUI onto FastAPI ----------
nicegui_app.include_router(app.router)
nicegui_app.mount("/static", StaticFiles(directory="static"), name="static")

# Run server
ui.run(title="Photo Sharing App", port=8080, reload=False)
