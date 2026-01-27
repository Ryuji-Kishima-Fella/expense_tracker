import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkinter import filedialog
import csv
import os

EXPENSE_FILE = "expenses.csv"
EXPENSE_FIELDS = ["date", "amount", "category", "note"]



class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker v2.0")
        self.root.geometry("420x420")

        # -------------------------
        # THEME SETUP (MUST BE FIRST)
        # -------------------------
        self.setup_themes()
        self.apply_theme()


        # -------------------------
        # Menu bar
        # -------------------------
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(
            label="Export CSV",
            command=self.export_csv
        )

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Exit",
            command=self.exit_app
        )

        self.theme_var = tk.StringVar(value=self.current_theme)

        theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Theme", menu=theme_menu)

        theme_menu.add_radiobutton(
            label="Light",
            variable=self.theme_var,
            value="light",
            command=lambda: self.set_theme("light")
        )

        theme_menu.add_radiobutton(
            label="Dark",
            variable=self.theme_var,
            value="dark",
            command=lambda: self.set_theme("dark")
        )


        # Track child windows
        self.expenses = []
        self.load_expenses()
        self.history_window = None
        self.summary_window = None
        self.add_window = None


        # Title
        ttk.Label(
            root,
            text="Expense Tracker v2.0",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Buttons
        ttk.Button(root, text="➕ Add Expense", width=25, command=self.add_expense).pack(pady=5)
        ttk.Button(root, text="📖 View History", width=25, command=self.view_history).pack(pady=5)
        ttk.Button(root, text="📊 View Summary", width=25, command=self.view_summary).pack(pady=5)
        ttk.Button(root, text="📤 Export to CSV", width=25, command=self.export_csv).pack(pady=5)

        # Status bar
        self.status = ttk.Label(root, text="Ready", style="Status.TLabel")
        self.status.pack(side="bottom", fill="x", pady=5)

        # Keyboard shortcuts
        self.root.bind("<Alt-F4>", lambda e: self.exit_app())
        self.root.bind("<Escape>", self.close_active_window)

        # -------------------------
        # Keyboard shortcuts
        # -------------------------
        self.root.bind("<Control-n>", lambda e: self.add_expense())
        self.root.bind("<Control-h>", lambda e: self.view_history())
        self.root.bind("<Control-s>", lambda e: self.view_summary())
        self.root.bind("<Control-d>", lambda e: self.toggle_theme())

        



    # -------------------------
    # Core placeholders
    # -------------------------

    def apply_theme(self):
        t = self.themes[self.current_theme]
        self.root.configure(background=t["bg"])
        self.style.theme_use(t["theme"])

        self.style.configure(
            "TFrame",
            background=t["bg"]
        )
        self.style.configure(
            "TLabel",
            background=t["bg"],
            foreground=t["fg"]
        )
        self.style.configure(
            "TButton",
            background=t["button_bg"],
            foreground=t["fg"]
        )
        self.style.configure(
            "TEntry",
            fieldbackground=t["bg"],
            foreground=t["fg"]
        )

        self.style.configure(
            "Status.TLabel",
            background=t["bg"],
            foreground=t["status_fg"]
        )


    def setup_themes(self):
        self.style = ttk.Style()

        self.themes = {
            "light": {
                "theme": "default",
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#e0e0e0",
                "status_fg": "gray"
            },
            "dark": {
                "theme": "clam",
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "button_bg": "#2d2d2d",
                "status_fg": "#aaaaaa"
            }
        }

        self.current_theme = "light"

    def set_theme(self, theme_name):
        if theme_name not in self.themes:
            return

        self.current_theme = theme_name
        self.theme_var.set(theme_name)
        self.apply_theme()



    def apply_theme_to_window(self, win):
        if not win or not win.winfo_exists():
            return

        t = self.themes[self.current_theme]
        win.configure(background=t["bg"])

        for child in win.winfo_children():
            if isinstance(child, tk.Listbox):
                child.configure(
                    bg=t["bg"],
                    fg=t["fg"],
                    selectbackground="#444444" if self.current_theme == "dark" else "#cccccc",
                    selectforeground=t["fg"],
                    highlightthickness=0,
                    borderwidth=0
                )


    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

        # Update all open windows
        self.apply_theme_to_window(self.add_window)
        self.apply_theme_to_window(self.history_window)
        self.apply_theme_to_window(self.summary_window)



    def add_expense(self):

        if self.add_window and self.add_window.winfo_exists():
            self.add_window.lift()
            self.add_window.focus_force()
            return

        win = tk.Toplevel(self.root)
        win.configure(background=self.themes[self.current_theme]["bg"])
        self.add_window = win
        win.title("Add Expense")
        win.geometry("350x300")
        win.resizable(False, False)

        win.protocol("WM_DELETE_WINDOW", self.close_add_window)

        # ---- Form fields ----

        ttk.Label(win, text="Add New Expense", font=("Arial", 14, "bold")).pack(pady=10)

        form = ttk.Frame(win)
        form.pack(pady=10)

        # Amount
        ttk.Label(form, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=amount_var).grid(row=0, column=1, padx=5)

        # Category
        ttk.Label(form, text="Category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]
        category_var = tk.StringVar(value=categories[0])
        ttk.OptionMenu(form, category_var, *categories).grid(row=1, column=1, padx=5, sticky="ew")

        # Date
        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=date_var).grid(row=2, column=1, padx=5)

        # Note
        ttk.Label(form, text="Note (optional):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        note_var = tk.StringVar()
        ttk.Entry(form, textvariable=note_var).grid(row=3, column=1, padx=5)

        # ---- Buttons ----

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="💾 Save",
            width=10,
            command=lambda: self.save_expense(
                amount_var.get(),
                category_var.get(),
                date_var.get(),
                note_var.get()
            )
        ).pack(side="left", padx=10)

        ttk.Button(
            btn_frame,
            text="❌ Cancel",
            width=10,
            command=self.close_add_window
        ).pack(side="left", padx=10)

        win.bind(
            "<Return>",
            lambda e: self.save_expense(
                amount_var.get(),
                category_var.get(),
                date_var.get(),
                note_var.get()
            )
        )

        win.after(100, lambda: win.focus_force())
        win.bind("<Escape>", self.close_active_window)

        win.transient(self.root)
        win.grab_set()
        win.focus_force()


    def save_expense(self, amount, category, date, note):
        # Basic validation
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid positive number.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
            return

        # For now, just confirm success (no file saving yet)
        expense = {
            "amount": amount,
            "category": category,
            "date": date,
            "note": note if note else ""
        }

        self.expenses.append(expense)
        self.save_expenses()
        
        self.status.config(text="Expense added")        
        messagebox.showinfo("Expense Added", "Expense saved successfully.")
        self.close_add_window()




    def load_expenses(self):
        if not os.path.exists(EXPENSE_FILE):
            return

        with open(EXPENSE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Backward compatibility
                date = row.get("date") or row.get("Date")
                amount = row.get("amount") or row.get("Amount")
                category = row.get("category") or row.get("Category")

                if date and amount and category:
                    self.expenses.append({
                    "date": date,
                    "amount": float(amount),
                    "category": category,
                    "note": row.get("note", "")
                })


    
    def save_expenses(self):
        with open(EXPENSE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["date", "category", "amount", "note"]
            )
            writer.writeheader()
            writer.writerows(self.expenses)
    


    def close_add_window(self):
        if self.add_window:
            self.add_window.grab_release()
            self.add_window.destroy()
            self.add_window = None



    def export_csv(self):
        messagebox.showinfo("Export", "CSV export coming in v2.0")
        self.status.config(text="Export clicked")

    # -------------------------
    # History window
    # -------------------------

    def view_history(self):

        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            self.history_window.focus_force()
            return

        win = tk.Toplevel(self.root)
        win.configure(background=self.themes[self.current_theme]["bg"])
        self.history_window = win
        win.title("Expense History")
        win.geometry("450x350")

        win.protocol("WM_DELETE_WINDOW", self.close_history_window)

        ttk.Label(win, text="Expense History", font=("Arial", 14, "bold")).pack(pady=10)

        if not self.expenses:
            tk.Label(win, text="No expenses recorded yet.").pack(pady=20)
            return

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 11)
        )

        t = self.themes[self.current_theme]
        self.history_listbox.configure(
            bg=t["bg"],
            fg=t["fg"],
            selectbackground="#444444" if self.current_theme == "dark" else "#cccccc",
            selectforeground=t["fg"],
            highlightthickness=0,
            borderwidth=0
        )

        self.history_listbox.pack(expand=True, fill="both", padx=10, pady=10)
        scrollbar.config(command=self.history_listbox.yview)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✏️ Edit", width=10, command=self.edit_expense).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Delete", width=10, command=self.delete_expense).pack(side="left", padx=10)



        for exp in self.expenses:
            line = f"{exp['date']} | {exp['category']:<14} | ${exp['amount']:.2f}"
            note = exp.get("note", "")
            if note:
                line += f" | {exp['note']}"
            self.history_listbox.insert(tk.END, line)

        win.bind("<Control-e>", lambda e: self.edit_expense())

        # Escape closes History window (no matter where focus is)
        win.bind("<Escape>", lambda e: self.close_history_window())
        self.history_listbox.bind("<Escape>", lambda e: self.close_history_window())


    def delete_expense(self):
        try:
            index = self.history_listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Delete Expense", "Please select an expense to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if confirm:
            del self.expenses[index]
            self.refresh_history()
            self.status.config(text="Expense deleted")

    def edit_expense(self):


        try:
            index = self.history_listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Edit Expense", "Please select an expense to edit.")
            return

        exp = self.expenses[index]

        self.open_edit_window(index, exp)


    def open_edit_window(self, index, exp):
        win = tk.Toplevel(self.root)
        win.configure(background=self.themes[self.current_theme]["bg"])
        win.title("Edit Expense")
        win.geometry("350x300")
        win.resizable(False, False)

        # -------------------------
        # MODAL BEHAVIOR
        # -------------------------
        win.transient(self.history_window)   # attach to History
        win.grab_set()                       # block other windows
        win.focus_force()                    # keyboard focus

        ttk.Label(win, text="Edit Expense", font=("Arial", 14, "bold")).pack(pady=10)

        form = ttk.Frame(win)
        form.pack(pady=10)

        amount_var = tk.StringVar(value=str(exp["amount"]))
        category_var = tk.StringVar(value=exp["category"])
        date_var = tk.StringVar(value=exp["date"])
        note = exp.get("note", "")
        note_var = tk.StringVar(value=exp.get("note", ""))


        ttk.Label(form, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=amount_var).grid(row=0, column=1)

        ttk.Label(form, text="Category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        categories = ["Food", "Transport", "Bills", "Entertainment", "Other"]
        ttk.OptionMenu(form, category_var, *categories).grid(row=1, column=1, sticky="ew")

        ttk.Label(form, text="Date:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=date_var).grid(row=2, column=1)

        ttk.Label(form, text="Note:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=note_var).grid(row=3, column=1, padx=5)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="💾 Save",
            command=lambda: self.save_edit(
                index,
                amount_var.get(),
                category_var.get(),
                date_var.get(),
                note_var.get(),
                win
            )
        ).pack(side="left", padx=10)

        ttk.Button(btn_frame, text="❌ Cancel", command=win.destroy).pack(side="left", padx=10)

        win.bind(
            "<Return>",
            lambda e: self.save_edit(
                index,
                amount_var.get(),
                category_var.get(),
                date_var.get(),
                note_var.get(),
                win
            )
        )

        win.bind("<Escape>", lambda e: self.close_edit_window(win))


    def save_edit(self, index, amount, category, date, note, win):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Enter a valid positive number.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date must be YYYY-MM-DD.")
            return

        self.expenses[index] = {
            "amount": amount,
            "category": category,
            "date": date,
            "note": note if note else ""
        }

        # Save to CSV
        self.save_expenses()

        # Close edit window
        win.grab_release()
        win.destroy()
        self.refresh_history()
        self.status.config(text="Expense updated")

    def refresh_history(self):
        if not self.history_window or not self.history_window.winfo_exists():
            return

        self.history_listbox.delete(0, tk.END)

        for exp in self.expenses:
            line = f"{exp['date']} | {exp['category']:<14} | ${exp['amount']:.2f}"
            if exp["note"]:
                line += f" | {exp['note']}"
            self.history_listbox.insert(tk.END, line)

    def close_edit_window(self, win):
        win.grab_release()
        win.destroy()


    def close_history_window(self):
        if self.history_window:
            self.history_window.destroy()
            self.history_window = None



    # -------------------------
    # Summary window
    # -------------------------

    def view_summary(self):

        if self.summary_window and self.summary_window.winfo_exists():
            self.summary_window.lift()
            self.summary_window.focus_force()
            return

        win = tk.Toplevel(self.root)
        win.configure(background=self.themes[self.current_theme]["bg"])
        self.summary_window = win
        win.title("Expense Summary")
        win.geometry("400x350")

        win.protocol("WM_DELETE_WINDOW", self.close_summary_window)

        ttk.Label(win, text="Expense Summary", font=("Arial", 14, "bold")).pack(pady=10)

        if not self.expenses:
            ttk.Label(win, text="No expenses recorded yet.").pack(pady=20)
            return

        # ---- Calculate totals ----
        totals = {}
        total_spent = 0.0

        for exp in self.expenses:
            category = exp["category"]
            amount = exp["amount"]
            totals[category] = totals.get(category, 0) + amount
            total_spent += amount

        # ---- Display results ----
        frame = ttk.Frame(win)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        for category, amount in totals.items():
            ttk.Label(
                frame,
                text=f"{category:<15} : ${amount:.2f}",
                anchor="w",
                font=("Consolas", 11)
            ).pack(fill="x", pady=2)

        ttk.Label(win, text="—" * 30).pack(pady=10)

        ttk.Label(
            win,
            text=f"Total Spent: ${total_spent:.2f}",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

    def export_csv(self):
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Expenses"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Category", "Amount", "Note"])

                for exp in self.expenses:
                    writer.writerow([
                        exp.get("date", ""),
                        exp.get("category", ""),
                        exp.get("amount", ""),
                        exp.get("note", "")
                    ])

            messagebox.showinfo("Export Complete", "Expenses exported successfully.")

        except Exception as e:
            messagebox.showerror("Export Failed", str(e))


    def close_summary_window(self):
        if self.summary_window:
            self.summary_window.destroy()
            self.summary_window = None

    # -------------------------
    # Window management
    # -------------------------

    def close_active_window(self, event=None):
        # Close Add window first
        if self.add_window and self.add_window.winfo_exists():
            self.add_window.destroy()
            self.add_window = None
            return

        # Close History window
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.destroy()
            self.history_window = None
            return

        # Close Summary window
        if self.summary_window and self.summary_window.winfo_exists():
            self.summary_window.destroy()
            self.summary_window = None
            return

        # No child windows open → exit app
        self.exit_app()


    def exit_app(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
