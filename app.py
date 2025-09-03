# File: app.py
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('risk_model.joblib')

# Define the input columns in the correct order
# This must match the order of columns the model was trained on
input_cols = [
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History',
    'Gender_Male', 'Married_Yes', 'Dependents_1', 'Dependents_2', 'Dependents_3+',
    'Education_Not Graduate', 'Self_Employed_Yes', 'Property_Area_Semiurban', 'Property_Area_Urban'
]

# --- Create the Streamlit web app UI ---
st.title("Loan Default Risk Prediction 🔮")
st.write("Enter applicant details to predict loan approval risk.")

applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount", min_value=0)
loan_term = st.number_input("Loan Term (in months)", min_value=12, step=12)
credit_history = st.selectbox("Credit History Available?", (1.0, 0.0))
gender = st.selectbox("Gender", ("Male", "Female"))
married = st.selectbox("Married?", ("Yes", "No"))
education = st.selectbox("Education", ("Graduate", "Not Graduate"))
self_employed = st.selectbox("Self Employed?", ("Yes", "No"))
property_area = st.selectbox("Property Area", ("Urban", "Semiurban", "Rural"))
# Note: Dependents input is simplified here for brevity

# --- Prediction Logic (runs only when the button is clicked) ---
if st.button("Predict Loan Status"):
    # All of the following code is now indented to be inside the 'if' block
    
    # Get the full list of columns from your training notebook
    # Ensure this list is 100% correct and in the same order as your training data
    input_cols = [
        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History',
        'Gender_Male', 'Married_Yes', 'Dependents_1', 'Dependents_2', 'Dependents_3+',
        'Education_Not Graduate', 'Self_Employed_Yes', 'Property_Area_Semiurban', 'Property_Area_Urban'
    ]

    # Create a dictionary to hold the user's input
    input_data = {}

    # Populate with numerical data
    input_data['ApplicantIncome'] = applicant_income
    input_data['CoapplicantIncome'] = coapplicant_income
    input_data['LoanAmount'] = loan_amount
    input_data['Loan_Amount_Term'] = loan_term
    input_data['Credit_History'] = credit_history

    # Populate with categorical data (one-hot encoding)
    # Set all categorical feature columns to 0 first
    input_data['Gender_Male'] = 0
    input_data['Married_Yes'] = 0
    input_data['Dependents_1'] = 0
    input_data['Dependents_2'] = 0
    input_data['Dependents_3+'] = 0
    input_data['Education_Not Graduate'] = 0
    input_data['Self_Employed_Yes'] = 0
    input_data['Property_Area_Semiurban'] = 0
    input_data['Property_Area_Urban'] = 0

    # Update the specific categorical column that matches the user's selection
    if gender == 'Male': input_data['Gender_Male'] = 1
    if married == 'Yes': input_data['Married_Yes'] = 1
    # Note: A more robust app would handle the 'Dependents' field better
    if education == 'Not Graduate': input_data['Education_Not Graduate'] = 1
    if self_employed == 'Yes': input_data['Self_Employed_Yes'] = 1
    if property_area == 'Semiurban': input_data['Property_Area_Semiurban'] = 1
    if property_area == 'Urban': input_data['Property_Area_Urban'] = 1

    # Convert the dictionary to a DataFrame
    input_df = pd.DataFrame([input_data], columns=input_cols)

    # Display the final input being sent to the model (for debugging)
    st.write("Final Model Input:")
    st.write(input_df)

    # Make prediction
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    # Display result
    if prediction == 1:
        # This line is indented further to be inside the 'if prediction == 1' block
        st.success(f"Loan Approved! ✅ (Approval Probability: {probability:.2%})")
    else:
        # This line is indented further to be inside the 'else' block
        st.error(f"Loan Rejected! ❌ (Approval Probability: {probability:.2%})")