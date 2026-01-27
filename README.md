# 💰 Personal Expense Tracker (Python)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![GUI](https://img.shields.io/badge/interface-Tkinter-success)
![License](https://img.shields.io/badge/license-MIT-green)

A **desktop-based expense tracker** built with **Python and Tkinter**, featuring expense management, theming, keyboard shortcuts, and CSV persistence.

This project evolved from a **command-line application (v1.x)** into a fully functional **GUI desktop app (v2.x)** to demonstrate technical growth and clean software iteration.

---

## ✨ Features (GUI – v2.x)

- ➕ Add, edit, and delete expenses
- 📖 Expense history view
- 📊 Category-based summary
- 🌗 Light / Dark mode support
- ⌨ Keyboard shortcuts (Ctrl+N, Ctrl+H, Esc, Enter, Alt+F4)
- 🪟 Modal dialogs (safe editing)
- 💾 Local CSV persistence
- 📤 Export expenses to CSV
- 🧼 Clean ttk-based UI

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Tkinter / ttk**
- CSV file storage
- No external dependencies

---

## ▶️ How to Run (GUI Version)

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
python expense_tracker_gui.py
````

---

## ⌨ Keyboard Shortcuts

| Shortcut | Action              |
| -------- | ------------------- |
| Ctrl + N | Add expense         |
| Ctrl + H | View history        |
| Ctrl + S | View summary        |
| Ctrl + D | Toggle theme        |
| Enter    | Save / Confirm      |
| Esc      | Close active window |
| Alt + F4 | Exit app            |

---

## 📂 Project Structure

```
expense_tracker/
├── expense_tracker_gui.py   # GUI version (v2.x)
├── expense_tracker.py       # CLI version (v1.x)
├── expenses.csv
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
```

---

## 🧭 Legacy CLI Version (v1.x)

The original **command-line version** is preserved for learning purposes.

### CLI Features

* Add, edit, and delete expenses
* Monthly summary by category
* CSV export
* Text-based storage

Run it with:

```bash
python expense_tracker.py
```

📌 This version demonstrates early-stage Python fundamentals such as file I/O, validation, and structured logic.

---

## 🧠 Project Purpose

This project demonstrates:

* Progressive development from CLI → GUI
* GUI architecture and state management
* Modal window behavior and accessibility
* Theme systems and UI consistency
* File persistence and backward compatibility
* Clean documentation and versioning

---

## 📜 Documentation

* [CHANGELOG](CHANGELOG.md)
* [ROADMAP](ROADMAP.md)

---

## 📄 License

MIT License

---

✨ *Built as part of a structured learning journey in Python and desktop application development.*
