# 💰 Personal Expense Tracker (Python)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)

A beginner-friendly **command-line expense tracker** built with Python.  
This project helps users log, view, edit, and analyze daily expenses while practicing **file I/O, data validation, and version control**.

---

## 🌟 Features

- ➕ Add expenses with category and notes  
- 📜 View expense history with numbering  
- ✏️ Edit existing expense entries  
- 🗑️ Delete expenses safely  
- 📊 Monthly summary by category  
- 📤 Export expense history to CSV  
- 💾 All data stored locally for privacy  

---

## ⌨️ Menu Options

```text
1. Add expense
2. View expense history
3. View monthly summary
4. Export to CSV
5. Edit expense
6. Delete expense
7. Exit
````

---

## 🛠️ How It Works

* Expenses are saved in a plain text file (`expenses.txt`)
* Each entry follows this format:

```text
YYYY-MM-DD | Category | Amount | Note
```

* CSV exports are generated as `expenses.csv`

---

## ▶️ How to Run

1. Install **Python 3.10 or newer**
2. Clone the repository:

```bash
git clone https://github.com/your-username/expense-tracker.git
```

3. Navigate to the project folder:

```bash
cd expense-tracker
```

4. Run the program:

```bash
python expense_tracker.py
```

---

## 📊 Example Output

```text
📊 Monthly Summary
Month: 2026-01
Total spent: $123.45

By category:
- Food: $45.00
- Transport: $30.00
- Education: $48.45
```

---

## 📦 Data Storage

* `expenses.txt` — main data storage
* `expenses.csv` — optional export for analysis

---

## 🧭 Project Purpose

This project was built to practice:

* Python fundamentals
* File handling (read/write)
* Input validation
* Clean program structure
* Git & GitHub workflow

It demonstrates **progressive development** through milestone-based versions.

---

## 🕓 Version History

| Version  | Milestone     | Description                  |
| -------- | ------------- | ---------------------------- |
| **v1.0** | Basic logging | Add & view expenses          |
| **v1.1** | Validation    | Input validation for amounts |
| **v1.2** | Categories    | Category selection menu      |
| **v1.3** | Analytics     | Monthly summary by category  |
| **v1.4** | Export        | CSV export functionality     |
| **v1.5** | CRUD          | Edit & delete expenses       |

---

## 📜 Changelog

See detailed version changes in [CHANGELOG.md](CHANGELOG.md).

---

## 🚀 Future Improvements

* GUI version (Tkinter / CustomTkinter)
* Data visualization (charts)
* Monthly budget limits
* Search and filter by category/date

---

## 📄 License

This project is licensed under the **MIT License**.

---

✨ *Built as part of a learning journey in Python and software development.*

