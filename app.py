import streamlit as st
import pandas as pd
import numpy as np  
import pickle
import urllib.parse

import joblib
import gzip

with gzip.open("med_dict.pkl.gz", "rb") as f:
    med_dict = joblib.load(f)

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = joblib.load(f)




medis=pd.DataFrame(med_dict)


def recommend(med):
    med_index=medis[medis['Drug_Name']==med].index[0]
    distance=similarity[med_index]
    med_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:4]
    return [medis.iloc[i[0]].Drug_Name for i in med_list]
        


st.title("Medicine Recommendation System")
st.subheader("Find Similar Medicines")
with st.form("Medicine Form"):
    st.write("Enter the medicine name to get similar medicines")
    med_name=st.selectbox("Medicine Name",medis['Drug_Name'].tolist())
    submit=st.form_submit_button("Recommend")
rmed=recommend(med_name)
if submit:
    st.success("Recommended Medicines")
    st.write("Similar Medicines are:")
    for med in rmed:
        st.write(med)
    encoded_med_name = urllib.parse.quote(med_name)
    pharmacy_url = f"https://pharmeasy.in/search/all?name={encoded_med_name}"
    st.markdown(f"[🔍 Click Here to Buy on PharmEasy]({pharmacy_url})", unsafe_allow_html=True)