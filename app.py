import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io
import base64
from PIL import Image

# ======== إعدادات الصفحة ========
st.set_page_config(page_title="Data Beast Pro", layout="wide", page_icon="🦁")

# ======== تهيئة session_state ========
if 'df' not in st.session_state:
    st.session_state.df = None
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'cleaning_history' not in st.session_state:
    st.session_state.cleaning_history = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ======== النصوص ========
TEXTS = {
    'ar': {
        'title': 'Data Beast Pro',
        'home': '🏠 الرئيسية',
        'ocr': '👁️ OCR Vision',
        'upload': '📥 رفع بيانات',
        'cleaner': '🧹 منظف البيانات',
        'excel': '📊 Excel Pro',
        'powerbi': '📈 Power BI',
        'sql': '🗄️ SQL',
        'ai': '🤖 AI',
        'export': '💾 تصدير',
        'settings': '⚙️ الإعدادات',
        'sample': '📊 بيانات تجريبية',
        'clear': '🗑️ مسح',
        'save': '💾 حفظ',
        'signature': '🔥 MIA8444 | Data Beast Pro © 2024'
    },
    'en': {
        'title': 'Data Beast Pro',
        'home': '🏠 Home',
        'ocr': '👁️ OCR Vision',
        'upload': '📥 Upload',
        'cleaner': '🧹 Cleaner',
        'excel': '📊 Excel Pro',
        'powerbi': '📈 Power BI',
        'sql': '🗄️ SQL',
        'ai': '🤖 AI',
        'export': '💾 Export',
        'settings': '⚙️ Settings',
        'sample': '📊 Sample',
        'clear': '🗑️ Clear',
        'save': '💾 Save',
        'signature': '🔥 MIA8444 | Data Beast Pro © 2024'
    }
}

def t(key):
    return TEXTS[st.session_state.language].get(key, key)

# ======== CSS ========
theme_css = """
<style>
    .main {background-color: #0E1117; color: #FAFAFA;}
    .stButton>button {width: 100%; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; border: none; border-radius: 10px; padding: 10px;}
    .stButton>button:hover {transform: scale(1.05);}
    .metric-card {background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; color: white; text-align: center;}
</style>
""" if st.session_state.dark_mode else """
<style>
    .main {background-color: #FFFFFF; color: #333333;}
    .stButton>button {width: 100%; background: linear-gradient(45deg, #667eea, #764ba2); color: white;}
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# ======== دوال مساعدة ========
def generate_sample_data():
    return pd.DataFrame({
        'التاريخ': pd.date_range('2024-01-01', periods=100),
        'المنتج': np.random.choice(['لابتوب', 'موبايل', 'تابلت', 'سماعات'], 100),
        'الفئة': np.random.choice(['إلكترونيات', 'اكسسوارات'], 100),
        'المبيعات': np.random.randint(1000, 50000, 100),
        'الكمية': np.random.randint(1, 50, 100),
        'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض'], 100),
        'التقييم': np.random.randint(1, 6, 100)
    })

# ======== Sidebar ========
with st.sidebar:
    # اللوجو
    try:
        st.image("logo.jpg", use_column_width=True)
    except:
        st.markdown("<h1 style='text-align:center;'>🦁</h1>", unsafe_allow_html=True)
    
    st.title(t('title'))
    
    # زر الإعدادات
    if st.button("⚙️ " + t('settings'), key='btn_settings'):
        st.session_state.page = 'settings'
        st.rerun()
    
    st.write("---")
    
    # القائمة
    menu_options = [t('home'), t('ocr'), t('upload'), t('cleaner'), t('excel'), t('powerbi'), t('sql'), t('ai'), t('export')]
    
    for i, option in enumerate(menu_options):
        if st.button(option, key=f'menu_{i}'):
            st.session_state.page = ['home', 'ocr', 'upload', 'cleaner', 'excel', 'powerbi', 'sql', 'ai', 'export'][i]
            st.rerun()
    
    st.write("---")
    
    # أدوات سريعة
    st.markdown("### ⚡ " + ("أدوات سريعة" if st.session_state.language == 'ar' else "Quick Tools"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(t('sample'), key='btn_sample'):
            st.session_state.df = generate_sample_data()
            st.success("✅ تم!")
            st.rerun()
    
    with col2:
        if st.button(t('clear'), key='btn_clear'):
            st.session_state.df = None
            st.session_state.cleaning_history = []
            st.success("✅ تم!")
            st.rerun()
    
    st.write("---")
    st.caption(t('signature'))

# ======== الصفحات ========
page = st.session_state.page
df = st.session_state.df

# --- الإعدادات ---
if page == 'settings':
    st.header("⚙️ " + t('settings'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 اللغة / Language")
        lang = st.radio("اختر / Choose:", ['العربية', 'English'], 
                       index=0 if st.session_state.language == 'ar' else 1)
        if lang == 'العربية':
            st.session_state.language = 'ar'
        else:
            st.session_state.language = 'en'
    
    with col2:
        st.subheader("🎨 الثيم / Theme")
        theme = st.radio("اختر / Choose:", 
                        ['داكن / Dark', 'فاتح / Light'],
                        index=0 if st.session_state.dark_mode else 1)
        st.session_state.dark_mode = (theme == 'داكن / Dark')
    
    if st.button("💾 " + t('save'), type='primary'):
        st.session_state.page = 'home'
        st.rerun()

# --- الرئيسية ---
elif page == 'home':
    st.markdown("<h1 style='text-align:center;'>🦁 Data Beast Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>منصة تحليل البيانات الشاملة</p>", unsafe_allow_html=True)
    
    if df is not None:
        # بطاقات إحصائية
        cols = st.columns(4)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        cols[0].metric("📊 الصفوف", len(df))
        cols[1].metric("📋 الأعمدة", len(df.columns))
        
        if len(numeric_cols) > 0:
            cols[2].metric("💰 الإجمالي", f"{df[numeric_cols[0]].sum():,.0f}")
            cols[3].metric("📈 المتوسط", f"{df[numeric_cols[0]].mean():,.0f}")
        
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("📊 اضغط 'بيانات تجريبية' في القائمة للبدء")

# --- OCR ---
elif page == 'ocr':
    st.header("👁️ OCR Vision")
    
    uploaded = st.file_uploader("📸 ارفع صورة:", ['jpg', 'jpeg', 'png'])
    
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
        
        with st.spinner("⏳ جاري التحليل..."):
            import time
            time.sleep(1)
            
            # محاكاة OCR
            ocr_data = {
                'المنتج': ['لابتوب', 'موبايل', 'تابلت'],
                'السعر': [12000, 25000, 8000],
                'الكمية': [2, 1, 3]
            }
            df_ocr = pd.DataFrame(ocr_data)
            
            st.success("✅ تم استخراج البيانات!")
            st.dataframe(df_ocr)
            
            if st.button("📊 استخدم البيانات", type='primary'):
                st.session_state.df = df_ocr
                st.success("✅ تم التحميل!")

# --- رفع بيانات ---
elif page == 'upload':
    st.header(t('upload'))
    
    uploaded = st.file_uploader("اختر ملف:", ['csv', 'xlsx', 'xls'])
    
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df_new = pd.read_csv(uploaded)
            else:
                df_new = pd.read_excel(uploaded)
            
            st.session_state.df = df_new
            st.success(f"✅ تم استيراد {len(df_new)} صف!")
            st.dataframe(df_new.head())
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")

# --- منظف البيانات ---
elif page == 'cleaner':
    st.header("🧹 " + t('cleaner'))
    
    if df is not None:
        # إحصائيات
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("الصفوف", len(df))
        col2.metric("الأعمدة", len(df.columns))
        col3.metric("الفارغ", int(df.isnull().sum().sum()))
        col4.metric("التكرار", int(df.duplicated().sum()))
        
        st.write("---")
        
        # أدوات التنظيف
        st.subheader("🔧 أدوات التنظيف")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ حذف الفارغ", key='drop_na'):
                st.session_state.df = df.dropna()
                st.session_state.cleaning_history.append("حذف القيم الفارغة")
                st.success("✅ تم!")
                st.rerun()
        
        with col2:
            if st.button("📋 حذف التكرار", key='drop_dup'):
                st.session_state.df = df.drop_duplicates()
                st.session_state.cleaning_history.append("حذف التكرارات")
                st.success("✅ تم!")
                st.rerun()
        
        with col3:
            if st.button("🔤 تنظيف النص", key='clean_text'):
                df_clean = df.copy()
                for col in df_clean.select_dtypes(include=['object']):
                    df_clean[col] = df_clean[col].str.strip().str.title()
                st.session_state.df = df_clean
                st.session_state.cleaning_history.append("تنظيف النصوص")
                st.success("✅ تم!")
                st.rerun()
        
        # سجل التنظيف
        if st.session_state.cleaning_history:
            with st.expander("📜 سجل التنظيف"):
                for i, action in enumerate(st.session_state.cleaning_history, 1):
                    st.write(f"{i}. {action}")
        
        st.write("---")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

# --- Excel Pro ---
elif page == 'excel':
    st.header(t('excel'))
    
    if df is not None:
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=500)
        
        if st.button("💾 " + t('save'), type='primary'):
            st.session_state.df = edited
            st.success("✅ تم الحفظ!")
            st.balloons()
    else:
        st.error("❌ لا توجد بيانات")

# --- Power BI ---
elif page == 'powerbi':
    st.header(t('powerbi'))
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            kpi = st.selectbox("اختر المؤشر:", numeric_cols)
            
            cols = st.columns(4)
            cols[0].metric("الإجمالي", f"{df[kpi].sum():,.0f}")
            cols[1].metric("المتوسط", f"{df[kpi].mean():,.0f}")
            cols[2].metric("الأعلى", f"{df[kpi].max():,.0f}")
            cols[3].metric("العدد", len(df))
            
            cat_cols = df.select_dtypes(include=['object']).columns
            if len(cat_cols) > 0:
                cat = st.selectbox("التصنيف:", cat_cols)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.pie(df, values=kpi, names=cat, title=f"توزيع {kpi}")
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    fig2 = px.bar(df.groupby(cat)[kpi].sum().reset_index(), x=cat, y=kpi, title=f"مجموع {kpi}")
                    st.plotly_chart(fig2, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

# --- SQL ---
elif page == 'sql':
    st.header(t('sql'))
    
    if df is not None:
        st.info("🔧 SQL - قيد التطوير")
        
        query = st.text_area("اكتب استعلام SQL:", "SELECT * FROM data LIMIT 10")
        
        if st.button("▶️ تشغيل"):
            st.warning("مكتبة DuckDB غير مثبتة في السحابة")
    else:
        st.error("❌ لا توجد بيانات")

# --- AI ---
elif page == 'ai':
    st.header(t('ai'))
    
    if df is not None:
        question = st.text_input("🤖 اسأل الوحش:", "ما إجمالي المبيعات؟")
        
        if st.button("🚀 تحليل"):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                total = df[numeric_cols].sum().sum()
                st.success(f"💰 الإجمالي: {total:,.0f}")
                
                if 'الفرع' in df.columns:
                    best_branch = df.groupby('الفرع')[numeric_cols[0]].sum().idxmax()
                    st.info(f"🏆 أفضل فرع: {best_branch}")
    else:
        st.error("❌ لا توجد بيانات")

# --- تصدير ---
elif page == 'export':
    st.header(t('export'))
    
    if df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="data.csv"><button style="width:100%; padding:10px; background:#4ECDC4; color:white; border:none; border-radius:5px;">📥 CSV</button></a>', unsafe_allow_html=True)
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            b64 = base64.b64encode(output.getvalue()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data.xlsx"><button style="width:100%; padding:10px; background:#FF6B6B; color:white; border:none; border-radius:5px;">📥 Excel</button></a>', unsafe_allow_html=True)
    else:
        st.error("❌ لا توجد بيانات")

# ======== Footer ========
st.write("---")
st.markdown(f"<p style='text-align:center; color:#4ECDC4;'>{t('signature')}</p>", unsafe_allow_html=True)
