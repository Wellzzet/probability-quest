"""Языки сайта: русский, английский, казахский."""
import streamlit as st

LANGS = {"ru": "🇷🇺 RU", "en": "🇬🇧 EN", "kk": "🇰🇿 KZ"}
DEFAULT = "ru"


def lang() -> str:
    try:
        v = st.session_state.get("lang", DEFAULT)
    except Exception:  # noqa: BLE001 — вне Streamlit
        v = DEFAULT
    return v if v in LANGS else DEFAULT


def L(lg, ru, en, kk):
    """Выбрать текст для заданного языка."""
    return {"ru": ru, "en": en, "kk": kk}.get(lg, ru)


def tr(ru, en, kk):
    """Выбрать текст для текущего языка сайта."""
    return L(lang(), ru, en, kk)
