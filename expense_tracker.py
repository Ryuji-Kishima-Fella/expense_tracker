from datetime import datetime
import os

EXPENSE_FILE = "expenses.txt"


def show_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. Add expense")
    print("2. View expense history")
    print("3. View monthly summary")
    print("4. Export to CSV")
    print("5. Exit")

def add_expense():
    print("\n--- Add New Expense ---")

    try:
        amount = float(input("Enter amount: ").strip())
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return

    category = input("Enter category: ").strip()
    note = input("Enter note (optional): ").strip()

    date = datetime.now().strftime("%Y-%m-%d")

    expense_line = f"{date} | {category} | {amount:.2f} | {note}\n"

    with open(EXPENSE_FILE, "a", encoding="utf-8") as file:
        file.write(expense_line)

    print("✅ Expense saved successfully!")

def view_expenses():
    print("\n--- Expense History ---")

    if not os.path.exists(EXPENSE_FILE):
        print("📭 No expenses recorded yet.")
        return

    with open(EXPENSE_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        print("📭 No expenses recorded yet.")
        return

    for idx, line in enumerate(lines, start=1):
        print(f"{idx}. {line.strip()}")

def main():
    print("Welcome to Personal Expense Tracker!")
    print("Track your daily expenses easily.\n")

    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Summary feature coming soon.")
        elif choice == "4":
            print("Export feature coming soon.")
        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
