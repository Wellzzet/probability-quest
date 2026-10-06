"""Финальный Босс: задачи из пробного теста (Section A, 1–10), на трёх языках."""

AR_OPTS = {
    "ru": ["(a) A и R верны, R — правильное объяснение A", "(b) A и R верны, но R не объясняет A",
           "(c) A верно, R ложно", "(d) A ложно, R верно"],
    "en": ["(a) Both A and R are true, and R correctly explains A", "(b) Both A and R are true, but R does not explain A",
           "(c) A is true, R is false", "(d) A is false, R is true"],
    "kk": ["(a) A мен R дұрыс, R — A-ның дұрыс түсіндірмесі", "(b) A мен R дұрыс, бірақ R A-ны түсіндірмейді",
           "(c) A дұрыс, R жалған", "(d) A жалған, R дұрыс"],
}

_Q = [
    {
        "q": {"ru": r"$P(A)=0.6$, $P(B)=0.2$, $P(A\mid B)=0.5$. Тогда $P(A'\mid B')$ равно",
              "en": r"$P(A)=0.6$, $P(B)=0.2$, $P(A\mid B)=0.5$. Then $P(A'\mid B')$ equals",
              "kk": r"$P(A)=0.6$, $P(B)=0.2$, $P(A\mid B)=0.5$. Онда $P(A'\mid B')$ тең"},
        "opts": ["(a) 1/10", "(b) 3/10", "(c) 3/8", "(d) 6/7"], "ans": 2,
        "expl": r"$P(AB)=0.1$; $P(A'B')=1-(0.6+0.2-0.1)=0.3$; $P(A'\mid B')=\frac{0.3}{0.8}=\frac38$.",
    },
    {
        "q": {"ru": r"A и B независимы, $P(A)=p$, $P(B)=q$, $P(\text{ровно одно из } A,B)=\frac23$. Найдите $3p+3q-6pq$.",
              "en": r"A and B are independent, $P(A)=p$, $P(B)=q$, $P(\text{exactly one of } A,B)=\frac23$. Find $3p+3q-6pq$.",
              "kk": r"A мен B тәуелсіз, $P(A)=p$, $P(B)=q$, $P(A,B\text{ тек біреуі})=\frac23$. $3p+3q-6pq$ табыңыз."},
        "opts": ["(a) 2", "(b) −2", "(c) 4", "(d) −4"], "ans": 0,
        "expl": r"$p(1-q)+q(1-p)=p+q-2pq=\frac23$ $\Rightarrow$ $3p+3q-6pq=2$.",
    },
    {
        "q": {"ru": r"$P(A\cap B)=70\%$, $P(B)=85\%$. Тогда $P(A\mid B)$ равно",
              "en": r"$P(A\cap B)=70\%$, $P(B)=85\%$. Then $P(A\mid B)$ equals",
              "kk": r"$P(A\cap B)=70\%$, $P(B)=85\%$. Онда $P(A\mid B)$ тең"},
        "opts": ["(a) 14/17", "(b) 17/20", "(c) 7/8", "(d) 1/8"], "ans": 0,
        "expl": r"$\frac{0.70}{0.85}=\frac{70}{85}=\frac{14}{17}$.",
    },
    {
        "q": {"ru": "Бросают два кубика. Известно, что сумма меньше 6. Вероятность, что сумма равна 3:",
              "en": "Two dice are thrown. The sum is known to be less than 6. The probability that the sum is 3:",
              "kk": "Екі ойын сүйегі лақтырылады. Қосынды 6-дан кіші екені белгілі. Қосындының 3 болу ықтималдығы:"},
        "opts": ["(a) 1/18", "(b) 5/18", "(c) 1/5", "(d) 2/5"], "ans": 2,
        "expl": r"1+2+3+4 = 10; $\frac{2}{10}=\frac15$.",
    },
    {
        "q": {"ru": "Закон распределения: X = 2, 3, 4, 5; P = 5/k, 7/k, 9/k, 11/k. Найдите k.",
              "en": "Distribution: X = 2, 3, 4, 5; P = 5/k, 7/k, 9/k, 11/k. Find k.",
              "kk": "Үлестірім заңы: X = 2, 3, 4, 5; P = 5/k, 7/k, 9/k, 11/k. k-ны табыңыз."},
        "opts": ["(a) 8", "(b) 16", "(c) 32", "(d) 48"], "ans": 2,
        "expl": r"$\frac{5+7+9+11}{k}=\frac{32}{k}=1\Rightarrow k=32$.",
    },
    {
        "q": {"ru": r"Вероятности, что A, B и C решат задачу: $\frac12,\frac13,\frac14$. Вероятность, что задача будет решена:",
              "en": r"The probabilities of A, B and C solving a problem are $\frac12,\frac13,\frac14$. The probability that it is solved:",
              "kk": r"A, B және C есепті шығару ықтималдықтары: $\frac12,\frac13,\frac14$. Есептің шығарылу ықтималдығы:"},
        "opts": {"ru": ["(a) 1/2", "(b) 3/4", "(c) 1/4", "(d) ни один из вариантов"],
                 "en": ["(a) 1/2", "(b) 3/4", "(c) 1/4", "(d) none of these"],
                 "kk": ["(a) 1/2", "(b) 3/4", "(c) 1/4", "(d) ешқайсысы емес"]}, "ans": 1,
        "expl": r"$1-\frac12\cdot\frac23\cdot\frac34=1-\frac14=\frac34$.",
    },
    {
        "q": {"ru": "A, B и C стреляют по мишени с вероятностями попадания 0.2, 0.3 и 0.5. Вероятность, что мишень поражена:",
              "en": "A, B and C fire at a target with hit probabilities 0.2, 0.3 and 0.5. The probability that the target is hit:",
              "kk": "A, B және C нысанаға 0.2, 0.3 және 0.5 тигізу ықтималдықтарымен атады. Нысанаға тию ықтималдығы:"},
        "opts": ["(a) 0.993", "(b) 0.94", "(c) 0.72", "(d) 0.90"], "ans": 2,
        "expl": r"$1-0.8\cdot0.7\cdot0.5=1-0.28=0.72$.",
    },
    {
        "q": {"ru": "Мешок A: 3 красных и 5 чёрных; мешок B: 2 красных и 4 чёрных. Шар достают из случайного мешка. P(красный) =",
              "en": "Bag A: 3 red and 5 black; bag B: 2 red and 4 black. A ball is drawn from a random bag. P(red) =",
              "kk": "A қабы: 3 қызыл және 5 қара; B қабы: 2 қызыл және 4 қара. Кездейсоқ қаптан шар алынады. P(қызыл) ="},
        "opts": ["(a) 17/24", "(b) 17/48", "(c) 3/8", "(d) 1/3"], "ans": 1,
        "expl": r"$\frac12\cdot\frac38+\frac12\cdot\frac26=\frac{3}{16}+\frac16=\frac{17}{48}$.",
    },
    {
        "q": {"ru": ("**Assertion (A):** бросают три кубика; E — «сумма не меньше 5», F — «на всех трёх одно и то же число», "
                     "G — «сумма равна 15». Тогда E, F, G независимы в совокупности.\n\n"
                     "**Reason (R):** три события независимы в совокупности, если выполнены все четыре равенства "
                     r"$P(AB)=P(A)P(B)$, $P(AC)=P(A)P(C)$, $P(BC)=P(B)P(C)$, $P(ABC)=P(A)P(B)P(C)$."),
              "en": ("**Assertion (A):** three dice are rolled; E — \"the total is at least 5\", F — \"the same number on all three\", "
                     "G — \"the total is 15\". Then E, F, G are mutually independent.\n\n"
                     "**Reason (R):** three events are mutually independent if all four equalities hold: "
                     r"$P(AB)=P(A)P(B)$, $P(AC)=P(A)P(C)$, $P(BC)=P(B)P(C)$, $P(ABC)=P(A)P(B)P(C)$."),
              "kk": ("**Assertion (A):** үш ойын сүйегі лақтырылады; E — «қосынды кемінде 5», F — «үшеуінде де бірдей сан», "
                     "G — «қосынды 15». Онда E, F, G жиынтықта тәуелсіз.\n\n"
                     "**Reason (R):** үш оқиға жиынтықта тәуелсіз, егер төрт теңдіктің бәрі орындалса: "
                     r"$P(AB)=P(A)P(B)$, $P(AC)=P(A)P(C)$, $P(BC)=P(B)P(C)$, $P(ABC)=P(A)P(B)P(C)$.")},
        "opts": "AR", "ans": 3,
        "expl": {"ru": r"$P(E)=\frac{212}{216}$, $P(F)=\frac{6}{216}$, $P(E\cap F)=\frac{5}{216}\ne P(E)P(F)$ → A ложно; R — верное определение. Ответ (d).",
                 "en": r"$P(E)=\frac{212}{216}$, $P(F)=\frac{6}{216}$, $P(E\cap F)=\frac{5}{216}\ne P(E)P(F)$ → A is false; R is the correct definition. Answer (d).",
                 "kk": r"$P(E)=\frac{212}{216}$, $P(F)=\frac{6}{216}$, $P(E\cap F)=\frac{5}{216}\ne P(E)P(F)$ → A жалған; R — дұрыс анықтама. Жауабы (d)."},
    },
    {
        "q": {"ru": (r"**Assertion (A):** A и B несовместны, $P(\bar A)=\frac56$, $P(B)=\frac13$. Тогда $P(A\mid B)=\frac14$." "\n\n"
                     r"**Reason (R):** если $P(A)=0.2$, $P(B)=0.6$ и $P(A\mid B)=0.2$, то $P(A\mid\bar B)=0.2$."),
              "en": (r"**Assertion (A):** A and B are mutually exclusive, $P(\bar A)=\frac56$, $P(B)=\frac13$. Then $P(A\mid B)=\frac14$." "\n\n"
                     r"**Reason (R):** if $P(A)=0.2$, $P(B)=0.6$ and $P(A\mid B)=0.2$, then $P(A\mid\bar B)=0.2$."),
              "kk": (r"**Assertion (A):** A мен B үйлесімсіз, $P(\bar A)=\frac56$, $P(B)=\frac13$. Онда $P(A\mid B)=\frac14$." "\n\n"
                     r"**Reason (R):** егер $P(A)=0.2$, $P(B)=0.6$ және $P(A\mid B)=0.2$ болса, онда $P(A\mid\bar B)=0.2$.")},
        "opts": "AR", "ans": 3,
        "expl": {"ru": r"$P(A\cap B)=0$ → $P(A\mid B)=0\ne\frac14$: A ложно. В R $P(A\mid B)=P(A)$ → независимы → $P(A\mid\bar B)=0.2$: R верно. Ответ (d).",
                 "en": r"$P(A\cap B)=0$ → $P(A\mid B)=0\ne\frac14$: A is false. In R, $P(A\mid B)=P(A)$ → independent → $P(A\mid\bar B)=0.2$: R is true. Answer (d).",
                 "kk": r"$P(A\cap B)=0$ → $P(A\mid B)=0\ne\frac14$: A жалған. R-де $P(A\mid B)=P(A)$ → тәуелсіз → $P(A\mid\bar B)=0.2$: R дұрыс. Жауабы (d)."},
    },
]


def boss_questions(lg):
    out = []
    for q in _Q:
        expl = q["expl"][lg] if isinstance(q["expl"], dict) else q["expl"]
        if q["opts"] == "AR":
            opts = AR_OPTS[lg]
        elif isinstance(q["opts"], dict):
            opts = q["opts"][lg]
        else:
            opts = q["opts"]
        out.append({"q": q["q"][lg], "opts": opts, "ans": q["ans"], "expl": expl})
    return out


BOSS_COUNT = len(_Q)
