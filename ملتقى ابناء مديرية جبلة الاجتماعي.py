import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="نظام إدارة ملتقى أبناء مديرية جبلة الاجتماعي",
    page_icon="🏛️",
    layout="wide"
)

# اسم ملف البيانات
EXCEL_FILE = "data.xlsx"

# قائمة اللجان الرسمية التابعة للملتقى
COMMITTEES = [
    "اللجنة الاجتماعية",
    "اللجنة القانونية",
    "اللجنة الإعلامية",
    "اللجنة العسكرية",
    "اللجنة المالية"
]

# إنشاء ملف إكسل افتراضي إذا لم يكن موجوداً
if not os.path.exists(EXCEL_FILE):
    df_init = pd.DataFrame(columns=[
        "رقم الاستمارة", "الاسم الكامل", "رقم الهوية", "رقم الهاتف", 
        "المحافظة الأصلية", "المديرية", "عدد أفراد الأسرة", "حالة السكن", "اللجنة التابعة", "ملاحظات"
    ])
    df_init.to_excel(EXCEL_FILE, index=False)

# 2. تهيئة جلسة المستخدم (Session State)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# 3. القائمة الجانبية وتحديد الصلاحيات
st.sidebar.title("🏛️ ملتقى جبلة الاجتماعي")

# نموذج تسجيل الدخول في القائمة الجانبية
if not st.session_state['logged_in']:
    st.sidebar.subheader("🔑 تسجيل الدخول")
    user_input = st.sidebar.text_input("اسم المستخدم")
    pass_input = st.sidebar.text_input("كلمة المرور", type="password")
    
    if st.sidebar.button("تسجيل الدخول"):
        if user_input == "admin" and pass_input == "123456":
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'admin'
            st.session_state['username'] = 'مدير النظام (المشرف)'
            st.sidebar.success("تم تسجيل الدخول كمدير نظام!")
            st.rerun()
        elif user_input == "user" and pass_input == "1234":
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'user'
            st.session_state['username'] = 'مدخل بيانات'
            st.sidebar.success("تم تسجيل الدخول كمستخدم!")
            st.rerun()
        else:
            st.sidebar.error("بيانات الدخول غير صحيحة!")
else:
    st.sidebar.write(f"مرحباً بك: **{st.session_state['username']}**")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['username'] = ""
        st.rerun()

st.sidebar.markdown("---")

# 4. تحديد القوائم المتاحة بناءً على الصلاحيات
menu_options = [
    "📊 لوحة التحكم الإحصائية", 
    "📝 تعبئة استمارة جديدة"
]

# إضافة كافة قوائم مدير النظام المتقدمة فقط للمشرف (admin)
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
# صفحات النظام
# ---------------------------------------------------------

if choice == "📊 لوحة التحكم الإحصائية":
    st.title("📊 لوحة التحكم الموحدة للملتقى")
    st.subheader("الجمهورية اليمنية - ملتقى أبناء مديرية جبلة")
    st.markdown("---")
    df = pd.read_excel(EXCEL_FILE)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الاستمارات", f"{len(df)} استمارة")
    total_family = df['عدد أفراد الأسرة'].sum() if 'عدد أفراد الأسرة' in df.columns and not df.empty else 0
    col2.metric("إجمالي الأفراد المستفيدين", f"{int(total_family)} فرد")
    col3.metric("عدد اللجان التابعة", f"{len(COMMITTEES)} لجان")
    col4.metric("رصيد الصندوق الحالي", "0 ر.ي")

elif choice == "📝 تعبئة استمارة جديدة":
    st.title("📝 استمارة حصر وتجميع البيانات")
    with st.form("displacement_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        form_id = c1.text_input("رقم الاستمارة")
        full_name = c2.text_input("الاسم الكامل للمستفيد")
        
        c3, c4 = st.columns(2)
        national_id = c3.text_input("رقم الهوية / البطاقة الشخصية")
        phone = c4.text_input("رقم الهاتف للتواصل")
        
        c5, c6 = st.columns(2)
        orig_gov = c5.text_input("المحافظة الأصلية")
        orig_dir = c6.text_input("المديرية")
        
        c7, c8, c9 = st.columns(3)
        family_members = c7.number_input("عدد أفراد الأسرة", min_value=1, value=1, step=1)
        housing_status = c8.selectbox("حالة السكن", ["مستأجر", "مستضاف", "مأوى موقت", "ملك"])
        selected_committee = c9.selectbox("اللجنة المشرفة / التابع لها", COMMITTEES)
        
        notes = st.text_area("ملاحظات إضافية أو احتياجات خاصة")
        
        submit = st.form_submit_button("💾 حفظ الاستمارة")
        if submit:
            if full_name and form_id:
                new_data = {
                    "رقم الاستمارة": form_id, "الاسم الكامل": full_name,
                    "رقم الهوية": national_id, "رقم الهاتف": phone,
                    "المحافظة الأصلية": orig_gov, "المديرية": orig_dir,
                    "عدد أفراد الأسرة": family_members, "حالة السكن": housing_status,
                    "اللجنة التابعة": selected_committee,
                    "ملاحظات": notes
                }
                df = pd.read_excel(EXCEL_FILE)
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                st.success(f"تم حفظ استمارة الأخ/ت ({full_name}) وتوجيهها إلى ({selected_committee}) بنجاح!")
            else:
                st.error("يرجى تعبئة الحقول الأساسية.")

elif choice == "🔍 عرض استمارات النازحين":
    st.title("🔍 عرض وإدارة كافة استمارات النازحين")
    df = pd.read_excel(EXCEL_FILE)
    if df.empty:
        st.warning("لا توجد استمارات مسجلة حالياً.")
    else:
        st.dataframe(df, use_container_width=True)

elif choice == "🏢 إدارة اللجان المتخصصة":
    st.title("🏢 اللجان الرسمية التابعة لملتقى أبناء مديرية جبلة")
    st.info("قسم مخصص لعرض وتصنيف البيانات والمهام حسب اللجان التابعة للملتقى.")
    
    # عرض اللجان الخمس في بطاقات
    cols = st.columns(3)
    for i, comm in enumerate(COMMITTEES):
        with cols[i % 3]:
            st.markdown(f"### 📌 {comm}")
            df = pd.read_excel(EXCEL_FILE)
            count = len(df[df['اللجنة التابعة'] == comm]) if 'اللجنة التابعة' in df.columns else 0
            st.metric("عدد الاستمارات والمرتبطين", f"{count} معني")

elif choice == "✏️ تعديل بيانات الاستمارات":
    st.title("✏️ تعديل بيانات الاستمارات المسجلة")
    st.info("قسم مخصص لمدير النظام لتعديل أو تحديث الاستمارات.")

elif choice == "📦 توزيع السلال الغذائية":
    st.title("📦 إدارة توزيع السلال الغذائية (اللجنة الاجتماعية)")
    st.info("تسجيل وقيد السلال الموزعة للمستفيدين.")

elif choice == "🤝 إدارة الكفالات والرعايات":
    st.title("🤝 إدارة كفالات الأسر والأيتام والرعايات")
    st.info("سجل الكفلاء والمستفيدين من الرعايات الشهرية.")

elif choice == "📁 الأرشيف والمستندات":
    st.title("📁 الأرشيف الرقمي والمستندات (اللجنة الإعلامية/القانونية)")
    st.info("رفع وأرشفة وثائق الاستمارات والهويات.")

elif choice == "💰 الصندوق والحسابات (الوارد والمنصرف)":
    st.title("💰 إدارة الصندوق المالية (اللجنة المالية)")
    st.info("تسجيل المقبوضات والمصروفات المالية الخاصة بالملتقى.")

elif choice == "👥 إدارة القوى البشرية والكادر":
    st.title("👥 إدارة القوى البشرية وكادر الملتقى (اللجنة العسكرية/الإدارية)")
    st.info("سجل الأعضاء واللجان العاملة في المديرية.")

elif choice == "🔐 إدارة المستخدمين وكلمات المرور":
    st.title("🔐 إدارة حسابات المستخدمين والتصاريح")
    st.info("إضافة مستخدمين جديد وتغيير كلمات المرور.")

elif choice == "📥 تصدير التقارير (Excel)":
    st.title("📥 تصدير البيانات والتقارير الشاملة")
    df = pd.read_excel(EXCEL_FILE)
    st.download_button(
        label="📥 تحميل كافة البيانات بملف Excel",
        data=open(EXCEL_FILE, "rb").read(),
        file_name="استمارات_ملتقى_جبلة.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

