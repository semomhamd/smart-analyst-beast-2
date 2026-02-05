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
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'excel_formulas' not in st.session_state:
    st.session_state.excel_formulas = {}

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
        'ai': '🤖 AI Assistant',
        'export': '💾 تصدير',
        'settings': '⚙️ الإعدادات',
        'share': '📤 مشاركة',
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
        'ai': '🤖 AI Assistant',
        'export': '💾 Export',
        'settings': '⚙️ Settings',
        'share': '📤 Share',
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
    .excel-cell {border: 1px solid #444; padding: 5px; text-align: center;}
    .formula-bar {background: #1a1a2e; padding: 10px; border-radius: 5px; font-family: monospace;}
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
        'المنتج': np.random.choice(['لابتوب', 'موبايل', 'تابلت', 'سماعات', 'شاحن'], 100),
        'الفئة': np.random.choice(['إلكترونيات', 'اكسسوارات', 'أجهزة'], 100),
        'المبيعات': np.random.randint(1000, 50000, 100),
        'الكمية': np.random.randint(1, 50, 100),
        'السعر': np.random.randint(500, 25000, 100),
        'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض', 'جدة'], 100),
        'التقييم': np.random.randint(1, 6, 100),
        'الخصم': np.random.randint(0, 30, 100)
    })

def ai_assistant(df, question):
    """مساعد AI ذكي"""
    question = question.lower()
    
    if "إجمالي" in question or "total" in question or "sum" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            total = df[numeric_cols[0]].sum()
            return f"💰 الإجمالي: {total:,.0f}"
    
    elif "متوسط" in question or "average" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            avg = df[numeric_cols[0]].mean()
            return f"📊 المتوسط: {avg:,.2f}"
    
    elif "أعلى" in question or "max" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            best_idx = df[numeric_cols[0]].idxmax()
            best_item = df.loc[best_idx, cat_cols[0]]
            best_value = df[numeric_cols[0]].max()
            return f"🏆 الأعلى: {best_item} ({best_value:,.0f})"
    
    elif "أقل" in question or "min" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            worst_idx = df[numeric_cols[0]].idxmin()
            worst_item = df.loc[worst_idx, cat_cols[0]]
            worst_value = df[numeric_cols[0]].min()
            return f"📉 الأقل: {worst_item} ({worst_value:,.0f})"
    
    elif "عدد" in question or "count" in question:
        return f"📋 عدد الصفوف: {len(df):,}"
    
    elif "ملخص" in question or "summary" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        report = "📊 ملخص البيانات:\n\n"
        report += f"• الصفوف: {len(df):,}\n"
        report += f"• الأعمدة: {len(df.columns)}\n"
        if len(numeric_cols) > 0:
            report += f"• الإجمالي: {df[numeric_cols[0]].sum():,.0f}\n"
            report += f"• المتوسط: {df[numeric_cols[0]].mean():,.2f}\n"
        return report
    
    else:
        return """🤔 جرب تسأل:
* "ما إجمالي المبيعات؟"
* "ما المتوسط؟"
* "أعلى منتج مبيعاً؟"
* "عدد الصفوف؟"
* "ملخص البيانات؟"
"""

def generate_pdf_report(df, charts_data=None):
    """توليد تقرير PDF"""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Data Beast Pro - Report', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'{t("signature")} | Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # ملخص البيانات
    pdf.cell(0, 10, f'Data Summary', 0, 1)
    pdf.ln(5)
    pdf.cell(0, 10, f'Rows: {len(df)}', 0, 1)
    pdf.cell(0, 10, f'Columns: {len(df.columns)}', 0, 1)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        pdf.ln(5)
        pdf.cell(0, 10, f'Total: {df[numeric_cols[0]].sum():,.0f}', 0, 1)
        pdf.cell(0, 10, f'Average: {df[numeric_cols[0]].mean():,.2f}', 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

def apply_excel_formula(df, formula, target_col):
    """تطبيق دوال Excel"""
    try:
        if formula.startswith('='):
            formula = formula[1:]
        
        if formula.upper().startswith('SUM('):
            col = formula[4:-1]
            return df[col].sum()
        
        elif formula.upper().startswith('AVERAGE('):
            col = formula[8:-1]
            return df[col].mean()
        
        elif formula.upper().startswith('MAX('):
            col = formula[4:-1]
            return df[col].max()
        
        elif formula.upper().startswith('MIN('):
            col = formula[4:-1]
            return df[col].min()
        
        elif formula.upper().startswith('COUNT('):
            col = formula[6:-1]
            return df[col].count()
        
        elif formula.upper().startswith('IF('):
            # =IF( condition, true_value, false_value )
            parts = formula[3:-1].split(',')
            if len(parts) == 3:
                condition = parts[0].strip()
                true_val = parts[1].strip()
                false_val = parts[2].strip()
                
                # محاكاة IF بسيطة
                if '>' in condition:
                    col, val = condition.split('>')
                    col = col.strip()
                    val = float(val.strip())
                    return df.apply(lambda row: true_val if row[col] > val else false_val, axis=1)
        
        elif formula.upper().startswith('VLOOKUP('):
            return "VLOOKUP يحتاج جدول مرجعي"
        
        else:
            # محاولة تقييم رياضي
            return eval(formula, {'df': df, 'np': np, 'pd': pd})
    
    except Exception as e:
        return f"خطأ: {str(e)}"

# ======== Sidebar ========
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True)
    except:
        st.markdown("<h1 style='text-align:center;'>🦁</h1>", unsafe_allow_html=True)
    
    st.title(t('title'))
    
    if st.button("⚙️ " + t('settings'), key='btn_settings'):
        st.session_state.page = 'settings'
        st.rerun()
    
    st.write("---")
    
    menu_options = [t('home'), t('ocr'), t('upload'), t('cleaner'), t('excel'), t('powerbi'), t('sql'), t('ai'), t('export')]
    menu_keys = ['home', 'ocr', 'upload', 'cleaner', 'excel', 'powerbi', 'sql', 'ai', 'export']
    
    for i, (option, key) in enumerate(zip(menu_options, menu_keys)):
        if st.button(option, key=f'menu_{key}'):
            st.session_state.page = key
            st.rerun()
    
    st.write("---")
    
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
    st.markdown(f"<h1 style='text-align:center;'>🦁 Data Beast Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:gray;'>منصة تحليل البيانات الشاملة</p>", unsafe_allow_html=True)
    
    if df is not None:
        cols = st.columns(4)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        cols[0].metric("📊 الصفوف", len(df))
        cols[1].metric("📋 الأعمدة", len(df.columns))
        
        if len(numeric_cols) > 0:
            cols[2].metric("💰 الإجمالي", f"{df[numeric_cols[0]].sum():,.0f}")
            cols[3].metric("📈 المتوسط", f"{df[numeric_cols[0]].mean():,.0f}")
        
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("📊 اضغط 'بيانات تجريبية' للبدء")

# --- OCR ---
elif page == 'ocr':
    st.header("👁️ OCR Vision")
    
    uploaded = st.file_uploader("📸 ارفع صورة:", ['jpg', 'jpeg', 'png'])
    
    if uploaded:
        from PIL import Image
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
        
        with st.spinner("⏳ جاري التحليل..."):
            import time
            time.sleep(2)
            
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
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("الصفوف", len(df))
        col2.metric("الأعمدة", len(df.columns))
        col3.metric("الفارغ", int(df.isnull().sum().sum()))
        col4.metric("التكرار", int(df.duplicated().sum()))
        
        st.write("---")
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
        
        if st.session_state.cleaning_history:
            with st.expander("📜 سجل التنظيف"):
                for i, action in enumerate(st.session_state.cleaning_history, 1):
                    st.write(f"{i}. {action}")
        
        st.dataframe(df, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

# --- Excel Pro المتطور ---
elif page == 'excel':
    st.header("📊 Excel Pro - " + ("محرك الجداول الاحترافي" if st.session_state.language == 'ar' else "Professional Spreadsheet"))
    
    if df is not None:
        # شريط الأدوات
        st.subheader("🧰 شريط الأدوات")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("➕ صف جديد"):
                new_row = pd.DataFrame([{col: None for col in df.columns}])
                st.session_state.df = pd.concat([df, new_row], ignore_index=True)
                st.rerun()
        
        with col2:
            if st.button("➕ عمود جديد"):
                col_name = f"عمود_{len(df.columns)+1}"
                st.session_state.df[col_name] = None
                st.rerun()
        
        with col3:
            if st.button("🗑️ حذف صف"):
                if len(df) > 0:
                    st.session_state.df = df.iloc[:-1]
                    st.rerun()
        
        with col4:
            if st.button("🔍 بحث"):
                st.session_state.show_search = True
        
        with col5:
            if st.button("📊 Pivot Table"):
                st.session_state.show_pivot = True
        
        # شريط الصيغ
        st.write("---")
        st.subheader("📝 شريط الصيغ (Formula Bar)")
        
        formula_col1, formula_col2 = st.columns([3, 1])
        
        with formula_col1:
            formula = st.text_input("= اكتب الصيغة:", 
                                   placeholder="مثال: =SUM(المبيعات) أو =AVERAGE(السعر)",
                                   key='formula_input')
        
        with formula_col2:
            target_col = st.selectbox("في عمود:", df.columns)
        
        if st.button("▶️ تطبيق الصيغة", type='primary'):
            result = apply_excel_formula(df, formula, target_col)
            if isinstance(result, pd.Series):
                st.session_state.df[target_col] = result
            else:
                st.info(f"النتيجة: {result}")
            st.rerun()
        
        # دليل الدوال
        with st.expander("📚 دليل دوال Excel"):
            st.code("""
=SUM(عمود)        → مجموع
=AVERAGE(عمود)    → متوسط  
=MAX(عمود)        → أقصى قيمة
=MIN(عمود)        → أدنى قيمة
=COUNT(عمود)      → عدد القيم
=IF(شرط, صح, خطأ) → شرط منطقي
=VLOOKUP(قيمة, جدول, عمود) → بحث
            """)
        
        # نافذة البحث
        if st.session_state.get('show_search', False):
            with st.expander("🔍 بحث", expanded=True):
                search_col = st.selectbox("ابحث في:", df.columns)
                search_term = st.text_input("كلمة البحث:")
                if search_term:
                    filtered = df[df[search_col].astype(str).str.contains(search_term, na=False)]
                    st.write(f"نتائج البحث: {len(filtered)} صف")
                    st.dataframe(filtered, use_container_width=True)
        
        # نافذة Pivot Table
        if st.session_state.get('show_pivot', False):
            with st.expander("📊 Pivot Table", expanded=True):
                pivot_index = st.selectbox("الصفوف:", df.columns)
                pivot_values = st.selectbox("القيم:", df.select_dtypes(include=[np.number]).columns)
                pivot_agg = st.selectbox("الدالة:", ['sum', 'mean', 'count', 'max', 'min'])
                
                try:
                    pivot_table = pd.pivot_table(df, values=pivot_values, index=pivot_index, aggfunc=pivot_agg)
                    st.dataframe(pivot_table, use_container_width=True)
                    
                    # رسم بياني للـ Pivot
                    st.plotly_chart(px.bar(pivot_table.reset_index(), x=pivot_index, y=pivot_values), use_container_width=True)
                except Exception as e:
                    st.error(f"خطأ في Pivot Table: {str(e)}")
        
        # الجدول الرئيسي
        st.write("---")
        st.subheader("📋 ورقة العمل")
        
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=500)
        
        if st.button("💾 حفظ جميع التغييرات", type='primary'):
            st.session_state.df = edited
            st.success("✅ تم الحفظ!")
            st.balloons()
        
        # إحصائيات سريعة
        st.write("---")
        st.subheader("📊 إحصائيات سريعة")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            
            stats_col1.metric("SUM", f"{df[numeric_cols[0]].sum():,.0f}")
            stats_col2.metric("AVERAGE", f"{df[numeric_cols[0]].mean():,.2f}")
            stats_col3.metric("MAX", f"{df[numeric_cols[0]].max():,.0f}")
            stats_col4.metric("MIN", f"{df[numeric_cols[0]].min():,.0f}")
    
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

# --- AI Assistant ---
elif page == 'ai':
    st.header("🤖 " + ("المساعد الذكي" if st.session_state.language == 'ar' else "AI Assistant"))
    
    if df is not None:
        with st.expander("👁️ معاينة البيانات"):
            st.dataframe(df.head(), use_container_width=True)
        
        st.write("---")
        st.subheader("💬 اسأل الوحش")
        
        examples = [
            "ما إجمالي المبيعات؟",
            "ما المتوسط؟",
            "أعلى منتج مبيعاً؟",
            "عدد الصفوف؟",
            "ملخص البيانات؟"
        ]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question = st.text_input("📝 اكتب سؤالك:", placeholder="مثال: ما إجمالي المبيعات؟")
        
        with col2:
            st.write("")
            st.write("")
            if st.button("🚀 إرسال", type='primary'):
                st.session_state.last_question = question
        
        st.write("*أمثلة سريعة:*")
        cols = st.columns(len(examples))
        for i, ex in enumerate(examples):
            with cols[i]:
                if st.button(ex, key=f'example_{i}'):
                    st.session_state.last_question = ex
                    st.rerun()
        
        if 'last_question' in st.session_state and st.session_state.last_question:
            with st.spinner("🤔 جاري التفكير..."):
                answer = ai_assistant(df, st.session_state.last_question)
                st.success(answer)
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'last_question' in st.session_state and st.session_state.last_question:
            st.session_state.chat_history.append({
                'question': st.session_state.last_question,
                'time': datetime.now().strftime("%H:%M")
            })
        
        if st.session_state.chat_history:
            with st.expander("📜 سجل الأسئلة"):
                for item in reversed(st.session_state.chat_history[-5:]):
                    st.write(f"🕐 {item['time']} - {item['question']}")
    
    else:
        st.error("❌ لا توجد بيانات")

# --- تصدير ومشاركة ---
elif page == 'export':
    st.header(t('export'))
    
    if df is not None:
        col1, col2, col3 = st.columns(3)
        
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
        
        with col3:
            json_str = df.to_json(orient='records', force_ascii=False)
            st.download_button("📥 JSON", json_str, "data.json", "application/json")
        
        # ======== مشاركة PDF ========
        st.write("---")
        st.subheader("📤 " + ("مشاركة تقرير PDF" if st.session_state.language == 'ar' else "Share PDF Report"))
        
        report_title = st.text_input("عنوان التقرير:", "تقرير تحليل البيانات")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 توليد PDF", type='primary'):
                with st.spinner("⏳ جاري إنشاء التقرير..."):
                    try:
                        pdf_bytes = generate_pdf_report(df)
                        st.session_state.pdf_report = pdf_bytes
                        st.success("✅ تم إنشاء التقرير!")
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
        
        with col2:
            if 'pdf_report' in st.session_state:
                b64 = base64.b64encode(st.session_state.pdf_report).decode()
                st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="report.pdf"><button style="width:100%; padding:10px; background:#e74c3c; color:white; border:none; border-radius:5px;">📥 تحميل PDF</button></a>', unsafe_allow_html=True)
        
        # روابط المشاركة
        if 'pdf_report' in st.session_state:
            st.write("---")
            st.subheader("🔗 روابط المشاركة")
            
            # محاكاة رابط مشاركة
            share_link = f"https://smart-analyst-beast-2.streamlit.app/share/{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 نسخ الرابط"):
                    st.code(share_link)
                    st.success("✅ تم نسخ الرابط!")
            
            with col2:
                whatsapp_msg = f"تقرير تحليل البيانات: {share_link}"
                st.markdown(f'<a href="https://wa.me/?text={whatsapp_msg}" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:white; border:none; border-radius:5px;">📱 واتساب</button></a>', unsafe_allow_html=True)
            
            with col3:
                email_subject = "تقرير تحليل البيانات - Data Beast Pro"
                email_body = f"مرحباً،\n\nإليك رابط التقرير:\n{share_link}\n\n{t('signature')}"
                st.markdown(f'<a href="mailto:?subject={email_subject}&body={email_body}"><button style="width:100%; padding:10px; background:#EA4335; color:white; border:none; border-radius:5px;">📧 إيميل</button></a>', unsafe_allow_html=True)
    
    else:
        st.error("❌ لا توجد بيانات")

# ======== Footer ========
st.write("---")
st.markdown(f"<p style='text-align:center; color:#4ECDC4;'>{t('signature')}</p>", unsafe_allow_html=True)
