"""Финальная проектная работа, которая выдаётся после победы над Боссом."""

_RU = r"""
# 📜 Проектная работа «Вероятностная лаборатория»
### Probability Lab: theory vs. simulation

**Цель (goal):** показать, что формулы теории вероятностей работают на практике. Для каждой задачи вы
сначала решаете её **аналитически** (analytical solution), а затем проверяете ответ **методом Монте-Карло**
(Monte Carlo simulation) на Python и сравниваете результаты.

---

## Часть 1. Теоретический обзор (theoretical review) — 25 баллов
Кратко (1–2 страницы) изложите своими словами, с формулами и примерами:
1. Классическое определение вероятности и комбинаторику (permutations, arrangements, combinations).
2. Теорему сложения и законы де Моргана.
3. Условную вероятность и теорему умножения.
4. Независимость событий: попарная и в совокупности (pairwise vs. mutual independence).
5. Формулу полной вероятности и формулу Байеса (prior → posterior).
6. Дискретную случайную величину: закон распределения, $E[X]$, $D(X)$.

> Для каждого термина дайте английский эквивалент в скобках.

## Часть 2. Аналитика + симуляция (analysis + simulation) — 45 баллов
Для **каждой** задачи: (а) аналитическое решение с шагами; (б) симуляция на Python с $N=100\,000$ повторений;
(в) таблица «теория / симуляция / разница»; (г) график сходимости частоты к вероятности при росте $N$.

| № | Задача | Теоретический ответ, который нужно получить |
|---|--------|---------------------------------------------|
| 1 | Три стрелка: 0.2, 0.3, 0.5. P(мишень поражена) | $0.72$ |
| 2 | Мешки A (3К, 5Ч) и B (2К, 4Ч). P(красный) и P(мешок A ∣ красный) | $\frac{17}{48}$ и $\frac{9}{17}$ |
| 3 | Два кубика: P(сумма = 3 ∣ сумма < 6) | $\frac15$ |
| 4 | Потерянная карта: P(пика ∣ вынуты 3 пики) | $\frac{10}{49}$ |
| 5 | Большее из двух чисел 1…6: закон распределения и $E[X]$ | $P(X=k)=\frac{k-1}{15}$, $E[X]=\frac{14}{3}$ |
| 6 | Монеты: $2n+1$ монет, $n$ двусторонних, P(орёл) = 31/42. Найти n и проверить симуляцией | $n=10$ |

Подсказка для симуляции (simulation hint):
```python
import numpy as np
rng = np.random.default_rng(42)
N = 100_000
hits = (rng.random((N, 3)) < [0.2, 0.3, 0.5]).any(axis=1)
print(hits.mean())   # ≈ 0.72
```

## Часть 3. Собственное исследование (own case study) — 20 баллов
Придумайте **свою** жизненную задачу на формулу Байеса (например: спам-фильтр, медицинский тест,
опоздание на пару из-за пробок в Алматы). Опишите гипотезы, априорные вероятности, правдоподобия;
посчитайте апостериорные вероятности и покажите, как они меняются, если изменить априорную вероятность
(график posterior vs. prior).

## Часть 4. Выводы (conclusions) — 10 баллов
- Насколько близки результаты симуляции к теории? Почему они не совпадают точно?
- Как разница зависит от $N$ (закон больших чисел, law of large numbers)?
- Какая тема курса показалась самой сложной и почему?

---

### Требования к оформлению
- Код: Python 3 (numpy, pandas, matplotlib), один Jupyter Notebook или `.py`-скрипты.
- Отчёт: 6–10 страниц, PDF или DOCX; формулы, таблицы, графики подписаны.
- Презентация: 5–7 слайдов для защиты (5 минут).

### Критерии оценки (rubric)
| Критерий | Баллы |
|----------|-------|
| Корректность аналитических решений | 30 |
| Корректность и читаемость кода симуляций | 25 |
| Графики и таблицы сравнения | 15 |
| Собственная задача на Байеса | 15 |
| Выводы и оформление | 15 |
| **Итого** | **100** |
"""

_EN = r"""
# 📜 Course project "Probability Lab"
### Theory vs. simulation

**Goal:** show that the formulas of probability theory work in practice. For every problem, first solve it
**analytically**, then check the answer with a **Monte Carlo simulation** in Python and compare the results.

---

## Part 1. Theoretical review — 25 points
Briefly (1–2 pages), in your own words, with formulas and examples, describe:
1. The classical definition of probability and combinatorics (permutations, arrangements, combinations).
2. The addition rule and De Morgan's laws.
3. Conditional probability and the multiplication rule.
4. Independence of events: pairwise vs. mutual independence.
5. The law of total probability and Bayes' theorem (prior → posterior).
6. Discrete random variables: the distribution, $E[X]$, $\operatorname{Var}(X)$.

## Part 2. Analysis + simulation — 45 points
For **each** problem: (a) an analytical solution with steps; (b) a Python simulation with $N=100\,000$ repetitions;
(c) a "theory / simulation / difference" table; (d) a plot of the relative frequency converging to the probability as $N$ grows.

| # | Problem | Theoretical answer to obtain |
|---|---------|------------------------------|
| 1 | Three shooters: 0.2, 0.3, 0.5. P(target is hit) | $0.72$ |
| 2 | Bags A (3R, 5B) and B (2R, 4B). P(red) and P(bag A ∣ red) | $\frac{17}{48}$ and $\frac{9}{17}$ |
| 3 | Two dice: P(sum = 3 ∣ sum < 6) | $\frac15$ |
| 4 | Lost card: P(spade ∣ 3 spades drawn) | $\frac{10}{49}$ |
| 5 | The larger of two numbers from 1…6: distribution and $E[X]$ | $P(X=k)=\frac{k-1}{15}$, $E[X]=\frac{14}{3}$ |
| 6 | Coins: $2n+1$ coins, $n$ double-headed, P(heads) = 31/42. Find n and verify by simulation | $n=10$ |

Simulation hint:
```python
import numpy as np
rng = np.random.default_rng(42)
N = 100_000
hits = (rng.random((N, 3)) < [0.2, 0.3, 0.5]).any(axis=1)
print(hits.mean())   # ≈ 0.72
```

## Part 3. Own case study — 20 points
Invent **your own** real-life Bayes problem (e.g. a spam filter, a medical test, being late for class because of
Almaty traffic). Describe the hypotheses, priors and likelihoods; compute the posteriors and show how they change
when the prior changes (a posterior vs. prior plot).

## Part 4. Conclusions — 10 points
- How close are the simulation results to theory? Why are they not exactly equal?
- How does the difference depend on $N$ (law of large numbers)?
- Which topic of the course was the hardest and why?

---

### Formatting requirements
- Code: Python 3 (numpy, pandas, matplotlib), one Jupyter Notebook or `.py` scripts.
- Report: 6–10 pages, PDF or DOCX; formulas, tables and plots with captions.
- Presentation: 5–7 slides for the defence (5 minutes).

### Rubric
| Criterion | Points |
|-----------|--------|
| Correct analytical solutions | 30 |
| Correct and readable simulation code | 25 |
| Comparison plots and tables | 15 |
| Own Bayes problem | 15 |
| Conclusions and formatting | 15 |
| **Total** | **100** |
"""

_KK = r"""
# 📜 Жобалық жұмыс «Ықтималдық зертханасы»
### Probability Lab: theory vs. simulation

**Мақсаты (goal):** ықтималдықтар теориясының формулалары іс жүзінде жұмыс істейтінін көрсету. Әр есепті алдымен
**аналитикалық** түрде (analytical solution) шешіп, содан кейін жауапты Python-да **Монте-Карло әдісімен**
(Monte Carlo simulation) тексеріп, нәтижелерді салыстырасыз.

---

## 1-бөлім. Теориялық шолу (theoretical review) — 25 ұпай
Қысқаша (1–2 бет), өз сөзіңізбен, формулалар мен мысалдар арқылы баяндаңыз:
1. Ықтималдықтың классикалық анықтамасы және комбинаторика (алмастырулар, орналастырулар, терулер).
2. Қосу теоремасы және де Морган заңдары.
3. Шартты ықтималдық және көбейту теоремасы.
4. Оқиғалардың тәуелсіздігі: қос-қостан және жиынтықта (pairwise vs. mutual independence).
5. Толық ықтималдық формуласы және Байес формуласы (prior → posterior).
6. Дискретті кездейсоқ шама: үлестірім заңы, $E[X]$, $D(X)$.

> Әр термин үшін ағылшынша баламасын жақшада беріңіз.

## 2-бөлім. Аналитика + симуляция (analysis + simulation) — 45 ұпай
**Әр** есеп үшін: (а) қадамдары бар аналитикалық шешім; (ә) $N=100\,000$ қайталаумен Python-дағы симуляция;
(б) «теория / симуляция / айырма» кестесі; (в) $N$ өскенде жиіліктің ықтималдыққа жинақталу графигі.

| № | Есеп | Алынуы тиіс теориялық жауап |
|---|------|-----------------------------|
| 1 | Үш атқыш: 0.2, 0.3, 0.5. P(нысанаға тиді) | $0.72$ |
| 2 | A (3Қз, 5Қр) және B (2Қз, 4Қр) қаптары. P(қызыл) және P(A қабы ∣ қызыл) | $\frac{17}{48}$ және $\frac{9}{17}$ |
| 3 | Екі ойын сүйегі: P(қосынды = 3 ∣ қосынды < 6) | $\frac15$ |
| 4 | Жоғалған карта: P(қарға ♠ ∣ 3 қарға алынды) | $\frac{10}{49}$ |
| 5 | 1…6 сандарынан екі санның үлкені: үлестірім заңы және $E[X]$ | $P(X=k)=\frac{k-1}{15}$, $E[X]=\frac{14}{3}$ |
| 6 | Тиындар: $2n+1$ тиын, $n$-і екі жағы да елтаңба, P(елтаңба) = 31/42. n-ді тауып, симуляциямен тексеру | $n=10$ |

Симуляцияға кеңес (simulation hint):
```python
import numpy as np
rng = np.random.default_rng(42)
N = 100_000
hits = (rng.random((N, 3)) < [0.2, 0.3, 0.5]).any(axis=1)
print(hits.mean())   # ≈ 0.72
```

## 3-бөлім. Өз зерттеуіңіз (own case study) — 20 ұпай
Байес формуласына **өз** өмірлік есебіңізді ойлап табыңыз (мысалы: спам-сүзгі, медициналық тест,
Алматыдағы кептелістен сабаққа кешігу). Гипотезаларды, априорлық ықтималдықтарды, шындыққа ұқсастықтарды сипаттаңыз;
апостериорлық ықтималдықтарды есептеп, априорлық ықтималдық өзгергенде олардың қалай өзгеретінін көрсетіңіз
(posterior vs. prior графигі).

## 4-бөлім. Қорытынды (conclusions) — 10 ұпай
- Симуляция нәтижелері теорияға қаншалықты жақын? Неліктен дәл сәйкес келмейді?
- Айырма $N$-ге қалай тәуелді (үлкен сандар заңы, law of large numbers)?
- Курстың қай тақырыбы ең қиын болды және неге?

---

### Рәсімдеу талаптары
- Код: Python 3 (numpy, pandas, matplotlib), бір Jupyter Notebook немесе `.py` скрипттер.
- Есеп: 6–10 бет, PDF немесе DOCX; формулалар, кестелер, графиктер қол қойылған.
- Презентация: қорғауға 5–7 слайд (5 минут).

### Бағалау критерийлері (rubric)
| Критерий | Ұпай |
|----------|------|
| Аналитикалық шешімдердің дұрыстығы | 30 |
| Симуляция кодының дұрыстығы мен оқылуы | 25 |
| Салыстыру графиктері мен кестелері | 15 |
| Байес бойынша өз есебі | 15 |
| Қорытынды және рәсімдеу | 15 |
| **Барлығы** | **100** |
"""

PROJECT_MD = {"ru": _RU, "en": _EN, "kk": _KK}
