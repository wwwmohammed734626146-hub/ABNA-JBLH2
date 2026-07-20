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

# إنشاء ملف إكسل افتراضي إذا لم يكن موجوداً
if not os.path.exists(EXCEL_FILE):
    df_init = pd.DataFrame(columns=[
        "رقم الاستمارة", "الاسم الكامل", "رقم الهوية", "رقم الهاتف",
        "المحافظة الأصلية", "المديرية", "عدد أفراد الأسرة", "حالة السكن", "ملاحظات"
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
        # حساب المشرف (يمكنك تعديل بيانات الدخول هنا)
        if user_input == "admin" and pass_input == "123456":
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'admin'
            st.session_state['username'] = 'المشرف العام'
            st.sidebar.success("تم تسجيل الدخول كمشرف!")
            st.rerun()
        # حساب مستخدم عادي/مدخل بيانات
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

# بناء قائمة خيارات القائمة الرئيسية بناءً على صلاحية المشرف
menu_options = ["📊 لوحة التحكم الإحصائية", "📝 تعبئة استمارة جديدة"]

# إظهار أداة عرض الاستمارات للمشرف فقط
if st.session_state['logged_in'] and st.session_state['user_role'] == 'admin':
    menu_options.append("🔍 عرض استمارات النازحين")

choice = st.sidebar.radio("القائمة الرئيسية:", menu_options)

# ---------------------------------------------------------
# الصفحة الأولى: لوحة التحكم الإحصائية
# ---------------------------------------------------------
if choice == "📊 لوحة التحكم الإحصائية":
    st.title("📊 لوحة التحكم الموحدة للملتقى")
    st.subheader("الجمهورية اليمنية - ملتقى أبناء مديرية جبلة - اللجنة الاجتماعية")
    st.markdown("---")

    df = pd.read_excel(EXCEL_FILE)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الاستمارات", f"{len(df)} استمارة")

    total_family = df['عدد أفراد الأسرة'].sum() if 'عدد أفراد الأسرة' in df.columns and not df.empty else 0
    col2.metric("إجمالي الأفراد المستفيدين", f"{int(total_family)} فرد")

    col3.metric("السلال الموزعة", "0 سلة")
    col4.metric("رصيد الصندوق الحالي", "0 ر.ي")

# ---------------------------------------------------------
# الصفحة الثانية: تعبئة استمارة جديدة (متاحة للجميع)
# ---------------------------------------------------------
elif choice == "📝 تعبئة استمارة جديدة":
    st.title("📝 استمارة حصر وتجميع بيانات النازحين")
    st.write("يرجى إدخال كافة البيانات المطلوبة بدقة:")

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

        c7, c8 = st.columns(2)
        family_members = c7.number_input("عدد أفراد الأسرة", min_value=1, value=1, step=1)
        housing_status = c8.selectbox("حالة السكن", ["مستأجر", "مستضاف", "مأوى موقت", "ملك"])

        notes = st.text_area("ملاحظات إضافية أو احتياجات خاصة")

        submit = st.form_submit_button("💾 حفظ الاستمارة")

        if submit:
            if full_name and form_id:
                new_data = {
                    "رقم الاستمارة": form_id,
                    "الاسم الكامل": full_name,
                    "رقم الهوية": national_id,
                    "رقم الهاتف": phone,
                    "المحافظة الأصلية": orig_gov,
                    "المديرية": orig_dir,
                    "عدد أفراد الأسرة": family_members,
                    "حالة السكن": housing_status,
                    "ملاحظات": notes
                }

                df = pd.read_excel(EXCEL_FILE)
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=False)
                df.to_excel(EXCEL_FILE, index=False)
                st.success(f"تم حفظ استمارة الأخ/ت ({full_name}) بنجاح!")
            else:
                st.error("يرجى تعبئة الحقول الأساسية (رقم الاستمارة والاسم الكامل).")

# ---------------------------------------------------------
# الصفحة الثالثة: عرض كافة الاستمارات (خاصة بالمشرف فقط)
# ---------------------------------------------------------
elif choice == "🔍 عرض استمارات النازحين":
    st.title("🔍 عرض وإدارة كافة استمارات النازحين")
    st.info("💡 هذه الشاشة مخصصة للمشرف العام فقط، وتوفر البيانات الأصلية الكاملة.")

    df = pd.read_excel(EXCEL_FILE)

    if df.empty:
        st.warning("لا توجد استمارات مسجلة حالياً.")
    else:
        st.subheader("📋 جدول البيانات الكامل المباشر")
        # عرض كافة البيانات المدخلة في الاستمارة الأصلية دون اقتطاع
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("🔎 بطاقة التفاصيل الكاملة لاستمارة محددة")

        # اختيار استمارة لعرض كامل بياناتها بالتفصيل
        search_list = df["الاسم الكامل"].astype(str) + " (استمارة رقم: " + df["رقم الاستمارة"].astype(str) + ")"
        selected_option = st.selectbox("اختر المستفيد لاستعراض بياناته كاملة:", search_list)

        if selected_option:
            selected_idx = search_list[search_list == selected_option].index[0]
            person = df.loc[selected_idx]

            st.write("### 📄 البيانات الأصلية المكتملة:")

            # عرض الحقول في كروت مرتبة
            cols = st.columns(2)
            for i, (col_name, value) in enumerate(person.items()):
                cols[i % 2].write(f"**{col_name}:** {value}")

