import streamlit as st
import pandas as pd
import numpy as np

def ai_assistant(df, question):
    """مساعد AI ذكي يحلل البيانات"""
    
    question = question.lower()
    
    # تحليل الأسئلة
    if "إجمالي" in question or "total" in question or "sum" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            total = df[numeric_cols[0]].sum()
            return f"💰 الإجمالي: {total:,.0f}"
    
    elif "متوسط" in question or "average" in question or "mean" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            avg = df[numeric_cols[0]].mean()
            return f"📊 المتوسط: {avg:,.2f}"
    
    elif "أعلى" in question or "max" in question or "best" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            best_idx = df[numeric_cols[0]].idxmax()
            best_item = df.loc[best_idx, cat_cols[0]]
            best_value = df[numeric_cols[0]].max()
            return f"🏆 الأعلى: {best_item} ({best_value:,.0f})"
    
    elif "أقل" in question or "min" in question or "worst" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            worst_idx = df[numeric_cols[0]].idxmin()
            worst_item = df.loc[worst_idx, cat_cols[0]]
            worst_value = df[numeric_cols[0]].min()
            return f"📉 الأقل: {worst_item} ({worst_value:,.0f})"
    
    elif "عدد" in question or "count" in question or "كم" in question:
        return f"📋 عدد الصفوف: {len(df):,}"
    
    elif "ملخص" in question or "summary" in question or "نظرة عامة" in question:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        report = "📊 ملخص البيانات:\n\n"
        report += f"• الصفوف: {len(df):,}\n"
        report += f"• الأعمدة: {len(df.columns)}\n"
        
        if len(numeric_cols) > 0:
            report += f"• الإجمالي: {df[numeric_cols[0]].sum():,.0f}\n"
            report += f"• المتوسط: {df[numeric_cols[0]].mean():,.2f}\n"
            report += f"• الأعلى: {df[numeric_cols[0]].max():,.0f}\n"
            report += f"• الأدنى: {df[numeric_cols[0]].min():,.0f}\n"
        
        return report
    
    elif "رسم" in question or "chart" in question or "graph" in question:
        return "📈 اذهب لصفحة 'Power BI' لرؤية الرسوم البيانية"
    
    elif "تصدير" in question or "export" in question or "حفظ" in question:
        return "💾 اذهب لصفحة 'تصدير' لتحميل البيانات"
    
    else:
        return f"""🤔 لم أفهم السؤال بالضبط.

جرب تسأل:
* "ما إجمالي المبيعات؟"
* "ما المتوسط؟"
* "أعلى منتج مبيعاً؟"
* "أقل فرع مبيعاً؟"
* "عدد الصفوف؟"
* "ملخص البيانات؟"
"""

# ======== اختبار ========
if _name_ == "_main_":
    # بيانات تجريبية
    df = pd.DataFrame({
        'المنتج': ['A', 'B', 'C', 'D'],
        'المبيعات': [100, 200, 150, 300]
    })
    
    print(ai_assistant(df, "ما إجمالي المبيعات؟"))
    print(ai_assistant(df, "ما المتوسط؟"))
    print(ai_assistant(df, "أعلى منتج؟"))
