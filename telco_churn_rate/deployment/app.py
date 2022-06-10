import streamlit as st
import pickle
import pandas as pd
from tensorflow.keras.models import load_model

st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "# This is hacktiv8 FTDS milestone 1 Phase 2."
    }
)

st.title('Telco Customer Churn Prediction')

senior_citizen = st.selectbox("Senior Citizen", ['No', 'Yes'])
partner = st.selectbox("Has partner?", ['No', 'Yes'])
dependents = st.selectbox("Has dependents?", ['No', 'Yes'])
tenure = st.number_input("Tenure :", 0.00, None, 2.00)
multiple_lines = st.selectbox("Has multiple lines?", ['No', 'No phone service','Yes'])
internet_service = st.selectbox("Has internet service?", ['No', 'DSL','Fiber optic'])
online_security = st.selectbox("Has online security?", ['No', 'No internet service','Yes'])
online_backup = st.selectbox("Has online backup?", ['No', 'No internet service','Yes'])
device_protection = st.selectbox("Has device protection?", ['No', 'No internet service','Yes'])
tech_support = st.selectbox("Has tech support?", ['No', 'No internet service','Yes'])
streaming_tv = st.selectbox("Has streaming tv?", ['No', 'No internet service','Yes'])
streaming_movies = st.selectbox("Has streaming movies?", ['No', 'No internet service','Yes'])
contract = st.selectbox("Contract type:", ['Month-to-month', 'One year','Two year'])
paperless_billing = st.selectbox("Paperless billing:", ['No', 'Yes'])
payment_method = st.selectbox("Payment method:", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
monthly_charges = st.number_input("Monthly Charges :", 0.00, None, 100.00)

# inference
data = [senior_citizen, partner, dependents, tenure, multiple_lines, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv,
        streaming_movies, contract, paperless_billing, payment_method, monthly_charges]

columns = ['SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'MultipleLines',
       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
       'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
       'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges']

with open("prep_pipe.pkl", "rb") as f:
    prep_pipe_load = pickle.load(f)

model = load_model("telco_churn_model.h5")

if st.button('Predict'):
    df = pd.DataFrame([data], columns=columns)
    prep = prep_pipe_load.transform(df)
    result = model.predict(prep)
    if result>=0.5:
        st.title('This customer will leave')
    else:
        st.title('This customer will stay')
        