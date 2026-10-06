"""Генераторы случайных задач для испытаний (3 языка).

Каждый генератор получает random.Random и код языка ("ru" / "en" / "kk") и возвращает
{"q": текст, "opts": [варианты], "ans": индекс, "expl": решение}.
Числа зависят только от rng, поэтому при смене языка задача остаётся той же.
"""
import random
from .i18n import L
from .mathutil import F, comb, perm, factorial, tex, tex_approx, make_mcq, text_mcq


def P20(rng, lo, hi):
    return F(rng.randint(lo, hi), 20)


def P10(rng, lo, hi):
    return F(rng.randint(lo, hi), 10)


# ---------------------------------------------------------------- Тема 1
def t1_urn(rng, lg):
    r, b, w = rng.randint(2, 8), rng.randint(2, 8), rng.randint(1, 5)
    n = r + b + w
    ans = F(r, n)
    q = L(lg,
          f"В урне {r} красных, {b} синих и {w} белых шаров. Наугад вынимают один шар. Какова вероятность, что он **красный**?",
          f"An urn holds {r} red, {b} blue and {w} white balls. One ball is drawn at random. What is the probability that it is **red**?",
          f"Жәшікте {r} қызыл, {b} көк және {w} ақ шар бар. Кездейсоқ бір шар алынады. Оның **қызыл** болу ықтималдығы қандай?")
    e = L(lg,
          rf"Всего исходов $n = {r}+{b}+{w} = {n}$, благоприятных $m = {r}$. $P = \frac{{m}}{{n}} = {tex_approx(ans)}$.",
          rf"All outcomes $n = {r}+{b}+{w} = {n}$, favourable $m = {r}$. $P = \frac{{m}}{{n}} = {tex_approx(ans)}$.",
          rf"Барлық нәтижелер $n = {r}+{b}+{w} = {n}$, қолайлылары $m = {r}$. $P = \frac{{m}}{{n}} = {tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(r, b + w), F(1, 3), F(r, n - 1)], e)


def t1_die(rng, lg):
    k = rng.randint(1, 4)
    ans = F(6 - k, 6)
    good = ", ".join(str(i) for i in range(k + 1, 7))
    q = L(lg, f"Бросают игральный кубик. Какова вероятность, что выпадет число **больше {k}**?",
          f"A die is rolled. What is the probability of getting a number **greater than {k}**?",
          f"Ойын сүйегі лақтырылады. **{k}-ден үлкен** сан түсу ықтималдығы қандай?")
    e = L(lg, rf"Благоприятные исходы: {good} — их {6 - k}. $P = \frac{{{6 - k}}}{{6}} = {tex_approx(ans)}$.",
          rf"Favourable outcomes: {good} — {6 - k} of them. $P = \frac{{{6 - k}}}{{6}} = {tex_approx(ans)}$.",
          rf"Қолайлы нәтижелер: {good} — барлығы {6 - k}. $P = \frac{{{6 - k}}}{{6}} = {tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(7 - k, 6), F(k, 6), F(6 - k, 5)], e)


def t1_two_dice(rng, lg):
    s = rng.choice([3, 4, 5, 6, 8, 9, 10, 11, 7])
    cnt = 6 - abs(s - 7)
    ans = F(cnt, 36)
    pairs = ", ".join(f"({i},{s - i})" for i in range(1, 7) if 1 <= s - i <= 6)
    q = L(lg, f"Бросают два кубика. Какова вероятность, что **сумма очков равна {s}**?",
          f"Two dice are rolled. What is the probability that **the sum equals {s}**?",
          f"Екі ойын сүйегі лақтырылады. **Ұпайлар қосындысы {s}-ке тең** болу ықтималдығы қандай?")
    e = L(lg, rf"Всего $6\cdot 6 = 36$ равновозможных пар. Пары с суммой {s}: {pairs} — их {cnt}. $P = \frac{{{cnt}}}{{36}} = {tex_approx(ans)}$.",
          rf"There are $6\cdot 6 = 36$ equally likely pairs. Pairs with sum {s}: {pairs} — {cnt} of them. $P = \frac{{{cnt}}}{{36}} = {tex_approx(ans)}$.",
          rf"Барлығы $6\cdot 6 = 36$ тең мүмкіндікті жұп. Қосындысы {s} болатын жұптар: {pairs} — барлығы {cnt}. $P = \frac{{{cnt}}}{{36}} = {tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(1, 11), F(cnt + 1, 36), F(cnt, 21)], e)


def t1_coins(rng, lg):
    n = rng.choice([3, 4])
    k = rng.randint(1, n - 1)
    ans = F(comb(n, k), 2 ** n)
    q = L(lg, f"Монету бросают {n} раза. Какова вероятность, что **орёл выпадет ровно {k} раз(а)**?",
          f"A coin is tossed {n} times. What is the probability of getting **exactly {k} head(s)**?",
          f"Тиын {n} рет лақтырылады. **Елтаңба дәл {k} рет** түсу ықтималдығы қандай?")
    e = L(lg, rf"Всего исходов $2^{n} = {2 ** n}$. Способов выбрать броски с орлом: $C_{{{n}}}^{{{k}}} = {comb(n, k)}$. $P = \frac{{{comb(n, k)}}}{{{2 ** n}}} = {tex_approx(ans)}$.",
          rf"There are $2^{n} = {2 ** n}$ outcomes. Ways to choose which tosses are heads: $C_{{{n}}}^{{{k}}} = {comb(n, k)}$. $P = \frac{{{comb(n, k)}}}{{{2 ** n}}} = {tex_approx(ans)}$.",
          rf"Барлық нәтижелер $2^{n} = {2 ** n}$. Елтаңба түсетін лақтыруларды таңдау тәсілдері: $C_{{{n}}}^{{{k}}} = {comb(n, k)}$. $P = \frac{{{comb(n, k)}}}{{{2 ** n}}} = {tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(1, 2 ** n), F(k, n), F(1, n + 1)], e)


def t1_multiple(rng, lg):
    N, m = rng.randint(20, 60), rng.randint(3, 7)
    cnt = N // m
    ans = F(cnt, N)
    q = L(lg, f"Из чисел 1, 2, …, {N} наугад выбирают одно. Какова вероятность, что оно **делится на {m}**?",
          f"A number is chosen at random from 1, 2, …, {N}. What is the probability that it is **divisible by {m}**?",
          f"1, 2, …, {N} сандарынан кездейсоқ біреуі таңдалады. Оның **{m}-ге бөліну** ықтималдығы қандай?")
    e = L(lg, rf"Чисел, кратных {m}: $\lfloor {N}/{m} \rfloor = {cnt}$. $P = \frac{{{cnt}}}{{{N}}} = {tex_approx(ans)}$.",
          rf"Multiples of {m}: $\lfloor {N}/{m} \rfloor = {cnt}$. $P = \frac{{{cnt}}}{{{N}}} = {tex_approx(ans)}$.",
          rf"{m}-ге еселік сандар: $\lfloor {N}/{m} \rfloor = {cnt}$. $P = \frac{{{cnt}}}{{{N}}} = {tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(1, m), F(cnt + 1, N), F(cnt, N - 1)], e)


# ---------------------------------------------------------------- Тема 2
def t2_perm(rng, lg):
    n = rng.randint(4, 7)
    ans = factorial(n)
    q = L(lg, f"Сколькими способами можно рассадить **{n} человек** на {n} стульев в ряд?",
          f"In how many ways can **{n} people** be seated on {n} chairs in a row?",
          f"**{n} адамды** қатардағы {n} орындыққа неше тәсілмен отырғызуға болады?")
    e = L(lg, rf"Это перестановки: $P_{n} = {n}! = {ans}$.", rf"These are permutations: $P_{n} = {n}! = {ans}$.",
          rf"Бұл алмастырулар: $P_{n} = {n}! = {ans}$.")
    return make_mcq(rng, q, ans, [factorial(n - 1), n * (n - 1), 2 ** n], e, kind="int")


def t2_arr(rng, lg):
    n = rng.randint(6, 12)
    ans = perm(n, 3)
    q = L(lg, f"В соревновании участвуют {n} спортсменов. Сколькими способами можно распределить **золото, серебро и бронзу**?",
          f"{n} athletes take part in a competition. In how many ways can **gold, silver and bronze** be awarded?",
          f"Жарысқа {n} спортшы қатысады. **Алтын, күміс және қола** медальдарды неше тәсілмен бөлуге болады?")
    tail = rf"$A_{{{n}}}^{{3}} = \frac{{{n}!}}{{({n}-3)!}} = {n}\cdot{n - 1}\cdot{n - 2} = {ans}$."
    e = L(lg, "Порядок важен → размещения: " + tail, "Order matters → arrangements: " + tail,
          "Рет маңызды → орналастырулар: " + tail)
    return make_mcq(rng, q, ans, [comb(n, 3), n ** 3, 3 * n], e, kind="int")


def t2_comb(rng, lg):
    n, k = rng.randint(6, 15), rng.randint(2, 4)
    ans = comb(n, k)
    q = L(lg, f"Сколькими способами можно выбрать **{k} дежурных** из {n} студентов?",
          f"In how many ways can **{k} people on duty** be chosen from {n} students?",
          f"{n} студенттің ішінен **{k} кезекшіні** неше тәсілмен таңдауға болады?")
    tail = rf"$C_{{{n}}}^{{{k}}} = \frac{{{n}!}}{{{k}!\,({n}-{k})!}} = {ans}$."
    e = L(lg, "Порядок не важен → сочетания: " + tail, "Order does not matter → combinations: " + tail,
          "Рет маңызды емес → терулер: " + tail)
    return make_mcq(rng, q, ans, [perm(n, k), n * k, comb(n, k - 1)], e, kind="int")


CARD_KINDS = [  # (ru, en, kk, K)
    ("тузы", "aces", "тұз", 4), ("короли", "kings", "король", 4), ("пики ♠", "spades ♠", "қарға ♠", 13),
    ("червы ♥", "hearts ♥", "♥ мастьті", 13), ("дамы", "queens", "дама", 4),
]


def t2_cards(rng, lg):
    ru, en, kk, K = rng.choice(CARD_KINDS)
    ans = F(comb(K, 2), comb(52, 2))
    q = L(lg, f"Из колоды в 52 карты наугад вынимают **2 карты** (без возвращения). Какова вероятность, что обе карты — **{ru}**?",
          f"**2 cards** are drawn at random from a 52-card deck (without replacement). What is the probability that both are **{en}**?",
          f"52 картадан тұратын колодадан кездейсоқ **2 карта** алынады (қайтарусыз). Екеуі де **{kk}** болу ықтималдығы қандай?")
    f1 = rf"$P = \frac{{C_{{{K}}}^{{2}}}}{{C_{{52}}^{{2}}}} = \frac{{{comb(K, 2)}}}{{{comb(52, 2)}}} = {tex_approx(ans)}$. "
    f2 = rf"$\frac{{{K}}}{{52}}\cdot\frac{{{K - 1}}}{{51}}$"
    e = L(lg, f1 + "Проверка через умножение: " + f2 + " — то же самое.",
          f1 + "Check with the multiplication rule: " + f2 + " — the same.",
          f1 + "Көбейту арқылы тексеру: " + f2 + " — дәл солай.")
    return make_mcq(rng, q, ans, [F(K, 52) ** 2, F(K, 52), F(K, 52) * F(K, 51)], e)


def t2_urn(rng, lg):
    r, b, k = rng.randint(4, 8), rng.randint(3, 7), rng.choice([2, 3])
    n = r + b
    ans = F(comb(r, k), comb(n, k))
    q = L(lg, f"В ящике {r} исправных и {b} бракованных деталей. Наугад берут **{k} детали**. Какова вероятность, что **все они исправны**?",
          f"A box contains {r} good and {b} defective parts. **{k} parts** are taken at random. What is the probability that **all of them are good**?",
          f"Жәшікте {r} жарамды және {b} ақаулы бөлшек бар. Кездейсоқ **{k} бөлшек** алынады. **Барлығы жарамды** болу ықтималдығы қандай?")
    e = rf"$P = \frac{{C_{{{r}}}^{{{k}}}}}{{C_{{{n}}}^{{{k}}}}} = \frac{{{comb(r, k)}}}{{{comb(n, k)}}} = {tex_approx(ans)}$."
    return make_mcq(rng, q, ans, [F(r, n) ** k, F(k, n), F(r, n)], e)


# ---------------------------------------------------------------- Тема 3
def _abc(rng):
    while True:
        a, b = rng.randint(4, 14), rng.randint(3, 12)
        lo, hi = max(1, a + b - 19), min(a, b) - 1
        if lo <= hi:
            c = rng.randint(lo, hi)
            return F(a, 20), F(b, 20), F(c, 20)


def _given(a, b, c):
    return rf"$P(A)={tex(a)}$, $P(B)={tex(b)}$, $P(A\cap B)={tex(c)}$"


def t3_union(rng, lg):
    a, b, c = _abc(rng)
    ans = a + b - c
    q = L(lg, f"Известно: {_given(a, b, c)}. Найдите $P(A\\cup B)$.", f"Given: {_given(a, b, c)}. Find $P(A\\cup B)$.",
          f"Берілгені: {_given(a, b, c)}. $P(A\\cup B)$ табыңыз.")
    f = rf"$P(A\cup B)=P(A)+P(B)-P(A\cap B)={tex(a)}+{tex(b)}-{tex(c)}={tex(ans)}$."
    e = L(lg, "Теорема сложения: " + f, "Addition rule: " + f, "Қосу теоремасы: " + f)
    return make_mcq(rng, q, ans, [a + b, a + b - 2 * c, a * b], e)


def t3_inter(rng, lg):
    a, b, c = _abc(rng)
    u = a + b - c
    g = rf"$P(A)={tex(a)}$, $P(B)={tex(b)}$, $P(A\cup B)={tex(u)}$"
    q = L(lg, f"Известно: {g}. Найдите $P(A\\cap B)$.", f"Given: {g}. Find $P(A\\cap B)$.", f"Берілгені: {g}. $P(A\\cap B)$ табыңыз.")
    f = rf"$P(A\cap B)=P(A)+P(B)-P(A\cup B)={tex(a)}+{tex(b)}-{tex(u)}={tex(c)}$."
    e = L(lg, "Из теоремы сложения: " + f, "From the addition rule: " + f, "Қосу теоремасынан: " + f)
    return make_mcq(rng, q, c, [u - a, a * b, u - b], e)


def t3_neither(rng, lg):
    a, b, c = _abc(rng)
    ans = 1 - (a + b - c)
    q = L(lg, f"{_given(a, b, c)}. Найдите вероятность того, что **не произойдёт ни одно** из событий, т.е. $P(\\bar A\\cap\\bar B)$.",
          f"{_given(a, b, c)}. Find the probability that **neither** event happens, i.e. $P(\\bar A\\cap\\bar B)$.",
          f"{_given(a, b, c)}. Оқиғалардың **ешқайсысы орындалмау** ықтималдығын табыңыз, яғни $P(\\bar A\\cap\\bar B)$.")
    f = rf"$\bar A\cap\bar B=\overline{{A\cup B}}$; $P(A\cup B)={tex(a + b - c)}$ → $P(\bar A\cap\bar B)=1-{tex(a + b - c)}={tex(ans)}$."
    e = L(lg, "По закону де Моргана " + f, "By De Morgan's law " + f, "Де Морган заңы бойынша " + f)
    return make_mcq(rng, q, ans, [(1 - a) * (1 - b), 1 - a - b, a + b - c], e)


def t3_exactly_one(rng, lg):
    a, b, c = _abc(rng)
    ans = a + b - 2 * c
    q = L(lg, f"{_given(a, b, c)}. Найдите вероятность того, что произойдёт **ровно одно** из событий A, B.",
          f"{_given(a, b, c)}. Find the probability that **exactly one** of the events A, B happens.",
          f"{_given(a, b, c)}. A, B оқиғаларының **тек біреуі ғана** орындалу ықтималдығын табыңыз.")
    f = (rf"$(A\setminus B)\cup(B\setminus A)$: $P=(P(A)-P(AB))+(P(B)-P(AB))={tex(a)}+{tex(b)}-2\cdot{tex(c)}={tex(ans)}$.")
    e = L(lg, "Ровно одно = " + f, "Exactly one = " + f, "Тек біреуі = " + f)
    return make_mcq(rng, q, ans, [a + b - c, a + b, 1 - (a + b - c)], e)


def t3_exclusive(rng, lg):
    while True:
        x, b = rng.randint(10, 18), rng.randint(2, 8)
        if (20 - x) + b <= 19:
            break
    x, b = F(x, 20), F(b, 20)
    ans = (1 - x) + b
    g = rf"$P(\bar A)={tex(x)}$, $P(B)={tex(b)}$"
    q = L(lg, f"События A и B **несовместны**, {g}. Найдите $P(A\\cup B)$.",
          f"Events A and B are **mutually exclusive**, {g}. Find $P(A\\cup B)$.",
          f"A және B оқиғалары **үйлесімсіз**, {g}. $P(A\\cup B)$ табыңыз.")
    p1 = rf"$P(A)=1-P(\bar A)={tex(1 - x)}$"
    p2 = rf"$P(A\cup B)=P(A)+P(B)={tex(1 - x)}+{tex(b)}={tex(ans)}$"
    e = L(lg, f"Сначала {p1}. Для несовместных $P(A\\cap B)=0$, поэтому {p2}.",
          f"First {p1}. For mutually exclusive events $P(A\\cap B)=0$, so {p2}.",
          f"Алдымен {p1}. Үйлесімсіз оқиғалар үшін $P(A\\cap B)=0$, сондықтан {p2}.")
    return make_mcq(rng, q, ans, [x + b, 1 - x, (1 - x) * b], e)


# ---------------------------------------------------------------- Тема 4
def t4_basic(rng, lg):
    b = P20(rng, 6, 17)
    c = F(rng.randint(1, int(b * 20) - 1), 20)
    a = c + F(rng.randint(1, min(4, 19 - int(b * 20))), 20)
    ans = c / b
    q = L(lg, f"{_given(a, b, c)}. Найдите $P(A\\mid B)$.", f"{_given(a, b, c)}. Find $P(A\\mid B)$.",
          f"{_given(a, b, c)}. $P(A\\mid B)$ табыңыз.")
    f = rf"$P(A\mid B)=\frac{{P(A\cap B)}}{{P(B)}}=\frac{{{tex(c)}}}{{{tex(b)}}}={tex_approx(ans)}$. "
    e = L(lg, f + "Делим на $P(B)$ — на условие!", f + "Divide by $P(B)$ — the condition!", f + "$P(B)$-ға — шартқа бөлеміз!")
    return make_mcq(rng, q, ans, [c / a, c * b, b / c], e)


def t4_mult(rng, lg):
    a, p = P10(rng, 2, 9), P10(rng, 1, 9)
    ans = a * p
    q = L(lg, rf"Доля студентов из Алматы (событие A) $P(A)={tex(a)}$. Среди них доля тех, кто пришёл на пару пешком (B), "
              rf"$P(B\mid A)={tex(p)}$. Найдите вероятность, что случайный студент **из Алматы и пришёл пешком**.",
          rf"The share of students from Almaty (event A) is $P(A)={tex(a)}$. Among them, the share who walked to class (B) is "
          rf"$P(B\mid A)={tex(p)}$. Find the probability that a random student is **from Almaty and walked**.",
          rf"Алматыдан келген студенттердің үлесі (A оқиғасы) $P(A)={tex(a)}$. Олардың ішінде сабаққа жаяу келгендердің үлесі (B) "
          rf"$P(B\mid A)={tex(p)}$. Кездейсоқ студенттің **Алматыдан және жаяу келген** болу ықтималдығын табыңыз.")
    f = rf"$P(A\cap B)=P(A)\cdot P(B\mid A)={tex(a)}\cdot{tex(p)}={tex(ans)}$."
    e = L(lg, "Теорема умножения: " + f, "Multiplication rule: " + f, "Көбейту теоремасы: " + f)
    return make_mcq(rng, q, ans, [p, p / a, a + p - a * p], e)


def t4_dice(rng, lg):
    t = rng.randint(5, 9)
    s = rng.randint(3, t - 1)
    cnt_s = 6 - abs(s - 7)
    cnt_t = sum(6 - abs(v - 7) for v in range(2, t))
    ans = F(cnt_s, cnt_t)
    q = L(lg, f"Бросают два кубика. Известно, что **сумма меньше {t}**. Какова условная вероятность, что **сумма равна {s}**?",
          f"Two dice are rolled. It is known that **the sum is less than {t}**. What is the conditional probability that **the sum equals {s}**?",
          f"Екі ойын сүйегі лақтырылады. **Қосынды {t}-ден кіші** екені белгілі. **Қосынды {s}-ке тең** болуының шартты ықтималдығы қандай?")
    fr = rf"$P = \frac{{{cnt_s}}}{{{cnt_t}}} = {tex_approx(ans)}$."
    e = L(lg, rf"Новое пространство исходов — пары с суммой $<{t}$: их {cnt_t}. Из них сумму {s} дают {cnt_s}. " + fr,
          rf"The new sample space is the pairs with sum $<{t}$: {cnt_t} of them. Of these, {cnt_s} give sum {s}. " + fr,
          rf"Жаңа кеңістік — қосындысы $<{t}$ жұптар: барлығы {cnt_t}. Олардың {cnt_s}-і {s} қосындысын береді. " + fr)
    return make_mcq(rng, q, ans, [F(cnt_s, 36), F(1, t - 2), F(cnt_t, 36)], e)


def t4_family(rng, lg):
    v = rng.randint(0, 2)
    cond = [L(lg, "хотя бы один ребёнок — девочка", "at least one child is a girl", "ең болмағанда бір бала — қыз"),
            L(lg, "младший ребёнок — девочка", "the younger child is a girl", "кіші бала — қыз"),
            L(lg, "старший ребёнок — девочка", "the elder child is a girl", "үлкен бала — қыз")][v]
    ans = F(1, 3) if v == 0 else F(1, 2)
    q = L(lg, f"В семье двое детей; мальчик и девочка равновероятны. Известно, что **{cond}**. Какова вероятность, что **обе — девочки**?",
          f"A family has two children; a boy and a girl are equally likely. It is known that **{cond}**. What is the probability that **both are girls**?",
          f"Отбасында екі бала бар; ұл мен қыз тең ықтимал. **{cond.capitalize()}** екені белгілі. **Екеуі де қыз** болу ықтималдығы қандай?")
    if v == 0:
        e = L(lg, r"Исходы: ММ, МД, ДМ, ДД. Условие оставляет МД, ДМ, ДД — 3 исхода, из них ДД один. $P=\frac{1}{3}$.",
              r"Outcomes: BB, BG, GB, GG. The condition leaves BG, GB, GG — 3 outcomes, one of which is GG. $P=\frac{1}{3}$.",
              r"Нәтижелер: ҰҰ, ҰҚ, ҚҰ, ҚҚ. Шарт ҰҚ, ҚҰ, ҚҚ — 3 нәтижені қалдырады, олардың біреуі ҚҚ. $P=\frac{1}{3}$.")
    else:
        e = L(lg, r"Условие фиксирует пол одного конкретного ребёнка. Остаются 2 исхода, из них ДД один. $P=\frac{1}{2}$.",
              r"The condition fixes the sex of one specific child. 2 outcomes remain, one of which is GG. $P=\frac{1}{2}$.",
              r"Шарт нақты бір баланың жынысын бекітеді. 2 нәтиже қалады, олардың біреуі ҚҚ. $P=\frac{1}{2}$.")
    return make_mcq(rng, q, ans, [F(1, 4), F(1, 2) if ans != F(1, 2) else F(1, 3), F(2, 3), F(3, 4)], e)


def t4_complement(rng, lg):
    while True:
        b, c = P10(rng, 2, 6), P10(rng, 2, 8)
        ab = b * c
        lo = ab + F(1, 20)
        cands = [F(k, 20) for k in range(1, 20) if F(k, 20) >= lo and F(k, 20) + b - ab <= F(19, 20)]
        if cands:
            a = rng.choice(cands)
            break
    ans = (1 - a - b + ab) / (1 - b)
    g = rf"$P(A)={tex(a)}$, $P(B)={tex(b)}$, $P(A\mid B)={tex(c)}$"
    q = L(lg, f"{g}. Найдите $P(\\bar A\\mid \\bar B)$. _(Как задача №1 из теста.)_",
          f"{g}. Find $P(\\bar A\\mid \\bar B)$. _(Like problem 1 of the test.)_",
          f"{g}. $P(\\bar A\\mid \\bar B)$ табыңыз. _(Тесттің 1-есебі сияқты.)_")
    e = (rf"1) $P(A\cap B)=P(A\mid B)P(B)={tex(c)}\cdot{tex(b)}={tex(ab)}$. "
         rf"2) $P(\bar A\cap\bar B)=1-P(A\cup B)=1-({tex(a)}+{tex(b)}-{tex(ab)})={tex(1 - a - b + ab)}$. "
         rf"3) $P(\bar A\mid\bar B)=\frac{{{tex(1 - a - b + ab)}}}{{1-{tex(b)}}}={tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [1 - c, 1 - a, 1 - a - b + ab], e)


# ---------------------------------------------------------------- Тема 5
def t5_inter(rng, lg):
    a, b = P10(rng, 1, 9), P10(rng, 1, 9)
    ans = a * b
    g = rf"$P(A)={tex(a)}$, $P(B)={tex(b)}$"
    q = L(lg, f"События A и B **независимы**, {g}. Найдите $P(A\\cap B)$.",
          f"Events A and B are **independent**, {g}. Find $P(A\\cap B)$.",
          f"A және B оқиғалары **тәуелсіз**, {g}. $P(A\\cap B)$ табыңыз.")
    f = rf"$P(A\cap B)=P(A)P(B)={tex(a)}\cdot{tex(b)}={tex(ans)}$."
    e = L(lg, "Для независимых " + f, "For independent events " + f, "Тәуелсіз оқиғалар үшін " + f)
    return make_mcq(rng, q, ans, [a + b - a * b, min(a, b), F(0)], e)


def t5_union(rng, lg):
    a, b = P10(rng, 1, 8), P10(rng, 1, 8)
    ans = a + b - a * b
    g = rf"$P(A)={tex(a)}$, $P(B)={tex(b)}$"
    q = L(lg, f"События A и B **независимы**, {g}. Найдите $P(A\\cup B)$.",
          f"Events A and B are **independent**, {g}. Find $P(A\\cup B)$.",
          f"A және B оқиғалары **тәуелсіз**, {g}. $P(A\\cup B)$ табыңыз.")
    f1 = rf"$P(A\cup B)=P(A)+P(B)-P(A)P(B)={tex(a)}+{tex(b)}-{tex(a * b)}={tex(ans)}$. "
    f2 = rf"$1-(1-{tex(a)})(1-{tex(b)})={tex(ans)}$."
    e = L(lg, f1 + "Или через противоположное: " + f2, f1 + "Or via the complement: " + f2, f1 + "Немесе қарама-қарсы оқиға арқылы: " + f2)
    return make_mcq(rng, q, ans, [a + b, a * b, 1 - a * b], e)


def t5_three(rng, lg):
    ps = [P10(rng, 1, 7) for _ in range(3)]
    miss = (1 - ps[0]) * (1 - ps[1]) * (1 - ps[2])
    ans = 1 - miss
    p = f"{tex(ps[0])}, {tex(ps[1])}, {tex(ps[2])}"
    q = L(lg, f"Три стрелка независимо стреляют по мишени. Вероятности попадания: {p}. Какова вероятность, что **мишень поражена хотя бы раз**?",
          f"Three shooters fire at a target independently. Hit probabilities: {p}. What is the probability that **the target is hit at least once**?",
          f"Үш атқыш нысанаға бір-біріне тәуелсіз атады. Тигізу ықтималдықтары: {p}. **Нысанаға ең болмағанда бір рет тию** ықтималдығы қандай?")
    f = rf"$P=1-(1-{tex(ps[0])})(1-{tex(ps[1])})(1-{tex(ps[2])})=1-{tex(miss)}={tex(ans)}$."
    e = L(lg, "«Хотя бы один» = 1 − «все промахнулись»: " + f, "\"At least one\" = 1 − \"all miss\": " + f,
          "«Ең болмағанда біреуі» = 1 − «барлығы жаңылды»: " + f)
    return make_mcq(rng, q, ans, [ps[0] * ps[1] * ps[2], miss, sum(ps)], e)


def t5_check(rng, lg):
    a, b = P10(rng, 2, 8), P10(rng, 2, 8)
    indep = rng.random() < 0.5
    if indep:
        c = a * b
    else:
        while True:
            c = a * b + rng.choice([-1, 1]) * F(rng.randint(1, 3), 20)
            if 0 < c <= min(a, b):
                break
    opts = [L(lg, "Независимы", "Independent", "Тәуелсіз"),
            L(lg, "Зависимы (не независимы)", "Dependent (not independent)", "Тәуелді (тәуелсіз емес)"),
            L(lg, "Несовместны", "Mutually exclusive", "Үйлесімсіз"),
            L(lg, "Данных недостаточно", "Not enough information", "Деректер жеткіліксіз")]
    q = L(lg, f"{_given(a, b, c)}. Что можно сказать о событиях A и B?",
          f"{_given(a, b, c)}. What can be said about events A and B?",
          f"{_given(a, b, c)}. A және B оқиғалары туралы не айтуға болады?")
    if indep:
        right = opts[0]
        f = rf"$P(A)P(B)={tex(a)}\cdot{tex(b)}={tex(a * b)}=P(A\cap B)$"
        e = L(lg, f + " → независимы.", f + " → independent.", f + " → тәуелсіз.")
    else:
        right = opts[1]
        f = rf"$P(A)P(B)={tex(a * b)}\ne{tex(c)}=P(A\cap B)$"
        e = L(lg, f + " → зависимы. Несовместными они не являются, ведь $P(A\\cap B)\\ne0$.",
              f + " → dependent. They are not mutually exclusive either, since $P(A\\cap B)\\ne0$.",
              f + " → тәуелді. Олар үйлесімсіз де емес, өйткені $P(A\\cap B)\\ne0$.")
    return text_mcq(rng, q, right, opts, e)


def t5_exactly_one(rng, lg):
    p1, p2 = P10(rng, 2, 9), P10(rng, 2, 9)
    ans = p1 * (1 - p2) + (1 - p1) * p2
    q = L(lg, rf"Два студента независимо решают задачу с вероятностями ${tex(p1)}$ и ${tex(p2)}$. Какова вероятность, что задачу решит **ровно один** из них?",
          rf"Two students solve a problem independently with probabilities ${tex(p1)}$ and ${tex(p2)}$. What is the probability that **exactly one** of them solves it?",
          rf"Екі студент есепті бір-біріне тәуелсіз ${tex(p1)}$ және ${tex(p2)}$ ықтималдықтарымен шығарады. Есепті **тек біреуі ғана** шығару ықтималдығы қандай?")
    e = rf"$P=p_1(1-p_2)+(1-p_1)p_2={tex(p1)}\cdot{tex(1 - p2)}+{tex(1 - p1)}\cdot{tex(p2)}={tex(ans)}$."
    return make_mcq(rng, q, ans, [p1 + p2 - p1 * p2, p1 * p2, p1 + p2], e)


# ---------------------------------------------------------------- Тема 6
def _bags(rng):
    while True:
        r1, b1, r2, b2 = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)
        if F(r1, r1 + b1) != F(r2, r2 + b2):
            return r1, b1, r2, b2


def _bags_text(lg, r1, b1, r2, b2):
    return L(lg, f"В мешке A — {r1} красных и {b1} чёрных шаров, в мешке B — {r2} красных и {b2} чёрных.",
             f"Bag A has {r1} red and {b1} black balls, bag B has {r2} red and {b2} black.",
             f"A қабында {r1} қызыл және {b1} қара шар, B қабында {r2} қызыл және {b2} қара шар бар.")


def t6_bags(rng, lg):
    r1, b1, r2, b2 = _bags(rng)
    p1, p2 = F(r1, r1 + b1), F(r2, r2 + b2)
    ans = F(1, 2) * p1 + F(1, 2) * p2
    q = _bags_text(lg, r1, b1, r2, b2) + " " + L(
        lg, "Наугад выбирают мешок и достают шар. Какова вероятность, что он **красный**?",
        "A bag is chosen at random and a ball is drawn. What is the probability that it is **red**?",
        "Кездейсоқ қап таңдалып, одан шар алынады. Оның **қызыл** болу ықтималдығы қандай?")
    f = rf"$P(R)=\frac12\cdot{tex(p1)}+\frac12\cdot{tex(p2)}={tex_approx(ans)}$."
    e = L(lg, r"Гипотезы $H_A, H_B$ по $\frac12$. " + f, r"Hypotheses $H_A, H_B$ with $\frac12$ each. " + f,
          r"$H_A, H_B$ гипотезалары, әрқайсысы $\frac12$. " + f)
    return make_mcq(rng, q, ans, [F(r1 + r2, r1 + b1 + r2 + b2), p1 * p2, p1 + p2], e)


def _factories(rng):
    s1 = rng.choice([40, 45, 50, 55, 60])
    s2 = rng.choice([x for x in (20, 25, 30, 35) if s1 + x < 100])
    s3 = 100 - s1 - s2
    d = [rng.randint(1, 6) for _ in range(3)]
    return [s1, s2, s3], d


def t6_factory(rng, lg):
    s, d = _factories(rng)
    ans = sum(F(si, 100) * F(di, 100) for si, di in zip(s, d))
    q = L(lg, f"Детали поступают с трёх заводов: {s[0]}%, {s[1]}% и {s[2]}% продукции. Доля брака на заводах: {d[0]}%, {d[1]}% и {d[2]}%. "
              "Какова вероятность, что случайная деталь **бракованная**?",
          f"Parts come from three factories: {s[0]}%, {s[1]}% and {s[2]}% of output. Defect rates: {d[0]}%, {d[1]}% and {d[2]}%. "
          "What is the probability that a random part is **defective**?",
          f"Бөлшектер үш зауыттан түседі: өнімнің {s[0]}%, {s[1]}% және {s[2]}%. Ақау үлесі: {d[0]}%, {d[1]}% және {d[2]}%. "
          "Кездейсоқ бөлшектің **ақаулы** болу ықтималдығы қандай?")
    e = (rf"$P(D)=\sum P(H_i)P(D\mid H_i)={tex(F(s[0],100))}\cdot{tex(F(d[0],100))}+"
         rf"{tex(F(s[1],100))}\cdot{tex(F(d[1],100))}+{tex(F(s[2],100))}\cdot{tex(F(d[2],100))}={tex(ans)}$.")
    return make_mcq(rng, q, ans, [F(sum(d), 300), F(sum(d), 100), F(max(d), 100)], e)


def t6_coins(rng, lg):
    n, m = rng.randint(1, 5), rng.randint(2, 6)
    ans = F(n, n + m) + F(m, n + m) * F(1, 2)
    q = L(lg, f"В кармане {n} монет(ы) с орлом на обеих сторонах и {m} обычных монет. Наугад берут монету и подбрасывают. Какова вероятность **орла**?",
          f"A pocket holds {n} double-headed coin(s) and {m} fair coins. A coin is taken at random and tossed. What is the probability of **heads**?",
          f"Қалтада екі жағы да елтаңба {n} тиын және {m} кәдімгі тиын бар. Кездейсоқ тиын алынып, лақтырылады. **Елтаңба** түсу ықтималдығы қандай?")
    f = rf"$P(H)=\frac{{{n}}}{{{n + m}}}\cdot1+\frac{{{m}}}{{{n + m}}}\cdot\frac12={tex_approx(ans)}$. "
    e = L(lg, f + "_(Похоже на задачу №15 — там решают обратную задачу и ищут n.)_",
          f + "_(Similar to problem 15 — there the inverse problem is solved to find n.)_",
          f + "_(15-есепке ұқсас — онда кері есеп шешіліп, n ізделеді.)_")
    return make_mcq(rng, q, ans, [F(1, 2), F(n, n + m), F(n + 1, n + m + 1)], e)


def t6_student(rng, lg):
    p, k = P10(rng, 3, 8), rng.choice([3, 4, 5])
    ans = p + (1 - p) * F(1, k)
    q = L(lg, rf"Студент знает ответ на тестовый вопрос с вероятностью ${tex(p)}$, иначе угадывает один из {k} вариантов. Какова вероятность, что он ответит **правильно**?",
          rf"A student knows the answer to a test question with probability ${tex(p)}$, otherwise guesses one of {k} options. What is the probability of answering **correctly**?",
          rf"Студент тест сұрағының жауабын ${tex(p)}$ ықтималдықпен біледі, әйтпесе {k} нұсқаның бірін болжайды. Оның **дұрыс** жауап беру ықтималдығы қандай?")
    w = L(lg, "верно", "correct", "дұрыс")
    e = rf"$P(\text{{{w}}})={tex(p)}\cdot1+{tex(1 - p)}\cdot\frac{{1}}{{{k}}}={tex_approx(ans)}$."
    return make_mcq(rng, q, ans, [p, F(1, k), p * F(1, k)], e)


def t6_weather(rng, lg):
    p, q1, q2 = P10(rng, 1, 6), P10(rng, 3, 8), P10(rng, 1, 2)
    ans = p * q1 + (1 - p) * q2
    q = L(lg, rf"Дождь в Алматы идёт с вероятностью ${tex(p)}$. В дождь вы опаздываете на пару с вероятностью ${tex(q1)}$, без дождя — ${tex(q2)}$. Какова вероятность **опоздать**?",
          rf"It rains in Almaty with probability ${tex(p)}$. When it rains you are late for class with probability ${tex(q1)}$, otherwise ${tex(q2)}$. What is the probability of **being late**?",
          rf"Алматыда жаңбыр ${tex(p)}$ ықтималдықпен жауады. Жаңбырда сабаққа ${tex(q1)}$ ықтималдықпен кешігесіз, жаңбырсыз — ${tex(q2)}$. **Кешігу** ықтималдығы қандай?")
    e = rf"$P(L)={tex(p)}\cdot{tex(q1)}+{tex(1 - p)}\cdot{tex(q2)}={tex(ans)}$."
    return make_mcq(rng, q, ans, [(q1 + q2) / 2, p * q1, q1 * q2], e)


# ---------------------------------------------------------------- Тема 7
def t7_factory(rng, lg):
    s, d = _factories(rng)
    terms = [F(si, 100) * F(di, 100) for si, di in zip(s, d)]
    tot = sum(terms)
    ans = terms[0] / tot
    q = L(lg, f"Заводы выпускают {s[0]}%, {s[1]}%, {s[2]}% деталей, брак — {d[0]}%, {d[1]}%, {d[2]}%. "
              "Взятая деталь оказалась **бракованной**. Какова вероятность, что она с **первого завода**?",
          f"Factories make {s[0]}%, {s[1]}%, {s[2]}% of parts with defect rates {d[0]}%, {d[1]}%, {d[2]}%. "
          "A part turned out **defective**. What is the probability it came from the **first factory**?",
          f"Зауыттар бөлшектердің {s[0]}%, {s[1]}%, {s[2]}%-ын шығарады, ақау — {d[0]}%, {d[1]}%, {d[2]}%. "
          "Алынған бөлшек **ақаулы** болып шықты. Оның **бірінші зауыттан** болу ықтималдығы қандай?")
    e = L(lg, "Полная вероятность", "Total probability", "Толық ықтималдық") + \
        rf": $P(D)={tex(tot)}$. " + L(lg, "Байес", "Bayes", "Байес") + \
        rf": $P(H_1\mid D)=\frac{{{tex(terms[0])}}}{{{tex(tot)}}}={tex_approx(ans)}$."
    return make_mcq(rng, q, ans, [F(s[0], 100), terms[0], F(d[0], sum(d))], e)


def t7_bags(rng, lg):
    r1, b1, r2, b2 = _bags(rng)
    p1, p2 = F(r1, r1 + b1), F(r2, r2 + b2)
    tot = F(1, 2) * (p1 + p2)
    ans = F(1, 2) * p1 / tot
    q = _bags_text(lg, r1, b1, r2, b2) + " " + L(
        lg, "Мешок выбрали наугад, вынутый шар — **красный**. Какова вероятность, что это был **мешок A**?",
        "A bag was chosen at random and the ball drawn is **red**. What is the probability that it was **bag A**?",
        "Қап кездейсоқ таңдалды, алынған шар — **қызыл**. Бұл **A қабы** болу ықтималдығы қандай?")
    e = (rf"$P(R)=\frac12({tex(p1)}+{tex(p2)})={tex_approx(tot)}$; "
         rf"$P(A\mid R)=\frac{{\frac12\cdot{tex(p1)}}}{{{tex(tot)}}}={tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(1, 2), F(r1, r1 + r2), tot], e)


def t7_test(rng, lg):
    p = F(rng.choice([1, 2, 5, 10]), 100)
    se = F(rng.choice([90, 95, 98, 99]), 100)
    fp = F(rng.choice([2, 5, 10]), 100)
    tot = p * se + (1 - p) * fp
    ans = p * se / tot
    q = L(lg, rf"Болезнь встречается у ${tex(p)}$ людей. Тест находит её у больного с вероятностью ${tex(se)}$, а у здорового ошибочно даёт «+» "
              rf"с вероятностью ${tex(fp)}$. Тест положительный. Какова вероятность, что человек **действительно болен**?",
          rf"A disease affects ${tex(p)}$ of people. The test detects it in an ill person with probability ${tex(se)}$, and gives a false \"+\" "
          rf"for a healthy person with probability ${tex(fp)}$. The test is positive. What is the probability that the person **is really ill**?",
          rf"Ауру адамдардың ${tex(p)}$ бөлігінде кездеседі. Тест ауруды науқаста ${tex(se)}$ ықтималдықпен анықтайды, ал сау адамда "
          rf"${tex(fp)}$ ықтималдықпен қате «+» береді. Тест оң. Адамның **шынымен ауру** болу ықтималдығы қандай?")
    ill = L(lg, "болен", "ill", "ауру")
    tail = L(lg, "Мало, потому что болезнь редкая!", "Small, because the disease is rare!", "Аз, өйткені ауру сирек кездеседі!")
    e = (rf"$P(+)={tex(p)}\cdot{tex(se)}+{tex(1 - p)}\cdot{tex(fp)}={tex(tot)}$. "
         rf"$P(\text{{{ill}}}\mid +)=\frac{{{tex(p * se)}}}{{{tex(tot)}}}={tex_approx(ans)}$. " + tail)
    return make_mcq(rng, q, ans, [se, 1 - fp, p], e)


def t7_coins(rng, lg):
    n, m = rng.randint(1, 4), rng.randint(2, 6)
    ans = F(2 * n, 2 * n + m)
    q = L(lg, f"Есть {n} монет(ы) с двумя орлами и {m} обычных. Взяли наугад монету, подбросили — выпал **орёл**. Какова вероятность, что монета **двусторонняя**?",
          f"There are {n} double-headed coin(s) and {m} fair ones. A coin is taken at random and tossed — **heads**. What is the probability that the coin is **double-headed**?",
          f"Екі жағы да елтаңба {n} тиын және {m} кәдімгі тиын бар. Кездейсоқ тиын лақтырылды — **елтаңба** түсті. Тиынның **екі жағы да елтаңба** болу ықтималдығы қандай?")
    e = (rf"$P(H)=\frac{{{n}}}{{{n + m}}}+\frac{{{m}}}{{{n + m}}}\cdot\frac12$; "
         rf"$P(H_2\mid H)=\frac{{{n}/{n + m}}}{{P(H)}}=\frac{{2\cdot{n}}}{{2\cdot{n}+{m}}}={tex_approx(ans)}$.")
    return make_mcq(rng, q, ans, [F(n, n + m), F(n, n + m) + F(m, 2 * (n + m)), F(1, 2)], e)


def t7_student(rng, lg):
    p, k = P10(rng, 3, 8), rng.choice([3, 4, 5])
    tot = p + (1 - p) * F(1, k)
    ans = p / tot
    q = L(lg, rf"Студент знает ответ с вероятностью ${tex(p)}$, иначе угадывает из {k} вариантов. Он ответил **правильно**. Какова вероятность, что он **знал** ответ?",
          rf"A student knows the answer with probability ${tex(p)}$, otherwise guesses among {k} options. The answer is **correct**. What is the probability that the student **knew** it?",
          rf"Студент жауапты ${tex(p)}$ ықтималдықпен біледі, әйтпесе {k} нұсқадан болжайды. Ол **дұрыс** жауап берді. Оның жауапты **білген** болу ықтималдығы қандай?")
    w1, w2 = L(lg, "верно", "correct", "дұрыс"), L(lg, "знал", "knew", "білді")
    e = rf"$P(\text{{{w1}}})={tex_approx(tot)}$; $P(\text{{{w2}}}\mid\text{{{w1}}})=\frac{{{tex(p)}}}{{{tex(tot)}}}={tex_approx(ans)}$."
    return make_mcq(rng, q, ans, [p, tot, 1 - F(1, k)], e)


# ---------------------------------------------------------------- Тема 8
def _dist(rng, n=4, base=0):
    while True:
        cuts = sorted(rng.sample(range(1, 10), n - 1))
        parts = [b - a for a, b in zip([0] + cuts, cuts + [10])]
        if all(p > 0 for p in parts):
            break
    xs = sorted(rng.sample(range(base, base + 6), n))
    return xs, [F(p, 10) for p in parts]


def _table(xs, ps):
    head = "| X | " + " | ".join(str(x) for x in xs) + " |"
    sep = "|---|" + "---|" * len(xs)
    row = "| P | " + " | ".join(tex(p) for p in ps) + " |"
    return f"\n\n{head}\n{sep}\n{row}\n\n"


def t8_find_k(rng, lg):
    cs = [rng.randint(1, 5) for _ in range(4)]
    S = sum(cs)
    plus = "+".join(map(str, cs))
    if rng.random() < 0.5:
        ans, cells, kind = F(S), [f"{c}/k" for c in cs], "num"
        f = rf"$\frac{{{plus}}}{{k}}=\frac{{{S}}}{{k}}=1 \Rightarrow k={S}$."
        wr = [F(1, S), F(S + 1), F(4)]
    else:
        ans, cells, kind = F(1, S), [f"{c}k" for c in cs], "prob"
        f = rf"$({plus})k={S}k=1 \Rightarrow k={tex(ans)}$."
        wr = [F(S), F(1, S + 1), F(1, 4)]
    tbl = "\n\n| X | 0 | 1 | 2 | 3 |\n|---|---|---|---|---|\n| P | " + " | ".join(cells) + " |\n\n"
    q = L(lg, "Закон распределения дискретной случайной величины:" + tbl + "Найдите **k**.",
          "The distribution of a discrete random variable:" + tbl + "Find **k**.",
          "Дискретті кездейсоқ шаманың үлестірім заңы:" + tbl + "**k**-ны табыңыз.")
    e = L(lg, "Сумма вероятностей равна 1: ", "The probabilities add up to 1: ", "Ықтималдықтар қосындысы 1-ге тең: ") + f
    return make_mcq(rng, q, ans, wr, e, kind=kind)


def t8_mean(rng, lg):
    xs, ps = _dist(rng)
    E = sum(F(x) * p for x, p in zip(xs, ps))
    q = L(lg, "Найдите **математическое ожидание** $E[X]$:", "Find the **expected value** $E[X]$:",
          "**Математикалық күтімді** $E[X]$ табыңыз:") + _table(xs, ps)
    e = rf"$E[X]=\sum x_i p_i=" + "+".join(rf"{x}\cdot{tex(p)}" for x, p in zip(xs, ps)) + rf"={tex(E)}$."
    return make_mcq(rng, q, E, [F(sum(xs), len(xs)), F(sum(xs)), E + F(1, 2)], e, kind="num")


def t8_cdf(rng, lg):
    xs, ps = _dist(rng)
    a = rng.choice(xs[1:])
    strict = rng.random() < 0.5
    ans = sum(p for x, p in zip(xs, ps) if (x < a if strict else x <= a))
    other = sum(p for x, p in zip(xs, ps) if (x <= a if strict else x < a))
    pa = ps[xs.index(a)]
    sym = "<" if strict else r"\le"
    q = L(lg, "Найдите", "Find", "Табыңыз:") + rf" $P(X {sym} {a})$:" + _table(xs, ps)
    s = "+".join(tex(p) for x, p in zip(xs, ps) if (x < a if strict else x <= a))
    e = L(lg, rf"Складываем вероятности значений $x {sym} {a}$: ${s}={tex(ans)}$. Следите за строгим/нестрогим знаком!",
          rf"Add the probabilities of the values $x {sym} {a}$: ${s}={tex(ans)}$. Watch the strict/non-strict sign!",
          rf"$x {sym} {a}$ мәндерінің ықтималдықтарын қосамыз: ${s}={tex(ans)}$. Қатаң/қатаң емес таңбаға назар аударыңыз!")
    return make_mcq(rng, q, ans, [other, pa, 1 - ans], e)


def t8_var(rng, lg):
    xs, ps = _dist(rng, n=3, base=0)
    E = sum(F(x) * p for x, p in zip(xs, ps))
    E2 = sum(F(x * x) * p for x, p in zip(xs, ps))
    D = E2 - E * E
    q = L(lg, "Найдите **дисперсию** $D(X)$:", "Find the **variance** $D(X)$:", "**Дисперсияны** $D(X)$ табыңыз:") + _table(xs, ps)
    e = (rf"$E[X]={tex(E)}$, $E[X^2]=" + "+".join(rf"{x*x}\cdot{tex(p)}" for x, p in zip(xs, ps))
         + rf"={tex(E2)}$. $D(X)=E[X^2]-(E[X])^2={tex(E2)}-{tex(E * E)}={tex(D)}$.")
    return make_mcq(rng, q, D, [E2, E * E, E2 - E], e, kind="num")


def t8_coin(rng, lg):
    m = rng.choice([2, 3, 4])
    pt = F(1, m + 1)
    ph = 1 - pt
    ans = 2 * pt * ph
    q = L(lg, f"Монета несимметрична: орёл выпадает в {m} раза чаще решки. Монету бросают дважды, X — число решек. Найдите $P(X=1)$. _(Как задача №17 OR.)_",
          f"A coin is biased: heads is {m} times as likely as tails. It is tossed twice; X is the number of tails. Find $P(X=1)$. _(Like problem 17 OR.)_",
          f"Тиын симметриялы емес: елтаңба саннан {m} есе жиі түседі. Тиын екі рет лақтырылады, X — сан жағының түсу саны. $P(X=1)$ табыңыз. _(17 OR есеп сияқты.)_")
    e = L(lg, rf"$P(\text{{решка}})=\frac{{1}}{{{m + 1}}}$, $P(\text{{орёл}})={tex(ph)}$. $X=1$: РО или ОР, ",
          rf"$P(T)=\frac{{1}}{{{m + 1}}}$, $P(H)={tex(ph)}$. $X=1$: TH or HT, ",
          rf"$P(\text{{сан}})=\frac{{1}}{{{m + 1}}}$, $P(\text{{елтаңба}})={tex(ph)}$. $X=1$: СЕ немесе ЕС, ") + \
        rf"$P=2\cdot{tex(pt)}\cdot{tex(ph)}={tex_approx(ans)}$."
    return make_mcq(rng, q, ans, [pt * ph, F(1, 2), pt * pt], e)


GENERATORS = {
    1: [t1_urn, t1_die, t1_two_dice, t1_coins, t1_multiple],
    2: [t2_perm, t2_arr, t2_comb, t2_cards, t2_urn],
    3: [t3_union, t3_inter, t3_neither, t3_exactly_one, t3_exclusive],
    4: [t4_basic, t4_mult, t4_dice, t4_family, t4_complement],
    5: [t5_inter, t5_union, t5_three, t5_check, t5_exactly_one],
    6: [t6_bags, t6_factory, t6_coins, t6_student, t6_weather],
    7: [t7_factory, t7_bags, t7_test, t7_coins, t7_student],
    8: [t8_find_k, t8_mean, t8_cdf, t8_var, t8_coin],
}


def build_quiz(topic_id: int, seed: int, lg: str = "ru"):
    rng = random.Random(seed * 1000 + topic_id)
    gens = list(GENERATORS[topic_id])
    rng.shuffle(gens)
    return [g(rng, lg) for g in gens]
