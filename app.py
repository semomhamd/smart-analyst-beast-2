import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import base64
from fpdf import FPDF
import json
import random

# ======== FETH - محلل البيانات الذكي ========
class FethPersonality:
    def _init_(self):
        self.name = "FETH"
        
    def respond(self, context, data_insight=None):
        responses = {
            'welcome': "أهلاً بيك! أنا FETH... جاهز أفتحلك أي بيانات 🎯",
            'analysis_ready': "فتحت البيانات... وده اللي لقيته 👇",
            'celebration': "🎉 كده! إنجاز رائع"
        }
        return responses.get(context, "FETH هنا... جاهز أساعدك!")

# ======== إعدادات الصفحة ========
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide", page_icon="🦁")

# ======== تهيئة session_state ========
if 'df' not in st.session_state:
    st.session_state.df = None
if 'feth' not in st.session_state:
    st.session_state.feth = FethPersonality()

# ======== Sidebar ========
with st.sidebar:
    st.title("🦁 Smart Analyst The Beast")
    st.markdown("### 🎯 FETH AI")
    
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'home'
    if st.button("📥 رفع بيانات"):
        st.session_state.page = 'upload'
    if st.button("🧹 تنظيف"):
        st.session_state.page = 'cleaner'
    if st.button("📊 تحليل"):
        st.session_state.page = 'powerbi'

# ======== الصفحة الرئيسية ========
st.markdown("<h1 style='text-align:center; color:#3498DB;'>🦁 Smart Analyst The Beast</h1>", unsafe_allow_html=True)

if st.session_state.df is not None:
    df = st.session_state.df
    st.success(f"🎯 {st.session_state.feth.respond('analysis_ready')}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("الصفوف", len(df))
    col2.metric("الأعمدة", len(df.columns))
    col3.metric("الحجم", f"{df.memory_usage().sum()/1024:.1f} KB")
    
    st.dataframe(df.head(), use_container_width=True)
else:
    st.info("🎯 أهلاً بيك! ارفع ملف أو جرب البيانات التجريبية")
    
    if st.button("📊 بيانات تجريبية", type='primary'):
        st.session_state.df = pd.DataFrame({
            'المنتج': ['لابتوب', 'موبايل', 'تابلت'],
            'المبيعات': [50000, 80000, 30000]
        })
        st.rerun()

# ======== رفع الملفات ========
uploaded = st.file_uploader("📥 ارفع ملف:", ['csv', 'xlsx'])
if uploaded:
    if uploaded.name.endswith('.csv'):
        st.session_state.df = pd.read_csv(uploaded)
    else:
        st.session_state.df = pd.read_excel(uploaded)
    st.success("✅ تم رفع الملف!")
    st.rerun()

st.markdown("---")
st.caption("🔥 MIA8444 | Smart Analyst The Beast © 2024")
