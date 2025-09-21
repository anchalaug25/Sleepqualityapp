import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Sleep Quality Prediction")

st.write("Enter the following details to predict your Sleep Quality:")

# Numeric inputs
age = st.number_input("Age", min_value=0)
coffee_intake = st.number_input("Coffee Intake (cups)", min_value=0)
caffeine_mg = st.number_input("Caffeine mg", min_value=0)
sleep_hours = st.number_input("Sleep Hours", min_value=0)
bmi = st.number_input("BMI", min_value=0.0, step=0.1)
heart_rate = st.number_input("Heart Rate", min_value=0)
stress_level = st.number_input("Stress Level (1-10)", min_value=0)
physical_activity = st.number_input("Physical Activity Hours", min_value=0)

# Categorical inputs (converted to 0/1 dummy format)
gender = st.selectbox("Gender", ["Male", "Other", "Female"])
smoking = st.selectbox("Smoking", ["Yes", "No"])
alcohol = st.selectbox("Alcohol Consumption", ["Yes", "No"])
country = st.selectbox("Country", ["Belgium","Brazil","Canada","China","Finland",
                                   "France","Germany","India","Italy","Japan","Mexico",
                                   "Netherlands","Norway","South Korea","Spain","Sweden",
                                   "Switzerland","UK","USA"])

# Convert categorical inputs to 0/1 (dummy)
gender_male = 1 if gender == "Male" else 0
gender_other = 1 if gender == "Other" else 0
smoking_val = 1 if smoking == "Yes" else 0
alcohol_val = 1 if alcohol == "Yes" else 0

# Country dummies
country_list = ["Belgium","Brazil","Canada","China","Finland","France","Germany","India",
                "Italy","Japan","Mexico","Netherlands","Norway","South Korea","Spain",
                "Sweden","Switzerland","UK","USA"]
country_dummies = [1 if country==c else 0 for c in country_list]

# When user clicks Predict
if st.button("Predict Sleep Quality"):
    input_data = [age, coffee_intake, caffeine_mg, sleep_hours, bmi, heart_rate, 
                  stress_level, physical_activity, smoking_val, alcohol_val, gender_male, gender_other] + country_dummies
    input_df = pd.DataFrame([input_data], columns=['Age', 'Coffee_Intake', 'Caffeine_mg', 'Sleep_Hours',
                                                   'BMI', 'Heart_Rate', 'Stress_Level', 'Physical_Activity_Hours',
                                                   'Smoking', 'Alcohol_Consumption', 'Gender_Male', 'Gender_Other'] + 
                                                   [f"Country_{c}" for c in country_list])
    
    prediction = model.predict(input_df)
    st.success(f"Predicted Sleep Quality: {prediction[0]:.2f}")
