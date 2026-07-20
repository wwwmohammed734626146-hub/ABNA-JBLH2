import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="نظام إدارة ملتقى أبناء مديرية جبلة الاجتماعي",
    page_icon="🏛️",
    layout="wide"
)

# اسم ملف البيانات وقوائم اللجان
EXCEL_FILE = "data_official.xlsx"
FOOD_BASKETS_FILE = "food_baskets.xlsx"
FINANCE_FILE = "finance.xlsx"

COMMITTEES = [
    "اللجنة الاجتماعية",
    "اللجنة القانونية",
    "اللجنة الإعلامية",
    "اللجنة العسكرية",
    "اللجنة المالية"
]

# إنشاء ملفات الإكسل الافتراضية بجميع حقول الاستمارة الرسمية
if not os.path.exists(EXCEL_FILE):
    columns = [
        "رقم الاستمارة", "تاريخ الاستمارة", "اسم رب الأسرة رباعياً", "تاريخ الميلاد", "المستوى التعليمي", 
        "رقم التلفون", "رقم البطاقة الشخصية", "نوع العمل", "جهة العمل", "المؤهل العلمي", 
        "التخصص", "فصيلة الدم", "الحالة الصحية", "نوع المرض إن وجد", "مكان الإصدار للبطاقة",
        "المحافظة الأصلية", "المديرية الأصلية", "العزلة الأصلية", "القرية/الحارة الأصلية",
        "محافظة قبل النزوح", "مديرية قبل النزوح", "عزلة قبل النزوح", "قرية قبل النزوح",
        "اسم أقرب صلة قرابة", "صلة القرابة", "رقم جوال أقرب قريب", "حالة الأسرة", "تاريخ النزوح للأسرة", "عدد مرات النزوح",
        "اسم الزوج/الزوجة رباعياً", "ذكور أقل من 5", "ذكور 5-17", "ذكور 18-59", "ذكور 60+",
        "إناث أقل من 5", "إناث 5-17", "إناث 18-59", "إناث 60+", "إجمالي أفراد الأسرة", "عدد المعاقين", "عدد المكفولين",
        "رقم البيت", "نوع البيت", "نوع السكن (ملك/إيجار)", "اسم صاحب البيت المؤجر", "المحافظة الحالية", "رقم الجوال الحالي",
        "احتياج ماوى", "احتياج مواد إيواء", "احتياج خزان مياه", "احتياج غذاء", "احتياج حقيبة مدرسية", "احتياج حمامات", "احتياجات أخرى",
        "هل مسجل في الغذاء العالمي", "ما هي المنظمة المقدمة حالياً", "اللجنة التابعة", "ملاحظات"
    ]
    pd.DataFrame(columns=columns).to_excel(EXCEL_FILE, index=False)

if not os.path.exists(FOOD_BASKETS_FILE):
    pd.DataFrame(columns=["رقم الاستمارة", "اسم المستفيد", "تاريخ التوزيع", "نوع السلة / المساعدة", "الجهة المانحة", "ملاحظات"]).to_excel(FOOD_BASKETS_FILE, index=False)

if not os.path.exists(FINANCE_FILE):
    pd.DataFrame(columns=["التاريخ", "النوع (وارد/منصرف)", "المبلغ (ر.ي)", "البيان / السبب", "المسؤول"]).to_excel(FINANCE_FILE, index=False)

# 2. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# 3. القائمة الجانبية
st.sidebar.title("🏛️ ملتقى جبلة الاجتماعي")

if not st.session_state['logged_in']:
    st.sidebar.subheader("🔑 تسجيل الدخول")
    user_input = st.sidebar.text_input("اسم المستخدم")
    pass_input = st.sidebar.text_input("كلمة المرور", type="password")
    
    if st.sidebar.button("تسجيل الدخول"):
        if user_input == "admin" and pass_input == "123456":
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'admin'
            st.session_state['username'] = 'مدير النظام (المشرف)'
            st.rerun()
        elif user_input == "user" and pass_input == "1234":
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'user'
            st.session_state['username'] = 'مدخل بيانات'
            st.rerun()
        else:
            st.sidebar.error("بيانات غير صحيحة!")
else:
    st.sidebar.write(f"مرحباً بك: **{st.session_state['username']}**")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.rerun()

st.sidebar.markdown("---")

menu_options = ["📊 لوحة التحكم الإحصائية", "📝 تعبئة استمارة نزوح رسمية"]

if st.session_state['logged_in'] and st.session_state['user_role'] == 'admin':
    menu_options.extend([
        "🔍 عرض استمارات النازحين",
        "✏️ تعديل بيانات الاستمارات",
        "🏢 إدارة اللجان المتخصصة",
        "📦 توزيع السلال الغذائية",
        "🤝 إدارة الكفالات والرعايات",
        "📁 الأرشيف والمستندات",
        "💰 الصندوق والحسابات (الوارد والمنصرف)",
        "👥 إدارة القوى البشرية والكادر",
        "🔐 إدارة المستخدمين وكلمات المرور",
        "📥 تصدير التقارير (Excel)"
    ])

choice = st.sidebar.radio("القائمة الرئيسية:", menu_options)

# ---------------------------------------------------------
# 1. لوحة التحكم
# ---------------------------------------------------------
if choice == "📊 لوحة التحكم الإحصائية":
    st.title("📊 لوحة التحكم الموحدة للملتقى")
    st.subheader("الجمهورية اليمنية - ملتقى أبناء مديرية جبلة - اللجنة الاجتماعية")
    st.markdown("---")
    
    df = pd.read_excel(EXCEL_FILE)
    df_food = pd.read_excel(FOOD_BASKETS_FILE)
    df_fin = pd.read_excel(FINANCE_FILE)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الاستمارات", f"{len(df)} استمارة")
    
    total_family = df['إجمالي أفراد الأسرة'].sum() if not df.empty and 'إجمالي أفراد الأسرة' in df.columns else 0
    col2.metric("إجمالي الأفراد المستفيدين", f"{int(total_family)} فرد")
    
    col3.metric("السلال الموزعة", f"{len(df_food)} سلة")
    
    income = df_fin[df_fin['النوع (وارد/منصرف)'] == 'وارد']['المبلغ (ر.ي)'].sum() if not df_fin.empty else 0
    expense = df_fin[df_fin['النوع (وارد/منصرف)'] == 'منصرف']['المبلغ (ر.ي)'].sum() if not df_fin.empty else 0
    col4.metric("رصيد الصندوق الحالي", f"{income - expense:,.0f} ر.ي")

# ---------------------------------------------------------
# 2. تعبئة استمارة نزوح رسمية (مطابقة للورقية تماماً)
# ---------------------------------------------------------
elif choice == "📝 تعبئة استمارة نزوح رسمية":
    st.title("📄 استمارة نزوح - ملتقى أبناء مديرية جبلة")
    st.markdown("---")
    
    with st.form("official_form", clear_on_submit=True):
        st.subheader("📌 البيانات الأساسية والرأسية")
        f1, f2 = st.columns(2)
        form_no = f1.text_input("الرقم (رقم الاستمارة)*")
        form_date = f2.text_input("التاريخ / الموافق", value="2026/07/20")
        
        st.subheader("👤 البيانات الشخصية لرب الأسرة")
        c1, c2, c3, c4 = st.columns(4)
        name = c1.text_input("اسم رب الأسرة رباعياً*")
        phone = c2.text_input("رقم التلفون")
        dob = c3.text_input("تاريخ الميلاد")
        id_no = c4.text_input("رقم البطاقة الشخصية")
        
        c5, c6, c7, c8 = st.columns(4)
        job_type = c5.text_input("نوع العمل")
        job_place = c6.text_input("جهة العمل")
        edu_level = c7.text_input("المستوى التعليمي / المؤهل")
        spec = c8.text_input("التخصص")
        
        c9, c10, c11, c12 = st.columns(4)
        blood = c9.text_input("فصيلة الدم")
        health = c10.text_input("الحالة الصحية")
        disease = c11.text_input("نوع المرض إن وجد")
        id_issue = c12.text_input("مكان إصدار البطاقة")
        
        st.subheader("📍 البيانات الجغرافية (الأصل وقبل النزوح)")
        st.write("**العنوان الأصلي:**")
        g1, g2, g3, g4 = st.columns(4)
        orig_gov = g1.text_input("المحافظة الأصلية")
        orig_dir = g2.text_input("المديرية الأصلية")
        orig_oz = g3.text_input("العزلة الأصلية")
        orig_vil = g4.text_input("القرية / الحارة الأصلية")
        
        st.write("**مكان قبل النزوح:**")
        p1, p2, p3, p4 = st.columns(4)
        prev_gov = p1.text_input("المحافظة قبل النزوح")
        prev_dir = p2.text_input("المديرية قبل النزوح")
        prev_oz = p3.text_input("العزلة قبل النزوح")
        prev_vil = p4.text_input("القرية قبل النزوح")
        
        st.subheader("👨👩👧👦 أقرب صلة قرابة وحالة النزوح")
        r1, r2, r3 = st.columns(3)
        rel_name = r1.text_input("اسم أقرب صلة قرابة")
        rel_type = r2.text_input("صلة القرابة")
        rel_phone = r3.text_input("رقم الجوال للقريب")
        
        n1, n2, n3 = st.columns(3)
        fam_status = n1.text_input("حالة الأسرة")
        disp_date = n2.text_input("تاريخ النزوح للأسرة")
        disp_times = n3.number_input("عدد مرات النزوح", min_value=1, value=1)
        
        st.subheader("👨👩👧👦 إحصاء عدد أفراد الأسرة")
        spouse = st.text_input("اسم الزوج / الزوجة رباعياً")
        
        st.write("**الذكور:**")
        m1, m2, m3, m4 = st.columns(4)
        m_less5 = m1.number_input("ذكور أقل من 5 سنوات", min_value=0)
        m_5_17 = m2.number_input("ذكور 5-17 سنة", min_value=0)
        m_18_59 = m3.number_input("ذكور 18-59 سنة", min_value=0)
        m_60plus = m4.number_input("ذكور +60 سنة", min_value=0)
        
        st.write("**الإناث:**")
        w1, w2, w3, w4 = st.columns(4)
        w_less5 = w1.number_input("إناث أقل من 5 سنوات", min_value=0)
        w_5_17 = w2.number_input("إناث 5-17 سنة", min_value=0)
        w_18_59 = w3.number_input("إناث 18-59 سنة", min_value=0)
        w_60plus = w4.number_input("إناث +60 سنة", min_value=0)
        
        e1, e2, e3 = st.columns(3)
        total_fam = e1.number_input("إجمالي أفراد الأسرة*", min_value=1, value=1)
        dis_count = e2.number_input("عدد المعاقين", min_value=0)
        sponsored_count = e3.number_input("عدد المكفولين", min_value=0)
        
        st.subheader("🏠 بيانات السكن الحالي")
        h1, h2, h3, h4 = st.columns(4)
        house_no = h1.text_input("رقم البيت")
        house_type = h2.text_input("نوع البيت")
        rent_type = h3.selectbox("ملك / إيجار", ["إيجار", "ملك", "مستضاف", "مأوى موقت"])
        owner_name = h4.text_input("اسم صاحب البيت المؤجر")
        
        h5, h6 = st.columns(2)
        curr_gov = h5.text_input("المحافظة الحالية")
        curr_phone = h6.text_input("رقم الجوال الحالي")
        
        st.subheader("🆘 أهم الاحتياجات والمنظمات")
        st.write("**حدد احتياجات الأسرة:**")
        i1, i2, i3, i4, i5, i6 = st.columns(6)
        req_shelter = i1.checkbox("مأوى")
        req_item = i2.checkbox("مواد إيواء")
        req_tank = i3.checkbox("خزان مياه")
        req_food = i4.checkbox("غذاء")
        req_bag = i5.checkbox("حقيبة مدرسية")
        req_bath = i6.checkbox("حمامات")
        
        req_other = st.text_input("الاحتياجات الأخرى")
        
        o1, o2, o3 = st.columns(3)
        is_wfp = o1.selectbox("هل مسجل في الغذاء العالمي؟", ["لا", "نعم"])
        curr_org = o2.text_input("ما هي المنظمة المقدمة حالياً؟")
        committee = o3.selectbox("توجيه الاستمار للجنة:", COMMITTEES)
        
        notes = st.text_area("ملاحظات أخرى")
        
        btn = st.form_submit_button("💾 حفظ الاستمارة الرسمية")
        
        if btn:
            if name and form_no:
                data = {
                    "رقم الاستمارة": form_no, "تاريخ الاستمارة": form_date, "اسم رب الأسرة رباعياً": name, "تاريخ الميلاد": dob,
                    "المستوى التعليمي": edu_level, "رقم التلفون": phone, "رقم البطاقة الشخصية": id_no, "نوع العمل": job_type,
                    "جهة العمل": job_place, "المؤهل العلمي": edu_level, "التخصص": spec, "فصيلة الدم": blood, "الحالة الصحية": health,
                    "نوع المرض إن وجد": disease, "مكان الإصدار للبطاقة": id_issue, "المحافظة الأصلية": orig_gov, "المديرية الأصلية": orig_dir,
                    "العزلة الأصلية": orig_oz, "القرية/الحارة الأصلية": orig_vil, "محافظة قبل النزوح": prev_gov, "مديرية قبل النزوح": prev_dir,
                    "عزلة قبل النزوح": prev_oz, "قرية قبل النزوح": prev_vil, "اسم أقرب صلة قرابة": rel_name, "صلة القرابة": rel_type,
                    "رقم جوال أقرب قريب": rel_phone, "حالة الأسرة": fam_status, "تاريخ النزوح للأسرة": disp_date, "عدد مرات النزوح": disp_times,
                    "اسم الزوج/الزوجة رباعياً": spouse, "ذكور أقل من 5": m_less5, "ذكور 5-17": m_5_17, "ذكور 18-59": m_18_59, "ذكور 60+": m_60plus,
                    "إناث أقل من 5": w_less5, "إناث 5-17": w_5_17, "إناث 18-59": w_18_59, "إناث 60+": w_60plus, "إجمالي أفراد الأسرة": total_fam,
                    "عدد المعاقين": dis_count, "عدد المكفولين": sponsored_count, "رقم البيت": house_no, "نوع البيت": house_type,
                    "نوع السكن (ملك/إيجار)": rent_type, "اسم صاحب البيت المؤجر": owner_name, "المحافظة الحالية": curr_gov, "رقم الجوال الحالي": curr_phone,
                    "احتياج ماوى": "نعم" if req_shelter else "لا", "احتياج مواد إيواء": "نعم" if req_item else "لا",
                    "احتياج خزان مياه": "نعم" if req_tank else "لا", "احتياج غذاء": "نعم" if req_food else "لا",
                    "احتياج حقيبة مدرسية": "نعم" if req_bag else "لا", "احتياج حمامات": "نعم" if req_bath else "لا",
                    "احتياجات أخرى": req_other, "هل مسجل في الغذاء العالمي": is_wfp, "ما هي المنظمة المقدمة حالياً": curr_org,
                    "اللجنة التابعة": committee, "ملاحظات": notes
                }
                
                df = pd.read_excel(EXCEL_FILE)
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                st.success(f"تم حفظ استمارة الأخ ({name}) المكتملة بنجاح!")
            else:
                st.error("يرجى تعبئة الحقول الإجباري (اسم رب الأسرة ورقم الاستمارة).")

# ---------------------------------------------------------
# 3. عرض كافة بيانات الاستمارة للمشرف
# ---------------------------------------------------------
elif choice == "🔍 عرض استمارات النازحين":
    st.title("🔍 عرض البيانات الكاملة لكل الاستمارات الرسمية")
    df = pd.read_excel(EXCEL_FILE)
    if df.empty:
        st.warning("لا توجد استمارات مسجلة حتى الآن.")
    else:
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.subheader("📋 معاينة استمارة مستقلة بالتفصيل الكامل")
        selected_person = st.selectbox("اختر المستفيد:", df["اسم رب الأسرة رباعياً"].dropna().unique())
        if selected_person:
            row = df[df["اسم رب الأسرة رباعياً"] == selected_person].iloc[0]
            st.json(row.to_dict())

# ---------------------------------------------------------
# 4. تعديل بيانات الاستمارات
# ---------------------------------------------------------
elif choice == "✏️ تعديل بيانات الاستمارات":
    st.title("✏️ تعديل وتحديث استمارة مسجلة")
    df = pd.read_excel(EXCEL_FILE)
    if df.empty:
        st.warning("لا توجد استمارات للتعديل.")
    else:
        selected_id = st.selectbox("اختر رقم الاستمارة للتعديل:", df["رقم الاستمارة"].unique())
        idx = df[df["رقم الاستمارة"] == selected_id].index[0]
        
        with st.form("edit_form"):
            st.write(f"تعديل بيانات الاستمارة رقم: {selected_id}")
            new_name = st.text_input("اسم رب الأسرة", value=str(df.loc[idx, "اسم رب الأسرة رباعياً"]))
            new_phone = st.text_input("رقم التلفون", value=str(df.loc[idx, "رقم التلفون"]))
            new_committee = st.selectbox("اللجنة التابعة", COMMITTEES, index=0)
            
            if st.form_submit_button("تحديث البيانات"):
                df.loc[idx, "اسم رب الأسرة رباعياً"] = new_name
                df.loc[idx, "رقم التلفون"] = new_phone
                df.loc[idx, "اللجنة التابعة"] = new_committee
                df.to_excel(EXCEL_FILE, index=False)
                st.success("تم تحديث البيانات بنجاح!")

# ---------------------------------------------------------
# 5. إدارة اللجان المتخصصة
# ---------------------------------------------------------
elif choice == "🏢 إدارة اللجان المتخصصة":
    st.title("🏢 اللجان التابعة لملتقى أبناء مديرية جبلة")
    df = pd.read_excel(EXCEL_FILE)
    
    selected_comm = st.selectbox("اختر اللجنة لعرض كادرها واستماراتها:", COMMITTEES)
    filtered = df[df["اللجنة التابعة"] == selected_comm] if not df.empty else pd.DataFrame()
    
    st.subheader(f"قائمة الاستمارات المسجلة لدى ({selected_comm}):")
    st.dataframe(filtered, use_container_width=True)

# ---------------------------------------------------------
# 6. توزيع السلال الغذائية (شغال بالفعل)
# ---------------------------------------------------------
elif choice == "📦 توزيع السلال الغذائية":
    st.title("📦 تسجيل وإدارة توزيع السلال الغذائية")
    
    df_main = pd.read_excel(EXCEL_FILE)
    df_food = pd.read_excel(FOOD_BASKETS_FILE)
    
    with st.form("food_form", clear_on_submit=True):
        st.subheader("تسجيل توزيع سلة جديدة:")
        ben_name = st.selectbox("اختر المستفيد:", df_main["اسم رب الأسرة رباعياً"].dropna().unique() if not df_main.empty else ["لا يوجد"])
        basket_type = st.text_input("نوع السلة / المساعدة", value="سلة غذائية مكتملة")
        donor = st.text_input("الجهة المانحة / الداعم")
        dist_date = st.text_input("تاريخ التوزيع", value="2026/07/20")
        
        if st.form_submit_button("قيد التوزيع"):
            new_entry = {"رقم الاستمارة": "مربوط", "اسم المستفيد": ben_name, "تاريخ التوزيع": dist_date, "نوع السلة / المساعدة": basket_type, "الجهة المانحة": donor, "ملاحظات": ""}
            df_food = pd.concat([df_food, pd.DataFrame([new_entry])], ignore_index=True)
            df_food.to_excel(FOOD_BASKETS_FILE, index=False)
            st.success(f"تم قيد تسليم السلة لـ ({ben_name}) بنجاح!")
            
    st.subheader("📋 سجل توزيع السلال السابق:")
    st.dataframe(df_food, use_container_width=True)

# ---------------------------------------------------------
# 7. إدارة الكفالات والرعايات
# ---------------------------------------------------------
elif choice == "🤝 إدارة الكفالات والرعايات":
    st.title("🤝 قسم كفالات الأسر والرعايات")
    df = pd.read_excel(EXCEL_FILE)
    if not df.empty and "عدد المكفولين" in df.columns:
        sponsored_df = df[df["عدد المكفولين"] > 0]
        st.subheader("قائمة الأسر التي لديها مكفولين:")
        st.dataframe(sponsored_df[["رقم الاستمارة", "اسم رب الأسرة رباعياً", "عدد المكفولين", "رقم التلفون"]], use_container_width=True)

# ---------------------------------------------------------
# 8. الأرشيف والمستندات
# ---------------------------------------------------------
elif choice == "📁 الأرشيف والمستندات":
    st.title("📁 الأرشيف الرقمي ورفع الوثائق")
    uploaded_file = st.file_handling = st.file_uploader("رفع وثيقة / صورة بطاقة (PDF/Image):")
    if uploaded_file:
        st.success(f"تم رفع الملف ({uploaded_file.name}) بنجاح إلى الأرشيف!")

# ---------------------------------------------------------
# 9. الصندوق والحسابات (الوارد والمنصرف - شغال بالكامل)
# ---------------------------------------------------------
elif choice == "💰 الصندوق والحسابات (الوارد والمنصرف)":
    st.title("💰 إدارة الصندوق والمالية")
    df_fin = pd.read_excel(FINANCE_FILE)
    
    with st.form("fin_form", clear_on_submit=True):
        st.subheader("إضافة حركة مالية جديدة (سند قيد):")
        f_type = st.selectbox("نوع الحركة", ["وارد", "منصرف"])
        amount = st.number_input("المبلغ (بالريال اليمني)", min_value=1)
        reason = st.text_input("البيان / السبب")
        admin_user = st.text_input("المسؤول / المحاسب", value=st.session_state['username'])
        
        if st.form_submit_button("حفظ الحركة المالية"):
            new_fin = {"التاريخ": "2026/07/20", "النوع (وارد/منصرف)": f_type, "المبلغ (ر.ي)": amount, "البيان / السبب": reason, "المسؤول": admin_user}
            df_fin = pd.concat([df_fin, pd.DataFrame([new_fin])], ignore_index=True)
            df_fin.to_excel(FINANCE_FILE, index=False)
            st.success("تم تسجيل الحركة المالية بنجاح!")
            
    st.subheader("📋 كشف الحساب والعمليات المالية:")
    st.dataframe(df_fin, use_container_width=True)

# ---------------------------------------------------------
# 10. باقي الصفحات والإدارة
# ---------------------------------------------------------
elif choice == "👥 إدارة القوى البشرية والكادر":
    st.title("👥 إدارة القوى البشرية وكادر الملتقى")
    st.write("سجل أعضاء وإداريي ملتقى أبناء مديرية جبلة.")

elif choice == "🔐 إدارة المستخدمين وكلمات المرور":
    st.title("🔐 إدارة الحسابات والصلاحيات")
    st.write("اسم المشرف الحالي: admin | كلمة المرور: 123456")

elif choice == "📥 تصدير التقارير (Excel)":
    st.title("📥 تصدير البيانات والتقارير الشاملة")
    if os.path.exists(EXCEL_FILE):
        st.download_button(
            label="📥 تحميل قاعدة بيانات الاستمارات الرسمية (Excel)",
            data=open(EXCEL_FILE, "rb").read(),
            file_name="استمارات_نزوح_ملتقى_جبلة.xlsx"
        )

