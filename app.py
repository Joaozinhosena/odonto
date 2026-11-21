"""DR ODONTO — institutional website built with Flask + Tailwind CDN."""

import os
import re
from pathlib import Path
from urllib.parse import quote, urlparse

from dotenv import load_dotenv
from flask import Flask, render_template

# Carrega o .env da mesma pasta deste arquivo, independentemente de onde
# o comando python app.py for executado.
PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_DIR / ".env", override=False)

app = Flask(__name__)


def env_text(name: str, default: str = "") -> str:
    """Read a trimmed environment value."""
    return os.getenv(name, default).strip()


def digits_only(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def valid_http_url(value: str) -> str:
    """Only expose absolute HTTP(S) URLs in external links."""
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    return value if parsed.scheme in {"http", "https"} and parsed.netloc else ""


@app.route("/")
def index():
    whatsapp_number = digits_only(env_text("WHATSAPP_NUMBER"))
    message = quote("Olá! Gostaria de agendar uma consulta na DR ODONTO.", safe="")
    # O link wa.me funciona tanto no celular quanto no computador e abre
    # a conversa com o número já preenchido e a mensagem pronta.
    whatsapp_url = (
        f"https://wa.me/{whatsapp_number}?text={message}"
        if len(whatsapp_number) >= 12
        else ""
    )

    # Links oficiais informados pela clínica; podem ser sobrescritos no ambiente.
    instagram_url = valid_http_url(env_text("INSTAGRAM_URL")) or "https://www.instagram.com/drodonto_varzea/"
    social_links = [
        {"label": "Instagram", "url": instagram_url, "icon": "instagram"},
        {"label": "Facebook", "url": valid_http_url(env_text("FACEBOOK_URL")), "icon": "facebook"},
        {"label": "TikTok", "url": valid_http_url(env_text("TIKTOK_URL")), "icon": "tiktok"},
    ]
    social_links = [item for item in social_links if item["url"]]

    return render_template(
        "index.html",
        clinic_name=env_text("CLINIC_NAME", "DR ODONTO"),
        clinic_tagline=env_text("CLINIC_TAGLINE", "Odontologia especializada"),
        clinic_address=env_text("CLINIC_ADDRESS"),
        clinic_hours=env_text("CLINIC_HOURS"),
        clinic_phone=env_text("CLINIC_PHONE"),
        whatsapp_url=whatsapp_url,
        instagram_url=instagram_url,
        social_links=social_links,
    )


if __name__ == "__main__":
    # Debug fica desligado por padrão. Ative apenas durante o desenvolvimento.
    app.run(
        host="0.0.0.0",
        port=int(env_text("PORT", "5000")),
        debug=env_text("FLASK_DEBUG", "0") == "1",
    )
