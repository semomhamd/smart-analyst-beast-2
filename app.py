import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io
import base64

st.set_page_config(page_title="Data Beast", layout="wide", page_icon="🦁")

if 'df' not in st.session_state:
    st.session_state.df = None

SIGNATURE = "🔥 MIA8444 | Data Beast Pro © 2024"

with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True)
    except:
        st.title("🦁")
    
    st.title("Data Beast")
    
    menu = st.radio("القائمة:", [
        "🏠 الرئيسية",
        "📥 رفع بيانات", 
        "📊 Excel Pro",
        "📈 Power BI",
        "🗄️ SQL",
        "🤖 AI",
        "💾 تصدير"
    ])
    
    if st.button("📊 بيانات تجريبية"):
        st.session_state.df = pd.DataFrame({
            'المنتج': ['A', 'B', 'C'] * 100,
            'المبيعات': np.random.randint(1000, 50000, 300),
            'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض'], 300),
            'التقييم': np.random.randint(1, 6, 300)
        })
        st.rerun()
    
    st.caption(SIGNATURE)

df = st.session_state.df

if menu == "🏠 الرئيسية":
    st.title("🦁 Data Beast Pro")
    st.write("منصة تحليل البيانات الشاملة")
    
    if df is not None:
        st.success(f"✅ البيانات: {len(df):,} صف")
        st.dataframe(df.head(10))
    else:
        st.info("اضغط 'بيانات تجريبية'")

elif menu == "📥 رفع بيانات":
    st.header("📥 رفع ملف")
    f = st.file_uploader("اختر ملف", ['csv', 'xlsx'])
    if f:
        st.session_state.df = pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f)
        st.success("تم!")

elif menu == "📊 Excel Pro":
    st.header("📊 Excel Pro")
    if df is not None:
        edited = st.data_editor(df, num_rows="dynamic")
        if st.button("💾 حفظ"):
            st.session_state.df = edited
            st.success("تم الحفظ!")

elif menu == "📈 Power BI":
    st.header("📈 Power BI Dashboard")
    if df is not None:
        numeric = df.select_dtypes(include=[np.number]).columns
        if len(numeric) > 0:
            col = numeric[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("الإجمالي", f"{df[col].sum():,.0f}")
            c2.metric("المتوسط", f"{df[col].mean():,.0f}")
            c3.metric("العدد", len(df))
            
            if 'الفرع' in df.columns:
                st.plotly_chart(px.pie(df, values=col, names='الفرع'))

elif menu == "🗄️ SQL":
    st.header("🗄️ SQL")
    if df is not None:
        try:
            import duckdb
            query = st.text_area("SQL:", "SELECT * FROM data LIMIT 10")
            if st.button("تشغيل"):
                con = duckdb.connect(':memory:')
                con.register('data', df)
                result = con.execute(query).fetchdf()
                st.dataframe(result)
        except:
            st.error("مكتبة DuckDB غير مثبتة")

elif menu == "🤖 AI":
    st.header("🤖 AI")
    if df is not None:
        q = st.text_input("اسأل:")
        if q:
            st.success(f"الإجمالي: {df.select_dtypes(include=[np.number]).sum().sum():,.0f}")

elif menu == "💾 تصدير":
    st.header("💾 تصدير")
    if df is not None:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="data.csv"><button>تحميل CSV</button></a>', unsafe_allow_html=True)

st.write("---")
st.markdown(f"<p style='text-align:center; color:#4ECDC4;'>{SIGNATURE}</p>", unsafe_allow_html=True)
