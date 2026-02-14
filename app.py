import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
import os
from io import BytesIO

warnings.filterwarnings('ignore')

# ======= الإعدادات الأساسية =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "Smart Analyst The Beast"
APP_VERSION = "5.0.0"
LOGO_FILE = "logo.jpg"

st.set_page_config(
    page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======= Session State =======
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []
if 'forecast_results' not in st.session_state:
    st.session_state.forecast_results = None
if 'language' not in st.session_state:
    st.session_state.language = 'ar'

# ======= CSS احترافي =======
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
    
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    
    .stApp { 
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #0f172a 100%); 
        color: #f8fafc; 
    }
    
    .main-title {
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        margin: 0;
        padding: 0.5rem 0;
    }
    
    .section-header {
        color: #10b981;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .card {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .kpi-box {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
    }
    
    .kpi-number { font-size: 2rem; font-weight: 900; }
    .kpi-label { font-size: 0.9rem; opacity: 0.9; }
    
    .btn-primary {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
    }
    
    .recommendation {
        background: rgba(16, 185, 129, 0.15);
        border-right: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-logo img {
        max-width: 120px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .sidebar-title {
        color: #10b981;
        font-size: 1.3rem;
        font-weight: 800;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .sidebar-version {
        color: #64748b;
        font-size: 0.8rem;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ======= Sidebar =======
with st.sidebar:
    # اللوجو
    st.markdown("<div class='sidebar-logo'>", unsafe_allow_html=True)
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    else:
        st.markdown("<div style='font-size: 4rem;'>🦁</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # العنوان والإصدار
    st.markdown(f"<div class='sidebar-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sidebar-version'>v{APP_VERSION} | {AUTHOR_SIGNATURE}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # القائمة
    menu = st.radio("", [
        "📤 رفع وإنشاء البيانات",
        "⚡ Power Query والتنظيف",
        "📊 Power BI Dashboard",
        "🧠 التنبؤ الذكي",
        "📄 التقرير الاحترافي"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    # الإعدادات
    with st.expander("⚙️ الإعدادات"):
        lang = st.selectbox("اللغة:", ["العربية", "English"])
        st.session_state.language = 'ar' if lang == "العربية" else 'en'
    
    # حالة البيانات
    st.markdown("---")
    st.markdown("### 📊 حالة البيانات")
    if st.session_state.beast_df is not None:
        df = st.session_state.beast_df
        st.success(f"✅ {len(df):,} سجل")
    else:
        st.info("ℹ️ لا توجد بيانات")

# ======= القسم 1: رفع البيانات =======
def render_upload():
    st.markdown("<div class='section-header'>📤 رفع وإنشاء البيانات</div>", unsafe_allow_html=True)
    
    tabs = st.tabs(["📁 رفع ملفات", "🎲 بيانات اختبار", "📊 Excel"])
    
    with tabs[0]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        files = st.file_uploader("اختر الملفات:", type=['csv', 'xlsx', 'json'], accept_multiple_files=True)
        
        if files:
            for file in files:
                try:
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    elif file.name.endswith('.xlsx'):
                        df = pd.read_excel(file, engine='openpyxl')
                    else:
                        df = pd.read_json(file)
                    
                    st.success(f"✅ {file.name}: {len(df):,} سجل")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.dataframe(df.head(3), use_container_width=True)
                    with col2:
                        if st.button(f"استخدام", key=f"btn_{file.name}"):
                            st.session_state.beast_df = df.copy()
                            st.success("تم التحميل!")
                            
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            n = st.number_input("عدد السجلات:", 10, 100000, 1000, step=100)
            data_type = st.selectbox("النوع:", ["مبيعات", "عملاء", "موظفين"])
        
        with col2:
            if st.button("🚀 توليد", use_container_width=True):
                np.random.seed(42)
                
                if "مبيعات" in data_type:
                    df = pd.DataFrame({
                        'التاريخ': pd.date_range('2024-01-01', periods=n, freq='D'),
                        'المبيعات': np.random.normal(50000, 15000, n).clip(0).round(2),
                        'العملاء': np.random.poisson(150, n),
                        'المنطقة': np.random.choice(['الشمال', 'الجنوب', 'الشرق', 'الغرب'], n)
                    })
                elif "عملاء" in data_type:
                    df = pd.DataFrame({
                        'العميل': [f'CUST_{i:06d}' for i in range(1, n+1)],
                        'العمر': np.random.randint(18, 80, n),
                        'المدينة': np.random.choice(['الرياض', 'جدة', 'الدمام'], n)
                    })
                else:
                    df = pd.DataFrame({
                        'الموظف': [f'EMP_{i:05d}' for i in range(1, n+1)],
                        'القسم': np.random.choice(['IT', 'المبيعات', 'المالية'], n),
                        'المرتب': np.random.normal(15000, 5000, n).clip(5000).round(2)
                    })
                
                st.session_state.beast_df = df
                st.success(f"✅ تم توليد {len(df):,} سجل!")
                st.dataframe(df.head())
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if st.button("🔄 إنشاء شيت جديد"):
            st.session_state.excel_data = pd.DataFrame('', index=range(10), 
                                                       columns=[f'عمود_{chr(65+i)}' for i in range(5)])
        
        if 'excel_data' not in st.session_state or st.session_state.excel_data is None:
            st.session_state.excel_data = pd.DataFrame('', index=range(10), 
                                                       columns=[f'عمود_{chr(65+i)}' for i in range(5)])
        
        edited = st.data_editor(st.session_state.excel_data, num_rows="dynamic", height=300)
        st.session_state.excel_data = edited
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ في النظام", use_container_width=True):
                st.session_state.beast_df = edited.copy()
                st.success("تم!")
        with col2:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                edited.to_excel(writer, index=False)
            st.download_button("📥 Excel", buffer.getvalue(), "data.xlsx", 
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 2: Power Query =======
def render_power_query():
    st.markdown("<div class='section-header'>⚡ Power Query والتنظيف</div>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    
    # KPIs
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    cols = st.columns(4)
    
    metrics = [
        ("السجلات", len(df), "#3b82f6"),
        ("الفراغات", f"{df.isnull().sum().sum()/df.size*100:.1f}%", "#ef4444"),
        ("التكرار", df.duplicated().sum(), "#f59e0b"),
        ("الجودة", f"{max(0, 100-df.isnull().sum().sum()/df.size*100):.0f}%", "#10b981")
    ]
    
    for col, (label, val, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div style='background: {color}20; border: 1px solid {color}; border-radius: 12px; 
                        padding: 1rem; text-align: center;'>
                <div style='color: {color}; font-size: 0.85rem;'>{label}</div>
                <div style='color: {color}; font-size: 1.5rem; font-weight: 800;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # أدوات التنظيف
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🛠️ أدوات التنظيف")
    
    clean_cols = st.columns(4)
    buttons = [
        ("🗑️ حذف تكرار", lambda d: d.drop_duplicates()),
        ("📝 تعبئة فراغات", lambda d: d.fillna(d.median(numeric_only=True))),
        ("✂️ حذف فراغات", lambda d: d.dropna()),
        ("🔤 توحيد نص", lambda d: d.apply(lambda x: x.str.strip().str.title() if x.dtype == 'object' else x))
    ]
    
    for col, (label, action) in zip(clean_cols, buttons):
        with col:
            if st.button(label, use_container_width=True):
                try:
                    new_df = action(df)
                    st.session_state.beast_df = new_df
                    st.session_state.cleaning_log.append(label)
                    st.success("تم!")
                    st.rerun()
                except Exception as e:
                    st.error(f"خطأ: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 3: Dashboard =======
def render_dashboard():
    st.markdown("<div class='section-header'>📊 Power BI Dashboard</div>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols:
        st.warning("⚠️ لا توجد أعمدة رقمية")
        return
    
    # فلاتر
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    filt_cols = st.columns([2, 2, 1])
    
    with filt_cols[0]:
        selected_metric = st.selectbox("المؤشر:", numeric_cols, key="dash_metric")
    with filt_cols[1]:
        if categorical_cols:
            filter_vals = st.multiselect("الفئة:", df[categorical_cols[0]].unique(), 
                                        default=list(df[categorical_cols[0]].unique())[:3])
        else:
            filter_vals = None
    with filt_cols[2]:
        st.button("🔄 تحديث")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # تطبيق الفلاتر
    filtered_df = df.copy()
    if filter_vals and categorical_cols:
        filtered_df = filtered_df[filtered_df[categorical_cols[0]].isin(filter_vals)]
    
    # ✅ KPIs مع التحقق من الأخطاء
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    kpi_cols = st.columns(4)
    
    try:
        total_val = filtered_df[selected_metric].sum()
        avg_val = filtered_df[selected_metric].mean()
        max_val = filtered_df[selected_metric].max()
        
        # حساب النمو بأمان
        if len(filtered_df) > 1:
            first_val = filtered_df[selected_metric].iloc[0]
            last_val = filtered_df[selected_metric].iloc[-1]
            if pd.notna(first_val) and pd.notna(last_val) and first_val != 0:
                growth_val = ((last_val - first_val) / abs(first_val)) * 100
            else:
                growth_val = 0
        else:
            growth_val = 0
        
        kpi_data = [
            ("المجموع", total_val, "💰"),
            ("المتوسط", avg_val, "📊"),
            ("الأقصى", max_val, "🏆"),
            ("النمو", f"{growth_val:+.1f}%", "📈")
        ]
        
        for col, (label, val, icon) in zip(kpi_cols, kpi_data):
            with col:
                display_val = f"{val:,.0f}" if isinstance(val, (int, float)) else str(val)
                st.markdown(f"""
                <div class='kpi-box'>
                    <div class='kpi-label'>{icon} {label}</div>
                    <div class='kpi-number'>{display_val}</div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"خطأ في حساب المؤشرات: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ✅ الرسوم البيانية
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    chart_tabs = st.tabs(["📈 خطي", "🥧 دائري", "📊 أعمدة", "🔥 حراري"])
    
    try:
        with chart_tabs[0]:
            fig = px.line(filtered_df, y=selected_metric, template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_tabs[1]:
            if categorical_cols:
                pie_data = filtered_df.groupby(categorical_cols[0])[selected_metric].sum().reset_index()
                fig = px.pie(pie_data, values=selected_metric, names=categorical_cols[0], 
                           hole=0.5, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("لا توجد بيانات تصنيفية")
        
        with chart_tabs[2]:
            fig = px.bar(filtered_df.head(20), y=selected_metric, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_tabs[3]:
            if len(numeric_cols) > 1:
                corr = filtered_df[numeric_cols].corr()
                fig = px.imshow(corr, text_auto=True, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("يحتاج أعمدة رقمية متعددة")
                
    except Exception as e:
        st.error(f"خطأ في الرسوم: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 4: AI =======
def render_ai():
    st.markdown("<div class='section-header'>🧠 التنبؤ الذكي</div>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.error("❌ لا توجد أعمدة رقمية")
        return
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target = st.selectbox("المؤشر:", numeric_cols, key="ai_target")
    with col2:
        periods = st.slider("الفترة:", 7, 365, 30)
    with col3:
        model_type = st.selectbox("النموذج:", ["Linear", "Polynomial"])
    
    if st.button("🔮 تنبؤ", use_container_width=True):
        with st.spinner("جاري التحليل..."):
            try:
                from sklearn.linear_model import LinearRegression
                from sklearn.preprocessing import PolynomialFeatures
                
                y = df[target].dropna().values
                X = np.arange(len(y)).reshape(-1, 1)
                
                if model_type == "Polynomial":
                    poly = PolynomialFeatures(degree=2)
                    X = poly.fit_transform(X)
                    model = LinearRegression()
                    model.fit(X, y)
                    future_X = poly.transform(np.arange(len(y), len(y)+periods).reshape(-1, 1))
                else:
                    model = LinearRegression()
                    model.fit(X, y)
                    future_X = np.arange(len(y), len(y)+periods).reshape(-1, 1)
                
                predictions = model.predict(future_X)
                predictions = np.maximum(predictions, 0)
                
                # عرض النتائج
                result_cols = st.columns(4)
                result_cols[0].metric("المتوسط", f"{np.mean(predictions):,.0f}")
                result_cols[1].metric("القمة", f"{np.max(predictions):,.0f}")
                result_cols[2].metric("الحد الأدنى", f"{np.min(predictions):,.0f}")
                result_cols[3].metric("الاتجاه", "📈 صاعد" if predictions[-1] > predictions[0] else "📉 هابط")
                
                # رسم
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=y, name='تاريخي', line=dict(color='#3b82f6')))
                fig.add_trace(go.Scatter(x=list(range(len(y), len(y)+periods)), y=predictions, 
                                       name='تنبؤ', line=dict(color='#10b981', dash='dash')))
                fig.update_layout(template="plotly_dark", title=f"تنبؤ {target}")
                st.plotly_chart(fig, use_container_width=True)
                
                # توصيات
                st.subheader("💡 التوصيات")
                if predictions[-1] > predictions[0]:
                    st.markdown("<div class='recommendation'>📈 اتجاه إيجابي - زود المخزون</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='recommendation'>📉 اتجاه سلبي - راجع التكاليف</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 5: Report =======
def render_report():
    st.markdown("<div class='section-header'>📄 التقرير الاحترافي</div>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # ✅ إعدادات بدون أخطاء
    col1, col2 = st.columns(2)
    with col1:
        report_lang = st.selectbox("اللغة:", ["العربية 🇸🇦", "English 🇬🇧"], key="report_lang_select")
    with col2:
        st.selectbox("النمط:", ["احترافي أخضر", "أزرق تقني"], key="report_style_select")
    
    # معاينة
    st.subheader("👁️ معاينة")
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #059669, #10b981); 
                border-radius: 15px; color: white; margin: 1rem 0;'>
        <h2>🦁 {APP_NAME}</h2>
        <p>التاريخ: {datetime.now().strftime('%Y/%m/%d')}</p>
        <p>السجلات: {len(df):,} | الأعمدة: {len(df.columns)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تصدير
    export_cols = st.columns(2)
    
    with export_cols[0]:
        if st.button("📄 إنشاء PDF", use_container_width=True):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4)
                elements = []
                styles = getSampleStyleSheet()
                
                elements.append(Paragraph(APP_NAME, styles['Title']))
                elements.append(Spacer(1, 20))
                elements.append(Paragraph(f"التاريخ: {datetime.now().strftime('%Y/%m/%d')}", styles['Normal']))
                elements.append(Spacer(1, 20))
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    data = [['المؤشر', 'المجموع', 'المتوسط']]
                    for col in numeric_cols[:5]:
                        data.append([col, f"{df[col].sum():,.0f}", f"{df[col].mean():,.0f}"])
                    
                    table = Table(data)
                    table.setStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#059669')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ])
                    elements.append(table)
                
                doc.build(elements)
                buffer.seek(0)
                
                st.download_button("⬇️ تحميل PDF", buffer.getvalue(), 
                                 f"{APP_NAME.replace(' ', '_')}_Report.pdf", "application/pdf",
                                 use_container_width=True)
                st.success("✅ تم إنشاء التقرير!")
                
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
    
    with export_cols[1]:
        msg = f"🦁 {APP_NAME}%0A📅 {datetime.now().strftime('%Y/%m/%d')}%0A📊 {len(df):,} سجل"
        whatsapp_url = f"https://wa.me/?text={msg}"
        st.markdown(f"<a href='{whatsapp_url}' target='_blank' style='text-decoration: none;'><button style='width: 100%; padding: 0.75rem; background: linear-gradient(135deg, #25d366, #128c7e); color: white; border: none; border-radius: 10px; font-weight: 700; cursor: pointer;'>📱 مشاركة واتساب</button></a>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= التشغيل الرئيسي =======
if menu == "📤 رفع وإنشاء البيانات":
    render_upload()
elif menu == "⚡ Power Query والتنظيف":
    render_power_query()
elif menu == "📊 Power BI Dashboard":
    render_dashboard()
elif menu == "🧠 التنبؤ الذكي":
    render_ai()
elif menu == "📄 التقرير الاحترافي":
    render_report()

# ======= Footer =======
st.markdown(f"""
<div style='text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid #1e293b; color: #64748b;'>
    <div style='font-size: 2rem;'>🦁</div>
    <h3 style='color: #10b981;'>{APP_NAME}</h3>
    <p>© 2026 | {AUTHOR_SIGNATURE}</p>
</div>
""", unsafe_allow_html=True)
