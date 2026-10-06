"""Probability Quest — игра-курс по теории вероятностей (RU / EN / KZ).

Запуск:  streamlit run app.py
"""
import streamlit as st

from game import state as S
from game.avatar import avatar_svg, SKINS, HAIRS, OUTFITS, HAIRSTYLES, ARMOR_ORDER, LOOK_LABELS
from game.boss import boss_questions, BOSS_COUNT
from game.calculators import CALCULATORS
from game.content import TOPICS, TOPIC_BY_ID, TERMS, lesson, title, summary, armor_name
from game.i18n import LANGS, tr, lang
from game.project import PROJECT_MD
from game.quiz import build_quiz

st.set_page_config(page_title="Probability Quest", page_icon="🛡️", layout="wide")

PAGES = ["map", "learn", "calc", "shop", "char", "final"]


def page_name(p):
    return {
        "map": tr("🏰 Карта курса", "🏰 Course map", "🏰 Курс картасы"),
        "learn": tr("📖 Обучение", "📖 Learning", "📖 Оқу"),
        "calc": tr("🧮 Калькуляторы", "🧮 Calculators", "🧮 Калькуляторлар"),
        "shop": tr("🛒 Лавка", "🛒 Shop", "🛒 Дүкен"),
        "char": tr("🛡️ Персонаж", "🛡️ Character", "🛡️ Кейіпкер"),
        "final": tr("👑 Финал", "👑 Finale", "👑 Финал"),
    }[p]


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&display=swap');
h1, h2, h3, .game-title { font-family: 'Philosopher', serif !important; letter-spacing: .3px; }
.block-container { padding-top: 2.2rem; max-width: 1150px; }
.card { background: #1F1C30; border: 1px solid rgba(224,180,74,.18); border-radius: 14px;
        padding: 14px 16px 6px; margin-bottom: 8px; min-height: 258px; }
.card.done { border-color: rgba(110,200,140,.55); }
.card.open { border-color: rgba(224,180,74,.55); }
.card.locked { opacity: .62; }
.card h4 { margin: 0 0 4px; font-family: 'Philosopher', serif; font-size: 1.12rem; }
.card .en { color: #9D97B5; font-size: .82rem; margin-bottom: 6px; }
.card .sum { font-size: .9rem; color: #CFC9E0; }
.badge { display:inline-block; padding: 2px 9px; border-radius: 999px; font-size: .78rem; margin: 6px 0 4px;
         background: rgba(255,255,255,.07); }
.badge.done { background: rgba(110,200,140,.18); color: #8FE0A8; }
.badge.open { background: rgba(224,180,74,.16); color: #F0CF7A; }
.stat-row { display:flex; gap:6px; flex-wrap:wrap; margin: 4px 0 8px; }
.stat { background:#1F1C30; border-radius: 10px; padding: 5px 8px; font-size: .86rem; white-space: nowrap; }
.stat b { color: #F0CF7A; }
.result-box { background:#1F1C30; border-left: 4px solid #E0B44A; border-radius: 8px; padding: 8px 12px; margin: 6px 0 12px; }
.result-box span { color:#9D97B5; margin-right: 10px; }
.result-box b { font-size: 1.15rem; color:#F0CF7A; font-family: ui-monospace, monospace; }
.mono { font-family: ui-monospace, monospace; font-size: 1.05rem; padding-top: 10px; color:#F0CF7A; }
.term-table td, .term-table th { padding: 4px 10px; }
.hero { background: linear-gradient(135deg, #2A2342 0%, #1A1729 100%); border-radius: 16px; padding: 18px 22px;
        border: 1px solid rgba(224,180,74,.25); margin-bottom: 14px; }
.avatar-wrap { display:flex; justify-content:center; }
</style>
""", unsafe_allow_html=True)

G = S.game()


# ===================================================================== помощники
def synced(widget, label, options, state_key, format_func, **kw):
    """Виджет выбора, который не сбрасывается при смене языка и переходах по кнопкам.

    Настоящее значение хранится в st.session_state[state_key]; ключ виджета включает
    язык и текущее значение, поэтому подписи могут свободно меняться.
    """
    cur = st.session_state.get(state_key)
    if cur not in options:
        cur = options[0]
    st.session_state[state_key] = cur
    wkey = f"_w_{state_key}_{lang()}_{cur}"

    def _sync():
        st.session_state[state_key] = st.session_state[wkey]

    labels = {o: format_func(o) for o in options}  # подписи фиксируются в момент создания виджета
    return widget(label, options, index=options.index(cur), key=wkey, format_func=labels.get, on_change=_sync, **kw)


def lang_picker():
    synced(st.radio, "Language / Язык / Тіл", list(LANGS), "lang", LANGS.get, horizontal=True,
           label_visibility="collapsed")


def goto(page, topic=None):
    st.session_state["page"] = page
    if topic is not None:
        st.session_state["topic_sel"] = topic
        st.session_state["calc_sel"] = topic


def look_label(v):
    return tr(*LOOK_LABELS.get(v, (v, v, v)))


def avatar(size=220, final=False, show_ghost=False):
    worn = ARMOR_ORDER if G["boss_done"] else []
    ghost = S.forged_pieces() if show_ghost else []
    st.markdown(f"<div class='avatar-wrap'>{avatar_svg(G['look'], worn=worn, ghost=ghost, glow=final or G['boss_done'], size=size)}</div>",
                unsafe_allow_html=True)


def topic_label(tid):
    t = TOPIC_BY_ID[tid]
    return f"{tid}. {t['icon']} {title(t, lang())}"


def look_editor(prefix):
    look = G["look"]
    look["skin"] = st.selectbox(tr("Кожа", "Skin", "Тері"), list(SKINS), index=list(SKINS).index(look["skin"]),
                                format_func={o: look_label(o) for o in LOOK_LABELS}.get, key=f"{prefix}_s_{lang()}")
    look["hair"] = st.selectbox(tr("Волосы", "Hair", "Шаш"), list(HAIRS), index=list(HAIRS).index(look["hair"]),
                                format_func={o: look_label(o) for o in LOOK_LABELS}.get, key=f"{prefix}_h_{lang()}")
    look["style"] = st.radio(tr("Причёска", "Hairstyle", "Шаш үлгісі"), HAIRSTYLES, index=HAIRSTYLES.index(look["style"]),
                             horizontal=True, format_func={o: look_label(o) for o in LOOK_LABELS}.get, key=f"{prefix}_st_{lang()}")
    look["outfit"] = st.selectbox(tr("Одежда", "Outfit", "Киім"), list(OUTFITS), index=list(OUTFITS).index(look["outfit"]),
                                  format_func={o: look_label(o) for o in LOOK_LABELS}.get, key=f"{prefix}_o_{lang()}")


# ===================================================================== онбординг
def onboarding():
    lang_picker()
    st.markdown("<h1 class='game-title'>🛡️ Probability Quest</h1>", unsafe_allow_html=True)
    st.markdown("##### " + tr(
        "Пройди курс теории вероятностей как игру: учи темы, сдавай испытания, копи монеты, "
        "открывай новые земли и получи доспехи Рыцаря Вероятностей.",
        "Play through a probability theory course as a game: study topics, pass trials, collect coins, "
        "unlock new lands and earn the armour of the Knight of Probability.",
        "Ықтималдықтар теориясы курсын ойын ретінде өт: тақырыптарды оқы, сынақтардан өт, тиын жина, "
        "жаңа жерлерді аш және Ықтималдық рыцарының сауытын ал."))
    c1, c2 = st.columns([1, 1.3])
    with c2:
        st.markdown("### " + tr("Создай персонажа", "Create your character", "Кейіпкер жаса"))
        name = st.text_input(tr("Имя героя", "Hero's name", "Батырдың аты"), max_chars=24,
                             placeholder=tr("Например: Зере", "For example: Zere", "Мысалы: Зере"), key="onb_name")
        look_editor("onb")
        st.markdown(tr(
            "**Правила:** 8 тем → в каждой урок, испытание из 5 задач (нужно ≥ 4 верных) и калькулятор. "
            "За испытание даются 🪙 монеты и ⭐ опыт. На монеты покупается следующая тема. "
            "После всех тем — битва с Боссом (задачи из пробного теста), а за победу — доспехи и проектная работа.",
            "**Rules:** 8 topics → each has a lesson, a 5-problem trial (≥ 4 correct to pass) and a calculator. "
            "Trials give 🪙 coins and ⭐ XP. Coins buy the next topic. "
            "After all topics comes the Boss battle (problems from the practice test); victory brings armour and a course project.",
            "**Ережелер:** 8 тақырып → әрқайсысында сабақ, 5 есептен тұратын сынақ (өту үшін ≥ 4 дұрыс) және калькулятор. "
            "Сынақ үшін 🪙 тиын мен ⭐ тәжірибе беріледі. Тиынға келесі тақырып сатылып алынады. "
            "Барлық тақырыптан кейін — Босспен шайқас (сынама тест есептері), жеңіс үшін — сауыт пен жобалық жұмыс."))
        if st.button(tr("⚔️ Начать приключение", "⚔️ Start the adventure", "⚔️ Сапарды бастау"), type="primary",
                     disabled=not (name or "").strip()):
            G["name"] = name.strip()
            st.session_state["page"] = "map"
            st.rerun()
        with st.expander(tr("💾 У меня есть файл сохранения", "💾 I have a save file", "💾 Менде сақтау файлы бар")):
            save_loader("onb_upload")
    with c1:
        st.markdown(f"<div class='avatar-wrap'>{avatar_svg(G['look'], size=260)}</div>", unsafe_allow_html=True)


def save_loader(key):
    up = st.file_uploader(tr("Загрузить сохранение (.json)", "Load a save (.json)", "Сақтауды жүктеу (.json)"),
                          type=["json"], key=key)
    if up is not None and st.session_state.get("_loaded_id") != up.file_id:
        try:
            S.import_json(up.getvalue())
            st.session_state["_loaded_id"] = up.file_id
            st.session_state["flash"] = tr("💾 Сохранение загружено!", "💾 Save loaded!", "💾 Сақтау жүктелді!")
            st.rerun()
        except Exception as e:  # noqa: BLE001
            st.error(tr("Не удалось загрузить: ", "Could not load: ", "Жүктеу мүмкін болмады: ") + str(e))


# ===================================================================== сайдбар
def sidebar():
    with st.sidebar:
        lang_picker()
        st.markdown(f"<div class='avatar-wrap'>{avatar_svg(G['look'], worn=ARMOR_ORDER if G['boss_done'] else [], glow=G['boss_done'], size=150)}</div>",
                    unsafe_allow_html=True)
        rk, nxt = S.rank(G["xp"])
        st.markdown(f"<h3 style='text-align:center;margin:0'>{G['name']}</h3>"
                    f"<p style='text-align:center;color:#9D97B5;margin:0 0 6px'>{rk}</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-row' style='justify-content:center'>"
                    f"<div class='stat'>🪙 <b>{G['coins']}</b></div><div class='stat'>⭐ <b>{G['xp']}</b> XP</div>"
                    f"<div class='stat'>📚 <b>{len(G['completed'])}</b>/8</div></div>", unsafe_allow_html=True)
        if nxt:
            prev = max(r[0] for r in S.RANKS if r[0] <= G["xp"])
            left = nxt - G["xp"]
            st.progress((G["xp"] - prev) / (nxt - prev),
                        text=tr(f"До следующего звания: {left} XP", f"Next rank in: {left} XP", f"Келесі атаққа дейін: {left} XP"))
        synced(st.radio, "nav", PAGES, "page", page_name, label_visibility="collapsed")
        st.divider()
        with st.expander(tr("💾 Сохранение", "💾 Save", "💾 Сақтау")):
            st.caption(tr("Прогресс живёт, пока открыта вкладка. Скачай файл, чтобы продолжить позже.",
                          "Progress lives while the tab is open. Download the file to continue later.",
                          "Прогресс бет ашық тұрғанда ғана сақталады. Кейін жалғастыру үшін файлды жүктеп ал."))
            st.download_button(tr("⬇️ Скачать сохранение", "⬇️ Download save", "⬇️ Сақтауды жүктеп алу"), S.export_json(),
                               file_name=f"probability_quest_{G['name']}.json", mime="application/json", width="stretch")
            save_loader("side_upload")
            if st.button(tr("🗑️ Начать заново", "🗑️ Start over", "🗑️ Қайтадан бастау"), width="stretch"):
                keep = st.session_state.get("lang")
                st.session_state.clear()
                st.session_state["lang"] = keep
                st.rerun()


# ===================================================================== страницы
def page_map():
    lg = lang()
    st.markdown("<h1>" + page_name("map") + "</h1>", unsafe_allow_html=True)
    done = len(G["completed"])
    pm = S.PASS_MARK
    st.markdown("<div class='hero'>" + tr(
        f"<b>{G['name']}</b>, перед тобой 8 земель теории вероятностей. Пройди испытание темы (≥ {pm} из 5), получи 🪙 "
        "и купи следующую тему в Лавке. Каждая пройденная тема выковывает часть доспехов в кузнице — "
        "надеть их можно, только победив Босса.",
        f"<b>{G['name']}</b>, eight lands of probability theory lie before you. Pass a topic's trial (≥ {pm} of 5), earn 🪙 "
        "and buy the next topic in the Shop. Every completed topic forges a piece of armour — "
        "you can only wear it after defeating the Boss.",
        f"<b>{G['name']}</b>, алдыңда ықтималдықтар теориясының 8 жері бар. Тақырып сынағынан өт (5-тен ≥ {pm}), 🪙 ал "
        "да, Дүкеннен келесі тақырыпты сатып ал. Өтілген әр тақырып ұстаханада сауыттың бір бөлігін соғады — "
        "оны тек Боссты жеңгенде киюге болады.") + "</div>", unsafe_allow_html=True)
    st.progress(done / 8, text=tr(f"Пройдено тем: {done} из 8", f"Topics completed: {done} of 8", f"Өтілген тақырыптар: 8-ден {done}"))
    for row in range(0, 8, 4):
        cols = st.columns(4)
        for col, t in zip(cols, TOPICS[row:row + 4]):
            tid = t["id"]
            with col:
                if S.is_completed(tid):
                    cls = "done"
                    badge = f"<span class='badge done'>✅ {tr('пройдена', 'completed', 'өтілді')} · {G['completed'][str(tid)]}/5</span>"
                elif S.is_unlocked(tid):
                    cls, badge = "open", f"<span class='badge open'>🔓 {tr('открыта', 'unlocked', 'ашық')}</span>"
                else:
                    cls, badge = "locked", f"<span class='badge'>🔒 {t['cost']} 🪙</span>"
                sub = title(t, "en") if lg != "en" else ""
                st.markdown(f"<div class='card {cls}'><h4>{t['icon']} {tid}. {title(t, lg)}</h4>"
                            f"<div class='en'>{sub}</div><div class='sum'>{summary(t, lg)}</div>{badge}</div>",
                            unsafe_allow_html=True)
                if S.is_unlocked(tid):
                    st.button(tr("Учиться →", "Study →", "Оқу →"), key=f"map_go_{tid}", on_click=goto,
                              args=("learn", tid), width="stretch")
                else:
                    ok, why = S.buy_status(tid)
                    st.button(tr(f"Купить за {t['cost']} 🪙", f"Buy for {t['cost']} 🪙", f"{t['cost']} 🪙-ға сатып алу") if ok else why,
                              key=f"map_buy_{tid}", disabled=not ok, on_click=S.buy, args=(tid,), width="stretch")
    st.markdown("### " + tr("👑 Логово Босса", "👑 The Boss's lair", "👑 Босстың ордасы"))
    if G["boss_done"]:
        st.success(tr("Босс повержен! Доспехи надеты, проектная работа ждёт в разделе «Финал».",
                      "The Boss is defeated! Your armour is on, and the course project awaits in the \"Finale\" section.",
                      "Босс жеңілді! Сауыт киілді, жобалық жұмыс «Финал» бөлімінде күтіп тұр."))
    elif S.all_completed():
        st.warning(tr("Все темы пройдены — Босс ждёт тебя!", "All topics completed — the Boss awaits!", "Барлық тақырып өтілді — Босс сені күтуде!"))
    else:
        st.info(tr(f"Откроется после прохождения всех 8 тем. Сейчас: {done}/8.",
                   f"Opens after all 8 topics are completed. Now: {done}/8.",
                   f"Барлық 8 тақырып өткеннен кейін ашылады. Қазір: {done}/8."))
    st.button(tr("Перейти к Финалу →", "Go to the Finale →", "Финалға өту →"), on_click=goto, args=("final",),
              disabled=not S.all_completed())


def render_lesson(tid):
    lg = lang()
    for b in lesson(tid, lg):
        kind = b[0]
        if kind == "md":
            st.markdown(b[1])
        elif kind == "latex":
            st.latex(b[1])
        elif kind == "terms":
            if lg == "kk":
                head, cols = ("Қазақша", "Русский", "English"), (2, 0, 1)
            elif lg == "en":
                head, cols = ("English", "Русский", "Қазақша"), (1, 0, 2)
            else:
                head, cols = ("Русский", "English", "Қазақша"), (0, 1, 2)
            rows = "".join("<tr>" + "".join((f"<td><i>{t[i]}</i></td>" if j else f"<td><b>{t[i]}</b></td>")
                                            for j, i in enumerate(cols)) + "</tr>" for t in TERMS[tid])
            st.markdown(tr("**📘 Словарь терминов**", "**📘 Glossary**", "**📘 Терминдер сөздігі**"))
            st.markdown(f"<table class='term-table'><tr>{''.join(f'<th>{h}</th>' for h in head)}</tr>{rows}</table>",
                        unsafe_allow_html=True)
            st.write("")
        elif kind == "example":
            with st.expander(tr("✍️ Пример: ", "✍️ Example: ", "✍️ Мысал: ") + b[1], expanded=True):
                st.markdown(b[2])
        elif kind == "tip":
            st.info("💡 " + b[1])
        elif kind == "warn":
            st.warning("⚠️ " + b[1])


def show_review(qs, idx, label):
    for i, (q, chosen) in enumerate(zip(qs, idx)):
        ok = chosen == q["ans"]
        with st.expander(f"{'✅' if ok else '❌'} {label} {i + 1}", expanded=not ok):
            st.markdown(q["q"])
            your = tr("Твой ответ", "Your answer", "Сенің жауабың")
            right = tr("Верно", "Correct", "Дұрысы")
            st.markdown(f"{your}: **{q['opts'][chosen]}**" + ("" if ok else f" · {right}: **{q['opts'][q['ans']]}**"))
            st.markdown(tr("**Решение:** ", "**Solution:** ", "**Шешімі:** ") + q["expl"])


def quiz_block(tid):
    lg = lang()
    seed = S.quiz_seed(tid)
    qs = build_quiz(tid, seed, lg)
    rkey = f"quiz_result_{tid}"
    res = st.session_state.get(rkey)
    if S.is_completed(tid):
        best, rep = G["completed"][str(tid)], S.PER_CORRECT_REPEAT
        st.caption(tr(f"Тема уже пройдена (лучший результат {best}/5). Повторные испытания дают по {rep} 🪙 за верный ответ.",
                      f"Topic already completed (best {best}/5). Repeat trials give {rep} 🪙 per correct answer.",
                      f"Тақырып өтілген (ең жақсы нәтиже {best}/5). Қайталама сынақ әр дұрыс жауапқа {rep} 🪙 береді."))
    else:
        pm, fb, pc = S.PASS_MARK, S.FIRST_BONUS, S.PER_CORRECT_FIRST
        st.caption(tr(f"Нужно ≥ {pm} верных из 5. Награда за первое прохождение: {fb} + {pc}×(верные) 🪙 и часть доспехов в кузницу.",
                      f"You need ≥ {pm} of 5 correct. First-pass reward: {fb} + {pc}×(correct) 🪙 and a piece of armour for the forge.",
                      f"5-тен ≥ {pm} дұрыс жауап керек. Алғаш өткені үшін сыйлық: {fb} + {pc}×(дұрыс) 🪙 және ұстаханаға сауыт бөлігі."))
    label = tr("Задача", "Problem", "Есеп")
    if res is None:
        with st.form(f"quiz_form_{tid}_{seed}_{lg}"):
            for i, q in enumerate(qs):
                st.markdown(f"**{label} {i + 1}.** {q['q']}")
                st.radio("answer", q["opts"], index=None, key=f"q_{tid}_{seed}_{lg}_{i}", label_visibility="collapsed")
                st.write("")
            sent = st.form_submit_button(tr("⚔️ Сдать испытание", "⚔️ Submit the trial", "⚔️ Сынақты тапсыру"), type="primary")
        if sent:
            answers = [st.session_state.get(f"q_{tid}_{seed}_{lg}_{i}") for i in range(len(qs))]
            if any(a is None for a in answers):
                st.warning(tr("Ответь на все 5 задач, прежде чем сдавать.", "Answer all 5 problems before submitting.",
                              "Тапсырмас бұрын барлық 5 есепке жауап бер."))
                return
            idx = [q["opts"].index(a) for q, a in zip(qs, answers)]
            correct = sum(int(i == q["ans"]) for i, q in zip(idx, qs))
            coins, xp, first = S.record_quiz(tid, correct)
            st.session_state[rkey] = {"idx": idx, "correct": correct, "coins": coins, "xp": xp, "first": first, "seed": seed}
            st.rerun()
        return

    correct = res["correct"]
    if res["first"]:
        st.balloons()
        piece = armor_name(TOPIC_BY_ID[tid]["armor"], lg)
        st.success(tr(f"🏆 Тема пройдена! {correct}/5 · +{res['coins']} 🪙 · +{res['xp']} ⭐ · в кузнице выкован предмет: **{piece}**",
                      f"🏆 Topic completed! {correct}/5 · +{res['coins']} 🪙 · +{res['xp']} ⭐ · forged in the smithy: **{piece}**",
                      f"🏆 Тақырып өтілді! {correct}/5 · +{res['coins']} 🪙 · +{res['xp']} ⭐ · ұстаханада соғылды: **{piece}**"))
        res["first"] = False
    elif correct >= S.PASS_MARK:
        st.success(f"✅ {correct}/5 · +{res['coins']} 🪙 · +{res['xp']} ⭐")
    else:
        pm, x = S.PASS_MARK, res["xp"]
        st.error(tr(f"❌ {correct}/5 — не хватило до {pm}. Перечитай теорию, загляни в калькулятор и попробуй снова (+{x} ⭐ за старание).",
                    f"❌ {correct}/5 — short of {pm}. Reread the theory, try the calculator and go again (+{x} ⭐ for the effort).",
                    f"❌ {correct}/5 — {pm}-ке жетпеді. Теорияны қайта оқы, калькуляторды қара да, қайта көр (+{x} ⭐ талпынысың үшін)."))
    show_review(qs, res["idx"], label)

    def again():
        S.new_quiz_seed(tid)
        st.session_state.pop(rkey, None)

    c1, c2 = st.columns(2)
    c1.button(tr("🔁 Новое испытание (другие числа)", "🔁 New trial (different numbers)", "🔁 Жаңа сынақ (басқа сандар)"),
              on_click=again, width="stretch")
    nxt = tid + 1
    if nxt <= 8 and S.is_completed(tid) and not S.is_unlocked(nxt):
        ok, why = S.buy_status(nxt)
        cost = TOPIC_BY_ID[nxt]["cost"]
        lbl = tr(f"🛒 Купить тему {nxt} за {cost} 🪙", f"🛒 Buy topic {nxt} for {cost} 🪙", f"🛒 {nxt}-тақырыпты {cost} 🪙-ға сатып алу") \
            if ok else tr(f"Тема {nxt}: ", f"Topic {nxt}: ", f"{nxt}-тақырып: ") + why
        c2.button(lbl, disabled=not ok, on_click=S.buy, args=(nxt,), width="stretch")
    elif nxt <= 8 and S.is_unlocked(nxt):
        c2.button(tr(f"Перейти к теме {nxt} →", f"Go to topic {nxt} →", f"{nxt}-тақырыпқа өту →"), on_click=goto,
                  args=("learn", nxt), width="stretch")
    elif nxt > 8 and S.all_completed():
        c2.button(tr("👑 К Боссу →", "👑 To the Boss →", "👑 Боссқа →"), on_click=goto, args=("final",), width="stretch")


def page_learn():
    lg = lang()
    unlocked = sorted(G["unlocked"])
    if st.session_state.get("topic_sel") not in unlocked:
        st.session_state["topic_sel"] = unlocked[-1]
    tid = synced(st.selectbox, tr("Тема", "Topic", "Тақырып"), unlocked, "topic_sel", topic_label)
    t = TOPIC_BY_ID[tid]
    sub = title(t, "en") if lg != "en" else ""
    st.markdown(f"<h1>{t['icon']} {title(t, lg)}</h1><p style='color:#9D97B5;margin-top:-10px'>{sub}</p>",
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs([tr("📖 Теория", "📖 Theory", "📖 Теория"), tr("⚔️ Испытание", "⚔️ Trial", "⚔️ Сынақ")])
    with tab1:
        render_lesson(tid)
        st.button(tr("🧮 Открыть калькулятор этой темы", "🧮 Open this topic's calculator", "🧮 Осы тақырыптың калькуляторын ашу"),
                  on_click=goto, args=("calc", tid))
    with tab2:
        quiz_block(tid)


def page_calc():
    lg = lang()
    st.markdown("<h1>" + page_name("calc") + "</h1>", unsafe_allow_html=True)
    st.caption(tr("Калькулятор открывается вместе с темой. Вводить можно дроби (3/8), десятичные (0.375) и проценты (37.5%).",
                  "A calculator unlocks together with its topic. You can enter fractions (3/8), decimals (0.375) and percentages (37.5%).",
                  "Калькулятор тақырыппен бірге ашылады. Бөлшек (3/8), ондық (0.375) және пайыз (37.5%) енгізуге болады."))
    unlocked = sorted(G["unlocked"])
    tid = synced(st.selectbox, tr("Калькулятор темы", "Calculator for topic", "Тақырып калькуляторы"), unlocked, "calc_sel", topic_label)
    locked = [t for t in TOPICS if t["id"] not in unlocked]
    if locked:
        st.caption(tr("🔒 Ещё закрыты: ", "🔒 Still locked: ", "🔒 Әлі жабық: ") + ", ".join(f"{t['icon']} {title(t, lg)}" for t in locked))
    st.divider()
    CALCULATORS[tid]()


def page_shop():
    lg = lang()
    st.markdown("<h1>" + tr("🛒 Лавка знаний", "🛒 Shop of Knowledge", "🛒 Білім дүкені") + "</h1>", unsafe_allow_html=True)
    st.markdown("<div class='hero'>" + tr(
        f"У тебя <b>{G['coins']} 🪙</b>. Темы покупаются по порядку: следующая доступна, когда пройдена предыдущая.",
        f"You have <b>{G['coins']} 🪙</b>. Topics are bought in order: the next one is available once the previous one is completed.",
        f"Сенде <b>{G['coins']} 🪙</b> бар. Тақырыптар ретімен сатылады: алдыңғысы өтілгенде келесісі қолжетімді болады.")
        + "</div>", unsafe_allow_html=True)
    for t in TOPICS[1:]:
        tid = t["id"]
        c1, c2 = st.columns([3, 1.3])
        c1.markdown(f"**{t['icon']} {tid}. {title(t, lg)}**  \n{summary(t, lg)}")
        if S.is_unlocked(tid):
            c2.button(tr("✅ Куплено", "✅ Bought", "✅ Сатып алынды"), key=f"shop_{tid}", disabled=True, width="stretch")
        else:
            ok, why = S.buy_status(tid)
            c2.button(tr(f"Купить · {t['cost']} 🪙", f"Buy · {t['cost']} 🪙", f"Сатып алу · {t['cost']} 🪙") if ok else f"{t['cost']} 🪙 · {why}",
                      key=f"shop_{tid}", disabled=not ok, on_click=S.buy, args=(tid,),
                      type="primary" if ok else "secondary", width="stretch")
    st.divider()
    fb, pc, rp, br = S.FIRST_BONUS, S.PER_CORRECT_FIRST, S.PER_CORRECT_REPEAT, S.BOSS_REWARD
    st.markdown(tr(
        f"**Как заработать монеты:**\n- Первое прохождение темы: **{fb} + {pc} за каждый верный ответ** (до 225 🪙)\n"
        f"- Повторное испытание после прохождения: **{rp} 🪙** за верный ответ\n- Победа над Боссом: **{br} 🪙 и {br} ⭐**",
        f"**How to earn coins:**\n- First completion of a topic: **{fb} + {pc} per correct answer** (up to 225 🪙)\n"
        f"- Repeat trial after completion: **{rp} 🪙** per correct answer\n- Defeating the Boss: **{br} 🪙 and {br} ⭐**",
        f"**Тиынды қалай табуға болады:**\n- Тақырыпты алғаш өту: **{fb} + әр дұрыс жауапқа {pc}** (225 🪙-ға дейін)\n"
        f"- Өткеннен кейінгі қайталама сынақ: әр дұрыс жауапқа **{rp} 🪙**\n- Боссты жеңу: **{br} 🪙 және {br} ⭐**"))


def page_character():
    lg = lang()
    st.markdown("<h1>" + tr("🛡️ Персонаж и кузница", "🛡️ Character and forge", "🛡️ Кейіпкер және ұстахана") + "</h1>",
                unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.4])
    with c1:
        avatar(size=280, show_ghost=not G["boss_done"])
        if not G["boss_done"]:
            st.caption(tr("Полупрозрачные части — уже выкованные доспехи. Они станут настоящими после победы над Боссом.",
                          "Translucent parts are armour already forged. They become real after you defeat the Boss.",
                          "Жартылай мөлдір бөліктер — соғылып қойған сауыт. Олар Боссты жеңгеннен кейін шынайы болады."))
    with c2:
        rk, _ = S.rank(G["xp"])
        st.markdown(f"### {G['name']} · {rk}")
        st.markdown(f"<div class='stat-row'><div class='stat'>🪙 <b>{G['coins']}</b></div>"
                    f"<div class='stat'>⭐ <b>{G['xp']}</b> XP</div>"
                    f"<div class='stat'>🎯 {tr('Лучший бой с Боссом', 'Best Boss fight', 'Босспен ең жақсы шайқас')}: "
                    f"<b>{G['boss_best']}</b>/{BOSS_COUNT}</div></div>", unsafe_allow_html=True)
        st.markdown("#### " + tr("⚒️ Кузница", "⚒️ Forge", "⚒️ Ұстахана"))
        for t in TOPICS:
            piece = armor_name(t["armor"], lg)
            tid = t["id"]
            if G["boss_done"]:
                st.markdown(f"🟨 **{piece}** — " + tr("надет", "worn", "киілген"))
            elif S.is_completed(tid):
                st.markdown(f"🔨 **{piece}** — " + tr(f"выкован (тема {tid})", f"forged (topic {tid})", f"соғылды ({tid}-тақырып)"))
            else:
                st.markdown(f"<span style='color:#77718F'>⬜ {piece} — "
                            + tr(f"пройди тему {tid}", f"complete topic {tid}", f"{tid}-тақырыпты өт") + "</span>",
                            unsafe_allow_html=True)
        with st.expander(tr("🎨 Изменить внешность", "🎨 Change appearance", "🎨 Сыртқы түрін өзгерту")):
            look_editor("lk")


def page_final():
    lg = lang()
    st.markdown("<h1>" + tr("👑 Финал: Босс Вероятностей", "👑 Finale: the Boss of Probability", "👑 Финал: Ықтималдық Боссы")
                + "</h1>", unsafe_allow_html=True)
    if not S.all_completed():
        n = len(G["completed"])
        st.info(tr(f"Логово Босса закрыто. Пройди все 8 тем (сейчас {n}/8).",
                   f"The Boss's lair is closed. Complete all 8 topics (now {n}/8).",
                   f"Босстың ордасы жабық. Барлық 8 тақырыпты өт (қазір {n}/8)."))
        avatar(size=220, show_ghost=True)
        return

    if G["boss_done"]:
        c1, c2 = st.columns([1, 1.5])
        with c1:
            avatar(size=300, final=True)
        with c2:
            st.markdown("## " + tr(f"🏆 {G['name']}, ты — Рыцарь Вероятностей!", f"🏆 {G['name']}, you are a Knight of Probability!",
                                   f"🏆 {G['name']}, сен — Ықтималдық рыцарысың!"))
            st.markdown(tr("Босс повержен. Ты получаешь полный комплект доспехов:",
                           "The Boss is defeated. You receive the full set of armour:",
                           "Босс жеңілді. Сен сауыттың толық жиынтығын аласың:"))
            st.markdown("\n".join(f"- {t['icon']} **{armor_name(t['armor'], lg)}** — {title(t, lg)}" for t in TOPICS))
            st.markdown(tr("Лучший результат в бою: ", "Best battle score: ", "Шайқастағы ең жақсы нәтиже: ")
                        + f"**{G['boss_best']}/{BOSS_COUNT}**.")
        st.divider()
        st.markdown(PROJECT_MD[lg])
        st.download_button(tr("⬇️ Скачать задание проекта (.md)", "⬇️ Download the project brief (.md)", "⬇️ Жоба тапсырмасын жүктеп алу (.md)"),
                           PROJECT_MD[lg], file_name=f"probability_lab_project_{lg}.md", mime="text/markdown", type="primary")
        with st.expander(tr("⚔️ Сразиться с Боссом ещё раз (для тренировки)", "⚔️ Fight the Boss again (for practice)",
                            "⚔️ Босспен қайта шайқасу (жаттығу үшін)")):
            boss_fight()
        return

    bp, br = S.BOSS_PASS, S.BOSS_REWARD
    st.markdown("<div class='hero'>" + tr(
        f"Босс задаёт <b>{BOSS_COUNT} задач из пробного теста</b> (Section A). Нужно ≥ {bp} верных. "
        f"Награда: полный комплект доспехов, {br} 🪙, {br} ⭐ и проектная работа.",
        f"The Boss asks <b>{BOSS_COUNT} problems from the practice test</b> (Section A). You need ≥ {bp} correct. "
        f"Reward: the full armour set, {br} 🪙, {br} ⭐ and the course project.",
        f"Босс <b>сынама тесттен {BOSS_COUNT} есеп</b> береді (Section A). ≥ {bp} дұрыс жауап керек. "
        f"Сыйлық: сауыттың толық жиынтығы, {br} 🪙, {br} ⭐ және жобалық жұмыс.") + "</div>", unsafe_allow_html=True)
    boss_fight()


def boss_fight():
    lg = lang()
    qs = boss_questions(lg)
    res = st.session_state.get("boss_result")
    if res is None:
        with st.form(f"boss_form_{lg}"):
            for i, q in enumerate(qs):
                st.markdown(f"**{i + 1}.** {q['q']}")
                st.radio("answer", q["opts"], index=None, key=f"boss_{lg}_{i}", label_visibility="collapsed")
                st.write("")
            sent = st.form_submit_button(tr("🗡️ Атаковать!", "🗡️ Attack!", "🗡️ Шабуыл!"), type="primary")
        if sent:
            answers = [st.session_state.get(f"boss_{lg}_{i}") for i in range(len(qs))]
            if any(a is None for a in answers):
                st.warning(tr(f"Ответь на все {len(qs)} вопросов.", f"Answer all {len(qs)} questions.", f"Барлық {len(qs)} сұраққа жауап бер."))
                return
            idx = [q["opts"].index(a) for q, a in zip(qs, answers)]
            correct = sum(int(i == q["ans"]) for i, q in zip(idx, qs))
            won = S.record_boss(correct)
            st.session_state["boss_result"] = {"idx": idx, "correct": correct, "won": won}
            st.rerun()
        return
    correct = res["correct"]
    if res["won"]:
        st.balloons()
        res["won"] = False
    if correct >= S.BOSS_PASS:
        st.success(tr(f"⚔️ Победа! {correct}/{len(qs)}.", f"⚔️ Victory! {correct}/{len(qs)}.", f"⚔️ Жеңіс! {correct}/{len(qs)}."))
    else:
        bp = S.BOSS_PASS
        st.error(tr(f"💥 Босс устоял: {correct}/{len(qs)} (нужно {bp}). Разбери ошибки и атакуй снова.",
                    f"💥 The Boss holds: {correct}/{len(qs)} (need {bp}). Review your mistakes and attack again.",
                    f"💥 Босс төтеп берді: {correct}/{len(qs)} ({bp} керек). Қателерді талдап, қайта шабуыл жаса."))
    show_review(qs, res["idx"], tr("Вопрос", "Question", "Сұрақ"))

    def again():
        st.session_state.pop("boss_result", None)
        for k in [k for k in st.session_state if str(k).startswith("boss_")]:
            st.session_state.pop(k, None)

    st.button(tr("🔁 Сразиться снова", "🔁 Fight again", "🔁 Қайта шайқасу"), on_click=again)


# ===================================================================== main
if not G["name"]:
    onboarding()
    st.stop()

st.session_state.setdefault("page", "map")
sidebar()

if msg := st.session_state.pop("flash", None):
    st.toast(msg)

{
    "map": page_map, "learn": page_learn, "calc": page_calc,
    "shop": page_shop, "char": page_character, "final": page_final,
}[st.session_state["page"]]()
