"""Состояние игры: монеты, опыт, открытые темы, сохранение/загрузка."""
import json
import random
import streamlit as st
from .content import TOPICS, TOPIC_BY_ID, title
from .i18n import tr, lang

PASS_MARK = 4          # нужно правильных из 5, чтобы пройти тему
BOSS_PASS = 7          # нужно правильных из 10, чтобы победить Босса
FIRST_BONUS = 100      # бонус за первое прохождение темы
PER_CORRECT_FIRST = 25
PER_CORRECT_REPEAT = 10
BOSS_REWARD = 500

RANKS = [  # (нужно XP, ru, en, kk)
    (0, "Новичок", "Novice", "Жаңадан бастаушы"),
    (300, "Ученик", "Apprentice", "Шәкірт"),
    (700, "Оруженосец", "Squire", "Сауытшы"),
    (1200, "Страж", "Guardian", "Сақшы"),
    (1800, "Рыцарь", "Knight", "Рыцарь"),
]
FINAL_RANK = ("Рыцарь Вероятностей", "Knight of Probability", "Ықтималдық рыцары")


def default_game():
    return {
        "version": 1,
        "name": "",
        "look": {"skin": "Тёплая", "hair": "Чёрные", "outfit": "Синий", "style": "Длинные"},
        "coins": 0,
        "xp": 0,
        "unlocked": [1],
        "completed": {},       # "id" -> лучший результат
        "attempts": {},        # "id" -> число попыток
        "boss_done": False,
        "boss_best": 0,
        "quiz_seeds": {},
    }


def game():
    if "game" not in st.session_state:
        st.session_state.game = default_game()
    return st.session_state.game


def is_unlocked(tid):
    return tid in game()["unlocked"]


def is_completed(tid):
    return str(tid) in game()["completed"]


def all_completed():
    return all(is_completed(t["id"]) for t in TOPICS)


def buy_status(tid):
    """Возвращает (можно_купить, причина)."""
    G = game()
    t = TOPIC_BY_ID[tid]
    if is_unlocked(tid):
        return False, tr("уже открыта", "already unlocked", "ашылған")
    if tid > 1 and not is_completed(tid - 1):
        return False, tr(f"сначала пройди тему {tid - 1}", f"finish topic {tid - 1} first", f"алдымен {tid - 1}-тақырыпты өт")
    if G["coins"] < t["cost"]:
        need = t["cost"] - G["coins"]
        return False, tr(f"нужно ещё {need} 🪙", f"need {need} more 🪙", f"тағы {need} 🪙 керек")
    return True, ""


def buy(tid):
    ok, _ = buy_status(tid)
    if ok:
        G = game()
        G["coins"] -= TOPIC_BY_ID[tid]["cost"]
        G["unlocked"].append(tid)
        name = title(TOPIC_BY_ID[tid], lang())
        st.session_state["flash"] = tr(f"🔓 Тема «{name}» открыта!", f"🔓 Topic \"{name}\" unlocked!", f"🔓 «{name}» тақырыбы ашылды!")


def quiz_seed(tid):
    G = game()
    key = str(tid)
    if key not in G["quiz_seeds"]:
        G["quiz_seeds"][key] = random.randint(1, 10**9)
    return G["quiz_seeds"][key]


def new_quiz_seed(tid):
    game()["quiz_seeds"][str(tid)] = random.randint(1, 10**9)


def record_quiz(tid, correct):
    """Начисляет награду. Возвращает (монеты, опыт, впервые_пройдено)."""
    G = game()
    key = str(tid)
    G["attempts"][key] = G["attempts"].get(key, 0) + 1
    passed = correct >= PASS_MARK
    first = passed and key not in G["completed"]
    if first:
        coins, xp = FIRST_BONUS + PER_CORRECT_FIRST * correct, 50 * correct
        G["completed"][key] = correct
    elif passed:
        coins, xp = PER_CORRECT_REPEAT * correct, 10 * correct
        G["completed"][key] = max(G["completed"][key], correct)
    else:
        coins, xp = 0, 5 * correct
    G["coins"] += coins
    G["xp"] += xp
    return coins, xp, first


def record_boss(correct):
    G = game()
    G["boss_best"] = max(G["boss_best"], correct)
    if correct >= BOSS_PASS and not G["boss_done"]:
        G["boss_done"] = True
        G["coins"] += BOSS_REWARD
        G["xp"] += BOSS_REWARD
        return True
    return False


def rank(xp):
    if game()["boss_done"]:
        return tr(*FINAL_RANK), None
    name, nxt = tr(*RANKS[0][1:]), None
    for i, (need, *names) in enumerate(RANKS):
        if xp >= need:
            name = tr(*names)
            nxt = RANKS[i + 1][0] if i + 1 < len(RANKS) else None
    return name, nxt


def forged_pieces():
    return [t["armor"] for t in TOPICS if is_completed(t["id"])]


def export_json():
    return json.dumps(game(), ensure_ascii=False, indent=2)


def import_json(raw: bytes):
    data = json.loads(raw.decode("utf-8"))
    base = default_game()
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError(tr("Это не файл сохранения Probability Quest.", "This is not a Probability Quest save file.", "Бұл Probability Quest сақтау файлы емес."))
    for k in base:
        if k in data:
            base[k] = data[k]
    base["unlocked"] = sorted({int(x) for x in base["unlocked"]} | {1})
    base["coins"], base["xp"] = int(base["coins"]), int(base["xp"])
    st.session_state.game = base
