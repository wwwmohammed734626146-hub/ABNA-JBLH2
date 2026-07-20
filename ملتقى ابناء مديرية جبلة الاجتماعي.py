import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات الصفحة الأساسية والتنسيق
# ==========================================
st.set_page_config(
    page_title="لوحة التحكم الموحدة للملتقى - مديرية جبلة",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق اتجاه النص من اليمين إلى اليسار (RTL)
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: bold;
    }
    div[class*="stTextInput"], div[class*="stSelectbox"], div[class*="stNumberInput"], div[class*="stTextArea"] {
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إدارة حالة الجلسة (Session State)
# ==========================================
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# ==========================================
# 3. الشريط الجانبي (Sidebar) - تسجيل الدخول
# ==========================================
st.sidebar.title("🔐 دخول الإدارة")

if not st.session_state["is_admin"]:
    with st.sidebar.form("login_form"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submit_button = st.form_submit_button("تسجيل الدخول")
        
        if submit_button:
            # يمكنك تعديل كلمة المرور واسم المستخدم من هنا
            if username == "admin" and password == "123456":
                st.session_state["is_admin"] = True
                st.sidebar.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.sidebar.error("اسم المستخدم أو كلمة المرور غير صحيحة")
else:
    st.sidebar.success("أنت مسجل كـ **مدير النظام**")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["is_admin"] = False
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **ملاحظة:** بطاقات رصيد الصندوق والسلال الموزعة مخفية تلقائياً وتظهر فقط للمدراء.")

# ==========================================
# 4. الترويسة الرئيسية للوحة التحكم
# ==========================================
st.title("📊 لوحة التحكم الموحدة للملتقى")
st.subheader("الجمهورية اليمنية - ملتقى أبناء مديرية جبلة - اللجنة الاجتماعية")
st.markdown("---")

# قيم الإحصائيات (يمكن ربطها مع قاعدة البيانات مستقبلاً)
val_fund = "0 ر.ي"         # رصيد الصندوق
val_baskets = "0 سلة"       # السلال الموزعة
val_beneficiaries = "0 فرد" # إجمالي الأفراد المستفيدين
val_forms = "0 استمارة"     # إجمالي الاستمارات

# ==========================================
# 5. عرض البطاقات (Metrics) حسب الصلاحية
# ==========================================
if st.session_state["is_admin"]:
    # إذا كان المستخدم مديراً: عرض جميع البطاقات الـ 4
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="رصيد الصندوق الحالي 💰", value=val_fund)
    with col2:
        st.metric(label="السلال الموزعة 📦", value=val_baskets)
    with col3:
        st.metric(label="إجمالي الأفراد المستفيدين 👥", value=val_beneficiaries)
    with col4:
        st.metric(label="إجمالي الاستمارات 📄", value=val_forms)
else:
    # للزوار والعموم: عرض البطاقات العامة فقط (2) وإخفاء المالية والسلال
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="إجمالي الأفراد المستفيدين 👥", value=val_beneficiaries)
    with col2:
        st.metric(label="إجمالي الاستمارات 📄", value=val_forms)

st.markdown("---")

# ==========================================
# 6. التبويبات الرئيسية لتعبئة وإدارة الاستمارات
# ==========================================
tab_form, tab_records, tab_manage = st.tabs(["📋 تعبئة استمارة نزوح جديدة", "📁 سجل الاستمارات", "⚙️ إدارة النظام"])

# ------------------------------------------
# التبويب الأول: تعبئة استمارة نزوح كاملاً
# ------------------------------------------
with tab_form:
    st.header("📋 استمارة نزوح - اللجنة الاجتماعية")
    
    with st.form("displacement_full_form", clear_on_submit=False):
        
        # 1. الترويسة
        st.subheader("1️⃣ البيانات الأساسية للترويسة")
        c1, c2, c3, c4 = st.columns(4)
        with c1: num = st.text_input("الرقم")
        with c2: date_val = st.date_input("التاريخ")
        with c3: hijri_date = st.text_input("الموافق (هجري)")
        with c4: attachments = st.text_input("الملحقات")

        st.markdown("---")

        # 2. بيانات رب الأسرة
        st.subheader("2️⃣ بيانات رب الأسرة")
        col1, col2, col3, col4 = st.columns(4)
        with col1: head_name = st.text_input("اسم رب الأسرة رباعياً*")
        with col2: phone = st.text_input("رقم التلفون")
        with col3: edu_level = st.selectbox("المستوى التعليمي", ["امي", "ابتدائي", "إعدادي", "ثانوي", "جامعي", "حاصل على مؤهل"])
        with col4: id_card = st.text_input("رقم البطاقة الشخصية")

        col5, col6, col7, col8 = st.columns(4)
        with col5: job_type = st.text_input("نوع العمل")
        with col6: job_place = st.text_input("جهة العمل")
        with col7: qualification = st.text_input("المؤهل العلمي")
        with col8: specialization = st.text_input("التخصص")

        col9, col10, col11, col12 = st.columns(4)
        with col9: blood_type = st.selectbox("فصيلة الدم", ["غير معروف", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        with col10: health_status = st.text_input("الحالة الصحية")
        with col11: disease_type = st.text_input("نوع المرض إن وجد")
        with col12: id_issue_place = st.text_input("مكان الإصدار للبطاقة")

        st.markdown("---")

        # 3. بيانات السكن والنزوح
        st.subheader("3️⃣ بيانات السكن والنزوح")
        st.markdown("**السكن الأصلي:**")
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1: orig_gov = st.text_input("المحافظة (الأصلية)")
        with ca2: orig_dir = st.text_input("المديرية (الأصلية)")
        with ca3: orig_uzla = st.text_input("العزلة (الأصلية)")
        with ca4: orig_village = st.text_input("القرية / الحارة (الأصلية)")

        st.markdown("**مكان قبل النزوح:**")
        cb1, cb2, cb3, cb4 = st.columns(4)
        with cb1: prev_gov = st.text_input("المحافظة (قبل النزوح)")
        with cb2: prev_dir = st.text_input("المديرية (قبل النزوح)")
        with cb3: prev_uzla = st.text_input("العزلة (قبل النزوح)")
        with cb4: prev_village = st.text_input("القرية / الحارة (قبل النزوح)")

        st.markdown("---")

        # 4. بيانات أقرب صلة قرابة
        st.subheader("4️⃣ بيانات أقرب صلة قرابة")
        ck1, ck2, ck3, ck4, ck5 = st.columns(5)
        with ck1: kin_name = st.text_input("اسم أقرب صلة قرابة")
        with ck2: kin_rel = st.text_input("صلة القرابة")
        with ck3: kin_phone = st.text_input("رقم الجوال")
        with ck4: family_status = st.selectbox("حالة الأسرة", ["مقيم", "نازح", "عائد"])
        with ck5: disp_date_count = st.text_input("تاريخ / عدد مرات النزوح")

        st.markdown("---")

        # 5. إحصاء أفراد الأسرة التفصيلي
        st.subheader("5️⃣ إحصاء عدد أفراد الأسرة")
        spouse_name = st.text_input("اسم الزوج / الزوجة رباعياً")
        
        st.markdown("**توزيع الأفراد حسب الفئات العمرية والجنس:**")
        
        # أسطر الإدخال للذكور والإناث
        st.caption("الذكور:")
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1: m_under1 = st.number_input("ذكور أقل من سنة", min_value=0, step=1)
        with m2: m_1_5 = st.number_input("ذكور (1 - 5)", min_value=0, step=1)
        with m3: m_6_17 = st.number_input("ذكور (6 - 17)", min_value=0, step=1)
        with m4: m_18_59 = st.number_input("ذكور (18 - 59)", min_value=0, step=1)
        with m5: m_60plus = st.number_input("ذكور (60+)", min_value=0, step=1)

        st.caption("الإناث:")
        f1, f2, f3, f4, f5 = st.columns(5)
        with f1: f_under1 = st.number_input("إناث أقل من سنة", min_value=0, step=1)
        with f2: f_1_5 = st.number_input("إناث (1 - 5)", min_value=0, step=1)
        with f3: f_6_17 = st.number_input("إناث (6 - 17)", min_value=0, step=1)
        with f4: f_18_59 = st.number_input("إناث (18 - 59)", min_value=0, step=1)
        with f5: f_60plus = st.number_input("إناث (60+)", min_value=0, step=1)

        tot1, tot2 = st.columns(2)
        with tot1: disabled_count = st.number_input("عدد المعاقين", min_value=0, step=1)
        with tot2: breadwinner_count = st.number_input("عدد المكفولين", min_value=0, step=1)

        st.markdown("---")

        # 6. السكن الحالي
        st.subheader("6️⃣ السكن الحالي")
        h1, h2, h3, h4, h5 = st.columns(5)
        with h1: house_num = st.text_input("رقم البيت")
        with h2: house_type = st.text_input("نوع البيت")
        with h3: rent_own = st.selectbox("ملكية البيت", ["ملك", "إيجار", "استضافة", "مأوى"])
        with h4: landlord_name = st.text_input("اسم صاحب البيت المؤجر إن وجد")
        with h5: landlord_phone = st.text_input("رقم الجوال (لصاحب البيت)")

        st.markdown("---")

        # 7. أهم الاحتياجات والمنظمات
        st.subheader("7️⃣ أهم الاحتياجات والمنظمات")
        st.write("حدد الاحتياجات الرئيسية المطلوبة:")
        
        req_col1, req_col2, req_col3, req_col4 = st.columns(4)
        with req_col1:
            req_shelter = st.checkbox("مأوى")
            req_items = st.checkbox("مواد إيواء")
        with req_col2:
            req_water = st.checkbox("خزان مياه")
            req_food = st.checkbox("غذاء")
        with req_col3:
            req_medical = st.checkbox("طبية")
            req_school = st.checkbox("حقيبة مدرسية")
        with req_col4:
            req_toilets = st.checkbox("حمامات")

        o1, o2 = st.columns(2)
        with o1: in_wfp = st.selectbox("هل مسجل في الغذاء العالمي؟", ["لا", "نعم"])
        with o2: current_org = st.text_input("ما هي المنظمة المقدمة حالياً؟")
        
        other_needs = st.text_area("الاحتياجات الأخرى")

        st.markdown("---")
        
        # 8. وثائق المرفقات والتوقيعات
        st.subheader("8️⃣ وثائق المرفقات والاعتماد")
        attachments_info = st.text_input("المرفقات (إن وجدت لأصحاب الحالات)")
        
        sig1, sig2, sig3 = st.columns(3)
        with sig1: st.text_input("اسم مندوب العزلة")
        with sig2: st.caption("رئيس اللجنة الاجتماعية: **صلاح صادق عقلان**")
        with sig3: st.caption("رئيس الملتقى: **إبراهيم محمد سعيد الشرعبي**")

        # زر الحفظ والارسال
        submitted = st.form_submit_button("💾 حفظ الاستمارة وتحديث البيانات")
        if submitted:
            if head_name.strip() == "":
                st.error("يرجى إدخال اسم رب الأسرة على الأقل لحفظ الاستمارة.")
            else:
                st.success(f"تم حفظ بيانات استمارة ({head_name}) بنجاح!")

# ------------------------------------------
# التبويب الثاني: سجل الاستمارات المسجلة
# ------------------------------------------
with tab_records:
    st.header("📁 سجل الاستمارات المسجلة")
    
    # جدول نموذجي لعرض الاستمارات المسجلة
    demo_data = {
        "رقم الاستمارة": [101, 102],
        "اسم رب الأسرة": ["محمد علي أحمد", "عبدالله صالح حسن"],
        "رقم التلفون": ["770000000", "730000000"],
        "العزلة / القرية": ["جبلة - المركز", "الربادي"],
        "حالة الأسرة": ["نازح", "مقيم"],
        "تاريخ التسجيل": ["2026-07-01", "2026-07-15"]
    }
    st.dataframe(pd.DataFrame(demo_data), use_container_width=True)

# ------------------------------------------
# التبويب الثالث: إدارة النظام (للمشرفين)
# ------------------------------------------
with tab_manage:
    if st.session_state["is_admin"]:
        st.header("⚙️ لوحة إدارة المشرفين والصلاحيات")
        st.write("أهلاً بك في قسم الإدارة. يمكنك من هنا متابعة وتحديث السلال الموزعة، الأرصدة المالية، وإدارة الحسابات.")
    else:
        st.warning("🔒 هذا القسم مخصص لمدراء النظام فقط. يرجى تسجيل الدخول عبر الشريط الجانبي لوصول الإدارة.")

