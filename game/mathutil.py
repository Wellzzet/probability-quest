"""Небольшие помощники: точные дроби, форматирование, варианты ответов."""
from fractions import Fraction as F
from math import comb, perm, factorial


def _is_finite_decimal(x: F, max_digits: int = 4) -> bool:
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if d != 1:
        return False
    return (x * 10 ** max_digits).denominator == 1


def fmt(x) -> str:
    """Красивый текст числа: 3, 0.72, 17/48 ≈ 0.354."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    if _is_finite_decimal(x):
        s = f"{float(x):.4f}".rstrip("0").rstrip(".")
        return s
    return f"{x.numerator}/{x.denominator} ≈ {float(x):.3f}".rstrip("0")


def tex(x) -> str:
    """То же число в LaTeX."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    if _is_finite_decimal(x):
        return f"{float(x):.4f}".rstrip("0").rstrip(".")
    sign = "-" if x < 0 else ""
    x = abs(x)
    return rf"{sign}\frac{{{x.numerator}}}{{{x.denominator}}}"


def tex_approx(x) -> str:
    x = F(x)
    t = tex(x)
    if x.denominator != 1 and not _is_finite_decimal(x):
        t += rf" \approx {float(x):.3f}"
    return t


def make_mcq(rng, question, correct, wrongs, explanation, kind="prob"):
    """Собирает вопрос с 4 вариантами: правильный + 3 правдоподобные ошибки."""
    correct = F(correct)
    opts = [correct]

    def ok(v):
        v = F(v)
        if v in opts:
            return False
        if kind == "prob" and not (0 <= v <= 1):
            return False
        if kind in ("int", "count") and (v.denominator != 1 or v < 0):
            return False
        return True

    for w in wrongs:
        if w is None:
            continue
        if len(opts) >= 4:
            break
        if ok(w):
            opts.append(F(w))

    tries = 0
    while len(opts) < 4 and tries < 200:
        tries += 1
        if kind in ("int", "count"):
            step = max(1, int(abs(correct) * F(rng.choice([1, 2, 3]), 10)))
            cand = correct + rng.choice([-1, 1]) * rng.randint(1, 3) * step
        elif kind == "prob":
            cand = correct + rng.choice([-1, 1]) * F(rng.randint(1, 6), 40)
            if rng.random() < 0.4 and correct != 0:
                cand = correct * rng.choice([F(1, 2), F(2, 3), F(3, 2), F(4, 3)])
        else:
            cand = correct + rng.choice([-1, 1]) * F(rng.randint(1, 8), 10)
        if ok(cand):
            opts.append(F(cand))

    rng.shuffle(opts)
    return {
        "q": question,
        "opts": [fmt(o) for o in opts],
        "ans": opts.index(correct),
        "expl": explanation,
    }


def text_mcq(rng, question, correct_text, wrong_texts, explanation, shuffle=True):
    opts = [correct_text] + [w for w in wrong_texts if w != correct_text][:3]
    if shuffle:
        rng.shuffle(opts)
    return {"q": question, "opts": opts, "ans": opts.index(correct_text), "expl": explanation}


__all__ = ["F", "comb", "perm", "factorial", "fmt", "tex", "tex_approx", "make_mcq", "text_mcq"]
