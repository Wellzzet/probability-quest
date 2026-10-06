"""Темы курса: названия, краткие описания, словарь терминов, доспехи.

Тексты уроков лежат в lessons_ru.py, lessons_en.py, lessons_kk.py.
Блоки урока:
  ("md", текст) · ("latex", формула) · ("terms",) — общий словарь
  ("example", заголовок, решение) · ("tip", текст) · ("warn", текст)
"""
from .lessons_ru import LESSONS as _RU
from .lessons_en import LESSONS as _EN
from .lessons_kk import LESSONS as _KK

TOPICS = [
    {"id": 1, "icon": "🎲", "armor": "helmet", "cost": 0,
     "title": {"ru": "Классическая вероятность", "en": "Classical probability", "kk": "Классикалық ықтималдық"},
     "summary": {"ru": "Случайный эксперимент, пространство исходов, формула P = m/n.",
                 "en": "Random experiment, sample space, the formula P = m/n.",
                 "kk": "Кездейсоқ тәжірибе, элементар оқиғалар кеңістігі, P = m/n формуласы."}},
    {"id": 2, "icon": "🃏", "armor": "chest", "cost": 120,
     "title": {"ru": "Комбинаторика", "en": "Combinatorics", "kk": "Комбинаторика"},
     "summary": {"ru": "Перестановки, размещения, сочетания — как считать m и n.",
                 "en": "Permutations, arrangements, combinations — how to count m and n.",
                 "kk": "Алмастырулар, орналастырулар, терулер — m мен n-ді қалай санау керек."}},
    {"id": 3, "icon": "🔗", "armor": "shoulders", "cost": 140,
     "title": {"ru": "Операции над событиями", "en": "Algebra of events", "kk": "Оқиғаларға амалдар"},
     "summary": {"ru": "Объединение, пересечение, дополнение, несовместность, теорема сложения.",
                 "en": "Union, intersection, complement, mutually exclusive events, addition rule.",
                 "kk": "Бірігу, қиылысу, қарама-қарсы оқиға, үйлесімсіздік, қосу теоремасы."}},
    {"id": 4, "icon": "🎯", "armor": "gauntlets", "cost": 160,
     "title": {"ru": "Условная вероятность", "en": "Conditional probability", "kk": "Шартты ықтималдық"},
     "summary": {"ru": "P(A|B), теорема умножения, «сужение» пространства исходов.",
                 "en": "P(A|B), the multiplication rule, the reduced sample space.",
                 "kk": "P(A|B), көбейту теоремасы, оқиғалар кеңістігінің «тарылуы»."}},
    {"id": 5, "icon": "⚖️", "armor": "belt", "cost": 180,
     "title": {"ru": "Независимые события", "en": "Independent events", "kk": "Тәуелсіз оқиғалар"},
     "summary": {"ru": "P(AB) = P(A)P(B), «хотя бы один», независимость в совокупности.",
                 "en": "P(AB) = P(A)P(B), \"at least one\", mutual independence.",
                 "kk": "P(AB) = P(A)P(B), «ең болмағанда біреуі», жиынтықта тәуелсіздік."}},
    {"id": 6, "icon": "🌳", "armor": "boots", "cost": 200,
     "title": {"ru": "Формула полной вероятности", "en": "Law of total probability", "kk": "Толық ықтималдық формуласы"},
     "summary": {"ru": "Гипотезы H₁…Hₙ и вероятность события «через все пути».",
                 "en": "Hypotheses H₁…Hₙ and the probability of an event \"over all paths\".",
                 "kk": "H₁…Hₙ гипотезалары және оқиғаның «барлық жол арқылы» ықтималдығы."}},
    {"id": 7, "icon": "🔮", "armor": "shield", "cost": 220,
     "title": {"ru": "Формула Байеса", "en": "Bayes' theorem", "kk": "Байес формуласы"},
     "summary": {"ru": "Пересчёт вероятностей гипотез после того, как событие произошло.",
                 "en": "Updating the probabilities of hypotheses after an event has occurred.",
                 "kk": "Оқиға болғаннан кейін гипотезалардың ықтималдықтарын қайта есептеу."}},
    {"id": 8, "icon": "📊", "armor": "sword", "cost": 240,
     "title": {"ru": "Дискретная случайная величина", "en": "Discrete random variable", "kk": "Дискретті кездейсоқ шама"},
     "summary": {"ru": "Закон распределения, поиск k, E[X], D(X), функция распределения.",
                 "en": "Probability distribution, finding k, E[X], Var(X), the CDF.",
                 "kk": "Үлестірім заңы, k-ны табу, E[X], D(X), үлестірім функциясы."}},
]

TOPIC_BY_ID = {t["id"]: t for t in TOPICS}

# (русский, english, қазақша)
TERMS = {
    1: [("элементарный исход", "outcome", "элементар оқиға (нәтиже)"),
        ("пространство исходов", "sample space", "элементар оқиғалар кеңістігі"),
        ("событие", "event", "оқиға"),
        ("достоверное событие", "sure event", "ақиқат оқиға"),
        ("невозможное событие", "impossible event", "мүмкін емес оқиға"),
        ("противоположное событие", "complement", "қарама-қарсы оқиға"),
        ("равновозможные исходы", "equally likely outcomes", "тең мүмкіндікті нәтижелер")],
    2: [("перестановки", "permutations", "алмастырулар"),
        ("размещения", "arrangements", "орналастырулар"),
        ("сочетания", "combinations", "терулер"),
        ("факториал", "factorial", "факториал"),
        ("без возвращения", "without replacement", "қайтарусыз"),
        ("с возвращением", "with replacement", "қайтарумен")],
    3: [("объединение", "union", "бірігу (қосынды)"),
        ("пересечение", "intersection", "қиылысу (көбейтінді)"),
        ("несовместные события", "mutually exclusive events", "үйлесімсіз оқиғалар"),
        ("теорема сложения", "addition rule", "қосу теоремасы"),
        ("законы де Моргана", "De Morgan's laws", "де Морган заңдары"),
        ("ровно одно", "exactly one", "тек біреуі ғана"),
        ("хотя бы одно", "at least one", "ең болмағанда біреуі")],
    4: [("условная вероятность", "conditional probability", "шартты ықтималдық"),
        ("при условии", "given", "шарты бойынша"),
        ("теорема умножения", "multiplication rule", "көбейту теоремасы"),
        ("сужение пространства", "reduced sample space", "кеңістіктің тарылуы")],
    5: [("независимые события", "independent events", "тәуелсіз оқиғалар"),
        ("попарно независимые", "pairwise independent", "қос-қостан тәуелсіз"),
        ("независимы в совокупности", "mutually independent", "жиынтықта тәуелсіз"),
        ("хотя бы один", "at least one", "ең болмағанда біреуі"),
        ("не более одного", "at most one", "біреуінен артық емес")],
    6: [("полная вероятность", "total probability", "толық ықтималдық"),
        ("гипотеза", "hypothesis", "гипотеза"),
        ("полная группа событий", "partition", "оқиғалардың толық тобы"),
        ("дерево вероятностей", "probability tree", "ықтималдықтар ағашы")],
    7: [("формула Байеса", "Bayes' theorem", "Байес формуласы"),
        ("априорная вероятность", "prior probability", "априорлық ықтималдық"),
        ("апостериорная вероятность", "posterior probability", "апостериорлық ықтималдық"),
        ("правдоподобие", "likelihood", "шындыққа ұқсастық (likelihood)"),
        ("ложноположительный", "false positive", "жалған оң нәтиже")],
    8: [("случайная величина", "random variable", "кездейсоқ шама"),
        ("закон распределения", "probability distribution", "үлестірім заңы"),
        ("математическое ожидание", "expected value / mean", "математикалық күтім"),
        ("дисперсия", "variance", "дисперсия"),
        ("среднеквадратичное отклонение", "standard deviation", "орташа квадраттық ауытқу"),
        ("функция распределения", "cumulative distribution function (CDF)", "үлестірім функциясы")],
}

ARMOR_NAMES = {
    "helmet": {"ru": "Шлем Исходов", "en": "Helm of Outcomes", "kk": "Нәтижелер дулығасы"},
    "chest": {"ru": "Кираса Комбинаторики", "en": "Cuirass of Combinatorics", "kk": "Комбинаторика сауыты"},
    "shoulders": {"ru": "Наплечники Объединения", "en": "Pauldrons of Union", "kk": "Бірігу иықшалары"},
    "gauntlets": {"ru": "Перчатки Условия", "en": "Gauntlets of Condition", "kk": "Шарт қолғаптары"},
    "belt": {"ru": "Пояс Независимости", "en": "Belt of Independence", "kk": "Тәуелсіздік белдігі"},
    "boots": {"ru": "Сапоги Полной Вероятности", "en": "Boots of Total Probability", "kk": "Толық ықтималдық етігі"},
    "shield": {"ru": "Щит Байеса", "en": "Shield of Bayes", "kk": "Байес қалқаны"},
    "sword": {"ru": "Меч Ожидания", "en": "Sword of Expectation", "kk": "Күтім семсері"},
}

_LESSONS = {"ru": _RU, "en": _EN, "kk": _KK}


def lesson(tid, lg):
    return _LESSONS.get(lg, _RU)[tid]


def title(t, lg):
    return t["title"].get(lg, t["title"]["ru"])


def summary(t, lg):
    return t["summary"].get(lg, t["summary"]["ru"])


def armor_name(piece, lg):
    return ARMOR_NAMES[piece].get(lg, ARMOR_NAMES[piece]["ru"])
