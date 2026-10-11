import json
try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except FileNotFoundError:
    expenses = []



def add_expense():
    name = input("Enter expense name: ")

    try:
        amount = float(input("Enter amount (₹): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        expenses.append({
            "name": name,
            "amount": amount
        })

        with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)

        print("Expense added and saved successfully!")

    except ValueError:
        print("Please enter a valid number.")

def view_expenses():
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- Your Expenses ---")

    for i, expense in enumerate(expenses, start=1):
        print(
            f"{i}. {expense['name']} - "
            f"₹{expense['amount']:.2f}"
        )

    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal Expenses: ₹{total:.2f}")


def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Expense Tracker closed.")
            break
        else:
            print("Invalid choice. Select 1, 2, or 3.")


if __name__ == "__main__":
    main()