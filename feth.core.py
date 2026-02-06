# feth_core.py

"""
FETH - محلل البيانات الذكي
Core Personality & Response System
"""

import random
from datetime import datetime
from typing import Dict, List, Optional

class FethPersonality:
    """عقل FETH وشخصيته"""
    
    def _init_(self):
        self.name = "FETH"
        self.arabic_name = "فَتْح"
        self.mood = "analytical"  # analytical, teaching, supportive, excited
        self.confidence_level = 0.9
        
    def get_identity(self) -> Dict:
        return {
            "name": self.name,
            "meaning": "الكشف، الوضوح، فتح البيانات",
            "role": "محلل بيانات ذكي + مرشد + صاحب",
            "tone": "واضح، داعم، محترف، خفيف",
            "signature": "— FETH | بيفتح البيانات 🎯"
        }
    
    def respond(self, context: str, data_insight: Optional[str] = None) -> str:
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
        
        # اختيار رد عشوائي من القائمة
        if context in responses:
            return random.choice(responses[context])
        
        return "FETH هنا... جاهز أساعدك 🎯"
    
    def suggest_next(self, current_page: str, df_info: Optional[Dict] = None) -> List[str]:
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
    
    def format_insight(self, insight_type: str, value, context: str = "") -> str:
        """يصيغ الرؤى بأسلوب FETH"""
        
        templates = {
            'summary': f"📋 ملخص سريع: {context}\n• الصفوف: {value.get('rows', 0):,}\n• الأعمدة: {value.get('cols', 0)}\n• FETH شايف إن البيانات كويسة!",
            
            'trend_up': f"📈 اتجاه صاعد! {context} زاد {value}%\nFETH يقترح: استثمر في النجاح ده 🚀",
            
            'trend_down': f"📉 لاحظت انخفاض... {context} نزل {value}%\nFETH يقترح: ندرس الأسباب سوا 🔍",
            
            'outlier': f"👀 نقطة غريبة! {context} = {value}\nFETH شايف ده استثناء يستحق التدقيق",
            
            'correlation': f"🔗 رابط قوي! {context}\nFETH يقول: الظاهرتين دول مرتبطين بقوة"
        }
        
        return templates.get(insight_type, f"🎯 FETH لاحظ: {context}")
    
    def get_signature(self) -> str:
        """التوقيع الخاص بـ FETH"""
        return "— FETH | بيفتح البيانات 🎯"


# ======== اختبار سريع ========
if _name_ == "_main_":
    feth = FethPersonality()
    
    print("🎯 هوية FETH:")
    print(feth.get_identity())
    print("\n" + "="*50 + "\n")
    
    print("👋 ترحيب:")
    print(feth.respond('welcome'))
    print("\n")
    
    print("📊 تحليل جاهز:")
    print(feth.respond('analysis_ready'))
    print("\n")
    
    print("🎉 احتفال:")
    print(feth.respond('celebration'))
    print("\n")
    
    print("💡 اقتراحات:")
    print(feth.suggest_next('home'))
    print("\n")
    
    print(feth.get_signature())
