import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon='🚶‍♂️',
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "# This is hacktiv8 FTDS milestone 1 Phase 2."
    }
)
selected = st.sidebar.selectbox('Select Page: ', ['Machine Learning Model', 'Business Insight'])

@st.cache(allow_output_mutation=True)
def load_data1():
    data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    data['SeniorCitizen'] = data['SeniorCitizen'].map({1:'Yes', 0:'No'})
    hasil = []
    for i in data['TotalCharges']:
        try:
            a = float(i)
            hasil.append(a)
        except:
            hasil.append(a)
    data['TotalCharges'] = hasil
    return data
df = load_data1()

if selected == 'Machine Learning Model':
    st.title('Telco Customer Churn Prediction')
    st.image('customer-churn-1024x662.jpg')
    col21, col22 = st.columns(2)
    with col21:
        monthly_charges = st.slider("Monthly Charges ($):", 0.00, 120.00, 100.00)
    with col22:
        tenure = st.slider("Tenure (months):", 0.00, 80.00, 2.00)

    col1, col2 = st.columns(2)
    with col1:
        partner = st.selectbox("Has partner?", ['No', 'Yes'])
    with col2:
        senior_citizen = st.selectbox("Senior Citizen", ['No', 'Yes'])

    col3, col4 = st.columns(2)   
    with col3:
        dependents = st.selectbox("Has dependents?", ['No', 'Yes'])
    with col4:
        multiple_lines = st.selectbox("Has multiple lines?", ['No', 'No phone service','Yes'])

    col5, col6 = st.columns(2)
    with col5:
        internet_service = st.selectbox("Has internet service?", ['No', 'DSL','Fiber optic'])
    with col6:
        online_security = st.selectbox("Has online security?", ['No', 'No internet service','Yes'])

    col7, col8 = st.columns(2)
    with col7:
        online_backup = st.selectbox("Has online backup?", ['No', 'No internet service','Yes'])
    with col8:
        device_protection = st.selectbox("Has device protection?", ['No', 'No internet service','Yes'])

    col9, col10 = st.columns(2)
    with col9:
        tech_support = st.selectbox("Has tech support?", ['No', 'No internet service','Yes'])
    with col10:
        streaming_tv = st.selectbox("Has streaming tv?", ['No', 'No internet service','Yes'])

    col11, col12 = st.columns(2)
    with col11:
        streaming_movies = st.selectbox("Has streaming movies?", ['No', 'No internet service','Yes'])
    with col12:
        contract = st.selectbox("Contract type:", ['Month-to-month', 'One year','Two year'])

    col13, col14 = st.columns(2)
    with col13:
        paperless_billing = st.selectbox("Paperless billing:", ['No', 'Yes'])
    with col14:
        payment_method = st.selectbox("Payment method:", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])

    # inference
    data = [senior_citizen, partner, dependents, tenure, multiple_lines, internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv,
            streaming_movies, contract, paperless_billing, payment_method, monthly_charges]

    columns = ['SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'MultipleLines',
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
        'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges']

    data_inf = {}
    for i in range(len(data)):
        data_inf[columns[i]] = data[i]

    URL = "https://telco-churn-backend-fadlil.herokuapp.com/churn"

    if st.button('Predict'):
        r = requests.post(URL, json=data_inf)
        hasil = r.json()['result']
        if hasil<0.5:
            st.title('This customer will stay.')
        else:
            st.title('This customer will leave.')

elif selected == 'Business Insight':
    st.title('Telco Customers Insight')

    if st.checkbox('Show Dataframe'):
        st.subheader('Telco Customer Dataset')
        st.write(df.head())
    
    st.subheader('1. Number of Churn and Non-Churn Customers')
    buat_pie = df['Churn'].value_counts().reset_index()
    fig11 = px.pie(buat_pie,values='Churn',names='index',title='Customer Churn & Non-Churn Percentage',hole=.4,height=500,width=500)
    fig11.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(fig11)

    st.subheader('2. Customer Demographics')
    i = st.selectbox('Column :', ['gender','SeniorCitizen','Partner','Dependents','PhoneService','MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaperlessBilling','PaymentMethod'])
    category=df[i].unique().tolist()
    category.sort()
    churn = pd.crosstab(df[i], df['Churn']).reset_index()['Yes'].tolist()
    not_churn = pd.crosstab(df[i], df['Churn']).reset_index()['No'].tolist()
    fig = go.Figure(data=[
        go.Bar(name='Not Churn', x=category, y=not_churn, text=not_churn, textposition='auto'),
        go.Bar(name='Churn', x=category, y=churn, text=churn, textposition='auto')
            ])
    fig.update_layout(yaxis_title='Number of Customers',xaxis_title=i, barmode='group',height=600,width=800, title='Customer Demographics by '+i+' Column')
    st.plotly_chart(fig)

    st.subheader('3. Charges and Tenure')
    j = st.selectbox('Charges or Tenure?', ['tenure', 'MonthlyCharges', 'TotalCharges'])
    lihat = df.groupby('Churn')[[j]].mean().reset_index()
    fig3 = px.bar(lihat,y='Churn',x=j,color='Churn',height=500,width=750, text_auto='.2s')
    fig3.update_layout(xaxis_title=j,yaxis_title='Churn?', showlegend = False)
    st.plotly_chart(fig3)
    if st.checkbox('Show Distribution'):
        fig, ax = plt.subplots(figsize=(5,3))
        a = df[df.Churn=='Yes'][j]
        b = df[df.Churn=='No'][j]
        ax.hist(a, alpha=0.5, label='Churn')
        ax.hist(b, alpha=0.5, label='Not Churn')
        ax.set_title(j+' Distribution')
        ax.legend()
        st.pyplot(fig)
