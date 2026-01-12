def show_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. Add expense")
    print("2. View expense history")
    print("3. View monthly summary")
    print("4. Export to CSV")
    print("5. Exit")


def main():
    print("Welcome to Personal Expense Tracker!")
    print("Track your daily expenses easily.\n")

    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            print("Add expense feature coming soon.")
        elif choice == "2":
            print("View history feature coming soon.")
        elif choice == "3":
            print("Summary feature coming soon.")
        elif choice == "4":
            print("Export feature coming soon.")
        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
