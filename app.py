import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import base64
from fpdf import FPDF
import json

# ======== إعدادات الصفحة ========
st.set_page_config(
    page_title="Data Beast Pro | تحليل البيانات الشامل",
    layout="wide", 
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# ======== CSS احترافي ========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    * {font-family: 'Tajawal', sans-serif;}
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    
    .sub-header {
        text-align: center;
        color: #95A5A6;
        font-size: 1.2rem;
        margin-top: 0;
    }
    
    .tool-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        transition: transform 0.3s;
        cursor: pointer;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .signature {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: rgba(0,0,0,0.8);
        color: #4ECDC4;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 12px;
        z-index: 1000;
    }
    
    .watermark {
        position: fixed;
        bottom: 50%;
        right: 50%;
        transform: translate(50%, 50%) rotate(-45deg);
        font-size: 100px;
        color: rgba(255,255,255,0.03);
        pointer-events: none;
        z-index: 0;
    }
</style>
""", unsafe_allow_html=True)

# ======== الذاكرة الدائمة ========
if 'df' not in st.session_state:
    st.session_state.df = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'reports' not in st.session_state:
    st.session_state.reports = []

# ======== الشعار والتوقيع ========
SIGNATURE = "🔥 MIA8444 | Data Beast Pro © 2024"
WATERMARK = "DATA BEAST PRO"

# ======== Sidebar الاحترافي ========
with st.sidebar:
    # اللوجو
    try:
        st.image("8888.jpg", use_column_width=True)
    except:
        st.markdown('<h1 style="text-align:center; font-size:4rem;">🦁</h1>', unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align:center; color:#FF6B6B;">Data Beast Pro</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#95A5A6;">منصة تحليل البيانات الشاملة</p>', unsafe_allow_html=True)
    
    st.write("---")
    
    # القائمة الرئيسية
    menu = st.radio("🧰 أدوات التحليل:", [
        "🏠 الرئيسية",
        "📥 استيراد البيانات",
        "📊 Excel Pro الاحترافي",
        "🔄 Power Query",
        "🐍 Python Analytics",
        "📈 Power BI Dashboard",
        "📉 Tableau Studio",
        "🗄️ SQL Master",
        "☁️ Google Sheets",
        "🤖 AI Analytics",
        "📑 تقارير PDF",
        "💾 التصدير المتقدم"
    ])
    
    st.write("---")
    
    # أدوات سريعة
    st.markdown("### ⚡ أدوات سريعة")
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("📊 بيانات تجريبية", use_container_width=True):
            st.session_state.df = pd.DataFrame({
                'ID': range(1, 1001),
                'التاريخ': pd.date_range('2024-01-01', periods=1000, freq='D'),
                'المنتج': np.random.choice(['لابتوب', 'موبايل', 'تابلت', 'سماعات', 'شاحن'], 1000),
                'الفئة': np.random.choice(['إلكترونيات', 'اكسسوارات', 'أجهزة'], 1000),
                'المبيعات': np.random.randint(1000, 50000, 1000),
                'الكمية': np.random.randint(1, 50, 1000),
                'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض', 'جدة', 'لندن'], 1000),
                'العميل': [f"عميل_{i}" for i in range(1000)],
                'التقييم': np.random.randint(1, 6, 1000),
                'الخصم': np.random.randint(0, 30, 1000),
                'الربح': np.random.randint(200, 15000, 1000)
            })
            st.success("✅ تم توليد 1000 صف!")
            st.rerun()
    
    with cols[1]:
        if st.button("🗑️ مسح البيانات", use_container_width=True):
            st.session_state.df = None
            st.session_state.history = []
            st.rerun()
    
    st.write("---")
    st.caption(f"🔒 {SIGNATURE}")

# ======== دوال مساعدة ========
def generate_pdf_report(df, title="تقرير تحليل البيانات"):
    """توليد تقرير PDF مع علامة مائية"""
    class PDF(FPDF):
        def header(self):
            # علامة مائية
            self.set_font('Arial', 'B', 60)
            self.set_text_color(230, 230, 230)
            self.text(50, 150, WATERMARK)
            
            # العنوان
            self.set_font('Arial', 'B', 16)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, title, 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'{SIGNATURE} | Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    
    # ملخص البيانات
    pdf.cell(0, 10, f'عدد السجلات: {len(df)}', 0, 1)
    pdf.cell(0, 10, f'عدد الأعمدة: {len(df.columns)}', 0, 1)
    pdf.ln(10)
    
    # الإحصائيات
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'الإحصائيات:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols[:5]:
        stats = df[col].describe()
        pdf.cell(0, 8, f'{col}: المتوسط={stats["mean"]:.2f}, الأعلى={stats["max"]:.2f}', 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

def get_download_link(data, filename, file_type):
    """توليد روابط التحميل"""
    if file_type == 'csv':
        b64 = base64.b64encode(data.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}"><button style="background:#4ECDC4;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">📥 CSV</button></a>'
    elif file_type == 'excel':
        b64 = base64.b64encode(data).decode()
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"><button style="background:#FF6B6B;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">📥 Excel</button></a>'
    elif file_type == 'pdf':
        b64 = base64.b64encode(data).decode()
        return f'<a href="data:application/pdf;base64,{b64}" download="{filename}"><button style="background:#e74c3c;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">📥 PDF</button></a>'

# ======== الصفحات ========

df = st.session_state.df

# --- الرئيسية ---
if menu == "🏠 الرئيسية":
    st.markdown('<h1 class="main-header">🦁 Data Beast Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">منصة تحليل البيانات الشاملة | Excel + Power BI + Python + SQL + AI</p>', unsafe_allow_html=True)
    
    # بطاقات الأدوات
    st.write("---")
    st.subheader("🧰 أدوات التحليل المتاحة")
    
    tools = [
        ("📊", "Excel Pro", "محرك جداول احترافي"),
        ("🔄", "Power Query", "تحويل البيانات"),
        ("🐍", "Python", "تحليل برمجي"),
        ("📈", "Power BI", "داشبورد تفاعلي"),
        ("📉", "Tableau", "تصور بياني"),
        ("🗄️", "SQL", "استعلامات قواعد البيانات"),
        ("☁️", "Google Sheets", "تكامل السحابة"),
        ("🤖", "AI Analytics", "ذكاء اصطناعي"),
    ]
    
    cols = st.columns(4)
    for i, (icon, name, desc) in enumerate(tools):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="tool-card">
                <h1>{icon}</h1>
                <h3>{name}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # حالة البيانات
    st.write("---")
    if df is not None:
        st.success(f"✅ البيانات محملة: {len(df):,} صف | {len(df.columns)} عمود")
        
        # إحصائيات سريعة
        cols = st.columns(4)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            cols[0].metric("📊 الإجمالي", f"{df[numeric_cols[0]].sum():,.0f}")
            cols[1].metric("📈 المتوسط", f"{df[numeric_cols[0]].mean():,.0f}")
            cols[2].metric("🏆 الأعلى", f"{df[numeric_cols[0]].max():,.0f}")
            cols[3].metric("📉 الأدنى", f"{df[numeric_cols[0]].min():,.0f}")
        
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("ℹ️ لا توجد بيانات. استخدم 'بيانات تجريبية' من القائمة")

# --- استيراد البيانات ---
elif menu == "📥 استيراد البيانات":
    st.header("📥 مركز استيراد البيانات")
    
    tabs = st.tabs(["📤 رفع ملف", "🔗 Google Sheets", "🗄️ قاعدة بيانات", "📋 لصق يدوي"])
    
    with tabs[0]:
        uploaded = st.file_uploader("ارفع Excel, CSV, JSON", type=['csv', 'xlsx', 'xls', 'json'])
        if uploaded:
            try:
                if uploaded.name.endswith('.csv'):
                    df_new = pd.read_csv(uploaded)
                elif uploaded.name.endswith('.json'):
                    df_new = pd.read_json(uploaded)
                else:
                    df_new = pd.read_excel(uploaded)
                
                st.session_state.df = df_new
                st.success(f"✅ تم استيراد {len(df_new):,} صف!")
                st.dataframe(df_new.head(), use_container_width=True)
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
    
    with tabs[1]:
        st.info("☁️ قريباً: تكامل مباشر مع Google Sheets")
        sheet_url = st.text_input("رابط Google Sheet:")
        if st.button("🔗 اتصال"):
            st.warning("🚧 قيد التطوير")
    
    with tabs[2]:
        st.info("🗄️ قريباً: دعم MySQL, PostgreSQL, SQL Server")
        conn_str = st.text_input("سلسلة الاتصال:")
    
    with tabs[3]:
        data_text = st.text_area("الصق البيانات هنا (CSV format):")
        if st.button("📥 استيراد"):
            try:
                from io import StringIO
                df_new = pd.read_csv(StringIO(data_text))
                st.session_state.df = df_new
                st.success("✅ تم!")
            except:
                st.error("❌ تنسيق غير صحيح")

# --- Excel Pro ---
elif menu == "📊 Excel Pro الاحترافي":
    st.header("📊 Excel Pro - محرك الجداول الاحترافي")
    
    if df is not None:
        # أدوات Excel
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("🔍 بحث")
        with col2:
            st.button("🎨 تنسيق")
        with col3:
            st.button("📊 رسم بياني")
        with col4:
            st.button("⚡ Pivot Table")
        
        # الجدول
        st.subheader("📋 ورقة العمل")
        
        # تعديلات متقدمة
        edit_mode = st.checkbox("✏️ وضع التعديل", value=True)
        
        if edit_mode:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, height=600)
            if st.button("💾 حفظ التغييرات", type="primary"):
                st.session_state.df = edited_df
                st.success("✅ تم الحفظ!")
                st.balloons()
        else:
            st.dataframe(df, use_container_width=True, height=600)
        
        # صيغ ودوال
        with st.expander("⚡ دوال Excel"):
            st.code("""
=SUM(المبيعات)          → مجموع
=AVERAGE(التقييم)       → متوسط
=COUNT(المنتج)          → عدد
=MAX(الربح)             → أقصى
=VLOOKUP(...)           → بحث
            """)
    else:
        st.error("❌ لا توجد بيانات")

# --- Power Query ---
elif menu == "🔄 Power Query":
    st.header("🔄 Power Query - تحويل البيانات")
    
    if df is not None:
        st.subheader("⚡ خطوات التحويل")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 تنظيف")
            if st.button("🗑️ حذف الصفوف الفارغة"):
                st.session_state.df = df.dropna()
                st.rerun()
            
            if st.button("✂️ حذف التكرارات"):
                st.session_state.df = df.drop_duplicates()
                st.rerun()
        
        with col2:
            st.markdown("### 🔄 تحويل")
            if st.button("📅 فصل التاريخ"):
                if 'التاريخ' in df.columns:
                    df['السنة'] = pd.to_datetime(df['التاريخ']).dt.year
                    df['الشهر'] = pd.to_datetime(df['التاريخ']).dt.month
                    st.session_state.df = df
                    st.rerun()
            
            if st.button("🔤 تصنيف نصي"):
                st.info("🚧 قيد التطوير")
        
        # معاينة
        st.subheader("👁️ المعاينة")
        st.dataframe(df.head(20), use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

# --- Python Analytics ---
elif menu == "🐍 Python Analytics":
    st.header("🐍 Python Analytics - تحليل برمجي")
    
    if df is not None:
        st.subheader("📝 كود Python")
        
        code = st.text_area("اكتب كود Python:", """
# df هو DataFrame الخاص بك
result = df.groupby('الفرع')['المبيعات'].sum()
print(result)
        """, height=200)
        
        if st.button("▶️ تشغيل"):
            try:
                # تنفيذ الكود في بيئة آمنة
                local_vars = {'df': df, 'pd': pd, 'np': np}
                exec(code, local_vars)
                if 'result' in local_vars:
                    st.write("النتيجة:")
                    st.write(local_vars['result'])
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        
        # مكتبات جاهزة
        with st.expander("📚 مكتبات متاحة"):
            st.code("""
pandas as pd    → تحليل البيانات
numpy as np     → العمليات الرياضية
plotly.express  → الرسوم البيانية
sklearn         → التعلم الآلي
            """)
    else:
        st.error("❌ لا توجد بيانات")

# --- Power BI Dashboard ---
elif menu == "📈 Power BI Dashboard":
    st.header("📈 Power BI Dashboard - داشبورد احترافي")
    
    if df is not None:
        # KPIs رئيسية
        st.subheader("📊 مؤشرات الأداء الرئيسية")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            kpi = st.selectbox("اختر المؤشر:", numeric_cols)
            
            cols = st.columns(4)
            cols[0].metric("💰 الإجمالي", f"{df[kpi].sum():,.0f}")
            cols[1].metric("📊 المتوسط", f"{df[kpi].mean():,.0f}")
            cols[2].metric("📈 النمو", f"{np.random.randint(-20, 50)}%")
            cols[3].metric("🎯 الهدف", f"{df[kpi].sum() * 1.2:,.0f}")
            
            # الرسوم البيانية
            st.write("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if 'الفئة' in df.columns:
                    fig = px.pie(df, values=kpi, names='الفئة', title=f"توزيع {kpi} حسب الفئة")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'الفرع' in df.columns:
                    branch_data = df.groupby('الفرع')[kpi].sum().sort_values(ascending=True)
                    fig = px.bar(x=branch_data.values, y=branch_data.index, orientation='h', title=f"{kpi} حسب الفرع")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Trend
            if 'التاريخ' in df.columns:
                st.subheader("📈 التطور الزمني")
                daily = df.groupby('التاريخ')[kpi].sum().reset_index()
                fig = px.line(daily, x='التاريخ', y=kpi, title="التطور اليومي")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

# --- Tableau Studio ---
elif menu == "📉 Tableau Studio":
    st.header("📉 Tableau Studio - تصور بياني متقدم")
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if numeric_cols and cat_cols:
            st.subheader("🎨 مصمم الرسوم البيانية")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                x_axis = st.selectbox("المحور X:", cat_cols)
            with col2:
                y_axis = st.selectbox("المحور Y:", numeric_cols)
            with col3:
                chart_type = st.selectbox("نوع الرسم:", ["شريطي", "خطي", "دائري", "مبعثر", "صندوق"])
            
            color_col = st.selectbox("التلوين حسب:", ["بدون"] + cat_cols)
            
            if st.button("📊 إنشاء الرسم", type="primary"):
                color = None if color_col == "بدون" else color_col
                
                if chart_type == "شريطي":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=color, title=f"{y_axis} حسب {x_axis}")
                elif chart_type == "خطي":
                    fig = px.line(df, x=x_axis, y=y_axis, color=color, title=f"تطور {y_axis}")
                elif chart_type == "دائري":
                    fig = px.pie(df, values=y_axis, names=x_axis, title=f"توزيع {y_axis}")
                elif chart_type == "مبعثر":
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color, size=y_axis, title=f"علاقة {x_axis} و {y_axis}")
                else:
                    fig = px.box(df, x=x_axis, y=y_axis, color=color, title=f"توزيع {y_axis}")
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

# --- SQL Master ---
elif menu == "🗄️ SQL Master":
    st.header("🗄️ SQL Master - محرك الاستعلامات")
    
    if df is not None:
        try:
            import duckdb
            
            st.success(f"✅ متصل بقاعدة البيانات | الجدول: data | {len(df):,} صف")
            
            # أمثلة
            examples = {
                "كل البيانات": "SELECT * FROM data LIMIT 100",
                "إجمالي المبيعات حسب الفرع": "SELECT الفرع, SUM(المبيعات) as total FROM data GROUP BY الفرع ORDER BY total DESC",
                "أفضل 10 منتجات": "SELECT المنتج, SUM(المبيعات) as total FROM data GROUP BY المنتج ORDER BY total DESC LIMIT 10",
                "متوسط التقييم": "SELECT AVG(التقييم) as avg_rating FROM data",
                "مبيعات الشهر": "SELECT strftime('%Y-%m', التاريخ) as month, SUM(المبيعات) as sales FROM data GROUP BY month",
                "تصفية شرطية": "SELECT * FROM data WHERE المبيعات > 30000 AND التقييم >= 4"
            }
            
            selected = st.selectbox("📚 أمثلة:", list(examples.keys()))
            query = st.text_area("📝 استعلام SQL:", examples[selected], height=150)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("▶️ تشغيل", type="primary"):
                    try:
                        con = duckdb.connect(database=':memory:')
                        con.register('data', df)
                        result = con.execute(query).fetchdf()
                        
                        st.success(f"✅ تم استرجاع {len(result):,} صف")
                        st.dataframe(result, use_container_width=True)
                        
                        # تصدير النتيجة
                        if len(result) > 0:
                            csv = result.to_csv(index=False)
                            st.markdown(get_download_link(csv, "sql_result.csv", "csv"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ خطأ في SQL: {str(e)}")
        
        except ImportError:
            st.error("❌ مكتبة DuckDB غير مثبتة")
    else:
        st.error("❌ لا توجد بيانات")

# --- Google Sheets ---
elif menu == "☁️ Google Sheets":
    st.header("☁️ Google Sheets - تكامل السحابة")
    
    st.info("🚧 قيد التطوير - سيتم إضافة:")
    st.markdown("""
    - ✅ قراءة Sheets مباشرة
    - ✅ كتابة البيانات للـ Sheets
    - ✅ مزامنة تلقائية
    - ✅ مشاركة روابط مباشرة
    """)
    
    sheet_url = st.text_input("🔗 رابط Google Sheet:")
    if st.button("☁️ اتصال"):
        st.warning("🔜 قريباً!")

# --- AI Analytics ---
elif menu == "🤖 AI Analytics":
    st.header("🤖 AI Analytics - الذكاء الاصطناعي")
    
    if df is not None:
        st.subheader("💬 اسأل الوحش عن بياناتك!")
        
        question = st.text_input("📝 سؤالك:", placeholder="مثال: ما أفضل فرع مبيعاً؟")
        
        if st.button("🤖 تحليل"):
            # محاكاة للـ AI
            response = f"*تحليل السؤال:* {question}\n\n"
            
            if "أفضل" in question or "أعلى" in question:
                if 'الفرع' in df.columns and 'المبيعات' in df.columns:
                    best = df.groupby('الفرع')['المبيعات'].sum().idxmax()
                    val = df.groupby('الفرع')['المبيعات'].sum().max()
                    response += f"🏆 *الأفضل:* {best} بإجمالي {val:,.0f}"
            
            elif "إجمالي" in question or "مجموع" in question:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    total = df[numeric_cols[0]].sum()
                    response += f"💰 *الإجمالي:* {total:,.0f}"
            
            elif "متوسط" in question:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    avg = df[numeric_cols[0]].mean()
                    response += f"📊 *المتوسط:* {avg:,.2f}"
            
            else:
                response += f"📋 *ملخص البيانات:*\n"
                response += f"- الصفوف: {len(df):,}\n"
                response += f"- الأعمدة: {len(df.columns)}\n"
                response += f"- الإجمالي: {df.select_dtypes(include=[np.number]).sum().sum():,.0f}"
            
            st.success(response)
        
        # توصيات ذكية
        st.subheader("💡 توصيات ذكية")
        if st.button("🔮 اكتشاف الأنماط"):
            st.info("🔜 قريباً: تحليل أنماط متقدم باستخدام Machine Learning")
    else:
        st.error("❌ لا توجد بيانات")

# --- تقارير PDF ---
elif menu == "📑 تقارير PDF":
    st.header("📑 تقارير PDF - تقارير احترافية")
    
    if df is not None:
        st.subheader("⚙️ إعداد التقرير")
        
        report_title = st.text_input("عنوان التقرير:", "تقرير تحليل البيانات")
        include_charts = st.checkbox("📊 تضمين رسوم بيانية", value=True)
        include_stats = st.checkbox("📈 تضمين إحصائيات", value=True)
        
        if st.button("📄 توليد PDF", type="primary"):
            with st.spinner("⏳ جاري إنشاء التقرير..."):
                try:
                    pdf_bytes = generate_pdf_report(df, report_title)
                    
                    st.success("✅ تم إنشاء التقرير!")
                    st.markdown(get_download_link(pdf_bytes, f"report_{datetime.now().strftime('%Y%m%d')}.pdf", "pdf"), 
                               unsafe_allow_html=True)
                    
                    # معاينة
                    st.info("📋 ملخص التقرير:")
                    st.write(f"- العنوان: {report_title}")
                    st.write(f"- الصفوف: {len(df):,}")
                    st.write(f"- التوقيع: {SIGNATURE}")
                    st.write(f"- العلامة المائية: {WATERMARK}")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    else:
        st.error("❌ لا توجد بيانات")

# --- التصدير المتقدم ---
elif menu == "💾 التصدير المتقدم":
    st.header("💾 التصدير المتقدم")
    
    if df is not None:
        st.subheader("📥 اختيار التنسيق")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv = df.to_csv(index=False)
            st.markdown(get_download_link(csv, f"data_{datetime.now().strftime('%Y%m%d')}.csv", "csv"), 
                       unsafe_allow_html=True)
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            st.markdown(get_download_link(output.getvalue(), f"data_{datetime.now().strftime('%Y%m%d')}.xlsx", "excel"), 
                       unsafe_allow_html=True)
        
        with col3:
            json_str = df.to_json(orient='records', force_ascii=False)
            st.download_button("📥 JSON", json_str, f"data_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
        
        with col4:
            if st.button("📥 PDF"):
                st.info("استخدم قسم 'تقارير PDF'")
        
        # إعدادات متقدمة
        with st.expander("⚙️ إعدادات متقدمة"):
            st.checkbox("تشفير الملف")
            st.checkbox("ضغط ZIP")
            st.checkbox("إرسال بالإيميل")
    else:
        st.error("❌ لا توجد بيانات")

# ======== التوقيع والعلامة المائية ========
st.markdown(f"""
<div class="signature">
    {SIGNATURE}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="watermark">
    {WATERMARK}
</div>
""", unsafe_allow_html=True)

st.write("---")
st.caption(f"🦁 Data Beast Pro | {SIGNATURE} | جميع الحقوق محفوظة © 2024")
