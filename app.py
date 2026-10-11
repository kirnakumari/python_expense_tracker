
import json
from pathlib import Path
from datetime import date

import streamlit as st

DATA_FILE = Path("expenses.json")


def load_expenses():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_expenses(expenses):
    DATA_FILE.write_text(
        json.dumps(expenses, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Expense Tracker")
st.caption("Track your spending. Understand your money.")

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

expenses = st.session_state.expenses

st.subheader("Add a new expense")

with st.form("expense_form", clear_on_submit=True):
    name = st.text_input("Expense name", placeholder="e.g. Food, Travel")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Education", "Bills", "Other"]
    )
    expense_date = st.date_input("Date", value=date.today())

    submitted = st.form_submit_button("Add Expense", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter an expense name.")
        elif amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            new_expense = {
                "name": name.strip(),
                "amount": amount,
                "category": category,
                "date": expense_date.isoformat()
            }
            expenses.append(new_expense)
            save_expenses(expenses)
            st.success("Expense added successfully!")
            st.rerun()

st.divider()
st.subheader("Your spending overview")

total = sum(float(item.get("amount", 0)) for item in expenses)

col1, col2 = st.columns(2)
col1.metric("Total Expenses", f"₹{total:,.2f}")
col2.metric("Number of Expenses", len(expenses))

if expenses:
    st.subheader("Expense History")

    for index, item in enumerate(reversed(expenses)):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{item.get('name', 'Expense')}**")
            col1.caption(
                f"{item.get('category', 'Other')} · "
                f"{item.get('date', 'Date unavailable')}"
            )
            col2.write(f"₹{float(item.get('amount', 0)):,.2f}")

    if st.button("Clear All Expenses"):
        st.session_state.confirm_clear = True

    if st.session_state.get("confirm_clear", False):
        st.warning("Are you sure you want to delete all expenses?")
        yes, no = st.columns(2)

        if yes.button("Yes, clear all"):
            st.session_state.expenses = []
            save_expenses([])
            st.session_state.confirm_clear = False
            st.rerun()

        if no.button("Cancel"):
            st.session_state.confirm_clear = False
            st.rerun()
else:
    st.info("No expenses yet. Add your first expense above!")