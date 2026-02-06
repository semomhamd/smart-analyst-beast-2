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
    """عقل FETH وشخصيته"""
    
    def _init_(self):
        self.name = "FETH"
        self.arabic_name = "فَتْح"
        
    def get_identity(self):
        return {
            "name": self.name,
            "meaning": "الكشف، الوضوح، فتح البيانات",
            "role": "محلل بيانات ذكي + مرشد + صاحب",
            "tone": "واضح، داعم، محترف، خفيف",
            "signature": "— FETH | بيفتح البيانات 🎯"
        }
    
    def respond(self, context, data_insight=None):
        """يختار الرد المناسب حسب السياق"""
        
        responses = {
            'welcome': [
                "أهلاً بيك! أنا FETH... جاهز أفتحلك أي بيانات 🎯",
                "مرحباً! FETH هنا... خلينا نكتشف سوا إيه مخبية البيانات",
                "أهلاً! مع FETH البيانات هتتفتح زي كتاب 📖"
            ],
            'upload_success': [
                f"استلمت الملف! {data_insight or ''}... خليني أفتحه وأشوف جواه إيه 🔍",
                "تمام! البيانات جات... FETH بيفتحها دلوقتي",
                "ملف جديد! جاهزين نكتشف أسراره سوا؟"
            ],
            'analysis_ready': [
                "فتحت البيانات... وده اللي لقيته 👇",
                "التحليل جهز! خليني أفتحلك الرؤية واضحة",
                "كشفت البيانات... والنتيجة مثيرة!"
            ],
            'insight_high': [
                f"🚀 رقم قياسي! {data_insight}... ده أعلى قيمة شوفتها",
                f"🔥 لاحظت حاجة! {data_insight}... فوق المتوقع",
                f"✨ ممتاز! {data_insight}... إنجاز يستحق الاحتفال"
            ],
            'insight_low': [
                f"⚠️ فتحت البيانات ولقيت: {data_insight}... خليني أساعدك تفهم ليه",
                f"👀 لاحظت نقطة: {data_insight}... ممكن نحسنها سوا",
                f"💡 البيانات بتقول: {data_insight}... عندك فكرة ليه؟"
            ],
            'teaching': [
                "خليني أفتحلك النقطة دي ببساطة...",
                "تخيّل معايا كده...",
                "السر هنا إنه..."
            ],
            'support': [
                "ولا يهمك... خلينا نمشي خطوة خطوة 🤝",
                "تمام، أنا معاك... جرب كده",
                "مش مشكلة، FETH هيساعدك تعديها"
            ],
            'celebration': [
                "🎉 كده فتحتها! إنجاز رائع",
                "👏 أحسنت! البيانات دلوقتي واضحة زي الشمس",
                "🎯 هدف محقق! جاهز للخطوة الجاية؟"
            ],
            'error': [
                "حصلت حاجة بسيطة... خليني أجرب تاني",
                "مش مشكلة، كلنا بنغلط... جرب معايا كده",
                "FETH لسه بيتعلم... ساعدني أفهم المشكلة"
            ]
        }
        
        if context in responses:
            return random.choice(responses[context])
        return "FETH هنا... جاهز أساعدك 🎯"
    
    def suggest_next(self, current_page):
        """يقترح الخطوة الجاية حسب السياق"""
        
        suggestions = {
            'home': [
                "📥 ارفع ملف بيانات جديد",
                "📊 جرب البيانات التجريبية",
                "🤖 اسأل FETH عن أي حاجة"
            ],
            'upload': [
                "🧹 نظف البيانات من الفارغ",
                "📊 روح لتحليل Power BI",
                "🤖 اسأل FETH يحلللك البيانات"
            ],
            'cleaner': [
                "📊 شوف التحليلات البصرية",
                "📈 اعمل Pivot Table",
                "🤖 اسأل FETH عن النتائج"
            ],
            'excel': [
                "📈 اعمل رسم بياني",
                "📤 صدّر التقرير PDF",
                "🤖 اسأل FETH يفسر الصيغ"
            ],
            'powerbi': [
                "📊 غيّر نوع الرسم البياني",
                "📤 صدّر النتائج",
                "🤖 اسأل FETH عن التوجهات"
            ],
            'ai': [
                "📊 روح للتحليل البصري",
                "📤 جهّز تقرير PDF",
                "🧹 نظف البيانات أكتر"
            ]
        }
        return suggestions.get(current_page, ["🤖 اسأل FETH"])
    
    def get_signature(self):
        return "— FETH | بيفتح البيانات 🎯"


# ======== إعدادات الصفحة ========
st.set_page_config(page_title="Data Beast Pro | FETH", layout="wide", page_icon="🎯")

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
if 'feth' not in st.session_state:
    st.session_state.feth = FethPersonality()
if 'feth_welcomed' not in st.session_state:
    st.session_state.feth_welcomed = False

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
        'ai': '🤖 FETH AI',
        'export': '💾 تصدير',
        'settings': '⚙️ الإعدادات',
        'share': '📤 مشاركة',
        'sample': '📊 بيانات تجريبية',
        'clear': '🗑️ مسح',
        'save': '💾 حفظ',
        'signature': '🔥 MIA8444 | Data Beast Pro © 2024 | 🎯 FETH'
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
        'ai': '🤖 FETH AI',
        'export': '💾 Export',
        'settings': '⚙️ Settings',
        'share': '📤 Share',
        'sample': '📊 Sample',
        'clear': '🗑️ Clear',
        'save': '💾 Save',
        'signature': '🔥 MIA8444 | Data Beast Pro © 2024 | 🎯 FETH'
    }
}

def t(key):
    return TEXTS[st.session_state.language].get(key, key)

# ======== CSS ========
theme_css = """
<style>
    .main {background-color: #0E1117; color: #FAFAFA;}
    .stButton>button {width: 100%; background: linear-gradient(45deg, #3498DB, #2C3E50); color: white; border: none; border-radius: 10px; padding: 10px;}
    .stButton>button:hover {transform: scale(1.05); box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);}
    .metric-card {background: linear-gradient(135deg, #3498DB, #2C3E50); padding: 20px; border-radius: 15px; color: white; text-align: center;}
    .feth-box {background: linear-gradient(135deg, #3498DB, #2C3E50); padding: 15px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;}
    .excel-cell {border: 1px solid #444; padding: 5px; text-align: center;}
    .formula-bar {background: #1a1a2e; padding: 10px; border-radius: 5px; font-family: monospace;}
</style>
""" if st.session_state.dark_mode else """
<style>
    .main {background-color: #FFFFFF; color: #333333;}
    .stButton>button {width: 100%; background: linear-gradient(45deg, #3498DB, #2C3E50); color: white;}
    .feth-box {background: linear-gradient(135deg, #3498DB, #2C3E50); padding: 15px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;}
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
    """مساعد FETH الذكي"""
    question = question.lower()
    feth = st.session_state.feth
    
    if "إجمالي" in question or "total" in question or "sum" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            total = df[numeric_cols[0]].sum()
            return f"{feth.respond('insight_high', f'الإجمالي: {total:,.0f}')}\n\n💰 الإجمالي: {total:,.0f}"
    
    elif "متوسط" in question or "average" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            avg = df[numeric_cols[0]].mean()
            return f"📊 المتوسط: {avg:,.2f}\n\n{feth.get_signature()}"
    
    elif "أعلى" in question or "max" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            best_idx = df[numeric_cols[0]].idxmax()
            best_item = df.loc[best_idx, cat_cols[0]]
            best_value = df[numeric_cols[0]].max()
            return f"{feth.respond('insight_high', f'{best_item}: {best_value:,.0f}')}\n\n🏆 الأعلى: {best_item} ({best_value:,.0f})"
    
    elif "أقل" in question or "min" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            worst_idx = df[numeric_cols[0]].idxmin()
            worst_item = df.loc[worst_idx, cat_cols[0]]
            worst_value = df[numeric_cols[0]].min()
            return f"{feth.respond('insight_low', f'{worst_item}: {worst_value:,.0f}')}\n\n📉 الأقل: {worst_item} ({worst_value:,.0f})"
    
    elif "عدد" in question or "count" in question:
        return f"{feth.respond('analysis_ready')}\n\n📋 عدد الصفوف: {len(df):,}"
    
    elif "ملخص" in question or "summary" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        report = f"{feth.respond('analysis_ready')}\n\n"
        report += f"📊 ملخص البيانات:\n\n"
        report += f"• الصفوف: {len(df):,}\n"
        report += f"• الأعمدة: {len(df.columns)}\n"
        if len(numeric_cols) > 0:
            report += f"• الإجمالي: {df[numeric_cols[0]].sum():,.0f}\n"
            report += f"• المتوسط: {df[numeric_cols[0]].mean():,.2f}\n"
        return report + f"\n{feth.get_signature()}"
    
    else:
        return f"""{feth.respond('teaching')}

🤔 جرب تسأل FETH:
* "ما إجمالي المبيعات؟"
* "ما المتوسط؟"
* "أعلى منتج مبيعاً؟"
* "عدد الصفوف؟"
* "ملخص البيانات؟"

{feth.get_signature()}"""

def generate_pdf_report(df, charts_data=None):
    """توليد تقرير PDF"""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Data Beast Pro - FETH Report', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'FETH | بيفتح البيانات 🎯 | Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(0, 10, f'Data Summary by FETH', 0, 1)
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
            parts = formula[3:-1].split(',')
            if len(parts) == 3:
                condition = parts[0].strip()
                true_val = parts[1].strip()
                false_val = parts[2].strip()
                
                if '>' in condition:
                    col, val = condition.split('>')
                    col = col.strip()
                    val = float(val.strip())
                    return df.apply(lambda row: true_val if row[col] > val else false_val, axis=1)
        
        elif formula.upper().startswith('VLOOKUP('):
            return "VLOOKUP يحتاج جدول مرجعي"
        
        else:
            return "FETH: الصيغة مش واضحة، جرب دالة تانية"
    
    except Exception as e:
        return f"FETH لاحظ خطأ: {str(e)}"

# ======== Sidebar مع FETH ========
with st.sidebar:
    # FETH Box
    st.markdown("""
    <div class='feth-box'>
        <h2 style='margin:0; font-size:28px;'>🎯 FETH</h2>
        <p style='font-size:14px; margin:5px 0; opacity:0.9;'>بيفتح البيانات</p>
        <div style='width:60px; height:3px; background:white; margin:10px auto; border-radius:2px;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    # رسالة ترحيب من FETH
    if not st.session_state.feth_welcomed:
        st.info(st.session_state.feth.respond('welcome'))
        st.session_state.feth_welcomed = True
    
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
    
    # أدوات سريعة
    st.markdown("### ⚡ " + ("أدوات سريعة" if st.session_state.language == 'ar' else "Quick Tools"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(t('sample'), key='btn_sample'):
            st.session_state.df = generate_sample_data()
            st.success(st.session_state.feth.respond('celebration'))
            st.rerun()
    
    with col2:
        if st.button(t('clear'), key='btn_clear'):
            st.session_state.df = None
            st.session_state.cleaning_history = []
            st.info("🎯 FETH: جاهز نبدأ من جديد!")
            st.rerun()
    
    # اقتراحات FETH الذكية
    st.write("---")
    st.markdown("### 💡 " + ("FETH يقترح" if st.session_state.language == 'ar' else "FETH Suggests"))
    
    current_page = st.session_state.page
    suggestions = st.session_state.feth.suggest_next(current_page)
    
    for suggestion in suggestions[:2]:  # اقتراحين بس
        if st.button(suggestion, key=f"feth_sug_{suggestion}"):
            if "رفع" in suggestion or "Upload" in suggestion:
                st.session_state.page = 'upload'
            elif "نظف" in suggestion or "Clean" in suggestion:
                st.session_state.page = 'cleaner'
            elif "تحليل" in suggestion or "Power" in suggestion:
                st.session_state.page = 'powerbi'
            elif "Excel" in suggestion or "صيغ" in suggestion:
                st.session_state.page = 'excel'
            elif "سأل" in suggestion or "Ask" in suggestion:
                st.session_state.page = 'ai'
            elif "تجريبية" in suggestion or "Sample" in suggestion:
                st.session_state.df = generate_sample_data()
            st.rerun()
    
    st.write("---")
    st.caption(t('signature'))

# ======== الصفحات ========
page = st.session_state.page
df = st.session_state.df
feth = st.session_state.feth

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
        st.success("🎯 FETH: تم الحفظ!")
        st.session_state.page = 'home'
        st.rerun()

# --- الرئيسية مع FETH ---
elif page == 'home':
    st.markdown(f"<h1 style='text-align:center; color:#3498DB;'>🎯 FETH | Data Beast Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:gray; font-size:18px;'>"
                f"{feth.respond('welcome')}</p>", unsafe_allow_html=True)
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # FETH يحلل البيانات
        st.success(f"🎯 {feth.respond('analysis_ready')}")
        
        # مؤشرات سريعة
        cols = st.columns(4)
        cols[0].metric("📊 الصفوف", len(df))
        cols[1].metric("📋 الأعمدة", len(df.columns))
        
        if len(numeric_cols) > 0:
            total = df[numeric_cols[0]].sum()
            avg = df[numeric_cols[0]].mean()
            
            cols[2].metric("💰 الإجمالي", f"{total:,.0f}")
            cols[3].metric("📈 المتوسط", f"{avg:,.0f}")
            
            # FETH يعلق على الأرقام
            if total > 100000:
                st.balloons()
                st.success(f"🎯 {feth.respond('celebration')}")
        
        st.dataframe(df.head(10), use_container_width=True)
        
        # FETH يقترح الخطوة الجاية
        st.write("---")
        st.markdown(f"### 🎯 {feth.respond('teaching').replace('خليني أفتحلك النقطة دي ببساطة...', 'الخطوة الجاية؟')}")
        
        next_steps = feth.suggest_next('home')
        step_cols = st.columns(len(next_steps))
        for i, step in enumerate(next_steps):
            with step_cols[i]:
                if st.button(step, key=f"next_{i}"):
                    if "رفع" in step:
                        st.session_state.page = 'upload'
                    elif "تجريبية" in step:
                        st.session_state.df = generate_sample_data()
                    elif "اسأل" in step:
                        st.session_state.page = 'ai'
                    st.rerun()
    
    else:
        # FETH يشجع على البدء
        st.info(f"🎯 {feth.respond('welcome')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 جرب البيانات التجريبية", type='primary'):
                st.session_state.df = generate_sample_data()
                st.rerun()
        with col2:
            if st.button("📥 ارفع ملفك الخاص"):
                st.session_state.page = 'upload'
                st.rerun()

# --- OCR ---
elif page == 'ocr':
    st.header("👁️ OCR Vision | FETH")
    
    uploaded = st.file_uploader("📸 ارفع صورة:", ['jpg', 'jpeg', 'png'])
    
    if uploaded:
        from PIL import Image
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
        
        with st.spinner("🎯 FETH بيفتح الصورة..."):
            import time
            time.sleep(2)
            
            ocr_data = {
                'المنتج': ['لابتوب', 'موبايل', 'تابلت'],
                'السعر': [12000, 25000, 8000],
                'الكمية': [2, 1, 3]
            }
            df_ocr = pd.DataFrame(ocr_data)
            
            st.success(f"🎯 {feth.respond('analysis_ready')}")
            st.dataframe(df_ocr)
            
            if st.button("📊 استخدم البيانات", type='primary'):
                st.session_state.df = df_ocr
                st.success(f"🎯 {feth.respond('celebration')}")

# --- رفع بيانات ---
elif page == 'upload':
    st.header("📥 " + t('upload') + " | FETH")
    
    st.info(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'ارفع ملفك وهفتحهولك')}!")
    
    uploaded = st.file_uploader("اختر ملف:", ['csv', 'xlsx', 'xls'])
    
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df_new = pd.read_csv(uploaded)
            else:
                df_new = pd.read_excel(uploaded)
            
            st.session_state.df = df_new
            st.success(f"🎯 {feth.respond('upload_success', f'{len(df_new):,} صف')}")
            st.dataframe(df_new.head())
            
            st.write("---")
            st.markdown(f"### 💡 {feth.respond('teaching').replace('خليني أفتحلك النقطة دي ببساطة...', 'نعمل إيه دلوقتي؟')}")
            
            next_steps = feth.suggest_next('upload')
            cols = st.columns(len(next_steps))
            for i, step in enumerate(next_steps):
                with cols[i]:
                    if st.button(step, key=f"upload_next_{i}"):
                        if "نظف" in step:
                            st.session_state.page = 'cleaner'
                        elif "Power" in step:
                            st.session_state.page = 'powerbi'
                        elif "FETH" in step:
                            st.session_state.page = 'ai'
                        st.rerun()
                        
        except Exception as e:
            st.error(f"🎯 {feth.respond('error')}: {str(e)}")

# --- منظف البيانات ---
elif page == 'cleaner':
    st.header("🧹 " + t('cleaner') + " | FETH")
    
    if df is not None:
        st.info(f"🎯 {feth.respond('analysis_ready')}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("الصفوف", len(df))
        col2.metric("الأعمدة", len(df.columns))
        empty_count = int(df.isnull().sum().sum())
        dup_count = int(df.duplicated().sum())
        col3.metric("الفارغ", empty_count)
        col4.metric("التكرار", dup_count)
        
        if empty_count > 0:
            st.warning(f"🎯 {feth.respond('insight_low', f'{empty_count} قيمة فارغة')}")
        
        st.write("---")
        st.subheader("🔧 أدوات التنظيف")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ حذف الفارغ", key='drop_na'):
                st.session_state.df = df.dropna()
                st.session_state.cleaning_history.append("حذف القيم الفارغة")
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        with col2:
            if st.button("📋 حذف التكرار", key='drop_dup'):
                st.session_state.df = df.drop_duplicates()
                st.session_state.cleaning_history.append("حذف التكرارات")
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        with col3:
            if st.button("🔤 تنظيف النص", key='clean_text'):
                df_clean = df.copy()
                for col in df_clean.select_dtypes(include=['object']):
                    df_clean[col] = df_clean[col].str.strip().str.title()
                st.session_state.df = df_clean
                st.session_state.cleaning_history.append("تنظيف النصوص")
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        if st.session_state.cleaning_history:
            with st.expander("📜 سجل التنظيف"):
                for i, action in enumerate(st.session_state.cleaning_history, 1):
                    st.write(f"{i}. {action}")
        
        st.dataframe(df, use_container_width=True)
    else:
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'محتاج بيانات الأول! ارفع ملف')} ❌")

# --- Excel Pro ---
elif page == 'excel':
    st.header("📊 Excel Pro | FETH")
    
    if df is not None:
        st.info(f"🎯 {feth.respond('analysis_ready')}")
        
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
                st.success(f"🎯 {feth.respond('celebration')}")
            else:
                st.info(f"🎯 FETH: النتيجة = {result}")
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
            """)
        
        # الجدول
        st.write("---")
        st.subheader("📋 ورقة العمل")
        
        edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=400)
        
        if st.button("💾 حفظ جميع التغييرات", type='primary'):
            st.session_state.df = edited
            st.success(f"🎯 {feth.respond('celebration')}")
            st.balloons()
    
    else:
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'محتاج بيانات الأول')} ❌")

# --- Power BI ---
elif page == 'powerbi':
    st.header("📈 Power BI | FETH")
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            st.info(f"🎯 {feth.respond('analysis_ready')}")
            
            kpi = st.selectbox("اختر المؤشر:", numeric_cols)
            
            cols = st.columns(4)
            total_val = df[kpi].sum()
            avg_val = df[kpi].mean()
            max_val = df[kpi].max()
            
            cols[0].metric("الإجمالي", f"{total_val:,.0f}")
            cols[1].metric("المتوسط", f"{avg_val:,.0f}")
            cols[2].metric("الأعلى", f"{max_val:,.0f}")
            cols[3].metric("العدد", len(df))
            
            # FETH يعلق
            if total_val > df[kpi].mean() * len(df) * 0.5:
                st.success(f"🎯 {feth.respond('insight_high', f'أداء قوي في {kpi}')}")
            
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
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'محتاج بيانات الأول')} ❌")

# --- SQL ---
elif page == 'sql':
    st.header("🗄️ SQL | FETH")
    
    if df is not None:
        st.info(f"🎯 {feth.respond('teaching')}")
        
        query = st.text_area("اكتب استعلام SQL:", "SELECT * FROM data LIMIT 10")
        
        if st.button("▶️ تشغيل"):
            st.warning("🎯 FETH: مكتبة DuckDB غير مثبتة في السحابة حالياً")
    else:
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'محتاج بيانات الأول')} ❌")

# --- FETH AI Assistant ---
elif page == 'ai':
    st.header("🎯 FETH | المحلل الذكي")
    
    if df is not None:
        st.success(f"🎯 {feth.respond('analysis_ready')}")
        
        with st.expander("👁️ FETH شايف إيه؟"):
            st.dataframe(df.head(), use_container_width=True)
            st.write(f"📊 FETH يحلل {len(df):,} صف و {len(df.columns)} عمود")
        
        st.write("---")
        st.subheader("💬 اسأل FETH")
        
        examples = [
            "افتحلي المبيعات وقوللي إجماليها؟",
            "شايف إيه أعلى منتج مبيعاً؟",
            "فتحلي البيانات وقوللي ملخصها؟",
            "إيه الاتجاهات اللي لاحظتها؟",
            "قارنلي النتائج بالمتوسط"
        ]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question = st.text_input("📝 سؤالك لـ FETH:", 
                                   placeholder="مثال: افتحلي المبيعات...")
        
        with col2:
            st.write("")
            st.write("")
            ask_btn = st.button("🎯 اسأل FETH", type='primary')
        
        # أمثلة سريعة
        st.write("*FETH يقترح تسأل:*")
        ex_cols = st.columns(len(examples))
        for i, ex in enumerate(examples):
            with ex_cols[i]:
                if st.button(ex, key=f'feth_ex_{i}'):
                    st.session_state.last_question = ex
                    st.rerun()
        
        # الرد
        if ask_btn and question:
            with st.spinner("🎯 FETH بيفتح البيانات..."):
                answer = ai_assistant(df, question)
                st.success(answer)
                
                # FETH يقترح بعد الرد
                st.write("---")
                st.markdown(f"### 💡 {feth.respond('teaching').replace('خليني أفتحلك النقطة دي ببساطة...', 'تعمل إيه بعد كده؟')}")
                more = feth.suggest_next('ai')
                for m in more[:2]:
                    if st.button(m, key=f"feth_more_{m}"):
                        if "بصري" in m:
                            st.session_state.page = 'powerbi'
                        elif "PDF" in m:
                            st.session_state.page = 'export'
                        elif "نظف" in m:
                            st.session_state.page = 'cleaner'
                        st.rerun()
        
        # سجل المحادثة
        if 'last_question' in st.session_state:
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({
                'question': st.session_state.last_question,
                'time': datetime.now().strftime("%H:%M")
            })
            
            if st.session_state.chat_history:
                with st.expander("📜 سجل الأسئلة"):
                    for item in reversed(st.session_state.chat_history[-5:]):
                        st.write(f"🕐 {item['time']} - {item['question']}")
    
    else:
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'محتاج بيانات الأول! ارفع ملف')} ❌")

# --- تصدير ومشاركة ---
elif page == 'export':
    st.header("💾 " + t('export') + " | FETH")
    
    if df is not None:
        st.info(f"🎯 {feth.respond('analysis_ready')}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="data.csv"><button style="width:100%; padding:10px; background:#3498DB; color:white; border:none; border-radius:5px;">📥 CSV</button></a>', unsafe_allow_html=True)
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            b64 = base64.b64encode(output.getvalue()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data.xlsx"><button style="width:100%; padding:10px; background:#2C3E50; color:white; border:none; border-radius:5px;">📥 Excel</button></a>', unsafe_allow_html=True)
        
        with col3:
            json_str = df.to_json(orient='records', force_ascii=False)
            st.download_button("📥 JSON", json_str, "data.json", "application/json")
        
        # PDF
        st.write("---")
        st.subheader("📤 تقرير PDF | FETH")
        
        if st.button("📄 توليد PDF", type='primary'):
            with st.spinner("🎯 FETH بيعمل التقرير..."):
                try:
                    pdf_bytes = generate_pdf_report(df)
                    st.session_state.pdf_report = pdf_bytes
                    st.success(f"🎯 {feth.respond('celebration')}")
                except Exception as e:
                    st.error(f"🎯 {feth.respond('error')}: {str(e)}")
        
        if 'pdf_report' in st.session_state:
            b64 = base64.b64encode(st.session_state.pdf_report).decode()
            st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="feth_report.pdf"><button style="width:100%; padding:10px; background:#e74c3c; color:white; border:none; border-radius:5px;">📥 تحميل تقرير FETH</button></a>', unsafe_allow_html=True)
    
    else:
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة 🤝', 'محتاج بيانات الأول')} ❌")

# ======== Footer ========
st.write("---")
st.markdown(f"<p style='text-align:center; color:#3498DB; font-size:16px;'>"
            f"🎯 FETH | بيفتح البيانات</p>", 
            unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:gray; font-size:12px;'>"
            f"🔥 MIA8444 | Data Beast Pro © 2024</p>", 
            unsafe_allow_html=True)
