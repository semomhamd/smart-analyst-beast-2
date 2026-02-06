

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
import hashlib
import time
from typing import Optional, List, Dict, Any

# ======== محاولة استيراد Supabase ========
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("⚠️ مكتبة Supabase غير مثبتة. سيتم استخدام الوضع المحلي.")

# ======== إعدادات Smart Analyst The Beast ========
class BeastConfig:
    """إعدادات التطبيق"""
    APP_NAME = "Smart Analyst The Beast"
    APP_NAME_AR = "المحلل الذكي الوحش"
    VERSION = "2.0.0"
    AUTHOR = "MIA8444"
    
    # Supabase Settings - املأ هذه القيم
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "") if hasattr(st, 'secrets') else ""
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "") if hasattr(st, 'secrets') else ""
    
    # Logo URL من GitHub
    LOGO_URL = "https://raw.githubusercontent.com/semomhamd/smart-analyst-beast-2/main/logo.jpg"
    
    # Colors
    PRIMARY_COLOR = "#3498DB"
    SECONDARY_COLOR = "#2C3E50"
    ACCENT_COLOR = "#E74C3C"
    SUCCESS_COLOR = "#27AE60"

# ======== FETH - المحلل الذكي المتقدم ========
class FethPersonality:
    """عقل FETH المتقدم - محلل البيانات الذكي"""
    
    def _init_(self):
        self.name = "FETH"
        self.arabic_name = "فَتْح"
        self.version = "2.0"
        self.mood = "enthusiastic"
        
    def get_identity(self):
        return {
            "name": self.name,
            "meaning": "الكشف، الوضوح، فتح البيانات",
            "role": "محلل بيانات ذكي + مرشد + صاحب",
            "tone": "واضح، داعم، محترف، خفيف، ذكي",
            "signature": "— FETH | بيفتح البيانات 🎯",
            "version": self.version
        }
    
    def analyze_data_mood(self, df: pd.DataFrame) -> str:
        """يحلل مزاج البيانات ويرجع وصف"""
        if df is None or df.empty:
            return "empty"
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return "text_only"
        
        # تحليل الأرقام
        total = df[numeric_cols[0]].sum() if len(numeric_cols) > 0 else 0
        avg = df[numeric_cols[0]].mean() if len(numeric_cols) > 0 else 0
        
        if total > 1000000:
            return "massive"
        elif total > 100000:
            return "huge"
        elif total > 10000:
            return "good"
        elif len(df) > 1000:
            return "big_data"
        else:
            return "normal"
    
    def respond(self, context: str, data_insight: str = None, df: pd.DataFrame = None) -> str:
        """يختار الرد المناسب حسب السياق والبيانات"""
        
        # تحليل مزاج البيانات
        data_mood = self.analyze_data_mood(df) if df is not None else "normal"
        
        responses = {
            'welcome': {
                'normal': [
                    "أهلاً بيك في Smart Analyst The Beast! 🦁 أنا FETH... جاهز أفتحلك أي بيانات",
                    "مرحباً! FETH هنا في الوضعية الذكية... خلينا نكتشف سوا إيه مخبية البيانات",
                    "أهلاً بيك يا محلل! مع FETH البيانات هتتفتح زي كتاب 📖"
                ],
                'big_data': [
                    "🚀 واو! عندك بيانات ضخمة! FETH جاهز للتحدي!",
                    "💪 بيانات كبيرة؟ ده اختصاصي! خليني أوريك القوة الحقيقية"
                ]
            },
            'upload_success': {
                'normal': [
                    f"✅ استلمت الملف! {data_insight or ''}... خليني أفتحه وأشوف جواه إيه 🔍",
                    "📊 تمام! البيانات جات... FETH بيفتحها دلوقتي",
                    f"🎯 ملف جديد! {data_insight or ''} جاهزين نكتشف أسراره سوا؟"
                ],
                'huge': [
                    f"🔥 {data_insight or ''} ده كمية ضخمة! FETH بيحب التحديات!",
                    "💪 بيانات ضخمة استلمتها! جاهز أحللها في ثواني"
                ]
            },
            'analysis_ready': [
                "🧠 فتحت البيانات بذكاء... وده اللي لقيته 👇",
                "⚡ التحليل جهز بقوة الوحش! خليني أفتحلك الرؤية واضحة",
                "🎯 كشفت البيانات بالذكاء الاصطناعي... والنتيجة مثيرة!"
            ],
            'insight_high': [
                f"🚀 رقم قياسي! {data_insight}... ده أعلى قيمة شوفتها",
                f"🔥 لاحظت حاجة مثيرة! {data_insight}... فوق المتوقع بمراحل",
                f"✨ إنجاز ممتاز! {data_insight}... يستاهل الاحتفال 🎉"
            ],
            'insight_low': [
                f"⚠️ فتحت البيانات ولقيت: {data_insight}... خليني أساعدك تفهم ليه",
                f"👀 نقطة مهمة: {data_insight}... ممكن نحسنها سوا بذكاء",
                f"💡 البيانات بتقول: {data_insight}... عندك فكرة ليه؟"
            ],
            'teaching': [
                "🎓 خليني أفتحلك النقطة دي ببساطة وذكاء...",
                "💡 تخيّل معايا كده...",
                "🧠 السر هنا إنه...",
                "📚 من خبرة FETH في التحليل..."
            ],
            'support': [
                "🤝 ولا يهمك... خلينا نمشي خطوة خطوة",
                "👌 تمام، أنا معاك... جرب كده",
                "💪 مش مشكلة، FETH هيساعدك تعديها بقوة"
            ],
            'celebration': [
                "🎉 كده! إنجاز رائع يستاهل الاحتفال",
                "👏 أحسنت! البيانات دلوقتي واضحة زي الشمس",
                "🎯 هدف محقق! جاهز للخطوة الجاية؟"
            ],
            'error': [
                "⚠️ حصلت حاجة بسيطة... خليني أجرب تاني بذكاء",
                "🔄 مش مشكلة، كلنا بنتعلم... جرب معايا كده",
                "🛠️ FETH لسه بيتعلم... ساعدني أفهم المشكلة"
            ],
            'cloud_sync': [
                "☁️ تم حفظ البيانات في السحابة! جاهز من أي مكان",
                "🔄 متزامن مع السحابة! أمان تام لبياناتك",
                "💾 محفوظ في الذاكرة السحابية!"
            ]
        }
        
        # اختيار الرد المناسب
        if context in responses:
            if isinstance(responses[context], dict):
                mood_responses = responses[context].get(data_mood, responses[context]['normal'])
                return random.choice(mood_responses)
            return random.choice(responses[context])
        
        return "🎯 FETH هنا... جاهز أساعدك بقوة الوحش!"
    
    def suggest_next(self, current_page: str) -> List[str]:
        """يقترح الخطوة الجاية حسب السياق"""
        
        suggestions = {
            'home': [
                "📥 ارفع ملف بيانات جديد",
                "📊 جرب البيانات التجريبية الضخمة",
                "🔐 سجل دخول للوصول للسحابة",
                "🤖 اسأل FETH عن أي حاجة"
            ],
            'upload': [
                "🧹 نظف البيانات من الفارغ",
                "📊 روح لتحليل Power BI",
                "☁️ احفظ في السحابة",
                "🤖 اسأل FETH يحلللك البيانات"
            ],
            'cleaner': [
                "📊 شوف التحليلات البصرية",
                "📈 اعمل Pivot Table",
                "☁️ احفظ النسخة النظيفة",
                "🤖 اسأل FETH عن النتائج"
            ],
            'excel': [
                "📈 اعمل رسم بياني",
                "📤 صدّر التقرير PDF",
                "☁️ احفظ في السحابة",
                "🤖 اسأل FETH يفسر الصيغ"
            ],
            'powerbi': [
                "📊 غيّر نوع الرسم البياني",
                "📤 صدّر النتائج",
                "☁️ شارك التحليل",
                "🤖 اسأل FETH عن التوجهات"
            ],
            'ai': [
                "📊 روح للتحليل البصري",
                "📤 جهّز تقرير PDF",
                "☁️ احفظ المحادثة",
                "🧹 نظف البيانات أكتر"
            ],
            'login': [
                "📥 ارفع ملفات متعددة",
                "☁️ شوف بياناتك المحفوظة",
                "🤖 فعّل الذكاء الاصطناعي",
                "📊 ابدأ تحليل جديد"
            ]
        }
        return suggestions.get(current_page, ["🤖 اسأل FETH"])
    
    def get_signature(self) -> str:
        return "— FETH | بيفتح البيانات 🎯"

# ======== Supabase Manager ========
class SupabaseManager:
    """إدارة قاعدة البيانات السحابية"""
    
    def _init_(self):
        self.client: Optional[Client] = None
        self.connected = False
        self._init_connection()
    
    def _init_connection(self):
        """تهيئة الاتصال بـ Supabase"""
        if not SUPABASE_AVAILABLE:
            return
        
        try:
            url = BeastConfig.SUPABASE_URL
            key = BeastConfig.SUPABASE_KEY
            
            if url and key:
                self.client = create_client(url, key)
                self.connected = True
        except Exception as e:
            st.error(f"خطأ في الاتصال بـ Supabase: {e}")
            self.connected = False
    
    def sign_up(self, email: str, password: str) -> Dict:
        """تسجيل مستخدم جديد"""
        if not self.connected:
            return {"error": "Supabase غير متصل"}
        
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            return {"success": True, "user": response.user}
        except Exception as e:
            return {"error": str(e)}
    
    def sign_in(self, email: str, password: str) -> Dict:
        """تسجيل الدخول"""
        if not self.connected:
            return {"error": "Supabase غير متصل"}
        
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"success": True, "user": response.user, "session": response.session}
        except Exception as e:
            return {"error": str(e)}
    
    def save_dataframe(self, user_id: str, name: str, df: pd.DataFrame) -> Dict:
        """حفظ DataFrame في السحابة"""
        if not self.connected:
            return {"error": "Supabase غير متصل"}
        
        try:
            # تحويل DataFrame لـ JSON
            data_json = df.to_json(orient='records', force_ascii=False)
            
            # حفظ في قاعدة البيانات
            response = self.client.table('user_datasets').insert({
                'user_id': user_id,
                'name': name,
                'data': data_json,
                'created_at': datetime.now().isoformat(),
                'rows': len(df),
                'columns': len(df.columns)
            }).execute()
            
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_datasets(self, user_id: str) -> List[Dict]:
        """جلب بيانات المستخدم المحفوظة"""
        if not self.connected:
            return []
        
        try:
            response = self.client.table('user_datasets')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            return response.data
        except Exception as e:
            st.error(f"خطأ في جلب البيانات: {e}")
            return []
    
    def load_dataset(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """تحميل dataset من السحابة"""
        if not self.connected:
            return None
        
        try:
            response = self.client.table('user_datasets')\
                .select('data')\
                .eq('id', dataset_id)\
                .execute()
            
            if response.data:
                data_json = response.data[0]['data']
                return pd.read_json(data_json)
            return None
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات: {e}")
            return None

# ======== إعدادات الصفحة - Responsive Design ========
st.set_page_config(
    page_title="Smart Analyst The Beast | FETH",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="collapsed"  # أفضل للموبايل
)

# ======== CSS متجاوب للموبايل والديسكتوب ========
def get_responsive_css():
    return """
    <style>
        /* Base Styles */
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Responsive Container */
        .responsive-container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }
        
        /* Mobile-First Sidebar */
        @media (max-width: 768px) {
            .css-1d391kg { /* Sidebar */
                width: 100% !important;
            }
            .stButton > button {
                width: 100%;
                font-size: 14px;
                padding: 12px;
            }
            h1 {
                font-size: 24px !important;
            }
            h2 {
                font-size: 20px !important;
            }
            .metric-card {
                padding: 10px;
            }
            .feth-box {
                padding: 10px;
            }
        }
        
        /* Desktop Styles */
        @media (min-width: 769px) {
            .stButton > button {
                font-size: 16px;
                padding: 10px 20px;
            }
        }
        
        /* Beast Branding */
        .beast-header {
            background: linear-gradient(135deg, #3498DB, #2C3E50);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        }
        
        .beast-title {
            font-size: 32px;
            font-weight: bold;
            color: white;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .beast-subtitle {
            font-size: 18px;
            color: rgba(255,255,255,0.9);
            margin: 5px 0;
        }
        
        /* Cards */
        .metric-card {
            background: linear-gradient(135deg, #3498DB, #2C3E50);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        /* FETH Box */
        .feth-box {
            background: linear-gradient(135deg, #3498DB, #2C3E50);
            padding: 15px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(45deg, #3498DB, #2C3E50);
            color: white;
            border: none;
            border-radius: 10px;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
        }
        
        /* Mobile Menu Toggle */
        .mobile-menu-btn {
            display: block;
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: #3498DB;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 20px;
        }
        
        @media (min-width: 769px) {
            .mobile-menu-btn {
                display: none;
            }
        }
        
        /* Data Grid */
        .excel-cell {
            border: 1px solid #444;
            padding: 5px;
            text-align: center;
        }
        
        .formula-bar {
            background: #1a1a2e;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
        }
        
        /* Login Form */
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            padding: 30px;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        /* Multi-file Upload Zone */
        .upload-zone {
            border: 3px dashed #3498DB;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            background: rgba(52, 152, 219, 0.1);
            transition: all 0.3s;
        }
        
        .upload-zone:hover {
            background: rgba(52, 152, 219, 0.2);
            border-color: #2980B9;
        }
        
        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .beast-pulse {
            animation: pulse 2s infinite;
        }
    </style>
    """

st.markdown(get_responsive_css(), unsafe_allow_html=True)

# ======== تهيئة session_state ========
def init_session_state():
    defaults = {
        'df': None,
        'dfs': [],  # لرفع ملفات متعددة
        'language': 'ar',
        'dark_mode': True,
        'cleaning_history': [],
        'page': 'home',
        'chat_history': [],
        'excel_formulas': {},
        'feth': FethPersonality(),
        'feth_welcomed': False,
        'user': None,
        'session': None,
        'supabase': SupabaseManager(),
        'mobile_menu_open': False,
        'uploaded_files_count': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ======== النصوص متعددة اللغات ========
TEXTS = {
    'ar': {
        'title': 'Smart Analyst The Beast',
        'subtitle': 'المحلل الذكي الوحش',
        'home': '🏠 الرئيسية',
        'login': '🔐 تسجيل الدخول',
        'ocr': '👁️ OCR Vision',
        'upload': '📥 رفع بيانات',
        'multi_upload': '📁 رفع متعدد',
        'cleaner': '🧹 منظف البيانات',
        'excel': '📊 Excel Pro',
        'powerbi': '📈 Power BI',
        'sql': '🗄️ SQL',
        'ai': '🤖 FETH AI',
        'export': '💾 تصدير',
        'cloud': '☁️ السحابة',
        'settings': '⚙️ الإعدادات',
        'logout': '🚪 خروج',
        'sample': '📊 بيانات تجريبية',
        'clear': '🗑️ مسح',
        'save': '💾 حفظ',
        'welcome': 'أهلاً بيك في عالم التحليل الذكي!',
        'signature': '🔥 MIA8444 | Smart Analyst The Beast © 2024 | 🎯 FETH'
    },
    'en': {
        'title': 'Smart Analyst The Beast',
        'subtitle': 'The Intelligent Beast Analyst',
        'home': '🏠 Home',
        'login': '🔐 Login',
        'ocr': '👁️ OCR Vision',
        'upload': '📥 Upload',
        'multi_upload': '📁 Multi Upload',
        'cleaner': '🧹 Cleaner',
        'excel': '📊 Excel Pro',
        'powerbi': '📈 Power BI',
        'sql': '🗄️ SQL',
        'ai': '🤖 FETH AI',
        'export': '💾 Export',
        'cloud': '☁️ Cloud',
        'settings': '⚙️ Settings',
        'logout': '🚪 Logout',
        'sample': '📊 Sample',
        'clear': '🗑️ Clear',
        'save': '💾 Save',
        'welcome': 'Welcome to the world of intelligent analysis!',
        'signature': '🔥 MIA8444 | Smart Analyst The Beast © 2024 | 🎯 FETH'
    }
}

def t(key):
    return TEXTS[st.session_state.language].get(key, key)

# ======== دوال مساعدة ========
def generate_sample_data(size=100):
    """بيانات تجريبية أكبر وأكثر واقعية"""
    np.random.seed(42)
    
    products = ['لابتوب', 'موبايل', 'تابلت', 'سماعات', 'شاحن', 'كيبورد', 'ماوس', 'شاشة']
    categories = ['إلكترونيات', 'اكسسوارات', 'أجهزة', 'برمجيات']
    branches = ['القاهرة', 'دبي', 'الرياض', 'جدة', 'الكويت', 'الدوحة']
    
    data = {
        'التاريخ': pd.date_range('2024-01-01', periods=size, freq='D'),
        'المنتج': np.random.choice(products, size),
        'الفئة': np.random.choice(categories, size),
        'المبيعات': np.random.randint(1000, 100000, size),
        'الكمية': np.random.randint(1, 100, size),
        'السعر': np.random.randint(500, 50000, size),
        'الفرع': np.random.choice(branches, size),
        'التقييم': np.random.randint(1, 6, size),
        'الخصم': np.random.randint(0, 50, size),
        'العميل': [f'عميل_{i}' for i in range(size)],
        'الموظف': np.random.choice(['أحمد', 'محمد', 'علي', 'خالد', 'سامي'], size)
    }
    
    return pd.DataFrame(data)

def merge_dataframes(dfs: List[pd.DataFrame], merge_type='concat') -> pd.DataFrame:
    """دمج ملفات متعددة"""
    if not dfs:
        return None
    
    if merge_type == 'concat':
        return pd.concat(dfs, ignore_index=True)
    elif merge_type == 'join':
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, how='outer', left_index=True, right_index=True)
        return result
    else:
        return pd.concat(dfs, ignore_index=True)

def ai_assistant(df, question):
    """مساعد FETH الذكي المتقدم"""
    if df is None or df.empty:
        return "🎯 FETH: محتاج بيانات الأول عشان أساعدك!"
    
    question = question.lower()
    feth = st.session_state.feth
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object']).columns
    
    # تحليل ذكي للسؤال
    if any(word in question for word in ["إجمالي", "total", "sum", "مجموع"]):
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            total = df[col].sum()
            return f"{feth.respond('insight_high', f'الإجمالي: {total:,.0f}', df)}\n\n💰 الإجمالي: {total:,.0f}"
    
    elif any(word in question for word in ["متوسط", "average", "mean"]):
        if len(numeric_cols) > 0:
            avg = df[numeric_cols[0]].mean()
            return f"📊 المتوسط: {avg:,.2f}\n\n{feth.get_signature()}"
    
    elif any(word in question for word in ["أعلى", "max", "maximum", "أكبر"]):
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            best_idx = df[numeric_cols[0]].idxmax()
            best_item = df.loc[best_idx, cat_cols[0]]
            best_value = df[numeric_cols[0]].max()
            return f"{feth.respond('insight_high', f'{best_item}: {best_value:,.0f}', df)}\n\n🏆 الأعلى: {best_item} ({best_value:,.0f})"
    
    elif any(word in question for word in ["أقل", "min", "minimum", "أصغر"]):
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            worst_idx = df[numeric_cols[0]].idxmin()
            worst_item = df.loc[worst_idx, cat_cols[0]]
            worst_value = df[numeric_cols[0]].min()
            return f"{feth.respond('insight_low', f'{worst_item}: {worst_value:,.0f}', df)}\n\n📉 الأقل: {worst_item} ({worst_value:,.0f})"
    
    elif any(word in question for word in ["عدد", "count", "كم", "how many"]):
        return f"{feth.respond('analysis_ready', df=df)}\n\n📋 عدد الصفوف: {len(df):,}\n📊 عدد الأعمدة: {len(df.columns)}"
    
    elif any(word in question for word in ["ملخص", "summary", "نظرة عامة"]):
        report = f"{feth.respond('analysis_ready', df=df)}\n\n"
        report += f"📊 ملخص البيانات:\n\n"
        report += f"• الصفوف: {len(df):,}\n"
        report += f"• الأعمدة: {len(df.columns)}\n"
        report += f"• الأعمدة الرقمية: {len(numeric_cols)}\n"
        report += f"• الأعمدة النصية: {len(cat_cols)}\n"
        if len(numeric_cols) > 0:
            report += f"• الإجمالي: {df[numeric_cols[0]].sum():,.0f}\n"
            report += f"• المتوسط: {df[numeric_cols[0]].mean():,.2f}\n"
            report += f"• الأعلى: {df[numeric_cols[0]].max():,.0f}\n"
            report += f"• الأقل: {df[numeric_cols[0]].min():,.0f}\n"
        return report + f"\n{feth.get_signature()}"
    
    elif any(word in question for word in ["توقع", "predict", "مستقبل", "future"]):
        return f"""🔮 {feth.respond('teaching', df=df).replace('خليني أفتحلك النقطة دي ببساطة وذكاء...', 'التوقع يحتاج نموذج تعلم آلي متقدم...')}

📈 لكن FETH يلاحظ:
* اتجاه البيانات: {"صاعد 📈" if len(numeric_cols) > 0 and df[numeric_cols[0]].iloc[-1] > df[numeric_cols[0]].iloc[0] else "هابط 📉"}
* التذبذب: {df[numeric_cols[0]].std():.2f if len(numeric_cols) > 0 else "غير متاح"}

{feth.get_signature()}"""
    
    else:
        return f"""{feth.respond('teaching', df=df)}

🤔 جرب تسأل FETH:
* "ما إجمالي المبيعات؟"
* "ما المتوسط؟"
* "أعلى منتج مبيعاً؟"
* "أقل قيمة؟"
* "عدد الصفوف؟"
* "ملخص البيانات؟"
* "توقع المستقبل؟"

{feth.get_signature()}"""

def generate_pdf_report(df, charts_data=None):
    """توليد تقرير PDF متقدم"""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 20)
            self.set_text_color(52, 152, 219)
            self.cell(0, 15, 'Smart Analyst The Beast', 0, 1, 'C')
            self.set_font('Arial', '', 12)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'FETH Intelligence Report', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Smart Analyst The Beast | FETH AI | Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    
    # Summary
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Executive Summary', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    pdf.cell(0, 8, f'Total Rows: {len(df):,}', 0, 1)
    pdf.cell(0, 8, f'Total Columns: {len(df.columns)}', 0, 1)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Key Metrics', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f'Total: {df[numeric_cols[0]].sum():,.0f}', 0, 1)
        pdf.cell(0, 8, f'Average: {df[numeric_cols[0]].mean():,.2f}', 0, 1)
        pdf.cell(0, 8, f'Maximum: {df[numeric_cols[0]].max():,.0f}', 0, 1)
        pdf.cell(0, 8, f'Minimum: {df[numeric_cols[0]].min():,.0f}', 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

def apply_excel_formula(df, formula, target_col):
    """تطبيق دوال Excel متقدمة"""
    try:
        formula = formula.strip()
        if formula.startswith('='):
            formula = formula[1:]
        
        formula_upper = formula.upper()
        
        if formula_upper.startswith('SUM('):
            col = formula[4:-1].strip()
            return df[col].sum()
        
        elif formula_upper.startswith('AVERAGE(') or formula_upper.startswith('AVG('):
            col = formula[8:-1].strip() if formula_upper.startswith('AVERAGE(') else formula[4:-1].strip()
            return df[col].mean()
        
        elif formula_upper.startswith('MAX('):
            col = formula[4:-1].strip()
            return df[col].max()
        
        elif formula_upper.startswith('MIN('):
            col = formula[4:-1].strip()
            return df[col].min()
        
        elif formula_upper.startswith('COUNT('):
            col = formula[6:-1].strip()
            return df[col].count()
        
        elif formula_upper.startswith('COUNTA('):
            col = formula[7:-1].strip()
            return df[col].notna().sum()
        
        elif formula_upper.startswith('IF('):
            parts = formula[3:-1].split(',')
            if len(parts) >= 2:
                condition = parts[0].strip()
                true_val = parts[1].strip() if len(parts) > 1 else "Yes"
                false_val = parts[2].strip() if len(parts) > 2 else "No"
                
                # Parse simple conditions
                if '>' in condition:
                    col, val = condition.split('>', 1)
                    col = col.strip()
                    val = float(val.strip())
                    return df.apply(lambda row: true_val if pd.notna(row.get(col)) and row.get(col) > val else false_val, axis=1)
                elif '<' in condition:
                    col, val = condition.split('<', 1)
                    col = col.strip()
                    val = float(val.strip())
                    return df.apply(lambda row: true_val if pd.notna(row.get(col)) and row.get(col) < val else false_val, axis=1)
                elif '=' in condition:
                    col, val = condition.split('=', 1)
                    col = col.strip()
                    val = val.strip().strip('"\'')
                    return df.apply(lambda row: true_val if str(row.get(col)) == val else false_val, axis=1)
        
        elif formula_upper.startswith('VLOOKUP('):
            return "🔍 VLOOKUP: استخدم دمج الجداول من القائمة"
        
        elif formula_upper.startswith('CONCATENATE(') or formula_upper.startswith('CONCAT('):
            cols = formula[formula.find('(')+1:-1].split(',')
            cols = [c.strip() for c in cols]
            return df.apply(lambda row: ' '.join([str(row.get(c, '')) for c in cols if pd.notna(row.get(c))]), axis=1)
        
        else:
            return "❌ FETH: الصيغة مش واضحة. جرب: SUM, AVERAGE, MAX, MIN, COUNT, IF"
    
    except Exception as e:
        return f"⚠️ FETH لاحظ خطأ: {str(e)}"

# ======== Sidebar متجاوب مع FETH ========
def render_sidebar():
    with st.sidebar:
        # Logo and Branding
        st.markdown(f"""
        <div class='feth-box'>
            <img src='{BeastConfig.LOGO_URL}' style='width:80px; height:80px; border-radius:50%; margin-bottom:10px;'>
            <h2 style='margin:0; font-size:24px;'>🦁 Smart Analyst</h2>
            <h3 style='margin:5px 0; font-size:20px; color:#FFD700;'>The Beast</h3>
            <p style='font-size:14px; margin:5px 0; opacity:0.9;'>🎯 FETH AI v2.0</p>
            <div style='width:60px; height:3px; background:white; margin:10px auto; border-radius:2px;'></div>
        </div>
        """, unsafe_allow_html=True)
        
        # FETH Welcome
        feth = st.session_state.feth
        if not st.session_state.feth_welcomed:
            st.info(f"🎯 {feth.respond('welcome', df=st.session_state.df)}")
            st.session_state.feth_welcomed = True
        
        # User Status
        if st.session_state.user:
            st.success(f"👤 {st.session_state.user.email}")
            if st.button("🚪 " + t('logout')):
                st.session_state.user = None
                st.session_state.session = None
                st.rerun()
        else:
            st.warning("🔐 " + ("غير مسجل" if st.session_state.language == 'ar' else "Not logged in"))
            if st.button("🔐 " + t('login')):
                st.session_state.page = 'login'
                st.rerun()
        
        st.write("---")
        
        # Navigation
        st.title(t('title'))
        
        menu_items = [
            (t('home'), 'home'),
            (t('login'), 'login'),
            (t('upload'), 'upload'),
            (t('multi_upload'), 'multi_upload'),
            (t('cleaner'), 'cleaner'),
            (t('excel'), 'excel'),
            (t('powerbi'), 'powerbi'),
            (t('sql'), 'sql'),
            (t('ai'), 'ai'),
            (t('cloud'), 'cloud'),
            (t('export'), 'export'),
            (t('settings'), 'settings')
        ]
        
        for label, key in menu_items:
            if st.button(label, key=f'menu_{key}'):
                st.session_state.page = key
                st.rerun()
        
        st.write("---")
        
        # Quick Tools
        st.markdown("### ⚡ " + ("أدوات سريعة" if st.session_state.language == 'ar' else "Quick Tools"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(t('sample'), key='btn_sample'):
                st.session_state.df = generate_sample_data(500)  # بيانات أكبر
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        with col2:
            if st.button(t('clear'), key='btn_clear'):
                st.session_state.df = None
                st.session_state.dfs = []
                st.session_state.cleaning_history = []
                st.info("🎯 FETH: جاهز نبدأ من جديد!")
                st.rerun()
        
        # FETH Suggestions
        st.write("---")
        st.markdown("### 💡 " + ("FETH يقترح" if st.session_state.language == 'ar' else "FETH Suggests"))
        
        suggestions = feth.suggest_next(st.session_state.page)
        for suggestion in suggestions[:3]:
            if st.button(suggestion, key=f"feth_sug_{hash(suggestion)}"):
                # Parse suggestion
                if any(x in suggestion for x in ["رفع", "Upload"]):
                    st.session_state.page = 'upload'
                elif any(x in suggestion for x in ["نظف", "Clean"]):
                    st.session_state.page = 'cleaner'
                elif any(x in suggestion for x in ["تحليل", "Power"]):
                    st.session_state.page = 'powerbi'
                elif any(x in suggestion for x in ["Excel", "صيغ"]):
                    st.session_state.page = 'excel'
                elif any(x in suggestion for x in ["سأل", "Ask"]):
                    st.session_state.page = 'ai'
                elif any(x in suggestion for x in ["تجريبية", "Sample"]):
                    st.session_state.df = generate_sample_data(500)
                elif any(x in suggestion for x in ["سحابة", "Cloud"]):
                    st.session_state.page = 'cloud'
                elif any(x in suggestion for x in ["دخول", "Login"]):
                    st.session_state.page = 'login'
                st.rerun()
        
        st.write("---")
        st.caption(t('signature'))

# ======== الصفحات ========
def render_home():
    """الصفحة الرئيسية المتجاوبة"""
    feth = st.session_state.feth
    df = st.session_state.df
    
    # Hero Section
    st.markdown(f"""
    <div class='beast-header'>
        <h1 class='beast-title'>🦁 Smart Analyst The Beast</h1>
        <p class='beast-subtitle'>{feth.respond('welcome', df=df)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # FETH Analysis
        st.success(f"🎯 {feth.respond('analysis_ready', df=df)}")
        
        # Metrics Grid - Responsive
        cols = st.columns(4)
        metrics = [
            ("📊 الصفوف", len(df)),
            ("📋 الأعمدة", len(df.columns)),
            ("💾 الحجم", f"{df.memory_usage(deep=True).sum()/1024:.1f} KB"),
            ("🔢 الرقمية", len(numeric_cols))
        ]
        
        for i, (label, value) in enumerate(metrics):
            with cols[i]:
                st.metric(label, value)
        
        # Smart Insights
        if len(numeric_cols) > 0:
            total = df[numeric_cols[0]].sum()
            avg = df[numeric_cols[0]].mean()
            
            if total > 100000:
                st.balloons()
                st.success(f"🎯 {feth.respond('insight_high', f'إجمالي ضخم: {total:,.0f}', df)}")
            
            # Charts Preview
            st.write("---")
            st.subheader("📈 نظرة سريعة")
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(df, x=numeric_cols[0], title="توزيع القيم")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if len(df) > 10:
                    fig2 = px.line(df.head(50), y=numeric_cols[0], title="أول 50 قيمة")
                    st.plotly_chart(fig2, use_container_width=True)
        
        # Data Preview
        st.write("---")
        st.subheader("👁️ معاينة البيانات")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Next Steps
        st.write("---")
        st.markdown(f"### 🎯 {feth.respond('teaching', df=df).replace('خليني أفتحلك النقطة دي ببساطة وذكاء...', 'الخطوة الجاية؟')}")
        
        next_steps = feth.suggest_next('home')
        step_cols = st.columns(len(next_steps))
        for i, step in enumerate(next_steps):
            with step_cols[i]:
                if st.button(step, key=f"home_next_{i}"):
                    # Handle navigation
                    if any(x in step for x in ["رفع", "Upload"]):
                        st.session_state.page = 'upload'
                    elif any(x in step for x in ["تجريبية", "Sample"]):
                        st.session_state.df = generate_sample_data(500)
                    elif any(x in step for x in ["اسأل", "Ask"]):
                        st.session_state.page = 'ai'
                    elif any(x in step for x in ["دخول", "Login"]):
                        st.session_state.page = 'login'
                    st.rerun()
    
    else:
        # Empty State
        st.info(f"🎯 {feth.respond('welcome', df=None)}")
        
        # CTA Buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 بيانات تجريبية", type='primary', use_container_width=True):
                st.session_state.df = generate_sample_data(500)
                st.rerun()
        
        with col2:
            if st.button("📥 ارفع ملفك", use_container_width=True):
                st.session_state.page = 'upload'
                st.rerun()
        
        with col3:
            if st.button("🔐 سجل دخول", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        
        # Features Showcase
        st.write("---")
        st.subheader("🚀 مميزات الوحش")
        
        feat_cols = st.columns(4)
        features = [
            ("🤖", "FETH AI", "محلل ذكي يفهم بياناتك"),
            ("☁️", "سحابة", "احفظ ووصل من أي مكان"),
            ("📱", "موبايل", "تصميم يتكيف مع كل شاشة"),
            ("🔐", "أمان", "حماية كاملة لبياناتك")
        ]
        
        for i, (icon, title, desc) in enumerate(features):
            with feat_cols[i]:
                st.markdown(f"""
                <div style='text-align:center; padding:20px; background:#1a1a2e; border-radius:15px;'>
                    <div style='font-size:40px;'>{icon}</div>
                    <h4 style='color:#3498DB;'>{title}</h4>
                    <p style='font-size:12px; color:gray;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

def render_login():
    """صفحة تسجيل الدخول"""
    st.markdown("""
    <div class='beast-header'>
        <h1 class='beast-title'>🔐 تسجيل الدخول</h1>
        <p class='beast-subtitle'>Smart Analyst The Beast Cloud</p>
    </div>
    """, unsafe_allow_html=True)
    
    supabase_mgr = st.session_state.supabase
    
    if not supabase_mgr.connected:
        st.error("⚠️ Supabase غير متصل. تأكد من إعدادات الـ API.")
        st.info("💡 لكن ممكن تستخدم التطبيق في الوضع المحلي بدون تسجيل.")
        if st.button("← الرجوع للرئيسية"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("📧 البريد الإلكتروني")
            password = st.text_input("🔑 كلمة المرور", type="password")
            submit = st.form_submit_button("دخول", use_container_width=True)
            
            if submit:
                with st.spinner("🎯 FETH بيتصل بالسحابة..."):
                    result = supabase_mgr.sign_in(email, password)
                    if "error" in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.session_state.user = result['user']
                        st.session_state.session = result['session']
                        st.success("🎉 تم تسجيل الدخول!")
                        st.balloons()
                        time.sleep(1)
                        st.session_state.page = 'home'
                        st.rerun()
    
    with tab2:
        with st.form("signup_form"):
            new_email = st.text_input("📧 البريد الإلكتروني")
            new_password = st.text_input("🔑 كلمة المرور", type="password")
            confirm_password = st.text_input("🔑 تأكيد كلمة المرور", type="password")
            submit = st.form_submit_button("إنشاء حساب", use_container_width=True)
            
            if submit:
                if new_password != confirm_password:
                    st.error("❌ كلمتا المرور غير متطابقتين")
                elif len(new_password) < 6:
                    st.error("❌ كلمة المرور قصيرة جداً (6 أحرف على الأقل)")
                else:
                    with st.spinner("🎯 FETH بينشئ الحساب..."):
                        result = supabase_mgr.sign_up(new_email, new_password)
                        if "error" in result:
                            st.error(f"❌ {result['error']}")
                        else:
                            st.success("✅ تم إنشاء الحساب! افحص بريدك للتفعيل.")

def render_upload():
    """رفع ملف واحد"""
    st.header("📥 رفع بيانات | FETH")
    
    feth = st.session_state.feth
    
    st.info(f"🎯 {feth.respond('support', df=st.session_state.df).replace('ولا يهمك... خلينا نمشي خطوة خطوة', 'ارفع ملفك وهفتحهولك')}!")
    
    uploaded = st.file_uploader("اختر ملف:", ['csv', 'xlsx', 'xls'], key='single_upload')
    
    if uploaded:
        try:
            with st.spinner("🎯 FETH بيفتح الملف..."):
                if uploaded.name.endswith('.csv'):
                    df_new = pd.read_csv(uploaded)
                else:
                    df_new = pd.read_excel(uploaded)
                
                st.session_state.df = df_new
                st.session_state.uploaded_files_count += 1
                
                insight = f"{len(df_new):,} صف × {len(df_new.columns)} عمود"
                st.success(f"🎯 {feth.respond('upload_success', insight, df_new)}")
                
                st.dataframe(df_new.head(), use_container_width=True)
                
                # Save to cloud if logged in
                if st.session_state.user and st.session_state.supabase.connected:
                    if st.button("☁️ احفظ في السحابة", type='primary'):
                        result = st.session_state.supabase.save_dataframe(
                            st.session_state.user.id,
                            uploaded.name,
                            df_new
                        )
                        if "error" in result:
                            st.error(f"❌ {result['error']}")
                        else:
                            st.success(f"🎯 {feth.respond('cloud_sync')}")
                
                # Next steps
                st.write("---")
                next_steps = feth.suggest_next('upload')
                cols = st.columns(len(next_steps))
                for i, step in enumerate(next_steps):
                    with cols[i]:
                        if st.button(step, key=f"upload_next_{i}"):
                            if any(x in step for x in ["نظف", "Clean"]):
                                st.session_state.page = 'cleaner'
                            elif any(x in step for x in ["Power"]):
                                st.session_state.page = 'powerbi'
                            elif any(x in step for x in ["FETH", "Ask"]):
                                st.session_state.page = 'ai'
                            elif any(x in step for x in ["سحابة", "Cloud"]):
                                st.session_state.page = 'cloud'
                            st.rerun()
                        
        except Exception as e:
            st.error(f"🎯 {feth.respond('error')}: {str(e)}")

def render_multi_upload():
    """رفع ملفات متعددة ودمجها"""
    st.header("📁 رفع متعدد ودمج | FETH")
    
    feth = st.session_state.feth
    
    st.info("🎯 ارفع ملفات متعددة وFETH يدمجهم لك!")
    
    uploaded_files = st.file_uploader(
        "اختر ملفات متعددة:",
        ['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        key='multi_upload'
    )
    
    if uploaded_files:
        st.success(f"📦 استلمت {len(uploaded_files)} ملفات")
        
        # Preview all files
        dfs = []
        for i, file in enumerate(uploaded_files):
            with st.expander(f"📄 {file.name}"):
                try:
                    if file.name.endswith('.csv'):
                        df_temp = pd.read_csv(file)
                    else:
                        df_temp = pd.read_excel(file)
                    
                    dfs.append(df_temp)
                    st.write(f"الصفوف: {len(df_temp):,} | الأعمدة: {len(df_temp.columns)}")
                    st.dataframe(df_temp.head(3), use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ خطأ في {file.name}: {e}")
        
        if dfs:
            st.write("---")
            st.subheader("🔗 خيارات الدمج")
            
            merge_type = st.radio(
                "طريقة الدمج:",
                ["concat", "join"],
                format_func=lambda x: "دمج عمودي (Concat)" if x == "concat" else "دمج أفقي (Join)"
            )
            
            if st.button("🔄 دمج الملفات", type='primary'):
                with st.spinner("🎯 FETH بيدمج..."):
                    merged_df = merge_dataframes(dfs, merge_type)
                    if merged_df is not None:
                        st.session_state.df = merged_df
                        st.session_state.dfs = dfs
                        
                        st.success(f"""
                        🎉 تم الدمج بنجاح!
                        📊 إجمالي الصفوف: {len(merged_df):,}
                        📋 إجمالي الأعمدة: {len(merged_df.columns)}
                        """)
                        
                        st.dataframe(merged_df.head(), use_container_width=True)
                        
                        if st.button("→ الاستمرار للتحليل"):
                            st.session_state.page = 'powerbi'
                            st.rerun()

def render_cleaner():
    """منظف البيانات المتقدم"""
    st.header("🧹 منظف البيانات | FETH")
    
    df = st.session_state.df
    feth = st.session_state.feth
    
    if df is not None:
        st.info(f"🎯 {feth.respond('analysis_ready', df=df)}")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("الصفوف", len(df))
        col2.metric("الأعمدة", len(df.columns))
        empty_count = int(df.isnull().sum().sum())
        dup_count = int(df.duplicated().sum())
        col3.metric("الفارغ", empty_count, delta=-empty_count if empty_count > 0 else None)
        col4.metric("التكرار", dup_count, delta=-dup_count if dup_count > 0 else None)
        
        if empty_count > 0:
            st.warning(f"🎯 {feth.respond('insight_low', f'{empty_count} قيمة فارغة', df)}")
        
        # Cleaning Tools
        st.write("---")
        st.subheader("🔧 أدوات التنظيف الذكية")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🗑️ حذف الفارغ", use_container_width=True):
                st.session_state.df = df.dropna()
                st.session_state.cleaning_history.append(f"حذف {empty_count} قيمة فارغة")
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        with col2:
            if st.button("📋 حذف التكرار", use_container_width=True):
                st.session_state.df = df.drop_duplicates()
                st.session_state.cleaning_history.append(f"حذف {dup_count} صف مكرر")
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        with col3:
            if st.button("🔤 تنظيف النص", use_container_width=True):
                df_clean = df.copy()
                for col in df_clean.select_dtypes(include=['object']):
                    df_clean[col] = df_clean[col].str.strip().str.title()
                st.session_state.df = df_clean
                st.session_state.cleaning_history.append("تنظيف النصوص")
                st.success(f"🎯 {feth.respond('celebration')}")
                st.rerun()
        
        with col4:
            if st.button("🔄 إعادة تعيين", use_container_width=True):
                st.session_state.cleaning_history = []
                st.info("🔄 تم إعادة تعيين السجل")
                st.rerun()
        
        # Advanced Cleaning
        with st.expander("🔧 أدوات متقدمة"):
            col1, col2 = st.columns(2)
            
            with col1:
                numeric_col = st.selectbox("عمود رقمي:", df.select_dtypes(include=[np.number]).columns)
                if st.button("📊 إزالة القيم المتطرفة (Outliers)"):
                    Q1 = df[numeric_col].quantile(0.25)
                    Q3 = df[numeric_col].quantile(0.75)
                    IQR = Q3 - Q1
                    df_clean = df[~((df[numeric_col] < (Q1 - 1.5 * IQR)) | (df[numeric_col] > (Q3 + 1.5 * IQR)))]
                    st.session_state.df = df_clean
                    st.success(f"🎯 تمت إزالة {len(df) - len(df_clean)} قيمة متطرفة")
                    st.rerun()
            
            with col2:
                text_col = st.selectbox("عمود نصي:", df.select_dtypes(include=['object']).columns)
                if st.button("🔍 تصحيح الأخطاء الإملائية"):
                    st.info("🔮 FETH: ميزة التصحيح تحتاج مكتبة إضافية (textblob)")
        
        # History
        if st.session_state.cleaning_history:
            with st.expander("📜 سجل التنظيف"):
                for i, action in enumerate(st.session_state.cleaning_history, 1):
                    st.write(f"{i}. {action}")
        
        st.write("---")
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.error(f"🎯 {feth.respond('support').replace('ولا يهمك... خلينا نمشي خطوة خطوة', 'محتاج بيانات الأول! ارفع ملف')} ❌")

def render_excel():
    """Excel Pro متقدم"""
    st.header("📊 Excel Pro | FETH")
    
    df = st.session_st
