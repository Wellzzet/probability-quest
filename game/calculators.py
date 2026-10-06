"""Калькуляторы по темам. Каждый показывает не только ответ, но и шаги решения."""
from itertools import product
import altair as alt
import pandas as pd
import streamlit as st
from .i18n import tr, lang
from .mathutil import F, comb, perm, factorial, fmt, tex, tex_approx

ACCENT = "#E0B44A"


def PROB():
    return tr("Вероятность", "Probability", "Ықтималдық")


def _frac_input(label, default, key, help=None):
    """Поле, принимающее 0.3, 3/8 или 30%."""
    raw = st.text_input(label, value=default, key=key,
                        help=help or tr("Можно вводить 0.3, 3/8 или 30%", "You can enter 0.3, 3/8 or 30%", "0.3, 3/8 немесе 30% енгізуге болады"))
    try:
        s = raw.strip().replace(",", ".")
        if s.endswith("%"):
            return F(s[:-1]) / 100
        return F(s)
    except (ValueError, ZeroDivisionError):
        st.error(tr(f"Не понимаю число «{raw}». Пример: 0.25, 1/4 или 25%", f"Cannot read the number \"{raw}\". Example: 0.25, 1/4 or 25%",
                    f"«{raw}» санын түсіне алмадым. Мысалы: 0.25, 1/4 немесе 25%"))
        st.stop()


def _check_prob(x, name):
    if not (0 <= x <= 1):
        st.error(tr(f"{name} должна быть от 0 до 1 (сейчас {fmt(x)}).", f"{name} must be between 0 and 1 (now {fmt(x)}).",
                    f"{name} 0 мен 1 аралығында болуы керек (қазір {fmt(x)})."))
        st.stop()


def _bar(df, x, y, x_title, y_title):
    chart = (
        alt.Chart(df)
        .mark_bar(color=ACCENT, cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=26)
        .encode(
            x=alt.X(f"{x}:N", title=x_title, axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f"{y}:Q", title=y_title, axis=alt.Axis(grid=True, gridOpacity=0.15)),
            tooltip=[alt.Tooltip(f"{x}:N", title=x_title), alt.Tooltip(f"{y}:Q", title=y_title, format=".4f")],
        )
        .properties(height=260)
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(chart, width="stretch")


def _result(label, value):
    st.markdown(f"<div class='result-box'><span>{label}</span><b>{fmt(value)}</b></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------- 1
def calc_1():
    st.markdown(tr("#### 🎲 Классическая вероятность P = m / n", "#### 🎲 Classical probability P = m / n", "#### 🎲 Классикалық ықтималдық P = m / n"))
    c1, c2 = st.columns(2)
    m = c1.number_input(tr("Благоприятных исходов m", "Favourable outcomes m", "Қолайлы нәтижелер m"), 0, 10**9, 2, key="c1m")
    n = c2.number_input(tr("Всего исходов n", "All outcomes n", "Барлық нәтижелер n"), 1, 10**9, 36, key="c1n")
    if m > n:
        st.error(tr("m не может быть больше n.", "m cannot exceed n.", "m саны n-нен үлкен бола алмайды."))
    else:
        st.latex(rf"P=\frac{{{m}}}{{{n}}}={tex_approx(F(m, n))}")
        _result("P(A)", F(m, n))

    st.divider()
    st.markdown(tr("#### 🎲🎲 Два кубика: распределение суммы", "#### 🎲🎲 Two dice: distribution of the sum", "#### 🎲🎲 Екі ойын сүйегі: қосындының үлестірімі"))
    word = tr("сумма", "sum", "қосынды")
    cmp = st.selectbox(tr("Событие", "Event", "Оқиға"), ["=", "<", "≤", ">", "≥"], key=f"c1op_{lang()}",
                       format_func=lambda o: f"{word} {o}")
    s = st.slider(tr("Значение суммы", "Value of the sum", "Қосынды мәні"), 2, 12, 7, key="c1s")
    ops = {"=": lambda v: v == s, "<": lambda v: v < s, "≤": lambda v: v <= s,
           ">": lambda v: v > s, "≥": lambda v: v >= s}
    pairs = [(a, b) for a, b in product(range(1, 7), repeat=2) if ops[cmp](a + b)]
    st.latex(rf"P=\frac{{{len(pairs)}}}{{36}}={tex_approx(F(len(pairs), 36))}")
    with st.expander(tr(f"Показать все {len(pairs)} подходящих пар", f"Show all {len(pairs)} matching pairs",
                        f"Барлық {len(pairs)} сәйкес жұпты көрсету")):
        st.write(", ".join(f"({a},{b})" for a, b in pairs) or "—")
    df = pd.DataFrame({"x": list(range(2, 13)), "P": [(6 - abs(v - 7)) / 36 for v in range(2, 13)]})
    _bar(df, "x", "P", tr("Сумма очков", "Sum of points", "Ұпайлар қосындысы"), PROB())


# ---------------------------------------------------------------- 2
def calc_2():
    st.markdown(tr("#### 🃏 Перестановки, размещения, сочетания", "#### 🃏 Permutations, arrangements, combinations", "#### 🃏 Алмастырулар, орналастырулар, терулер"))
    c1, c2 = st.columns(2)
    n = c1.number_input(tr("n (всего объектов)", "n (total objects)", "n (барлық объектілер)"), 0, 170, 10, key="c2n")
    k = c2.number_input(tr("k (выбираем)", "k (chosen)", "k (таңдаймыз)"), 0, 170, 3, key="c2k")
    if k > n:
        st.warning(tr("k > n: без повторений так выбрать нельзя (результат 0).", "k > n: impossible without repetition (result 0).", "k > n: қайталаусыз бұлай таңдау мүмкін емес (нәтиже 0)."))
    rows = [
        (tr("Перестановки n!", "Permutations n!", "Алмастырулар n!"), r"P_n=n!", factorial(n)),
        (tr("Размещения (порядок важен)", "Arrangements (order matters)", "Орналастырулар (рет маңызды)"), r"A_n^k=\frac{n!}{(n-k)!}", perm(n, k) if k <= n else 0),
        (tr("Сочетания (порядок не важен)", "Combinations (order does not matter)", "Терулер (рет маңызды емес)"), r"C_n^k=\frac{n!}{k!(n-k)!}", comb(n, k)),
        (tr("Размещения с повторениями", "Arrangements with repetition", "Қайталаумен орналастырулар"), r"\bar A_n^k=n^k", n ** k),
        (tr("Сочетания с повторениями", "Combinations with repetition", "Қайталаумен терулер"), r"\bar C_n^k=C_{n+k-1}^k", comb(n + k - 1, k) if n + k - 1 >= 0 else 0),
    ]
    for name, formula, val in rows:
        a, b, c = st.columns([3, 3, 3])
        a.markdown(f"**{name}**")
        b.latex(formula)
        c.markdown(f"<div class='mono'>{val:,}</div>".replace(",", " "), unsafe_allow_html=True)

    st.divider()
    st.markdown(tr("#### 🎯 Выборка без возвращения (гипергеометрическая)", "#### 🎯 Sampling without replacement (hypergeometric)", "#### 🎯 Қайтарусыз іріктеу (гипергеометриялық)"))
    st.caption(tr("Из N предметов, где K «нужных», берём n. Вероятность получить ровно x нужных.", "From N items, K of which are \"good\", we take n. Probability of exactly x good ones.", "K «қажетті» заты бар N заттан n зат аламыз. Дәл x қажетті зат алу ықтималдығы."))
    c1, c2, c3, c4 = st.columns(4)
    N = c1.number_input(tr("N всего", "N total", "N барлығы"), 1, 1000, 52, key="c2N")
    K = c2.number_input(tr("K нужных", "K good", "K қажетті"), 0, 1000, 4, key="c2K")
    nn = c3.number_input(tr("n берём", "n taken", "n аламыз"), 0, 1000, 2, key="c2nn")
    x = c4.number_input(tr("x нужных в выборке", "x good in sample", "іріктемедегі x қажетті"), 0, 1000, 2, key="c2x")
    if K > N or nn > N:
        st.error(tr("Должно быть K ≤ N и n ≤ N.", "Need K ≤ N and n ≤ N.", "K ≤ N және n ≤ N болуы керек."))
        return
    p = F(comb(K, x) * comb(N - K, nn - x), comb(N, nn)) if x <= nn else F(0)
    st.latex(rf"P=\frac{{C_{{{K}}}^{{{x}}}\cdot C_{{{N - K}}}^{{{nn - x}}}}}{{C_{{{N}}}^{{{nn}}}}}="
             rf"\frac{{{comb(K, x)}\cdot{comb(N - K, nn - x) if nn >= x else 0}}}{{{comb(N, nn)}}}={tex_approx(p)}")
    _result(tr(f"P(ровно {x} нужных)", f"P(exactly {x} good)", f"P(дәл {x} қажетті)"), p)
    xs = list(range(0, min(K, nn) + 1))
    if 1 < len(xs) <= 30:
        df = pd.DataFrame({"x": xs, "P": [comb(K, i) * comb(N - K, nn - i) / comb(N, nn) for i in xs]})
        _bar(df, "x", "P", tr("Число нужных в выборке", "Good items in sample", "Іріктемедегі қажеттілер саны"), PROB())


# ---------------------------------------------------------------- 3
def calc_3():
    st.markdown(tr("#### 🔗 Всё про два события по P(A), P(B), P(A∩B)", "#### 🔗 Everything about two events from P(A), P(B), P(A∩B)", "#### 🔗 P(A), P(B), P(A∩B) бойынша екі оқиға туралы бәрі"))
    c1, c2, c3 = st.columns(3)
    with c1:
        a = _frac_input("P(A)", "0.6", "c3a")
    with c2:
        b = _frac_input("P(B)", "0.2", "c3b")
    with c3:
        c = _frac_input("P(A∩B)", "0.1", "c3c")
    for v, nm in ((a, "P(A)"), (b, "P(B)"), (c, "P(A∩B)")):
        _check_prob(v, nm)
    if c > min(a, b) or a + b - c > 1:
        st.error(tr("Такие вероятности невозможны: нужно P(A∩B) ≤ min(P(A), P(B)) и P(A∪B) ≤ 1.", "These probabilities are impossible: need P(A∩B) ≤ min(P(A), P(B)) and P(A∪B) ≤ 1.", "Мұндай ықтималдықтар мүмкін емес: P(A∩B) ≤ min(P(A), P(B)) және P(A∪B) ≤ 1 болуы керек."))
        return
    u = a + b - c
    res = [
        (r"P(A\cup B)=P(A)+P(B)-P(A\cap B)", u),
        (r"P(\bar A)=1-P(A)", 1 - a),
        (r"P(\bar B)=1-P(B)", 1 - b),
        (r"P(\bar A\cap\bar B)=1-P(A\cup B)", 1 - u),
        (r"P(\bar A\cup\bar B)=1-P(A\cap B)", 1 - c),
        (r"P(A\setminus B)=P(A)-P(A\cap B)", a - c),
        (r"P(B\setminus A)=P(B)-P(A\cap B)", b - c),
        (r"P(\text{" + tr("ровно одно", "exactly one", "тек біреуі") + r"})=P(A)+P(B)-2P(A\cap B)", a + b - 2 * c),
    ]
    for f, v in res:
        st.latex(f + "=" + tex_approx(v))
    yes, no = tr("да", "yes", "иә"), tr("нет", "no", "жоқ")
    st.markdown(tr("**Свойства:**", "**Properties:**", "**Қасиеттері:**"))
    st.write(tr("• Несовместны: ", "• Mutually exclusive: ", "• Үйлесімсіз: ") + (f"✅ {yes}, P(A∩B)=0" if c == 0 else f"❌ {no}, P(A∩B) ≠ 0"))
    st.write(tr("• Независимы: ", "• Independent: ", "• Тәуелсіз: ") + (f"✅ {yes}" if c == a * b else f"❌ {no}, P(A)·P(B) = {fmt(a * b)} ≠ {fmt(c)}"))


# ---------------------------------------------------------------- 4
def calc_4():
    st.markdown(tr("#### 🎯 Условная вероятность", "#### 🎯 Conditional probability", "#### 🎯 Шартты ықтималдық"))
    and_ = tr("и", "and", "және")
    mode = st.radio(tr("Что известно?", "What is known?", "Не белгілі?"), [0, 1], horizontal=True, key=f"c4mode_{lang()}",
                    format_func=[f"P(A∩B) {and_} P(B)", f"P(A), P(B) {and_} P(A|B)"].__getitem__)
    if mode == 0:
        c1, c2 = st.columns(2)
        with c1:
            ab = _frac_input("P(A∩B)", "0.7", "c4ab")
        with c2:
            b = _frac_input("P(B)", "0.85", "c4b")
        _check_prob(ab, "P(A∩B)")
        _check_prob(b, "P(B)")
        if b == 0 or ab > b:
            st.error(tr("Нужно P(B) > 0 и P(A∩B) ≤ P(B).", "Need P(B) > 0 and P(A∩B) ≤ P(B).", "P(B) > 0 және P(A∩B) ≤ P(B) болуы керек."))
            return
        st.latex(rf"P(A\mid B)=\frac{{P(A\cap B)}}{{P(B)}}=\frac{{{tex(ab)}}}{{{tex(b)}}}={tex_approx(ab / b)}")
        _result("P(A|B)", ab / b)
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            a = _frac_input("P(A)", "0.6", "c4a")
        with c2:
            b = _frac_input("P(B)", "0.2", "c4b2")
        with c3:
            c = _frac_input("P(A|B)", "0.5", "c4c")
        for v, nm in ((a, "P(A)"), (b, "P(B)"), (c, "P(A|B)")):
            _check_prob(v, nm)
        ab = c * b
        if ab > a or a + b - ab > 1 or b in (0, 1):
            st.error(tr("Такие данные несовместимы (или P(B) равна 0 или 1).", "These data are inconsistent (or P(B) is 0 or 1).", "Бұл деректер үйлеспейді (немесе P(B) 0 не 1-ге тең)."))
            return
        steps = [
            (r"P(A\cap B)=P(A\mid B)\,P(B)", ab),
            (r"P(B\mid A)=\frac{P(A\cap B)}{P(A)}", ab / a if a else F(0)),
            (r"P(A\cup B)=P(A)+P(B)-P(A\cap B)", a + b - ab),
            (r"P(\bar A\cap\bar B)=1-P(A\cup B)", 1 - a - b + ab),
            (r"P(\bar A\mid\bar B)=\frac{P(\bar A\cap\bar B)}{1-P(B)}", (1 - a - b + ab) / (1 - b)),
            (r"P(A\mid\bar B)=\frac{P(A)-P(A\cap B)}{1-P(B)}", (a - ab) / (1 - b)),
        ]
        for f, v in steps:
            st.latex(f + "=" + tex_approx(v))

    st.divider()
    st.markdown(tr("#### 🎲🎲 Два кубика: P(событие | условие)", "#### 🎲🎲 Two dice: P(event | condition)", "#### 🎲🎲 Екі ойын сүйегі: P(оқиға | шарт)"))
    ops = ["=", "<", "≤", ">", "≥"]
    fn = {"=": lambda v, s: v == s, "<": lambda v, s: v < s, "≤": lambda v, s: v <= s,
          ">": lambda v, s: v > s, "≥": lambda v, s: v >= s}
    c1, c2, c3, c4 = st.columns(4)
    op_a = c1.selectbox(tr("Событие A: сумма", "Event A: sum", "A оқиғасы: қосынды"), ops, key="c4opa")
    s_a = c2.number_input(tr("A: число", "A: number", "A: сан"), 2, 12, 3, key="c4sa")
    op_b = c3.selectbox(tr("Условие B: сумма", "Condition B: sum", "B шарты: қосынды"), ops, index=1, key="c4opb")
    s_b = c4.number_input(tr("B: число", "B: number", "B: сан"), 2, 12, 6, key="c4sb")
    all_pairs = list(product(range(1, 7), repeat=2))
    B = [p for p in all_pairs if fn[op_b](sum(p), s_b)]
    AB = [p for p in B if fn[op_a](sum(p), s_a)]
    if not B:
        st.error(tr("Условие B невозможно.", "Condition B is impossible.", "B шарты мүмкін емес."))
        return
    st.latex(rf"P(A\mid B)=\frac{{|A\cap B|}}{{|B|}}=\frac{{{len(AB)}}}{{{len(B)}}}={tex_approx(F(len(AB), len(B)))}")
    st.caption(tr(f"B содержит {len(B)} пар из 36; из них A выполняется в {len(AB)}: ",
                  f"B contains {len(B)} of 36 pairs; A holds in {len(AB)} of them: ",
                  f"B 36 жұптың {len(B)}-ін қамтиды; олардың {len(AB)}-інде A орындалады: ")
               + ", ".join(f"({a},{b})" for a, b in AB))


# ---------------------------------------------------------------- 5
def calc_5():
    st.markdown(tr("#### ⚖️ Проверка независимости", "#### ⚖️ Independence check", "#### ⚖️ Тәуелсіздікті тексеру"))
    c1, c2, c3 = st.columns(3)
    with c1:
        a = _frac_input("P(A)", "1/2", "c5a")
    with c2:
        b = _frac_input("P(B)", "7/12", "c5b")
    with c3:
        c = _frac_input("P(A∩B)", "7/24", "c5c")
    st.latex(rf"P(A)P(B)={tex(a)}\cdot{tex(b)}={tex_approx(a * b)}\quad\text{{vs}}\quad P(A\cap B)={tex_approx(c)}")
    if a * b == c:
        st.success(tr("Равны → события **независимы** (independent).", "Equal → the events are **independent**.", "Тең → оқиғалар **тәуелсіз** (independent)."))
    else:
        st.error(tr("Не равны → события **зависимы** (dependent).", "Not equal → the events are **dependent**.", "Тең емес → оқиғалар **тәуелді** (dependent)."))

    st.divider()
    st.markdown(tr("#### 🏹 n независимых попыток: «хотя бы один», «ровно один», «не более одного»", "#### 🏹 n independent trials: \"at least one\", \"exactly one\", \"at most one\"", "#### 🏹 n тәуелсіз сынақ: «ең болмағанда біреуі», «тек біреуі», «біреуінен артық емес»"))
    raw = st.text_input(tr("Вероятности успеха через пробел", "Success probabilities separated by spaces", "Сәттілік ықтималдықтары бос орын арқылы"),
                        "0.2 0.3 0.5", key="c5ps", help="1/3 1/4 1/5 2/3")
    try:
        ps = [F(x.replace(",", ".")) for x in raw.split()]
    except (ValueError, ZeroDivisionError):
        st.error(tr("Введите числа через пробел, например: 0.2 0.3 0.5", "Enter numbers separated by spaces, e.g. 0.2 0.3 0.5", "Сандарды бос орын арқылы енгізіңіз, мысалы: 0.2 0.3 0.5"))
        return
    if not ps or any(not (0 <= p <= 1) for p in ps):
        st.error(tr("Каждая вероятность должна быть от 0 до 1.", "Each probability must be between 0 and 1.", "Әр ықтималдық 0 мен 1 аралығында болуы керек."))
        return
    n = len(ps)
    # распределение числа успехов (динамика)
    dist = [F(1)] + [F(0)] * n
    for p in ps:
        new = [F(0)] * (n + 1)
        for k in range(n + 1):
            if dist[k]:
                new[k] += dist[k] * (1 - p)
                if k + 1 <= n:
                    new[k + 1] += dist[k] * p
        dist = new
    none = dist[0]
    T = lambda ru, en, kk: r"P(\text{" + tr(ru, en, kk) + "})"
    st.latex(T("ни одного", "none", "ешқайсысы") + r"=\prod(1-p_i)=" + r"\cdot".join(tex(1 - p) for p in ps) + "=" + tex_approx(none))
    st.latex(T("хотя бы один", "at least one", "ең болмағанда біреуі") + r"=1-\prod(1-p_i)=" + tex_approx(1 - none))
    st.latex(T("ровно один", "exactly one", "тек біреуі") + "=" + tex_approx(dist[1]))
    st.latex(T("не более одного", "at most one", "біреуінен артық емес") + "=" + tex_approx(dist[0] + dist[1]))
    st.latex(T("все", "all", "барлығы") + r"=\prod p_i=" + tex_approx(dist[n]))
    df = pd.DataFrame({"k": list(range(n + 1)), "P": [float(d) for d in dist]})
    _bar(df, "k", "P", tr("Число успехов k", "Number of successes k", "Сәттіліктер саны k"), PROB())


# ---------------------------------------------------------------- 6 & 7
def _conv(v):
    v = str(v).strip().replace(",", ".")
    return F(v[:-1]) / 100 if v.endswith("%") else F(v)


def _hyp_table(key):
    lg = lang()
    hcol = tr("Гипотеза", "Hypothesis", "Гипотеза")
    bag = tr("мешок", "bag", "қап")
    default = pd.DataFrame({
        hcol: [f"H1: {bag} A", f"H2: {bag} B"],
        "P(H)": ["1/2", "1/2"],
        "P(A|H)": ["3/8", "2/6"],
    })
    hint = tr("0.3, 3/10 или 30%", "0.3, 3/10 or 30%", "0.3, 3/10 немесе 30%")
    df = st.data_editor(default, num_rows="dynamic", key=f"{key}_{lg}", width="stretch",
                        column_config={"P(H)": st.column_config.TextColumn(help=hint),
                                       "P(A|H)": st.column_config.TextColumn(help=hint)})
    rows = []
    for _, r in df.iterrows():
        if not str(r[hcol]).strip() or pd.isna(r["P(H)"]) or pd.isna(r["P(A|H)"]):
            continue
        try:
            rows.append((str(r[hcol]), _conv(r["P(H)"]), _conv(r["P(A|H)"])))
        except (ValueError, ZeroDivisionError):
            st.error(tr(f"Не понимаю числа в строке «{r[hcol]}».", f"Cannot read the numbers in row \"{r[hcol]}\".",
                        f"«{r[hcol]}» жолындағы сандарды түсіне алмадым."))
            st.stop()
    if not rows:
        st.info(tr("Добавьте хотя бы одну гипотезу.", "Add at least one hypothesis.", "Кемінде бір гипотеза қосыңыз."))
        st.stop()
    sh = sum(r[1] for r in rows)
    if sh != 1:
        st.warning(tr(f"Сумма P(H) = {fmt(sh)}, а должна быть 1. Проверьте, все ли гипотезы учтены.",
                      f"Sum of P(H) = {fmt(sh)}, but it must be 1. Check that all hypotheses are included.",
                      f"P(H) қосындысы = {fmt(sh)}, ал 1 болуы керек. Барлық гипотезалар ескерілгенін тексеріңіз."))
    return rows


def calc_6():
    st.markdown(tr("#### 🌳 Формула полной вероятности", "#### 🌳 Law of total probability", "#### 🌳 Толық ықтималдық формуласы"))
    st.caption(tr("Заполните таблицу гипотез. Пример по умолчанию — задача 8 из теста.",
                  "Fill in the table of hypotheses. The default example is problem 8 of the test.",
                  "Гипотезалар кестесін толтырыңыз. Әдепкі мысал — тесттің 8-есебі."))
    rows = _hyp_table("c6tab")
    terms = [h * a for _, h, a in rows]
    total = sum(terms)
    st.latex(r"P(A)=\sum P(H_i)P(A\mid H_i)=" +
             "+".join(rf"{tex(h)}\cdot{tex(a)}" for _, h, a in rows) + "=" + tex_approx(total))
    _result("P(A)", total)
    df = pd.DataFrame({"x": [r[0] for r in rows], "P": [float(t) for t in terms]})
    _bar(df, "x", "P", tr("Гипотеза", "Hypothesis", "Гипотеза"), "P(Hᵢ)·P(A|Hᵢ)")


def calc_7():
    st.markdown(tr("#### 🔮 Формула Байеса", "#### 🔮 Bayes' theorem", "#### 🔮 Байес формуласы"))
    st.caption(tr("Событие A произошло. Пересчитаем вероятности гипотез. Пример — задача 8 «наоборот».",
                  "Event A has happened. Let's update the probabilities of the hypotheses. Example: problem 8 \"in reverse\".",
                  "A оқиғасы болды. Гипотезалардың ықтималдықтарын қайта есептейміз. Мысал — 8-есеп «керісінше»."))
    rows = _hyp_table("c7tab")
    terms = [h * a for _, h, a in rows]
    total = sum(terms)
    if total == 0:
        st.error(tr("P(A) = 0, событие невозможно — Байес не применим.", "P(A) = 0, the event is impossible — Bayes does not apply.",
                    "P(A) = 0, оқиға мүмкін емес — Байес қолданылмайды."))
        return
    st.latex(rf"P(A)={tex_approx(total)}")
    hcol = tr("Гипотеза", "Hypothesis", "Гипотеза")
    pri = tr("До опыта (prior)", "Prior", "Тәжірибеге дейін (prior)")
    post_c = tr("После опыта (posterior)", "Posterior", "Тәжірибеден кейін (posterior)")
    out = []
    for (name, h, a), t in zip(rows, terms):
        post = t / total
        st.latex(rf"P(\text{{{name.split(':')[0]}}}\mid A)=\frac{{{tex(h)}\cdot{tex(a)}}}{{{tex(total)}}}={tex_approx(post)}")
        out.append({hcol: name, pri: float(h), post_c: float(post)})
    st.dataframe(pd.DataFrame(out), hide_index=True, width="stretch")
    df = pd.DataFrame({"x": [o[hcol] for o in out], "P": [o[post_c] for o in out]})
    _bar(df, "x", "P", hcol, "P(H|A)")


# ---------------------------------------------------------------- 8
def calc_8():
    st.markdown(tr("#### 📊 Дискретная случайная величина", "#### 📊 Discrete random variable", "#### 📊 Дискретті кездейсоқ шама"))
    mode = st.radio(tr("Вероятности заданы", "Probabilities are given", "Ықтималдықтар берілген"), [0, 1], horizontal=True,
                    key=f"c8mode_{lang()}", format_func=[tr("числами", "as numbers", "сандармен"),
                                                     tr("через k (например 5/k или 2k)", "via k (e.g. 5/k or 2k)",
                                                        "k арқылы (мысалы 5/k немесе 2k)")].__getitem__)
    xs_lbl = tr("Значения X через пробел", "Values of X separated by spaces", "X мәндері бос орын арқылы")
    bad_num = tr("Проверьте числа.", "Check the numbers.", "Сандарды тексеріңіз.")
    if mode == 0:
        xs_raw = st.text_input(xs_lbl, "0 1 2", key="c8x")
        ps_raw = st.text_input(tr("Вероятности P через пробел", "Probabilities P separated by spaces", "P ықтималдықтары бос орын арқылы"),
                               "1/6 2/6 3/6", key="c8p")
        try:
            xs = [F(v.replace(",", ".")) for v in xs_raw.split()]
            ps = [F(v.replace(",", ".")) for v in ps_raw.split()]
        except (ValueError, ZeroDivisionError):
            st.error(bad_num)
            return
    else:
        xs_raw = st.text_input(xs_lbl, "2 3 4 5", key="c8xk")
        form = st.selectbox(tr("Вид вероятностей", "Form of probabilities", "Ықтималдықтар түрі"), ["cᵢ / k", "cᵢ · k"], key="c8form")
        cs_raw = st.text_input(tr("Коэффициенты cᵢ через пробел", "Coefficients cᵢ separated by spaces", "cᵢ коэффициенттері бос орын арқылы"),
                               "5 7 9 11", key="c8c")
        try:
            xs = [F(v.replace(",", ".")) for v in xs_raw.split()]
            cs = [F(v.replace(",", ".")) for v in cs_raw.split()]
        except (ValueError, ZeroDivisionError):
            st.error(bad_num)
            return
        S = sum(cs)
        if S == 0:
            st.error(tr("Сумма коэффициентов равна 0.", "The coefficients add up to 0.", "Коэффициенттер қосындысы 0-ге тең."))
            return
        if form == "cᵢ / k":
            k = S
            st.latex(rf"\frac{{{'+'.join(tex(c) for c in cs)}}}{{k}}=\frac{{{tex(S)}}}{{k}}=1\Rightarrow k={tex(k)}")
            ps = [c / k for c in cs]
        else:
            k = 1 / S
            st.latex(rf"({'+'.join(tex(c) for c in cs)})\,k={tex(S)}k=1\Rightarrow k={tex(k)}")
            ps = [c * k for c in cs]
        _result("k", k)
    if len(xs) != len(ps) or not xs:
        st.error(tr("Количество значений и вероятностей должно совпадать.", "The number of values and probabilities must match.",
                    "Мәндер мен ықтималдықтар саны бірдей болуы керек."))
        return
    if any(p < 0 for p in ps):
        st.error(tr("Вероятности не могут быть отрицательными.", "Probabilities cannot be negative.", "Ықтималдықтар теріс бола алмайды."))
        return
    if sum(ps) != 1:
        st.error(tr(f"Сумма вероятностей = {fmt(sum(ps))}, а должна быть 1.", f"The probabilities add up to {fmt(sum(ps))}, but must add up to 1.",
                    f"Ықтималдықтар қосындысы = {fmt(sum(ps))}, ал 1 болуы керек."))
        return
    E = sum(x * p for x, p in zip(xs, ps))
    E2 = sum(x * x * p for x, p in zip(xs, ps))
    D = E2 - E * E
    st.latex(r"E[X]=\sum x_ip_i=" + "+".join(rf"{tex(x)}\cdot{tex(p)}" for x, p in zip(xs, ps)) + "=" + tex_approx(E))
    st.latex(rf"E[X^2]={tex_approx(E2)},\qquad D(X)=E[X^2]-(E[X])^2={tex_approx(D)},\qquad \sigma\approx{float(D) ** 0.5:.4f}")
    c1, c2, c3 = st.columns(3)
    with c1:
        _result("E[X]", E)
    with c2:
        _result("D(X)", D)
    with c3:
        st.markdown(f"<div class='result-box'><span>σ</span><b>{float(D) ** 0.5:.4f}</b></div>", unsafe_allow_html=True)

    st.markdown(tr("**Вероятность интервала**", "**Probability of an interval**", "**Аралық ықтималдығы**"))
    c1, c2 = st.columns(2)
    op = c1.selectbox("P(X ? a)", ["<", "≤", ">", "≥", "="], key="c8op")
    a = c2.number_input("a", value=float(xs[len(xs) // 2]), key="c8a")
    a = F(str(a))
    fn = {"<": lambda x: x < a, "≤": lambda x: x <= a, ">": lambda x: x > a, "≥": lambda x: x >= a, "=": lambda x: x == a}
    pr = sum(p for x, p in zip(xs, ps) if fn[op](x))
    st.latex(rf"P(X {op.replace('≤', chr(92) + 'le ').replace('≥', chr(92) + 'ge ')} {tex(a)})={tex_approx(pr)}")

    cdf, acc = [], F(0)
    for p in ps:
        acc += p
        cdf.append(acc)
    st.dataframe(pd.DataFrame({"x": [fmt(x) for x in xs], "P(X=x)": [fmt(p) for p in ps],
                               "F(x)=P(X≤x)": [fmt(c) for c in cdf]}), hide_index=True, width="stretch")
    df = pd.DataFrame({"x": [fmt(x) for x in xs], "P": [float(p) for p in ps]})
    _bar(df, "x", "P", tr("Значение X", "Value of X", "X мәні"), "P(X = x)")


CALCULATORS = {1: calc_1, 2: calc_2, 3: calc_3, 4: calc_4, 5: calc_5, 6: calc_6, 7: calc_7, 8: calc_8}
