"""Lessons in English. The ("terms",) block inserts the shared glossary."""

LESSONS = {
    1: [
        ("md", "A **random experiment** is a trial whose result is not known in advance: rolling a die, drawing a card, "
               "tossing a coin. Each possible result is an **outcome**. The set of all outcomes is the "
               "**sample space** $\\Omega$."),
        ("md", "An **event** is any subset of $\\Omega$. For example, for one die roll "
               "$\\Omega=\\{1,2,3,4,5,6\\}$, and the event \"an even number\" is $A=\\{2,4,6\\}$."),
        ("md", "If all outcomes are **equally likely**, the classical definition applies:"),
        ("latex", r"P(A)=\frac{m}{n}=\frac{\text{number of favourable outcomes}}{\text{number of all outcomes}}"),
        ("md", "Properties to remember at all times:"),
        ("latex", r"0\le P(A)\le 1,\qquad P(\Omega)=1,\qquad P(\varnothing)=0,\qquad P(\bar A)=1-P(A)"),
        ("terms",),
        ("example", "Two dice: the sum equals 3",
         "Sample space: all pairs $(i,j)$, $n=6\\cdot6=36$. A sum of 3 comes from $(1,2)$ and $(2,1)$, so $m=2$.\n\n"
         "$P=\\frac{2}{36}=\\frac{1}{18}$."),
        ("tip", "For two dice, draw a 6×6 table and count cells. "
                "The sum $s$ appears $6-|s-7|$ times; 7 is the most frequent sum (6 times)."),
        ("warn", "The outcomes \"sum = 2\", \"sum = 3\", …, \"sum = 12\" are **not equally likely**! "
                 "You cannot say each sum has probability $\\frac{1}{11}$."),
    ],
    2: [
        ("md", "When there are many outcomes, we do not list them — we **count them with formulas**. "
               "The key questions: **does order matter** and **are repetitions allowed**?"),
        ("md", "**Rule of product**: if the first action can be done in $a$ ways and the second in $b$ ways, "
               "both together can be done in $a\\cdot b$ ways."),
        ("md", "**Permutations** — order all $n$ objects:"),
        ("latex", r"P_n=n!=1\cdot2\cdot\ldots\cdot n"),
        ("md", "**Arrangements (k-permutations)** — choose $k$ of $n$, **order matters**:"),
        ("latex", r"A_n^k=\frac{n!}{(n-k)!}"),
        ("md", "**Combinations** — choose $k$ of $n$, **order does not matter**:"),
        ("latex", r"C_n^k=\binom{n}{k}=\frac{n!}{k!\,(n-k)!}"),
        ("md", "With repetition: $\\bar A_n^k=n^k$ (a combination lock), $\\bar C_n^k=C_{n+k-1}^k$."),
        ("md", "**Hypergeometric scheme** — from $N$ items, $K$ of which are \"good\", we take $n$ without replacement. "
               "The probability of getting exactly $k$ good items:"),
        ("latex", r"P=\frac{C_K^k\cdot C_{N-K}^{n-k}}{C_N^n}"),
        ("terms",),
        ("example", "Two cards: a queen and a king of opposite colours (problem 14 OR)",
         "We draw 2 cards out of 52 without replacement. Number of pairs: $C_{52}^2=1326$.\n\n"
         "Favourable: (red queen, black king) — $2\\cdot2=4$ pairs; (black queen, red king) — 4 more. "
         "Total $m=8$.\n\n$P=\\frac{8}{1326}=\\frac{4}{663}$."),
        ("tip", "Check yourself a second way: $P(\\text{two aces})=\\frac{C_4^2}{C_{52}^2}=\\frac{4}{52}\\cdot\\frac{3}{51}$."),
        ("warn", "A common mistake is using $A_n^k$ when order does not matter (e.g. choosing a committee). "
                 "The answer becomes $k!$ times too large."),
    ],
    3: [
        ("md", "Events are sets, so we work with them like sets (Venn diagrams):"),
        ("md", "- $A\\cup B$ — **union**: at least one of the events happened (\"A or B\")\n"
               "- $A\\cap B$ (or $AB$) — **intersection**: both happened (\"A and B\")\n"
               "- $\\bar A$ (or $A'$) — **complement**: A did not happen\n"
               "- $A\\setminus B$ — **difference**: A happened but B did not"),
        ("md", "**Mutually exclusive** events cannot happen at the same time: $A\\cap B=\\varnothing$, "
               "so $P(A\\cap B)=0$."),
        ("md", "**Addition rule**:"),
        ("latex", r"P(A\cup B)=P(A)+P(B)-P(A\cap B)"),
        ("md", "For mutually exclusive events simply $P(A\\cup B)=P(A)+P(B)$. For three events:"),
        ("latex", r"P(A\cup B\cup C)=\sum P(A)-\sum P(AB)+P(ABC)"),
        ("md", "**De Morgan's laws**:"),
        ("latex", r"\overline{A\cup B}=\bar A\cap\bar B,\qquad \overline{A\cap B}=\bar A\cup\bar B"),
        ("md", "Useful consequences:"),
        ("latex", r"P(\text{neither})=1-P(A\cup B),\qquad P(\text{exactly one})=P(A)+P(B)-2P(A\cap B)"),
        ("terms",),
        ("example", "Problem 12 of the test",
         "Given: $P(A\\cup B)=p$, $P(\\text{exactly one})=q$. Then $P(A\\cap B)=p-q$.\n\n"
         "$P(A')+P(B')=2-(P(A)+P(B))=2-(p+P(A\\cap B))=2-(p+p-q)=2-2p+q$. ∎"),
        ("tip", "Problem 11 of the test: \"P(not A or not B)\" $=P(\\bar A\\cup\\bar B)=1-P(A\\cap B)$ — De Morgan. "
                "Hence $P(A\\cap B)=\\frac34$, while $P(A)P(B)=\\frac{7}{24}$ → not independent. "
                "Note: $\\frac34>P(A)=\\frac12$, so the data in this (well-known textbook) problem are inconsistent — "
                "but the expected answer is \"not independent\"."),
        ("warn", "Mutually exclusive ≠ independent! If $P(A),P(B)>0$ and the events are mutually exclusive, "
                 "they are in fact **dependent**."),
    ],
    4: [
        ("md", "**Conditional probability** $P(A\\mid B)$ is the probability of A **given that** B has already happened. "
               "The sample space \"shrinks\" to B:"),
        ("latex", r"P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0"),
        ("md", "This gives the **multiplication rule**:"),
        ("latex", r"P(A\cap B)=P(B)\,P(A\mid B)=P(A)\,P(B\mid A)"),
        ("md", "For a chain of events (e.g. cards without replacement):"),
        ("latex", r"P(A_1A_2A_3)=P(A_1)\,P(A_2\mid A_1)\,P(A_3\mid A_1A_2)"),
        ("md", "All usual rules work for conditional probability, e.g. $P(\\bar A\\mid B)=1-P(A\\mid B)$."),
        ("terms",),
        ("example", "Problem 4 of the test: two dice, sum < 6",
         "Condition B: the sum is less than 6. Pairs: sum 2 — 1, sum 3 — 2, sum 4 — 3, sum 5 — 4. Total 10.\n\n"
         "Of these, sum 3 — 2 pairs. $P(\\text{sum}=3\\mid B)=\\frac{2}{10}=\\frac15$."),
        ("example", "Problem 1 of the test: find P(A'|B')",
         "$P(A)=0.6$, $P(B)=0.2$, $P(A\\mid B)=0.5$.\n\n"
         "1) $P(A\\cap B)=0.5\\cdot0.2=0.1$\n\n"
         "2) $P(A'\\cap B')=1-P(A\\cup B)=1-(0.6+0.2-0.1)=0.3$\n\n"
         "3) $P(A'\\mid B')=\\frac{0.3}{0.8}=\\frac38$ → answer (c)."),
        ("example", "Problem 16: a family with two children",
         "Outcomes BB, BG, GB, GG. (i) \"the youngest is a girl\": BG, GG → $P(GG)=\\frac12$. "
         "(ii) \"at least one is a girl\": BG, GB, GG → $P(GG)=\\frac13$."),
        ("warn", "$P(A\\mid B)\\ne P(B\\mid A)$! Always divide by the probability of the **condition** "
                 "(what stands after the bar)."),
    ],
    5: [
        ("md", "Events are **independent** if one happening does not change the probability of the other: "
               "$P(A\\mid B)=P(A)$. The equivalent definition (the one checked in problems):"),
        ("latex", r"P(A\cap B)=P(A)\,P(B)"),
        ("md", "If A and B are independent, so are the pairs $(\\bar A,B)$, $(A,\\bar B)$, $(\\bar A,\\bar B)$."),
        ("md", "**Mutual independence** of three events requires **all four** equalities:"),
        ("latex", r"P(AB)=P(A)P(B),\; P(AC)=P(A)P(C),\; P(BC)=P(B)P(C),\; P(ABC)=P(A)P(B)P(C)"),
        ("md", "Pairwise independence alone (the first three) is **not enough**."),
        ("md", "**\"At least one\"** — via the complement \"none\":"),
        ("latex", r"P(\text{at least one})=1-(1-p_1)(1-p_2)\cdots(1-p_n)"),
        ("terms",),
        ("example", "Problem 7: three shooters 0.2, 0.3, 0.5",
         "$P(\\text{hit})=1-0.8\\cdot0.7\\cdot0.5=1-0.28=0.72$ → answer (c)."),
        ("example", "Problem 20 (ii): \"at most one solves\", p = 1/3, 1/4, 1/5, 2/3",
         "$q_i=1-p_i$: $\\frac23,\\frac34,\\frac45,\\frac13$. Nobody: $\\prod q_i=\\frac{2}{15}$.\n\n"
         "Exactly one: $\\sum p_i\\prod_{j\\ne i}q_j=\\frac{1}{15}+\\frac{2}{45}+\\frac{1}{30}+\\frac{4}{15}=\\frac{37}{90}$.\n\n"
         "At most one: $\\frac{2}{15}+\\frac{37}{90}=\\frac{49}{90}$."),
        ("warn", "Independent ≠ mutually exclusive. For independent events $P(A\\cap B)=P(A)P(B)>0$, "
                 "for mutually exclusive ones $P(A\\cap B)=0$."),
    ],
    6: [
        ("md", "Let $H_1,\\ldots,H_n$ be a **partition** (complete set of hypotheses): they are pairwise mutually exclusive "
               "and together make up all of $\\Omega$ ($\\sum P(H_i)=1$). Then for any event A:"),
        ("latex", r"P(A)=\sum_{i=1}^{n}P(H_i)\,P(A\mid H_i)"),
        ("md", "It helps to draw a **probability tree**: the first level is the hypotheses, the second is event A. "
               "The probability of a path is the product along the branch; the total is the sum of paths leading to A."),
        ("terms",),
        ("example", "Problem 8: two bags",
         "Bag A: 3 red, 5 black; bag B: 2 red, 4 black; a bag is chosen at random.\n\n"
         "$P(R)=\\frac12\\cdot\\frac38+\\frac12\\cdot\\frac26=\\frac{3}{16}+\\frac16=\\frac{17}{48}$ → answer (b)."),
        ("example", "Problem 15: coins, find n",
         "There are $2n+1$ coins: $n$ double-headed and $n+1$ fair.\n\n"
         "$P(H)=\\frac{n}{2n+1}\\cdot1+\\frac{n+1}{2n+1}\\cdot\\frac12=\\frac{3n+1}{2(2n+1)}=\\frac{31}{42}$\n\n"
         "$42(3n+1)=62(2n+1)\\Rightarrow126n+42=124n+62\\Rightarrow n=10$."),
        ("tip", "Check: the probabilities of the hypotheses must add up to 1. If not, a hypothesis is missing."),
    ],
    7: [
        ("md", "The law of total probability goes \"forward\": from causes to the effect. **Bayes' theorem** goes "
               "\"backward\": event A **has already happened** — what is the probability that hypothesis $H_k$ was the cause?"),
        ("latex", r"P(H_k\mid A)=\frac{P(H_k)\,P(A\mid H_k)}{\sum_i P(H_i)\,P(A\mid H_i)}"),
        ("md", "- $P(H_k)$ — **prior** probability, before the experiment\n"
               "- $P(H_k\\mid A)$ — **posterior** probability, after the experiment\n"
               "- $P(A\\mid H_k)$ — **likelihood**\n"
               "- the denominator is the total probability $P(A)$"),
        ("md", "The posterior probabilities also add up to 1."),
        ("terms",),
        ("example", "Problem 19: knows, guesses or copies",
         "$P(\\text{guess})=\\frac13$, $P(\\text{copy})=\\frac16$, so $P(\\text{knows})=1-\\frac13-\\frac16=\\frac12$.\n\n"
         "$P(\\text{correct})=\\frac12\\cdot1+\\frac13\\cdot\\frac18+\\frac16\\cdot\\frac14=\\frac12+\\frac1{24}+\\frac1{24}=\\frac{7}{12}$.\n\n"
         "$P(\\text{knows}\\mid\\text{correct})=\\frac{1/2}{7/12}=\\frac67$."),
        ("example", "Problem 18: the lost card",
         "Hypotheses: the lost card is a spade ($\\frac14$) or not a spade ($\\frac34$). Then 3 spades are drawn from 51.\n\n"
         "$P(A\\mid H_1)=\\frac{C_{12}^3}{C_{51}^3}$, $P(A\\mid H_2)=\\frac{C_{13}^3}{C_{51}^3}$.\n\n"
         "$P(H_1\\mid A)=\\frac{\\frac14 C_{12}^3}{\\frac14C_{12}^3+\\frac34C_{13}^3}=\\frac{220}{220+858}=\\frac{10}{49}$."),
        ("warn", "Rare events and tests: even an accurate test for a rare disease gives many false \"+\". "
                 "Do not confuse $P(+\\mid\\text{ill})$ with $P(\\text{ill}\\mid +)$!"),
    ],
    8: [
        ("md", "A **random variable** X is a number that depends on the outcome of an experiment. "
               "A **discrete** one takes separate values $x_1,x_2,\\ldots$"),
        ("md", "The **probability distribution (PMF)** is a table of values and their probabilities. The main condition:"),
        ("latex", r"p_i\ge0,\qquad \sum_i p_i=1"),
        ("md", "This condition is used to find an unknown parameter $k$ (problems 5 and 17 of the test)."),
        ("md", "**Expected value (mean)** and **variance**:"),
        ("latex", r"E[X]=\sum_i x_i p_i,\qquad \operatorname{Var}(X)=E[X^2]-(E[X])^2,\qquad \sigma=\sqrt{\operatorname{Var}(X)}"),
        ("md", "The **cumulative distribution function (CDF)**: $F(x)=P(X\\le x)$ — the running sum of probabilities."),
        ("terms",),
        ("example", "Problem 5: find k",
         "$\\frac{5}{k}+\\frac{7}{k}+\\frac{9}{k}+\\frac{11}{k}=\\frac{32}{k}=1\\Rightarrow k=32$ → answer (c)."),
        ("example", "Problem 17: P(X) = k, 2k, 3k",
         "$k+2k+3k=6k=1\\Rightarrow k=\\frac16$. $P(X<2)=k+2k=\\frac12$, $P(X\\le2)=1$, $P(X\\ge2)=3k=\\frac12$."),
        ("example", "Problem 18 OR: the larger of two numbers from 1…6",
         "There are $C_6^2=15$ pairs. $X=k$ exactly when the other number is less than $k$: $k-1$ options. "
         "$P(X=k)=\\frac{k-1}{15}$, $k=2..6$.\n\n"
         "$E[X]=\\frac{2\\cdot1+3\\cdot2+4\\cdot3+5\\cdot4+6\\cdot5}{15}=\\frac{70}{15}=\\frac{14}{3}$."),
        ("warn", "$P(X<a)$ and $P(X\\le a)$ differ by $P(X=a)$ — this matters for discrete variables!"),
    ],
}
