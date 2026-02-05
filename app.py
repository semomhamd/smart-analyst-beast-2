import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io
import base64

# ======== إعدادات الصفحة ========
st.set_page_config(page_title="Data Beast Pro", layout="wide", page_icon="🦁")

# ======== إعدادات اللغة ========
if 'language' not in st.session_state:
    st.session_state.language = 'ar'

# ======== إعدادات الثيم ========
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# ======== النصوص متعددة اللغات ========
TEXTS = {
    'ar': {
        'title': 'Data Beast Pro',
        'subtitle': 'منصة تحليل البيانات الشاملة',
        'home': '🏠 الرئيسية',
        'ocr': '👁️ OCR Vision',
        'upload': '📥 رفع بيانات',
        'excel': '📊 Excel Pro',
        'powerbi': '📈 Power BI',
        'sql': '🗄️ SQL',
        'ai': '🤖 AI',
        'export': '💾 تصدير',
        'settings': '⚙️ الإعدادات',
        'data_cleaner': '🧹 منظف البيانات',
        'sample_data': '📊 بيانات تجريبية',
        'clear_data': '🗑️ مسح البيانات',
        'language': 'اللغة',
        'dark_mode': 'الوضع الداكن',
        'light_mode': 'الوضع الفاتح',
        'signature': '🔥 MIA8444 | Data Beast Pro © 2024'
    },
    'en': {
        'title': 'Data Beast Pro',
        'subtitle': 'Comprehensive Data Analysis Platform',
        'home': '🏠 Home',
        'ocr': '👁️ OCR Vision',
        'upload': '📥 Upload Data',
        'excel': '📊 Excel Pro',
        'powerbi': '📈 Power BI',
        'sql': '🗄️ SQL',
        'ai': '🤖 AI',
        'export': '💾 Export',
        'settings': '⚙️ Settings',
        'data_cleaner': '🧹 Data Cleaner',
        'sample_data': '📊 Sample Data',
        'clear_data': '🗑️ Clear Data',
        'language': 'Language',
        'dark_mode': 'Dark Mode',
        'light_mode': 'Light Mode',
        'signature': '🔥 MIA8444 | Data Beast Pro © 2024'
    }
}

def get_text(key):
    return TEXTS[st.session_state.language].get(key, key)

# ======== CSS ديناميكي حسب الثيم ========
def get_css():
    if st.session_state.dark_mode:
        return """
        <style>
            .main {background-color: #0E1117; color: #FAFAFA;}
            .sidebar .sidebar-content {background-color: #262730;}
            .stButton>button {background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white;}
            .tool-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white;}
        </style>
        """
    else:
        return """
        <style>
            .main {background-color: #FFFFFF; color: #333333;}
            .sidebar .sidebar-content {background-color: #F0F2F6;}
            .stButton>button {background: linear-gradient(45deg, #667eea, #764ba2); color: white;}
            .tool-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white;}
        </style>
        """

st.markdown(get_css(), unsafe_allow_html=True)

# ======== الذاكرة الدائمة ========
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaning_history' not in st.session_state:
    st.session_state.cleaning_history = []

# ======== Sidebar ========
with st.sidebar:
    # اللوجو
    try:
        st.image("logo.jpg", use_column_width=True)
    except:
        st.title("🦁")
    
    st.title(get_text('title'))
    
    # زر الإعدادات في الأعلى
    if st.button("⚙️ " + get_text('settings'), use_container_width=True):
        st.session_state.show_settings = True
    
    st.write("---")
    
    # القائمة الرئيسية
    menu = st.radio(get_text('settings'), [
        get_text('home'),
        get_text('ocr'),
        get_text('upload'),
        get_text('data_cleaner'),
        get_text('excel'),
        get_text('powerbi'),
        get_text('sql'),
        get_text('ai'),
        get_text('export')
    ], label_visibility="collapsed")
    
    st.write("---")
    
    # أدوات سريعة
    st.markdown("### ⚡ " + ("أدوات سريعة" if st.session_state.language == 'ar' else "Quick Tools"))
    
    cols = st.columns(2)
    with cols[0]:
        if st.button(get_text('sample_data'), use_container_width=True):
            st.session_state.df = pd.DataFrame({
                'التاريخ': pd.date_range('2024-01-01', periods=100),
                'المنتج': np.random.choice(['لابتوب', 'موبايل', 'تابلت'], 100),
                'الفئة': np.random.choice(['إلكترونيات', 'اكسسوارات'], 100),
                'المبيعات': np.random.randint(1000, 50000, 100),
                'الكمية': np.random.randint(1, 50, 100),
                'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض'], 100),
                'التقييم': np.random.randint(1, 6, 100),
                'الخصم': np.random.randint(0, 30, 100)
            })
            st.rerun()
    
    with cols[1]:
        if st.button(get_text('clear_data'), use_container_width=True):
            st.session_state.df = None
            st.session_state.cleaning_history = []
            st.rerun()
    
    st.write("---")
    st.caption(get_text('signature'))

# ======== نافذة الإعدادات المنبثقة ========
if st.session_state.get('show_settings', False):
    with st.expander("⚙️ " + get_text('settings'), expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # تغيير اللغة
            st.subheader("🌐 " + get_text('language'))
            lang = st.radio("Language / اللغة", ['العربية', 'English'], 
                          index=0 if st.session_state.language == 'ar' else 1)
            if lang == 'العربية':
                st.session_state.language = 'ar'
            else:
                st.session_state.language = 'en'
        
        with col2:
            # تغيير الثيم
            st.subheader("🎨 " + ("الثيم" if st.session_state.language == 'ar' else "Theme"))
            theme = st.radio("Theme", [get_text('dark_mode'), get_text('light_mode')], 
                           index=0 if st.session_state.dark_mode else 1)
            st.session_state.dark_mode = (theme == get_text('dark_mode'))
        
        if st.button("✅ " + ("حفظ" if st.session_state.language == 'ar' else "Save"), type="primary"):
            st.session_state.show_settings = False
            st.rerun()

df = st.session_state.df

# ======== الصفحات ========

# --- الرئيسية ---
if menu == get_text('home'):
    st.markdown(f"<h1 style='text-align:center;'>🦁 {get_text('title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:gray;'>{get_text('subtitle')}</p>", unsafe_allow_html=True)
    
    if df is not None:
        st.success(f"✅ {len(df):,} rows | {len(df.columns)} columns")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("📊 " + ("اضغط 'بيانات تجريبية' للبدء" if st.session_state.language == 'ar' else "Click 'Sample Data' to start"))

# --- OCR Vision ---
elif menu == get_text('ocr'):
    st.header("👁️ OCR Vision")
    
    uploaded = st.file_uploader("📸 " + ("ارفع صورة:" if st.session_state.language == 'ar' else "Upload image:"), 
                               ['jpg', 'jpeg', 'png'])
    
    if uploaded:
        from PIL import Image
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
        
        with st.spinner("⏳ " + ("جاري التحليل..." if st.session_state.language == 'ar' else "Analyzing...")):
            import time
            time.sleep(2)
            
            # محاكاة OCR
            ocr_data = {
                'المنتج': ['لابتوب Dell', 'iPhone 15', 'Samsung Tab', 'AirPods', 'Mouse'],
                'السعر': [12000, 25000, 8000, 3500, 500],
                'الكمية': [2, 1, 3, 2, 10],
                'التاريخ': ['2024-01-15'] * 5
            }
            df_ocr = pd.DataFrame(ocr_data)
            
            st.success("✅ " + ("تم استخراج البيانات!" if st.session_state.language == 'ar' else "Data extracted!"))
            st.dataframe(df_ocr, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 " + ("استخدم البيانات" if st.session_state.language == 'ar' else "Use Data"), type="primary"):
                    st.session_state.df = df_ocr
                    st.success("✅ Done!")
            with col2:
                csv = df_ocr.to_csv(index=False)
                st.download_button("📥 CSV", csv, "ocr_data.csv", "text/csv")

# --- رفع بيانات ---
elif menu == get_text('upload'):
    st.header(get_text('upload'))
    f = st.file_uploader("Choose file", ['csv', 'xlsx'])
    if f:
        st.session_state.df = pd.read_csv(f) if f.name.endswith('.csv') else pd.read_excel(f)
        st.success("✅ Done!")

# --- منظف البيانات ---
elif menu == get_text('data_cleaner'):
    st.header("🧹 " + ("منظف البيانات" if st.session_state.language == 'ar' else "Data Cleaner"))
    
    if df is not None:
        st.subheader("📊 " + ("حالة البيانات" if st.session_state.language == 'ar' else "Data Status"))
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("الصفوف" if st.session_state.language == 'ar' else "Rows", len(df))
        col2.metric("الأعمدة" if st.session_state.language == 'ar' else "Columns", len(df.columns))
        col3.metric("القيم الفارغة" if st.session_state.language == 'ar' else "Missing", df.isnull().sum().sum())
        col4.metric("التكرارات" if st.session_state.language == 'ar' else "Duplicates", df.duplicated().sum())
        
        st.write("---")
        st.subheader("🔧 " + ("أدوات التنظيف" if st.session_state.language == 'ar' else "Cleaning Tools"))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ " + ("حذف الفارغ" if st.session_state.language == 'ar' else "Drop NA"), use_container_width=True):
                st.session_state.df = df.dropna()
                st.session_state.cleaning_history.append("حذف الفارغ")
                st.rerun()
        
        with col2:
            if st.button("📋 " + ("حذف التكرار" if st.session_state.language == 'ar' else "Drop Duplicates"), use_container_width=True):
                st.session_state.df = df.drop_duplicates()
                st.session_state.cleaning_history.append("حذف التكرار")
                st.rerun()
        
        with col3:
            if st.button("🔤 " + ("تنظيف النص" if st.session_state.language == 'ar' else "Clean Text"), use_container_width=True):
                for col in df.select_dtypes(include=['object']):
                    df[col] = df[col].str.strip().str.title()
                st.session_state.df = df
                st.session_state.cleaning_history.append("تنظيف النص")
                st.rerun()
        
        # سجل التنظيف
        if st.session_state.cleaning_history:
            with st.expander("📜 " + ("سجل التنظيف" if st.session_state.language == 'ar' else "Cleaning History")):
                for i, action in enumerate(st.session_state.cleaning_history, 1):
                    st.write(f"{i}. {action}")
        
        st.dataframe(df, use_container_width=True)
    else:
        st.error("❌ " + ("لا توجد بيانات" if st.session_state.language == 'ar' else "No data"))

# --- Excel Pro ---
elif menu == get_text('excel'):
    st.header(get_text('excel'))
    if df is not None:
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=500)
        if st.button("💾 " + ("حفظ" if st.session_state.language == 'ar' else "Save"), type="primary"):
            st.session_state.df = edited
            st.success("✅ Done!")
    else:
        st.error("❌ No data")

# --- Power BI ---
elif menu == get_text('powerbi'):
    st.header(get_text('powerbi'))
    if df is not None:
        numeric = df.select_dtypes(include=[np.number]).columns
        if len(numeric) > 0:
            col = numeric[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Total", f"{df[col].sum():,.0f}")
            c2.metric("Average", f"{df[col].mean():,.0f}")
            c3.metric("Count", len(df))
            
            if 'الفرع' in df.columns or 'Branch' in df.columns:
                branch_col = 'الفرع' if 'الفرع' in df.columns else 'Branch'
                st.plotly_chart(px.pie(df, values=col, names=branch_col), use_container_width=True)
    else:
        st.error("❌ No data")

# --- SQL ---
elif menu == get_text('sql'):
    st.header(get_text('sql'))
    if df is not None:
        st.info("🔧 SQL - " + ("قيد التطوير" if st.session_state.language == 'ar' else "Coming soon"))
    else:
        st.error("❌ No data")

# --- AI ---
elif menu == get_text('ai'):
    st.header(get_text('ai'))
    if df is not None:
        q = st.text_input("Ask / اسأل:")
        if q:
            total = df.select_dtypes(include=[np.number]).sum().sum()
            st.success(f"Total: {total:,.0f}")
    else:
        st.error("❌ No data")

# --- تصدير ---
elif menu == get_text('export'):
    st.header(get_text('export'))
    if df is not None:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="data.csv"><button>📥 CSV</button></a>', unsafe_allow_html=True)
    else:
        st.error("❌ No data")

st.write("---")
st.markdown(f"<p style='text-align:center; color:#4ECDC4;'>{get_text('signature')}</p>", unsafe_allow_html=True)
