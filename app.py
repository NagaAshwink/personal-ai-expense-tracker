import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Page settings
st.set_page_config(page_title="AI Expense Tracker", page_icon="💰", layout="wide")

st.title("💰 Personal AI Expense Tracker")
st.write("Track your daily expenses and visualize your spending patterns")

# Load expense data
try:
    df = pd.read_csv("expenses.csv")
except:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

# Sidebar for adding expenses
st.sidebar.header("➕ Add New Expense")

expense_date = st.sidebar.date_input("Date", date.today())

category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
)

amount = st.sidebar.number_input("Amount", min_value=0)

note = st.sidebar.text_input("Note")

# Add expense
if st.sidebar.button("Add Expense"):

    new_expense = pd.DataFrame(
        [[expense_date, category, amount, note]],
        columns=["Date", "Category", "Amount", "Note"]
    )

    df = pd.concat([df, new_expense], ignore_index=True)

    df.to_csv("expenses.csv", index=False)

    st.success("Expense added successfully!")

st.write("---")

# Expense History
st.subheader("📊 Expense History")

if len(df) > 0:

    st.dataframe(df, use_container_width=True)

    # Delete option
    delete_index = st.number_input(
        "Enter the row number to delete",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    if st.button("Delete Selected Expense"):

        df = df.drop(delete_index).reset_index(drop=True)

        df.to_csv("expenses.csv", index=False)

        st.warning("Expense deleted successfully!")

        st.rerun()

else:
    st.info("No expenses recorded yet.")

# Total spending
if len(df) > 0:

    total_spending = df["Amount"].sum()

    st.metric("💸 Total Spending", f"₹ {total_spending}")

# Chart
st.subheader("📈 Spending by Category")

if len(df) > 0:

    category_sum = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()

    ax.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%")

    ax.set_title("Expense Distribution")

    st.pyplot(fig)

else:
    st.info("Add expenses to see visualization.")

st.write("---")

st.caption("Personal Expense Tracker | Built with Python & Streamlit")