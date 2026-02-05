
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io
import base64
import os

st.set_page_config(page_title="Data Beast", layout="wide", page_icon="🦁")

if 'df' not in st.session_state:
    st.session_state.df = None

with st.sidebar:
    # اللوجو في السايدبار
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    else:
        st.title("🦁")
        st.title("Data Beast")
    
    st.write("---")
    
    menu = st.radio("القائمة:", [
        "🏠 الرئيسية",
        "📥 رفع بيانات", 
        "📊 عرض البيانات",
        "📈 تحليل",
        "💾 تصدير"
    ])
    
    if st.button("📊 بيانات تجريبية"):
        st.session_state.df = pd.DataFrame({
            'المنتج': ['A', 'B', 'C'] * 100,
            'المبيعات': np.random.randint(1000, 50000, 300),
            'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض'], 300)
        })
        st.rerun()

df = st.session_state.df

if menu == "🏠 الرئيسية":
    st.title("🦁 Data Beast")
    if df is not None:
        st.write(f"الصفوف: {len(df)}")
        st.dataframe(df.head())
    else:
        st.info("اضغط 'بيانات تجريبية' في القائمة")

elif menu == "📥 رفع بيانات":
    f = st.file_uploader("اختر ملف", ['csv', 'xlsx'])
    if f:
        st.session_state.df = pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f)
        st.success("تم!")

elif menu == "📊 عرض البيانات":
    if df is not None:
        st.dataframe(df)

elif menu == "📈 تحليل":
    if df is not None:
        numeric = df.select_dtypes(include=[np.number]).columns
        if len(numeric) > 0:
            st.plotly_chart(px.histogram(df, x=numeric[0]))

elif menu == "💾 تصدير":
    if df is not None:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="data.csv"><button>تحميل CSV</button></a>', unsafe_allow_html=True)

st.caption("Data Beast - صنع بحب ❤️")
