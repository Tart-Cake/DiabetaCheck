# app.py
import streamlit as st
import pickle
import numpy as np

# Load trained model
@st.cache_resource
def load_model():
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def main():
    st.set_page_config(page_title="Diabetes Predictor", layout="centered")
    
    # Header
    st.title("Diabetes Risk Assessment")
    st.write("Enter your health information to assess diabetes risk")
    
    # Load model
    model = load_model()
    
    # Input Section
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age (years)", min_value=18, max_value=120, step=1)
            sex = st.radio("Gender", ["Male", "Female"])
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, step=0.1)
            hba1c = st.number_input("HbA1c Level", min_value=3.0, max_value=15.0, step=0.1)
            
        with col2:
            hypertension = st.radio("Hypertension", ["No", "Yes"])
            heart_disease = st.radio("Heart Disease", ["No", "Yes"])
            smoking = st.selectbox("Smoking History", [
                "Never smoked",
                "Former smoker",
                "Not current smoker",
                "Current smoker",
                "No information"
            ])
            glucose = st.number_input("Blood Glucose (mg/dL)", min_value=50, max_value=300, step=1)
        
        # Prediction button
        submitted = st.form_submit_button("Assess Risk")
    
    # Process inputs when form is submitted
    if submitted:
        try:
            # Convert inputs to model format
            inputs = [
                age,
                1 if sex == "Male" else 0,
                bmi,
                1 if hypertension == "Yes" else 0,
                1 if heart_disease == "Yes" else 0,
                {"Never smoked":4, "Former smoker":3, 
                 "Not current smoker":2, "Current smoker":1,
                 "No information":0}[smoking],
                hba1c,
                glucose
            ]
            
            # Make prediction
            prediction = model.predict(np.array(inputs).reshape(1, -1))[0]
            
            # Show results
            if prediction == 1:
                st.error("High Risk: Clinical indicators suggest potential diabetes risk")
            else:
                st.success("Low Risk: No significant diabetes indicators detected")
                
        except Exception as e:
            st.warning(f"Error processing request: {str(e)}")

if __name__ == "__main__":
    main()