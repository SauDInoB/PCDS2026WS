# Python para Ciência de Dados em Saúde
### Winter School 2026 · Universidade do Porto

> Course materials for **Python para Ciência de Dados em Saúde**, part of the [Winter School 2026](https://winterschool.med.up.pt/cursos/python-para-ciencia-de-dados-em-saude/) programme at the Faculty of Medicine, University of Porto.

**🌐 Slides:** [saudinob.github.io/PCDS2026WS](https://saudinob.github.io/PCDS2026WS)

| Session | Direct link |
|---------|-------------|
| Day 1 · Session 1 — Config, Tools & Best Practices | [Open slides →](https://saudinob.github.io/PCDS2026WS/d1s1/session1.html) |

---

## 📅 Programme

| Day | Session | Time | Topic | Lead |
|-----|---------|------|-------|------|
| Day 1 · 02 Mar | Session 1 | 14h–16h | Configuration, Tools & Best Practices | TJ |
| Day 1 · 02 Mar | Session 2 | 16h15–18h | Variables, Data Types & Functions | Abel |
| Day 2 · 05 Mar | Session 3 | 14h–16h | Data Import & Statistics | DMD |
| Day 2 · 05 Mar | Session 4 | 16h15–17h | Data Visualisation | DMD |
| Day 2 · 05 Mar | Session 5 | 17h–18h | Interfaces | DMD |
| Day 3 · 06 Mar | Session 6 | 14h–16h | Regression Models | DMD |
| Day 3 · 06 Mar | Session 7 | 16h15–18h | AI (Ollama, Positron Data Assistant) | DMD / TJ |

---

## 📁 Repository Structure

```
PCDS2026WS/
├── d1s1/                 # Config, Tools & Best Practices (TJ)
├── Day 1 - Session 2/    # Variables, Data Types & Functions (Abel)
├── Day 2 - Session 3/    # Data Import & Statistics (DMD)
├── Day 2 - Session 4/    # Data Visualisation (DMD)
├── Day 2 - Session 5/    # Interfaces (DMD)
├── Day 3 - Session 6/    # Regression Models (DMD)
└── Day 3 - Session 7/    # AI (DMD / TJ)
```

---

## 🛠️ Setup

Before the first session, please install the following:

### Python
Download and install **Python 3.11 or 3.12** from [python.org/downloads](https://www.python.org/downloads).

> **Windows:** tick "Add Python to PATH" during installation.  
> **macOS:** alternatively install via [Homebrew](https://brew.sh): `brew install python`

Verify your installation:
```bash
python --version   # or python3 --version on macOS
```

### Positron
Download and install **Positron** from [positron.posit.co](https://positron.posit.co) — the IDE we'll use throughout the course.

### GitHub Desktop
Download and install **GitHub Desktop** from [desktop.github.com](https://desktop.github.com) and create a free account at [github.com](https://github.com).

---

## 📦 Required Libraries

```bash
pip install pandas numpy scipy matplotlib seaborn streamlit
```

> **Note:** do not put patient data or any identifiable health data in this (or any public) repository. Code only.

---

## 👥 Instructors

- **TJ** — Session 1, Session 7
- **Abel** — Session 2
- **DMD** — Sessions 3–7
