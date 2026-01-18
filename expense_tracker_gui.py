import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker v2.0")
        self.root.geometry("420x420")

        # Track child windows
        self.expenses = []
        self.history_window = None
        self.summary_window = None
        self.add_window = None


        # Title
        tk.Label(
            root,
            text="Expense Tracker v2.0",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Buttons
        tk.Button(root, text="➕ Add Expense", width=25, command=self.add_expense).pack(pady=5)
        tk.Button(root, text="📖 View History", width=25, command=self.view_history).pack(pady=5)
        tk.Button(root, text="📊 View Summary", width=25, command=self.view_summary).pack(pady=5)
        tk.Button(root, text="📤 Export to CSV", width=25, command=self.export_csv).pack(pady=5)

        # Status bar
        self.status = tk.Label(root, text="Ready", fg="gray")
        self.status.pack(side="bottom", fill="x", pady=5)

        # Keyboard shortcuts
        self.root.bind("<Alt-F4>", lambda e: self.exit_app())
        self.root.bind("<Escape>", self.close_active_window)

    # -------------------------
    # Core placeholders
    # -------------------------

    def add_expense(self):
        if self.add_window and self.add_window.winfo_exists():
            self.add_window.lift()
            self.add_window.focus_force()
            return

        win = tk.Toplevel(self.root)
        self.add_window = win
        win.title("Add Expense")
        win.geometry("350x300")
        win.resizable(False, False)

        win.protocol("WM_DELETE_WINDOW", self.close_add_window)

        # ---- Form fields ----

        tk.Label(win, text="Add New Expense", font=("Arial", 14, "bold")).pack(pady=10)

        form = tk.Frame(win)
        form.pack(pady=10)

        # Amount
        tk.Label(form, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        amount_var = tk.StringVar()
        tk.Entry(form, textvariable=amount_var).grid(row=0, column=1, padx=5)

        # Category
        tk.Label(form, text="Category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        categories = ["Food", "Transport", "Bills", "Entertainment", "Other"]
        category_var = tk.StringVar(value=categories[0])
        tk.OptionMenu(form, category_var, *categories).grid(row=1, column=1, padx=5, sticky="ew")

        # Date
        tk.Label(form, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(form, textvariable=date_var).grid(row=2, column=1, padx=5)

        # Note
        tk.Label(form, text="Note (optional):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        note_var = tk.StringVar()
        tk.Entry(form, textvariable=note_var).grid(row=3, column=1, padx=5)

        # ---- Buttons ----

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=15)

        tk.Button(
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

        tk.Button(
            btn_frame,
            text="❌ Cancel",
            width=10,
            command=self.close_add_window
        ).pack(side="left", padx=10)

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
            "note": note
        }

        self.expenses.append(expense)

        messagebox.showinfo("Expense Added", "Expense saved successfully.")


        self.status.config(text="Expense added (not yet saved)")
        self.close_add_window()

    def close_add_window(self):
        if self.add_window:
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
        self.history_window = win
        win.title("Expense History")
        win.geometry("450x350")

        win.protocol("WM_DELETE_WINDOW", self.close_history_window)

        tk.Label(win, text="Expense History", font=("Arial", 14, "bold")).pack(pady=10)

        if not self.expenses:
            tk.Label(win, text="No expenses recorded yet.").pack(pady=20)
            return

        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 11)
        )
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        for exp in self.expenses:
            line = f"{exp['date']} | {exp['category']:<14} | ${exp['amount']:.2f}"
            if exp["note"]:
                line += f" | {exp['note']}"
            listbox.insert(tk.END, line)


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
        self.summary_window = win
        win.title("Expense Summary")
        win.geometry("400x300")

        win.protocol("WM_DELETE_WINDOW", self.close_summary_window)

        tk.Label(win, text="Expense Summary (v2.0)", font=("Arial", 14)).pack(pady=20)
        tk.Label(win, text="Charts and analytics coming soon...").pack()

    def close_summary_window(self):
        if self.summary_window:
            self.summary_window.destroy()
            self.summary_window = None

    # -------------------------
    # Window management
    # -------------------------

    def close_active_window(self, event=None):
        focused = self.root.focus_get()
        if focused:
            win = focused.winfo_toplevel()
            if win != self.root:
                win.destroy()
                return
        self.exit_app()

    def exit_app(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
