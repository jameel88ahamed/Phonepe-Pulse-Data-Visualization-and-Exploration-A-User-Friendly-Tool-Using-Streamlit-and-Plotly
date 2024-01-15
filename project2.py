#REQUIRED LIBRARIES
import json
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from PIL import Image

#TABLE CREATION
mydb=psycopg2.connect(host='localhost',
                        user='postgres',
                        password='Jameel123',
                        database='phonepe_data',
                        port='5432')
cursor=mydb.cursor()

#Aggregated_insurance Table
cursor.execute('select * from aggregated_insurance')
mydb.commit()
table7=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table7, columns = ('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))

#Aggregated_transaction Table
cursor.execute('select * from aggregated_transaction')
mydb.commit()
table1=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table1, columns = ('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))

#Aggregated_user Table
cursor.execute('select * from aggregated_user')
mydb.commit()
table2=cursor.fetchall()

Aggre_user=pd.DataFrame(table2, columns=('States', 'Years', 'Quarter', 'Brands', 'Transaction_count', 'Percentage'))

#Map_Insurance Table
cursor.execute('select * from map_insurance')
mydb.commit()
table8=cursor.fetchall()

Map_insurance=pd.DataFrame(table8, columns=('States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount'))

#Map_Transaction Table
cursor.execute('select * from map_transaction')
mydb.commit()
table3=cursor.fetchall()

Map_transaction=pd.DataFrame(table3, columns=('States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount'))

#Map_user Table
cursor.execute('select * from map_user')
mydb.commit()
table4=cursor.fetchall()

Map_user=pd.DataFrame(table4, columns=('States', 'Years', 'Quarter', 'Districts', 'RegisteredUser', 'AppOpens'))

#Top_insurance Table
cursor.execute('select * from top_insurance')
mydb.commit()
table9=cursor.fetchall()

Top_insurance=pd.DataFrame(table9, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount'))

#Top_transaction Table
cursor.execute('select * from top_transaction')
mydb.commit()
table5=cursor.fetchall()

Top_transaction=pd.DataFrame(table5, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount'))

#Top_user Table
cursor.execute('select * from top_user')
mydb.commit()
table6=cursor.fetchall()

Top_user=pd.DataFrame(table6, columns=('States', 'Years', 'Quarter', 'Pincodes', 'RegisteredUsers'))

#FUNCTION FOR DISPLAYING TRANSACTION COUNT AND AMOUNT YEAR WISE IN BAR AND GEO VISUALIZATION
def Year_wise_transaction(df, year):
    aiy = df[df['Years'] == year]
    aiy.reset_index(drop=True, inplace=True)

    aiyg = aiy.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
    aiyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(aiyg, x='States', y='Transaction_amount', title=f'{year} TRANSACTION AMOUNT',
                            width=600, height=650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        aiyg.States = states_name_tra

        fig_india_1 = px.choropleth(aiyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="thermal",
                                    range_color=(aiyg["Transaction_amount"].min(), aiyg["Transaction_amount"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION AMOUNT",
                                    fitbounds="locations", width=700, height=700)
        fig_india_1.update_geos(visible=False)

        st.plotly_chart(fig_india_1)

    with col2:
        fig_count = px.bar(aiyg, x='States', y='Transaction_count', title=f'{year} TRANSACTION COUNTS',
                           width=600, height=650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

        fig_india_2 = px.choropleth(aiyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="thermal",
                                    range_color=(aiyg["Transaction_count"].min(), aiyg["Transaction_count"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION COUNTS",
                                    fitbounds="locations", width=700, height=700)
        fig_india_2.update_geos(visible=False)

        st.plotly_chart(fig_india_2)

    return aiy

#FUNCTION FOR DISPLAYING TRANSACTION COUNT AND AMOUNT QUARTER WISE IN BAR AND GEO VISUALIZATION
def Quarter_wise_transaction(df,quarter):
    aiyq=df[df['Quarter']==quarter]
    aiyq.reset_index(drop=True,inplace=True)

    aiyqg=aiyq.groupby('States')[['Transaction_count', 'Transaction_amount']].sum()
    aiyqg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_q_amount)
    with col2:
        fig_q_count=px.bar(aiyqg, x='States', y='Transaction_count', title=f"{aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION COUNTS", width=600, height=650,
                           color_discrete_sequence=px.colors.sequential.Darkmint_r)
        st.plotly_chart(fig_q_count)

    col1,col2=st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        aiyqg['States'] = states_name_tra[:len(aiyqg)]

        fig_india_q_1=px.choropleth(aiyqg, geojson=data1, locations='States', featureidkey='properties.ST_NM',
                                    color='Transaction_amount', color_continuous_scale='Sunsetdark',
                                    range_color=(aiyqg['Transaction_amount'].min(), aiyqg['Transaction_amount'].max()),
                                    hover_name='States', title=f"{aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION AMOUNT",
                                    fitbounds='locations', width=700, height=700)
        fig_india_q_1.update_geos(visible=False)
        st.plotly_chart(fig_india_q_1)

    with col2:
        fig_india_q_2=px.choropleth(aiyqg, geojson=data1, locations='States', featureidkey='properties.ST_NM',
                                    color='Transaction_count', color_continuous_scale='Sunsetdark',
                                    range_color=(aiyqg['Transaction_count'].min(), aiyqg['Transaction_count'].max()),
                                    hover_name='States', title=f"{aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION COUNTS",
                                    fitbounds='locations', width=700, height=700)
        fig_india_q_2.update_geos(visible=False)
        st.plotly_chart(fig_india_q_2)

    return aiyq

#FUNCTION FOR DISPLAYING TRANSACTION TYPES
def Aggre_transaction_type(df, state):
    df_state=df[df['States']==state]
    df_state.reset_index(drop=True, inplace=True)

    agttg=df_state.groupby('Transaction_type')[['Transaction_count', 'Transaction_amount']].sum()
    agttg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_hbar_1=px.bar(agttg, x='Transaction_amount', y='Transaction_type', orientation='h',
                          color_discrete_sequence=px.colors.sequential.Aggrnyl, width=600,
                          title=f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height=500)
        st.plotly_chart(fig_hbar_1)

    with col2:
        fig_hbar_2=px.bar(agttg, x='Transaction_count', y='Transaction_type', orientation='h',
                          color_discrete_sequence=px.colors.sequential.Greens_r, width=600,
                          title=f"{state.upper()} TRANSACTION TYPE AND TRANSACTION COUNTS", height=500)
        st.plotly_chart(fig_hbar_2)

#FUNCTION FOR DISPLAYING AGGREGATED USER PLOTS
#YEAR WISE
def Aggre_user_plot_1(df,year):
    aguy=df[df['Years']==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby('Brands')['Transaction_count'].sum())
    aguyg.reset_index(inplace=True)

    fig_line_1=px.bar(aguyg, x='Brands', y='Transaction_count', title=f"{year} BRANDS AND TRANSACTION COUNTS",
                      width=1000, color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

#QUARTER WISE
def Aggre_user_plot_2(df,quarter):
    auqs=df[df['Quarter']==quarter]
    auqs.reset_index(drop=True, inplace=True)

    fig_pie_1=px.pie(data_frame=auqs, names='Brands', values='Transaction_count', hover_data='Percentage',
                     width=1000, title=f"{quarter} QUARTER TRANSACTION COUNTS WITH PERCENTAGE", hole=0.5, color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)
    return auqs

#STATE WISE
def Aggre_user_plot_3(df, state):
    aguqy=df[df['States']==state]
    aguqy.reset_index(drop=True, inplace=True)

    aguqyg=pd.DataFrame(aguqy.groupby('Brands')['Transaction_count'].sum())
    aguqyg.reset_index(inplace=True)

    fig_scatter_1=px.line(aguqyg, x='Brands', y='Transaction_count', markers=True, width=1000,
                          title= f"{state.upper()} BRAND V/S TRANSACTION COUNTS")
    st.plotly_chart(fig_scatter_1)

#FUNCTION FOR DISPLAYING MAP INSURANCE OR TRANSACTIONS IN BAR CHART
def map_insure_plot_1(df, state):
    miys=df[df['States']==state]
    miysg=miys.groupby('Districts')[['Transaction_count', 'Transaction_amount']].sum()
    miysg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_bar_1=px.bar(miysg, x='Districts', y='Transaction_amount',
                             width=600, height=500, title=f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                             color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_2=px.bar(miysg, x='Districts', y='Transaction_count',
                             width=600, height=500, title=f"{state.upper()} DISTRICTS TRANSACTION COUNTS",
                             color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_2)

#FUNCTION FOR DISPLAYING MAP INSURANCE OR TRANSACTIONS IN PIE CHART
def map_insure_plot_2(df, state):
    miys=df[df['States']==state]
    miysg=miys.groupby('Districts')[['Transaction_count', 'Transaction_amount']].sum()
    miysg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_pie_1=px.pie(miysg, names='Districts', values='Transaction_amount',
                             width=600, height=500, title=f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                             hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)
        st.plotly_chart(fig_map_pie_1)
    with col2:
        fig_map_pie_2=px.pie(miysg, names='Districts', values='Transaction_count',
                             width=600, height=500, title=f"{state.upper()} DISTRICTS TRANSACTION COUNTS",
                             hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_2)

#FUNCTION FOR DISPLAYING MAP USER PLOT YEAR WISE
def map_user_plot_1(df,year):
    muy=df[df['Years']==year]
    muy.reset_index(drop=True, inplace=True)

    muyg=muy.groupby('States')[['RegisteredUser', 'AppOpens']].sum()
    muyg.reset_index(inplace=True)

    fig_map_user_plot_1=px.line(muyg, x='States', y=['RegisteredUser', 'AppOpens'], markers=True,
                                width=1000, height=800, title=f"{year} REGISTERED USER AND APP OPENS", color_discrete_sequence=px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

#FUNCTION FOR DISPLAYING MAP USER PLOT QUARTER WISE
def map_user_plot_2(df,quarter):
    muyq=df[df['Quarter']==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg=muyq.groupby('States')[['RegisteredUser', 'AppOpens']].sum()
    muyqg.reset_index(inplace=True)

    fig_map_user_plot_2=px.line(muyqg, x='States', y=['RegisteredUser', 'AppOpens'], markers=True,
                                title=f"{df['Years'].min()}, {quarter} REGISTERED USERS AND APP OPENS",
                                width=1000, height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_2)

    return muyq

#FUNCTION FOR DISPLAYING MAP USER PLOT STATES WISE
def map_user_plot_3(df,state):
    muyqs=df[df['States']==state]
    muyqs.reset_index(drop=True, inplace=True)

    muyqsg=muyqs.groupby('Districts')[['RegisteredUser', 'AppOpens']].sum()
    muyqsg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_plot_3=px.bar(muyqsg, x='RegisteredUser', y='Districts', orientation='h',
                                   title=f"{state.upper()} REGISTERED USERS", height=800,
                                   color_discrete_sequence=px.colors.sequential.Viridis_r)
        st.plotly_chart(fig_map_user_plot_3)

#FUNCTION FOR DISPLAYING TOP USER YEAR WISE
def top_user_plot_1(df,year):
    tuy=df[df['Years']==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(['States', 'Quarter'])['RegisteredUsers'].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg, x='States', y='RegisteredUsers', barmode='group', color='Quarter',
                          width=1000, height=800, color_continuous_scale=px.colors.sequential.Emrld_r)
    st.plotly_chart(fig_top_plot_1)
    return tuy

#FUNCTION FOR DISPLAYING TOP USER STATE WISE
def top_user_plot_2(df,state):
    tuys=df[df['States']==state]
    tuys.reset_index(drop=True, inplace=True)

    tuysg=pd.DataFrame(tuys.groupby("Quarter")[["RegisteredUsers", "Pincodes"]].sum())
    tuysg.reset_index(inplace=True)

    fig_top_plot_2=px.bar(tuysg, x='Quarter', y='RegisteredUsers', barmode='group',
                        width=1000, height=800, color= "Pincodes", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Plasma_r)
    st.plotly_chart(fig_top_plot_2)
    return tuys

#STREAMLIT PART
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Jameel",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Jameel*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})
st.sidebar.header(":wave: :violet[**Hello! Welcome to PhonePe Data Analysis**]")

with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data","Top Charts"], 
                icons=["house","graph-up-arrow","bar-chart-line"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
if selected == "Home":
    st.image("img.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")

    st.write(" ")
    st.write(" ")
    st.markdown("### :violet[Domain :] Fintech")
    st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, PostgreSQL, Geo Visualizations, Streamlit, and Plotly.")
    st.markdown("### :violet[Overview :] In this streamlit web application you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

if selected == "Explore Data":
    tab1, tab2, tab3= st.tabs(["$\huge Aggregated Analysis $", "$\huge Map Analysis $", "$\huge Top Analysis $"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Aggregated Insurance Analysis", "Aggregated Transaction Analysis", "Aggregated User Analysis"])

        if method == "Aggregated Insurance Analysis":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider("**Select the Year for Aggregated Insurance**", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())

            df_agg_insur_Y= Year_wise_transaction(Aggre_insurance,years)

            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter for Aggregated Insurance**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(),df_agg_insur_Y["Quarter"].min())

            Quarter_wise_transaction(df_agg_insur_Y, quarters)

        elif method=="Aggregated Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year for Aggregated Transaction**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Year_wise_transaction(Aggre_transaction,years_at)

            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter for Aggregated Transaction**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Quarter_wise_transaction(df_agg_tran_Y, quarters_at)
            
            state_Y_Q= st.selectbox("**Select the State for Aggregated Transaction**",df_agg_tran_Y_Q["States"].unique())

            Aggre_transaction_type(df_agg_tran_Y_Q,state_Y_Q)

        elif method=='Aggregated User Analysis':
            year_au= st.selectbox("**Select the Year for Aggregated User**",Aggre_user["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Aggre_user,year_au)

            quarter_au= st.selectbox("**Select the Quarter for Aggregated User**",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State for Aggregated User**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the MAP Analysis Method**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_mi= st.slider("**Select the Year for Map Insurance**", Map_insurance["Years"].min(), Map_insurance["Years"].max(),Map_insurance["Years"].min())
            df_map_insur_Y= Year_wise_transaction(Map_insurance,years_mi)

            col1,col2= st.columns(2)
            with col1:
                state_mi= st.selectbox("Select the State for Map Insurance", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_mi)

            col1,col2= st.columns(2)
            with col1:
                quarters_mi= st.slider("**Select the Quarter for Map Insurance**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

            df_map_insur_Y_Q= Quarter_wise_transaction(df_map_insur_Y, quarters_mi)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State for Map Insurance 2", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

        elif method_map == "Map Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:
                years_mt=st.slider("**Select the Year for Map Transaction**", Map_transaction["Years"].min(), Map_transaction['Years'].max(), Map_transaction['Years'].min())

            df_map_trans_Y=Year_wise_transaction(Map_transaction, years_mt)

            col1,col2=st.columns(2)
            with col1:
                state_mt= st.selectbox("Select the State for Map Transaction", df_map_trans_Y["States"].unique())
            map_insure_plot_1(df_map_trans_Y, state_mt)

            col1,col2=st.columns(2)
            with col1:
                quarters_mt=st.slider("**Select the Quarter for Map Transaction**", df_map_trans_Y["Quarter"].min(), df_map_trans_Y["Quarter"].max(), df_map_trans_Y["Quarter"].min())

            df_map_trans_Y_Q=Quarter_wise_transaction(df_map_trans_Y, quarters_mt)

            col1,col2=st.columns(2)
            with col1:
                state_m3=st.selectbox("**Select the state for Map Transaction 2**", df_map_trans_Y_Q["States"].unique())
            map_insure_plot_2(df_map_trans_Y_Q, state_m3)

        elif method_map=="Map User Analysis":
            col1,col2=st.columns(2)
            with col1:
                year_mu=st.selectbox('**Select the Year for Map User**', Map_user['Years'].unique())
            map_user_Y=map_user_plot_1(Map_user,year_mu)

            col1,col2=st.columns(2)
            with col1:
                quarter_mu=st.selectbox('**Select the Quarter for Map User**', map_user_Y['Quarter'].unique())
            map_user_Y_Q=map_user_plot_2(map_user_Y, quarter_mu)

            col1,col2=st.columns(2)
            with col1:
                state_mu=st.selectbox('**Select the State for Map User**', map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu)

    with tab3:
        method_top=st.radio("**Select the method for TOP Analysis**", ['Top Insurance Analysis', 'Top Transaction Analysis', 'Top User Analysis'])

        if method_top=='Top Insurance Analysis':
            col1col2=st.columns(2)
            with col1:
                years_ti=st.slider('**Select the Year for Top Insurance**', Top_insurance['Years'].min(), Top_insurance['Years'].max(), Top_insurance['Years'].min())
            df_top_insur_Y=Year_wise_transaction(Top_insurance, years_ti)

            col1,col2=st.columns(2)
            with col1:
                quarters_ti=st.slider('**Select the Quarter for Top Insurance**', df_top_insur_Y['Quarter'].min(), df_top_insur_Y['Quarter'].max(), df_top_insur_Y['Quarter'].min())
            df_top_insur_Y_Q=Quarter_wise_transaction(df_top_insur_Y, quarters_ti)

        elif method_top=='Top Transaction Analysis':
            col1,col2=st.columns(2)
            with col1:
                years_tt=st.slider('**Select the Year for Top Transaction**', Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            df_top_tran_Y=Year_wise_transaction(Top_transaction, years_tt)

            col1,col2=st.columns(2)
            with col1:
                quarters_tt=st.slider('**Select the Quarter for Top Transaction**', df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(), df_top_tran_Y["Quarter"].min())
            df_top_tran_Y_Q=Quarter_wise_transaction(df_top_tran_Y, quarters_tt)

        elif method_top=='Top User Analysis':
            col1,col2=st.columns(2)
            with col1:
                year_tu=st.selectbox('**Select the Year for Top User**', Top_user['Years'].unique())
            df_top_user_Y=top_user_plot_1(Top_user, year_tu)

            col1,col2=st.columns(2)
            with col1:
                state_tu=st.selectbox('**Select the State for Top User**', df_top_user_Y['States'].unique())
            df_top_user_Y_S=top_user_plot_2(df_top_user_Y, state_tu)

if selected == "Top Charts":
    ques= st.selectbox("**Select the required question**",('Number of Top Brands Of Mobiles Used PhonePe','States With Lowest Trasaction Amount',
                                  'Top 10 Districts With Highest Transaction Amount','First 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=='Number of Top Brands Of Mobiles Used PhonePe':
        brand= Aggre_user[["Brands","Transaction_count"]]
        brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
        brand2= pd.DataFrame(brand1).reset_index()

        fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "TOP MOBILE BRANDS AND TRANSACTION COUNTS")
        st.plotly_chart(fig_brands)

    elif ques=="States With Lowest Trasaction Amount":
        lt= Aggre_transaction[["States", "Transaction_amount"]]
        lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
        lt2= pd.DataFrame(lt1).reset_index().head(10)

        fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION STATES with AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
        st.plotly_chart(fig_lts)

    elif ques=='Top 10 Districts With Highest Transaction Amount':
        htd= Map_transaction[["Districts", "Transaction_amount"]]
        htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
        htd2= pd.DataFrame(htd1).head(10).reset_index()

        fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
        st.plotly_chart(fig_htd)

    elif ques=='First 10 Districts With Lowest Transaction Amount':
        htd= Map_transaction[["Districts", "Transaction_amount"]]
        htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
        htd2= pd.DataFrame(htd1).head(10).reset_index()

        fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="LEAST 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_htd)

    elif ques=='Top 10 States With AppOpens':
        sa= Map_user[["States", "AppOpens"]]
        sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
        sa2= pd.DataFrame(sa1).reset_index().head(10)

        fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="TOP 10 STATES WITH APP OPENS",
                color_discrete_sequence= px.colors.sequential.deep_r)
        st.plotly_chart(fig_sa)

    elif ques=='Least 10 States With AppOpens':
        sa= Map_user[["States", "AppOpens"]]
        sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
        sa2= pd.DataFrame(sa1).reset_index().head(10)

        fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="LEAST 10 STAES WITH APP OPENS",
                color_discrete_sequence= px.colors.sequential.dense_r)
        st.plotly_chart(fig_sa)

    elif ques=='States With Lowest Trasaction Count':
        stc= Aggre_transaction[["States", "Transaction_count"]]
        stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
        stc2= pd.DataFrame(stc1).reset_index()

        fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNTS",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
        st.plotly_chart(fig_stc)

    elif ques=='States With Highest Trasaction Count':
        stc= Aggre_transaction[["States", "Transaction_count"]]
        stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
        stc2= pd.DataFrame(stc1).reset_index()

        fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNTS",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_stc)

    elif ques=='States With Highest Trasaction Amount':
        ht= Aggre_transaction[["States", "Transaction_amount"]]
        ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
        ht2= pd.DataFrame(ht1).reset_index().head(10)

        fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION STATES WITH AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
        st.plotly_chart(fig_lts)

    elif ques=='Top 50 Districts With Lowest Transaction Amount':
        dt= Map_transaction[["Districts", "Transaction_amount"]]
        dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
        dt2= pd.DataFrame(dt1).reset_index().head(50)

        fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_dt)