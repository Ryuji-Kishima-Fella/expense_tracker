from datetime import datetime
import os
import csv

EXPENSE_FILE = "expenses.txt"
CSV_FILE = "expenses.csv"

CATEGORIES = [
    "Food",
    "Transport",
    "Internet",
    "Shopping",
    "Education",
    "Entertainment",
    "Other"
]


def show_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. Add expense")
    print("2. View expense history")
    print("3. View monthly summary")
    print("4. Export to CSV")
    print("5. Edit expense")
    print("6. Delete expense")
    print("7. Exit")


def choose_category():
    print("\nSelect a category:")
    for idx, category in enumerate(CATEGORIES, start=1):
        print(f"{idx}. {category}")

    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(CATEGORIES):
                return CATEGORIES[index]
        print("❌ Invalid category. Please select a valid number.")


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: ").strip())
            if amount > 0:
                return amount
            print("❌ Amount must be greater than zero.")
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")


def load_expenses():
    if not os.path.exists(EXPENSE_FILE):
        return []

    with open(EXPENSE_FILE, "r", encoding="utf-8") as file:
        return file.readlines()


def save_expenses(lines):
    with open(EXPENSE_FILE, "w", encoding="utf-8") as file:
        file.writelines(lines)


def add_expense():
    print("\n--- Add New Expense ---")

    amount = get_valid_amount()
    category = choose_category()
    note = input("Enter note (optional): ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    line = f"{date} | {category} | {amount:.2f} | {note}\n"
    with open(EXPENSE_FILE, "a", encoding="utf-8") as file:
        file.write(line)

    print("✅ Expense saved successfully!")


def view_expenses(return_lines=False):
    print("\n--- Expense History ---")

    lines = load_expenses()
    if not lines:
        print("📭 No expenses recorded yet.")
        return [] if return_lines else None

    for idx, line in enumerate(lines, start=1):
        print(f"{idx}. {line.strip()}")

    return lines if return_lines else None


def view_monthly_summary():
    print("\n📊 Monthly Summary")

    lines = load_expenses()
    if not lines:
        print("📭 No expenses recorded yet.")
        return

    current_month = datetime.now().strftime("%Y-%m")
    total = 0.0
    category_totals = {cat: 0.0 for cat in CATEGORIES}

    for line in lines:
        if " | " not in line:
            continue

        date, category, amount, _ = line.strip().split(" | ", 3)
        if not date.startswith(current_month):
            continue

        try:
            amount = float(amount)
        except ValueError:
            continue

        total += amount
        if category in category_totals:
            category_totals[category] += amount

    if total == 0:
        print(f"No expenses found for {current_month}.")
        return

    print(f"\nMonth: {current_month}")
    print(f"Total spent: ${total:.2f}\n")

    print("By category:")
    for category, amount in category_totals.items():
        if amount > 0:
            print(f"- {category}: ${amount:.2f}")


def export_to_csv():
    print("\n📤 Exporting expenses to CSV...")

    lines = load_expenses()
    if not lines:
        print("📭 No expenses to export.")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Date", "Category", "Amount", "Note"])

        for line in lines:
            if " | " not in line:
                continue
            date, category, amount, note = line.strip().split(" | ", 3)
            writer.writerow([date, category, amount, note])

    print(f"✅ Export completed: {CSV_FILE}")


def edit_expense():
    lines = view_expenses(return_lines=True)
    if not lines:
        return

    choice = input("\nEnter expense number to edit: ").strip()
    if not choice.isdigit():
        print("❌ Invalid selection.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(lines):
        print("❌ Invalid expense number.")
        return

    old_line = lines[index].strip()
    date, _, _, _ = old_line.split(" | ", 3)

    print("\nEditing expense:")
    print(old_line)

    amount = get_valid_amount()
    category = choose_category()
    note = input("Enter note (optional): ").strip()

    lines[index] = f"{date} | {category} | {amount:.2f} | {note}\n"
    save_expenses(lines)

    print("✅ Expense updated successfully!")


def delete_expense():
    lines = view_expenses(return_lines=True)
    if not lines:
        return

    choice = input("\nEnter expense number to delete: ").strip()
    if not choice.isdigit():
        print("❌ Invalid selection.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(lines):
        print("❌ Invalid expense number.")
        return

    confirm = input("Are you sure you want to delete this expense? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    del lines[index]
    save_expenses(lines)

    print("🗑️ Expense deleted successfully!")


def main():
    print("Welcome to Personal Expense Tracker!")
    print("Track your daily expenses easily.\n")

    while True:
        show_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_monthly_summary()
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            edit_expense()
        elif choice == "6":
            delete_expense()
        elif choice == "7":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
