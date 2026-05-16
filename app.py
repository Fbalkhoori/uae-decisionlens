import os
from datetime import datetime
import streamlit as st
from openai import OpenAI

# OpenAI Client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Page Config
st.set_page_config(
    page_title="UAE DecisionLens",
    page_icon="🇦🇪",
    layout="wide"
)

# Language Selection
language = st.selectbox(
    "Choose Language / اختر اللغة",
    ["English", "العربية"]
)

is_arabic = language == "العربية"

# Current Date
current_date = datetime.now().strftime("%d/%m/%Y")

# Language Variables
if is_arabic:
    direction = "rtl"
    align = "right"

    title = "عدسة القرار الإماراتية"
    subtitle = "منصة ذكاء اصطناعي لتقييم القرارات الاستراتيجية قبل التنفيذ"

    input_label = "أدخل القرار الاستراتيجي أو السياسي المراد تقييمه"

    button_text = "إنشاء تقرير تقييم القرار"

    placeholder = "مثال: هل ينبغي لدولة الإمارات تسريع تبني الذكاء الاصطناعي في الخدمات الحكومية بحلول عام 2030؟"

    language_instruction = """
اكتب التقرير بالكامل باللغة العربية الفصحى المهنية.

يجب أن يكون:
- منسقاً بشكل تنفيذي
- واضحاً للقيادات الحكومية
- بمحاذاة صحيحة من اليمين إلى اليسار
- مع نقاط وقوائم عربية منظمة
"""
else:
    direction = "ltr"
    align = "left"

    title = "UAE DecisionLens"
    subtitle = "AI-Powered Sovereign Decision Intelligence Agent"

    input_label = "Enter the strategic or policy decision to evaluate"

    button_text = "Generate Decision Impact Brief"

    placeholder = "Example: Should the UAE accelerate AI adoption across public services by 2030?"

    language_instruction = """
Write the report in professional executive English suitable for UAE leadership.
"""

# Styling
st.markdown(
    f"""
<style>

.stApp {{
    background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
    direction: {direction};
    text-align: {align};
}}

.block-container {{
    max-width: 1150px;
    padding-top: 2rem;
}}

h1, h2, h3, h4, p, div, label {{
    direction: {direction};
    text-align: {align};
}}

.stMarkdown,
.stMarkdown p,
.stMarkdown div,
.stMarkdown ul,
.stMarkdown ol,
.stMarkdown li {{
    direction: {direction} !important;
    text-align: {align} !important;
}}

.stMarkdown ul,
.stMarkdown ol {{
    padding-right: 2rem !important;
    padding-left: 0 !important;
}}

.stMarkdown li {{
    margin-bottom: 0.5rem;
    line-height: 2;
}}

.metric-card {{
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e6edf5;
    box-shadow: 0 4px 18px rgba(16,32,51,0.06);
}}

.metric-title {{
    color: #5d6d7e;
    font-size: 14px;
    font-weight: 600;
}}

.metric-value {{
    color: #102033;
    font-size: 28px;
    font-weight: 800;
    margin-top: 10px;
}}

.stTextArea textarea {{
    border-radius: 16px;
    min-height: 180px;
    font-size: 17px;
    direction: {direction};
    text-align: {align};
}}

.stButton button {{
    background: linear-gradient(90deg, #102033, #1d4ed8);
    color: white;
    border-radius: 14px;
    padding: 0.8rem 1.6rem;
    font-weight: 700;
    border: none;
}}
.report-ar {{
    direction: rtl;
    text-align: right;
}}

.report-ar h1,
.report-ar h2,
.report-ar h3,
.report-ar p,
.report-ar li,
.report-ar table {{
    text-align: right !important;
}}
</style>
""",
    unsafe_allow_html=True
)

# Header
if is_arabic:
    st.markdown(
        f"""
<div style="width:100%; direction:rtl; text-align:right;">
    <div style="display:inline-flex; align-items:center; gap:14px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg" width="55">
        <h1 style="margin:0;">{title}</h1>
    </div>
</div>
""",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
<div style="display:flex; align-items:center; gap:14px; justify-content:flex-start;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg" width="55">
    <h1 style="margin:0;">{title}</h1>
</div>
""",
        unsafe_allow_html=True
    )

st.caption(subtitle)

# Cards
col1, col2, col3 = st.columns(3)

if is_arabic:
    col1.markdown("""
<div class="metric-card">
<div class="metric-title">الغرض</div>
<div class="metric-value">تقييم قبل التنفيذ</div>
</div>
""", unsafe_allow_html=True)

    col2.markdown("""
<div class="metric-card">
<div class="metric-title">اللغة</div>
<div class="metric-value">عربي / إنجليزي</div>
</div>
""", unsafe_allow_html=True)

    col3.markdown("""
<div class="metric-card">
<div class="metric-title">المخرجات</div>
<div class="metric-value">تقرير تنفيذي</div>
</div>
""", unsafe_allow_html=True)

else:
    col1.markdown("""
<div class="metric-card">
<div class="metric-title">Purpose</div>
<div class="metric-value">Pre-Implementation Evaluation</div>
</div>
""", unsafe_allow_html=True)

    col2.markdown("""
<div class="metric-card">
<div class="metric-title">Language</div>
<div class="metric-value">Arabic / English</div>
</div>
""", unsafe_allow_html=True)

    col3.markdown("""
<div class="metric-card">
<div class="metric-title">Output</div>
<div class="metric-value">Executive Brief</div>
</div>
""", unsafe_allow_html=True)

# User Input
decision = st.text_area(
    input_label,
    placeholder=placeholder,
    height=180
)

# Generate Button
if st.button(button_text):

    if not decision.strip():
        st.warning("Please enter a decision first / الرجاء إدخال القرار أولاً")

    else:

        prompt = f"""
You are UAE DecisionLens.

Today's date is {current_date}.

Evaluate this strategic or policy decision before implementation:

{decision}

{language_instruction}

Generate a polished executive Decision Impact Brief.

Do NOT:
- repeat the report title
- repeat the date
- include Prepared by
- include DecisionLens UAE Analysis Unit
- include UAE Leadership and Policy Makers
- include signatures
- include footer notes
- include closing statements
- include author credits

Start directly from section 1.

Use clean markdown formatting with:
- headings
- bullet points
- markdown tables where appropriate

Use tables specifically for:
- Strategic Alignment
- Stakeholder Impact
- Scenario Analysis

Use minimal tables only when truly useful.

Prioritize:
- executive summaries
- strategic analysis
- risks and opportunities
- actionable recommendations
- a strong final conclusion at the end

Avoid excessive scoring, ratings, or repeated evaluation tables.
"""

        with st.spinner("Generating analysis... / جاري إعداد التحليل..."):

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            if is_arabic:
                report_header = f"""
# عدسة القرار الإماراتية

## تقرير تقييم القرار الاستراتيجي

**التاريخ:** {current_date}

---
"""
            else:
                report_header = f"""
# UAE DecisionLens

## Decision Impact Brief

**Date:** {current_date}

---
"""

            report_content = (
                report_header
                + response.choices[0].message.content
            )

            st.markdown("----")

            if is_arabic:
                st.markdown(
                    f'<div class="report-ar">{report_content}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(report_content)