# File: app.py
import streamlit as st
import pandas as pd
import joblib
# Load the trained model
model = joblib.load('risk_model.joblib')
# Define the input columns in the correct order
# This must match the order of columns the model was trained on
# NOTE: This is a simplified list. You would need all columns from your training data.
# A better approach is to save the column list with your model.
input_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Gender_Male', 'Married_Yes', 'Dependents_1', 'Dependents_2', 'Dependents_3+', 'Education_Not Graduate', 'Self_Employed_Yes', 'Property_Area_Semiurban', 'Property_Area_Urban']
# Create the Streamlit web app
st.title("Loan Default Risk Prediction ")
st.write("Enter applicant details to predict loan approval risk.")
# Create input fields for user
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
# Predict button
if st.button("Predict Loan Status"):
# Create a DataFrame from the user's input
# This part needs careful one-hot encoding to match the model's training data
input_data = pd.DataFrame(columns=input_cols)
input_data.loc[0] = 0 # Initialize row with zeros

input_data['ApplicantIncome'] = applicant_income
input_data['CoapplicantIncome'] = coapplicant_income
input_data['LoanAmount'] = loan_amount
input_data['Loan_Amount_Term'] = loan_term
input_data['Credit_History'] = credit_history

# Handle categorical variables
if gender == 'Male': input_data['Gender_Male'] = 1
if married == 'Yes': input_data['Married_Yes'] = 1
if education == 'Not Graduate': input_data['Education_Not Graduate'] = 1
if self_employed == 'Yes': input_data['Self_Employed_Yes'] = 1
if property_area == 'Semiurban': input_data['Property_Area_Semiurban'] = 1
if property_area == 'Urban': input_data['Property_Area_Urban'] = 1

# Make prediction
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]
# Display result
if prediction == 1:
    st.success(f"Loan Approved! (Approval Probability: {probability:.2%})")
else:
    st.error(f"Loan Rejected! (Approval Probability: {probability:.2%})")