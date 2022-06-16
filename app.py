import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import joblib
from lime import lime_tabular
import streamlit.components.v1 as components
from load_css import local_css
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
local_css("style.css")


# Build app
title_text = 'LIME Explainer Dashboard'
subheader_text = '''Etude de solvabilité du client au prêt immobilier'''

st.markdown(f"<h2 style='text-align: center;'><b>{title_text}</b></h2>", unsafe_allow_html=True)
st.markdown(f"<h5 style='text-align: center;'>{subheader_text}</h5>", unsafe_allow_html=True)
st.text("")

path = r'/Users/Robin/DataScience/Projets/7_ImplémentezUnModèleDeScoring'
name = "interpretability_list.joblib"
interpretability_list = joblib.load(os.path.join(path, name))


# SELECTION DU CUSTOMER_ID
customer_id_list = np.arange(len(interpretability_list))
customer_id = st.selectbox('Please select the customer_ID to analyse :', customer_id_list)
st.write('You selected:', customer_id)
print("User selected the customer_id {}".format(customer_id))

# AFFICHAGE DU CLIENT
path_file = "/Users/Robin/DataScience/Projets/7_ImplémentezUnModèleDeScoring/X_test.joblib"
df = joblib.load(path_file)
st.dataframe(df.iloc[customer_id])

# PREDICTION
# using model from api
if customer_id != None :
    # Catch the model deployed in PythonAnyWhere
    url = 'https://rob128.pythonanywhere.com/api'
    r = requests.post(url=url, json={"customer_ID": str(customer_id)})
    response = r.json()
    # st.write(response["probabilite"])
    print("Probability {} \n Solvability {}".format(response["probabilite"], response["solvabilite"]))

    if response["solvabilite"] == 0:
        # st.write("The customer is solvent, with a probability of : {}".format(response["probabilite"]))
        t = "<div> <span class='highlight green'> The customer is solvent </span></div>"
        st.markdown(t, unsafe_allow_html=True)
        st.write("\n")
        st.write("With a probability of : {}%".format(response["probabilite"]*100))
    else:
        t = "<div> <span class='highlight red'> The customer is not solvent </span></div>"
        st.markdown(t, unsafe_allow_html=True)
        st.write("\n")
        st.write("With a probability of : {}%".format(response["probabilite"]*100))

    # INTERPRETABILITES
    if st.button("Explain Results"):
        with st.spinner('Calculating...'):
            html = interpretability_list[customer_id].as_html()
            components.html(html, height=800)

st.subheader("Below you can situate customer by plotting distribution.")
feature_selected = st.selectbox('Select a feature to plot', df.columns)
st.write('You selected:', feature_selected)

# PLOTTING
fig, ax = plt.subplots()
sns.histplot(data=df, x=feature_selected)
value2highlight = df.iloc[customer_id][feature_selected]
x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
for p in ax.patches :
    if abs(value2highlight - p.get_x()) == min(x_list):
        p.set_color('crimson')
ax.set_title("Distribution {}".format(feature_selected))
st.pyplot(fig)

# TOTAL DISTRIBUTION
# Features importances list : "CODE_GENDER", "NAME_INCOME_TYPE_Working"
# feat_imp_list = ["CODE_GENDER", "NAME_INCOME_TYPE_Working, "REG_CITY_NOT_WORK_CITY"]
# df["NAME_INCOME_TYPE_Working"].hist()
# plt.show()
# st.pyplot()
#
# fig, ax = plt.subplots()
# sns.histplot(data=df, x="EXT_SOURCE_3")
# value2highlight = df.iloc[customer_id]["EXT_SOURCE_3"]
# x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
# for p in ax.patches :
#     if abs(value2highlight - p.get_x()) == min(x_list):
#         p.set_color('crimson')
# ax.set_title("Distribution EXT_SOURCE_3")
# st.pyplot(fig)
#
#
# fig, ax = plt.subplots()
# sns.histplot(data=df, x="EXT_SOURCE_2")
# value2highlight = df.iloc[customer_id]["EXT_SOURCE_2"]
# x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
# for p in ax.patches :
#     if abs(value2highlight - p.get_x()) == min(x_list):
#         p.set_color('crimson')
# ax.set_title("Distribution EXT_SOURCE_2")
# st.pyplot(fig)
#
#
# fig, ax = plt.subplots()
# sns.histplot(data=df, x="EXT_SOURCE_1")
# value2highlight = df.iloc[customer_id]["EXT_SOURCE_1"]
# x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
# for p in ax.patches :
#     if abs(value2highlight - p.get_x()) == min(x_list):
#         p.set_color('crimson')
# ax.set_title("Distribution EXT_SOURCE_1")
# st.pyplot(fig)
#
#
# fig, ax = plt.subplots()
# sns.histplot(data=df, x="NAME_INCOME_TYPE_Working")
# value2highlight = df.iloc[customer_id]["NAME_INCOME_TYPE_Working"]
# x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
# for p in ax.patches :
#     if abs(value2highlight - p.get_x()) == min(x_list):
#         p.set_color('crimson')
# ax.set_title("Distribution NAME_INCOME_TYPE_Working")
# st.pyplot(fig)
#
#
# fig, ax = plt.subplots()
# sns.histplot(data=df, x="REG_CITY_NOT_WORK_CITY")
# value2highlight = df.iloc[customer_id]["REG_CITY_NOT_WORK_CITY"]
# x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
# for p in ax.patches :
#     if abs(value2highlight - p.get_x()) == min(x_list):
#         p.set_color('crimson')
# ax.set_title("Distribution REG_CITY_NOT_WORK_CITY")
# st.pyplot(fig)
#
#
# fig, ax = plt.subplots()
# value2highlight = df.iloc[customer_id]["CODE_GENDER"]
# sns.histplot(data=df, x="CODE_GENDER")
# x_list = [(abs(value2highlight - p.get_x())) for p in ax.patches]
# for p in ax.patches :
#     if abs(value2highlight - p.get_x()) == min(x_list):
#         p.set_color('crimson')
# ax.set_title("Distribution CODE_GENDER")
# st.pyplot(fig)