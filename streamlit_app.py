"""
COMPLETE STREAMLIT TUTORIAL IMPLEMENTATION
File: streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# ==================== BASIC SETUP ====================
st.set_page_config(page_title="Streamlit Tutorial", layout="wide")

# ==================== WHAT IS STREAMLIT ====================
def intro_section():
    st.title("Streamlit Tutorial")
    st.write("""
    Streamlit is an open-source Python library that makes it easy to create and share 
    beautiful custom web apps for machine learning and data science.
    """)
    
    if st.button("Say Hello"):
        st.write("Hello World!")
    
    st.divider()

# ==================== INPUT ELEMENTS ====================
def input_elements():
    st.header("Using Input Elements")
    
    # Text input
    movie = st.text_input("Favorite Movie?")
    if movie:
        st.write(f"Your favorite movie is: {movie}")
    
    # Button
    if st.button("Click Me"):
        st.success("Button clicked!")
    
    # Slider
    age = st.slider("Your Age", 0, 100, 25)
    st.write(f"You're {age} years old")
    
    # Checkbox
    if st.checkbox("Show/Hide"):
        st.write("Content appears when checked")
    
    st.divider()

# ==================== MARKDOWN ====================
def markdown_demo():
    st.header("Markdown Formatting")
    
    st.write("## This is a H2 Title!")
    st.markdown("*Streamlit* is **really** ***cool***.")
    st.markdown('''
        :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
        :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
    st.markdown("Here's a bouquet &mdash;\
                :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")
    
    multi = '''If you end a line with two spaces,
    a soft return is used for the next line.

    Two (or more) newline characters in a row will result in a hard return.
    '''
    st.markdown(multi)
    
    st.divider()

# ==================== WORKING WITH DATA ====================
def data_section():
    st.header("Working with Data")
    
    # Sample DataFrame
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["a", "b", "c"]
    )
    
    st.write("### Random Data Table")
    st.dataframe(chart_data)
    
    st.write("### Charts")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(chart_data)
    with col2:
        st.line_chart(chart_data)
    
    st.divider()

# ==================== LOAN CALCULATOR ====================
def loan_calculator():
    st.header("Loan Repayments Calculator")
    
    st.write("### Input Data")
    col1, col2 = st.columns(2)
    
    # Inputs
    home_value = col1.number_input("Home Value", min_value=0, value=500000)
    deposit = col1.number_input("Deposit", min_value=0, value=100000)
    interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
    loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)
    
    # Calculations
    loan_amount = home_value - deposit
    monthly_interest_rate = (interest_rate / 100) / 12
    number_of_payments = loan_term * 12
    
    if monthly_interest_rate > 0:
        monthly_payment = (
            loan_amount
            * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
            / ((1 + monthly_interest_rate) ** number_of_payments - 1)
        )
    else:
        monthly_payment = loan_amount / number_of_payments
    
    total_payments = monthly_payment * number_of_payments
    total_interest = total_payments - loan_amount
    
    # Display results
    st.write("### Repayments")
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Repayments", f"${monthly_payment:,.2f}")
    col2.metric("Total Repayments", f"${total_payments:,.0f}")
    col3.metric("Total Interest", f"${total_interest:,.0f}")
    
    # Payment schedule
    schedule = []
    remaining_balance = loan_amount
    
    for i in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        year = math.ceil(i / 12)
        schedule.append([i, monthly_payment, principal_payment, interest_payment, remaining_balance, year])
    
    df = pd.DataFrame(
        schedule,
        columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
    )
    
    st.write("### Payment Schedule")
    payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
    st.line_chart(payments_df)

# ==================== MAIN APP ====================
def main():
    intro_section()
    input_elements()
    markdown_demo()
    data_section()
    loan_calculator()
    
    st.sidebar.title("Navigation")
    st.sidebar.info("""
    This app demonstrates Streamlit capabilities including:
    - Input elements
    - Markdown formatting
    - Data visualization
    - Loan calculator
    """)

if __name__ == "__main__":
    main()