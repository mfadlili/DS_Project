import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="H&M 2020 Online Store Analysis",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "# This is hacktiv8 FTDS final project."
    }
)
selected = st.sidebar.selectbox('Select Page: ', ['Business Overview', 'RFM'])


@st.cache(allow_output_mutation=True)
def load_data1():
    data = pd.read_csv('eda_2020_ready_sample10%.csv')
    return data

@st.cache(allow_output_mutation=True)
def load_data2():
    data = pd.read_csv('rfm_2020_sample.csv')
    return data

eda_2020 = load_data1()
rfm_2020 = load_data2()

eda_2020['month'] = pd.to_datetime(eda_2020['t_dat']).dt.month
join_2020 = pd.merge(eda_2020,rfm_2020[['customer_id','Clusters', 'r_clust', 'rf_clust']],on='customer_id',how='inner')

if selected == 'Business Overview':
    st.title('H&M 2020 Online Store Business Review')
    st.title('')
    col1, col2, col3 = st.columns(3)

    def total_sales():
        total_price = round(eda_2020['price'].sum())
        st.metric(label="Total Sales", value=total_price, delta='-28%')

    def quantity():
        quant = eda_2020['price'].count()
        st.metric(label="Total Quantity Sold", value=quant, delta='-27%')

    def customer():
        total_cust = eda_2020.groupby('customer_id')['t_dat'].count().shape[0]
        st.metric(label="Total Active Customer", value=total_cust, delta='9.4%')

    with col1:
        total_sales()

    with col2:
        quantity()

    with col3:
        customer()

    st.title('')


    customer_growth = eda_2020.groupby('month')[['customer_id']].nunique().reset_index()
    percent = [0]
    for i in range(1,9):
        a = (customer_growth['customer_id'][i] - customer_growth['customer_id'][i-1] ) / customer_growth['customer_id'][i-1] * 100
        percent.append(a)
    customer_growth['growth_percentage'] = percent

    col1,col2 = st.columns([1,1])
    with col1:
        st.markdown("<h2 style='text-align: center; color: black;'>Monthly Active Customer</h2>", unsafe_allow_html=True)
        fig1= px.line(data_frame=customer_growth,x='month',y='customer_id',markers=True,height=500,width=700)
        fig1.add_bar(x=customer_growth['month'].tolist(),y=customer_growth['customer_id'].tolist())
        fig1.update_layout(xaxis_title='Month',yaxis_title=' ', showlegend = False)
        fig1.update_traces(marker_color='#5aa17f')
        st.plotly_chart(fig1)
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Customer Growth Each Month (Percent)</h2>", unsafe_allow_html=True)
        fig2 = px.bar(customer_growth,x='month',y='growth_percentage',height=500,width=700, text_auto=True)
        fig2.update_traces(marker_color='#5aa17f')
        fig2.update_layout(xaxis_title='Month',yaxis_title=' ')
        st.plotly_chart(fig2)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("<h2 style='text-align: center; color: black;'>Top 10 Product Sales</h2>", unsafe_allow_html=True)
        list_month = ['All Months', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']
        list_index = ['All Categories']
        for i in eda_2020[['index_name']].value_counts().reset_index().index_name.tolist():
            list_index.append(i)
        month = st.selectbox('Month :', list_month)
        index = st.selectbox('Wear Categories', list_index)
        month_num = [i for i in range(0,10)]
        dict_month = dict(zip(list_month, month_num))

        if month == 'All Months':
            if index=='All Categories':
                top_10_categories = eda_2020.groupby(['product_type_name'])['t_dat'].count().reset_index(name='qty_sold').sort_values(by='qty_sold',ascending=False)
                top_10_categories = top_10_categories.head(10).sort_values(by='qty_sold',ascending=False)
                fig3 = px.bar(top_10_categories,y='product_type_name',x='qty_sold',color='product_type_name',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
                fig3.update_layout(xaxis_title='Qty Sold',yaxis_title=' ', showlegend = False)
                st.plotly_chart(fig3)                
            else:
                top_10_categories = eda_2020[(eda_2020.index_name==index)].groupby(['product_type_name'])['t_dat'].count().reset_index(name='qty_sold').sort_values(by='qty_sold',ascending=False)
                top_10_categories = top_10_categories.head(10).sort_values(by='qty_sold',ascending=False)
                fig3 = px.bar(top_10_categories,y='product_type_name',x='qty_sold',color='product_type_name',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
                fig3.update_layout(xaxis_title='Qty Sold',yaxis_title=' ', showlegend = False)
                st.plotly_chart(fig3)                

        else:
            if index=='All Categories':
                top_10_categories = eda_2020[eda_2020.month==dict_month[month]].groupby(['product_type_name'])['t_dat'].count().reset_index(name='qty_sold').sort_values(by='qty_sold',ascending=False)
                top_10_categories = top_10_categories.head(10).sort_values(by='qty_sold',ascending=False)
                fig3 = px.bar(top_10_categories,y='product_type_name',x='qty_sold',color='product_type_name',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750)
                fig3.update_layout(xaxis_title='Qty Sold',yaxis_title=' ', showlegend = False)
                st.plotly_chart(fig3)
            else:
                top_10_categories = eda_2020[(eda_2020.month==dict_month[month]) & (eda_2020.index_name==index)].groupby(['product_type_name'])['t_dat'].count().reset_index(name='qty_sold').sort_values(by='qty_sold',ascending=False)
                top_10_categories = top_10_categories.head(10).sort_values(by='qty_sold',ascending=False)
                fig3 = px.bar(top_10_categories,y='product_type_name',x='qty_sold',color='product_type_name',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750)
                fig3.update_layout(xaxis_title='Qty Sold',yaxis_title=' ', showlegend = False)
                st.plotly_chart(fig3)

    with col5:
        st.markdown("<h2 style='text-align: center; color: black;'>Age Distribution</h2>", unsafe_allow_html=True)
        list_index = ['All Categories']
        for i in join_2020[['index_name']].value_counts().reset_index().index_name.tolist():
            list_index.append(i)
        index2 = st.selectbox('Wear Categories  ', list_index)
        st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
        if index2=='All Categories':
            age_distribution = join_2020[['customer_id','age']].drop_duplicates()
            counts, bins = np.histogram(age_distribution.age, bins=range(15, 85, 3))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig5 = px.bar(x=bins, y=counts, labels={'x':'age', 'y':'count'},height=500,width=700)
            fig5.update_traces(marker_color='#5aa17f')
            fig5.update_layout(xaxis_title='Age',yaxis_title='Count')
            st.plotly_chart(fig5)       
        else :
            age_distribution = join_2020[join_2020['index_name']==index2][['customer_id','age']].drop_duplicates()
            counts, bins = np.histogram(age_distribution.age, bins=range(15, 85, 3))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig4 = px.bar(x=bins, y=counts, labels={'x':'age', 'y':'count'},height=500,width=700)
            fig4.update_traces(marker_color='#5aa17f')
            fig4.update_layout(xaxis_title='Age',yaxis_title='Count')
            st.plotly_chart(fig4)

if selected == 'RFM':
    st.title('H&M 2020 Online Store RFM Analysis')
    st.title('')

    st.markdown("<h2 style='text-align: left; color: black;'>1. Recency Segmentation</h2>", unsafe_allow_html=True)
    st.subheader('')

    col1, col2 = st.columns(2)

    with col1:
        counts, bins = np.histogram(rfm_2020.Recency, bins=range(0, 276, 2))
        bins = 0.5 * (bins[:-1] + bins[1:])
        st.markdown("<h3 style='text-align: center; color: black;'>Recency Distribution</h3>", unsafe_allow_html=True)
        fig11 = px.bar(x=bins, y=counts, labels={'x':'Recency', 'y':'count'},height=500,width=700)
        fig11.update_traces(marker_color='#6EBF8B')
        fig11.update_layout(xaxis_title='Recency (days since last transaction)',yaxis_title='Total Customers')
        fig11.add_vline(30, line_dash = 'dash', line_color='blue')
        fig11.add_vline(75, line_dash = 'dash', line_color='blue')
        fig11.add_vline(150, line_dash = 'dash', line_color='blue')
        fig11.add_vrect(x0=0, x1=30, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Active: 31%")
        fig11.add_vrect(x0=30, x1=75, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Warm: 27%")
        fig11.add_vrect(x0=75, x1=150, line_width=0, fillcolor="blue", opacity=0.1, annotation_text="Cold: 22%")
        fig11.add_vrect(x0=150, x1=276, line_width=0, fillcolor="black", opacity=0.1, annotation_text="Inactive: 20%")
        st.plotly_chart(fig11)
    
    with col2:
        st.markdown("<h3 style='text-align: center; color: black;'>Explanation</h3>", unsafe_allow_html=True)
        st.subheader('')
        st.subheader('')
        st.write('1. Active Customers   : Customers that make the last transaction for less than or equal to 30 days.')
        st.write('2. Warm Customers     : Customers that make the last transaction between 30 and 75 days.')
        st.write('3. Cold Customers     : Customers that make the last transaction between 75 and 150 days.')
        st.write('4. Inactive Customers : Customers that make the last transaction for more than 150 days.')
    
    st.markdown("<h2 style='text-align: left; color: black;'>2. Cluster Characteristics based on Frequency and Monetary (Customer Value Segmentation)</h2>", unsafe_allow_html=True)
    st.write('From the clustering method using K-Means, we got 4 different customer clusters or groups.')
    col3, col4 = st.columns(2)
    with col3:
        i = st.selectbox('Frequency or Monetary? :', ['Frequency', 'Monetary'])
        lihat = rfm_2020.groupby('Clusters')[['Recency','Frequency', 'Monetary']].mean()[[i]].reset_index()
        lihat['Clusters'] = lihat['Clusters'].astype(str)
        fig12 = px.bar(lihat,x='Clusters',y=i,height=500,width=700, text_auto='.2s')
        fig12.update_traces(marker_color='#5aa17f')
        fig12.update_layout(yaxis_title=i,title='Average '+i+' per Cluster')
        st.plotly_chart(fig12)
    with col4:
        st.subheader('')
        st.subheader('')
        st.subheader('')       
        st.markdown("<h3 style='text-align: left; color: black;'>What can we conclude from graph beside?</h3>", unsafe_allow_html=True)
        st.write("""
        1. Cluster 1 shows the highest values both Frequency and Monetary, it means the customer in this cluster have very high purchasing power and make transactions very often. So we named it as 'Ultra High' customer.
        2. Cluster 2 shows the slightly lower than Cluster 1 both Frequency and Monetary, it means the customer in this cluster have high purchasing power and make transactions quite often. So we named it as 'High' customer.
        3. Cluster 0 shows the medium values both Frequency and Monetary, it means the customer in this cluster have medium purchasing power and make transactions less often. So we named it as 'Common' customer.
        4. Cluster 3 shows the lowest values both Frequency and Monetary, it means the customer in this cluster have low purchasing power and make transactions rarely. So we named it as 'Low' customer.
        """)
    
    st.markdown("<h2 style='text-align: left; color: black;'>3. Segmentation Result</h2>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.subheader('')
        st.subheader('')
        a = pd.crosstab(rfm_2020.r_clust, rfm_2020.rf_clust, normalize=True)*100
        a = a[['Ultra High', 'High', 'Common', 'Low']]
        a = a.reindex(['inactive', 'cold', 'warm', 'active'])
        fig13 = px.imshow(a, text_auto=True, color_continuous_scale='Darkmint',height=600,width=600)
        fig13.update_layout(yaxis_title='', xaxis_title='')
        st.plotly_chart(fig13)
    with col6:
        pilih = st.selectbox('Choose Segmentation :', ['Recency', 'Customer Value'])
        pilih_dict = {'Recency':'r_clust', 'Customer Value':'rf_clust'}
        buat_pie = rfm_2020[[pilih_dict[pilih]]].value_counts().reset_index()
        fig14 = px.pie(buat_pie,values=0,names=pilih_dict[pilih],title='Customer Segment Percentage',hole=.4,height=500,width=550, color_discrete_sequence=px.colors.sequential.Darkmint)
        fig14.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig14)

    col7, col8 = st.columns(2)
    with col7:
        st.markdown("<h3 style='text-align: center; color: black;'>Monetary based on Customer Segmentation</h3>", unsafe_allow_html=True)
        pilih = st.selectbox('Choose Segmentation  :', ['Recency', 'Customer Value'])
        pilih_dict = {'Recency':'r_clust', 'Customer Value':'rf_clust'}
        buat_pie2 = rfm_2020.groupby(pilih_dict[pilih])[['Monetary']].sum().reset_index()
        fig15 = px.treemap(buat_pie2, path=[pilih_dict[pilih]], values='Monetary',height=700,width=700, color_discrete_sequence=px.colors.sequential.Darkmint)
        fig15.update_traces(textinfo='label+value+percent root')
        st.plotly_chart(fig15)
    with col8:
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.markdown("<h3 style='text-align: left; color: black;'>Business Insight</h3>", unsafe_allow_html=True)
        st.subheader('')
        st.write("""
        1. The result from segmentation based on the Recency showed that almost 59% of customers are cold and inactive. It doesn't look good, yet this group only contributes 35% of total earnings. Meanwhile, the customers in the ‘Active’ and ‘Warm’ area provide better income with 65% of total earnings. 
        2. Based on the customer value segmentation, almost 46% of customers stay in ‘Low’ categories, yet almost 80% of our total revenue comes from customers with ‘Ultra High’ and ‘High’ Segmentation.
        """)
    st.markdown("<h3 style='text-align: left; color: black;'>Age Segmentation</h3>", unsafe_allow_html=True)
    inside3, inside4 = st.columns(2)
    with inside3:
        i = st.selectbox('Recency Segmentation  :', ['All', 'active', 'warm', 'inactive', 'cold'])
    with inside4:
        j = st.selectbox('Customer Value Segmentation  :', ['All', 'Ultra High', 'High', 'Low', 'Common'])
    
    col9, col10 = st.columns(2)
    with col9:
        join_2020['age_segment'] = join_2020.age.apply(lambda x: 'Gen Z' if x<=23 else 'Millenials' if x<=39 else 'Gen X' if x<=55 else 'Baby Boomers' if x<=74 else 'Traditionals')
        buat_age = join_2020.drop_duplicates(subset='customer_id')
        if i=='All' and j=='All':
            umur1 = buat_age['age_segment'].value_counts().reset_index()
            fig16 = px.bar(umur1,y='index',x='age_segment',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig16.update_layout(xaxis_title='Number of Customers',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig16)
        elif j=='All':
            umur2 = buat_age[buat_age.r_clust==i]['age_segment'].value_counts().reset_index()
            fig17 = px.bar(umur2,y='index',x='age_segment',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig17.update_layout(xaxis_title='Number of Customers',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig17)
        elif i=='All':
            umur3 = buat_age[buat_age.rf_clust==j]['age_segment'].value_counts().reset_index()
            fig18 = px.bar(umur3,y='index',x='age_segment',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig18.update_layout(xaxis_title='Number of Customers',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig18)
        else:
            umur4 = buat_age[(buat_age.r_clust==i)&(buat_age.rf_clust==j)].age_segment.value_counts().reset_index()
            fig19 = px.bar(umur4,y='index',x='age_segment',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig19.update_layout(xaxis_title='Number of Customers',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig19)
    with col10:
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.markdown("<h3 style='text-align: left; color: black;'>Explanation</h3>", unsafe_allow_html=True)
        st.write("""
        From the graph, it can be seen that the majority of H&M customers are Millennials, followed by Generations Z and X, regardless of their customer type, both in terms of Recency and Customer Value.
        """)

    st.markdown("<h3 style='text-align: left; color: black;'>Top 10 Products by Customers Segmentation</h3>", unsafe_allow_html=True)
    inside1, inside2 = st.columns(2)
    with inside1:
        i = st.selectbox('Recency Segmentation   :', ['All', 'active', 'warm', 'inactive', 'cold'])
    with inside2:
        j = st.selectbox('Customer Value Segmentation   :', ['All', 'Ultra High', 'High', 'Low', 'Common'])

    col11, col12 = st.columns(2)
    with col11:
        if i=='All' and j=='All':
            index1 = join_2020.product_type_name.value_counts().reset_index().head(10)
            fig20 = px.bar(index1,y='index',x='product_type_name',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig20.update_layout(xaxis_title='Number of Apparel Categories Sold',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig20)
        elif i=='All':
            index2 = join_2020[join_2020.rf_clust==j].product_type_name.value_counts().reset_index().head(10)
            fig21 = px.bar(index2,y='index',x='product_type_name',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig21.update_layout(xaxis_title='Number of Apparel Categories Sold',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig21)
        elif j=='All':
            index3 = join_2020[join_2020.r_clust==i].product_type_name.value_counts().reset_index().head(10)
            fig22= px.bar(index3,y='index',x='product_type_name',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig22.update_layout(xaxis_title='Number of Apparel Categories Sold',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig22)
        else:
            index4 = join_2020[(join_2020.rf_clust==j)&(join_2020.r_clust==i)].product_type_name.value_counts().reset_index().head(10)
            fig23= px.bar(index4,y='index',x='product_type_name',color='index',color_discrete_sequence=px.colors.sequential.Darkmint,height=500,width=750, text_auto='.2s')
            fig23.update_layout(xaxis_title='Number of Apparel Categories Sold',yaxis_title=' ', showlegend = False)
            st.plotly_chart(fig23)  
    with col12:
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.subheader('')
        st.markdown("<h3 style='text-align: left; color: black;'>Explanation</h3>", unsafe_allow_html=True)
        st.write("""
        Based on the visualization provided, both on the business overview or rfm page, it appears that regardless of the segmentation, this type of product is indeed the most popular (can be seen on the business overview page). So, it can be concluded that when people shop at H&M, especially via online stores, it is the top 10 items that are most in demand.
        """)