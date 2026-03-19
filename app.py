import streamlit as st
import requests

# 1. ตั้งค่าหน้ากระดาษ
st.set_page_config(
    page_title="LINE Profile Search Tool",
    page_icon="🔍",
    layout="centered"
)

# 2. ส่วนหัวข้อและคำอธิบาย
st.title("🔍 LINE Profile Search Tool R4")
st.markdown("""
เครื่องมือนี้ใช้สำหรับดึงข้อมูลชื่อโปรไฟล์จาก **LINE User ID** โดยคุณต้องมี **Channel Access Token** จาก LINE Developers Console
""")

# 3. ส่วน Input (เว้นว่างไว้ให้ผู้ใช้งานกรอกเองทั้งหมด)
with st.container():
    st.info("💡 กรุณากรอกข้อมูล API ของคุณด้านล่าง")
    
    access_token = st.text_input(
        "1. Channel Access Token (Long-lived)", 
        value="", 
        type="password",
        placeholder="วาง Token ของคุณที่นี่...",
        help="คัดลอกมาจากหน้า Messaging API setting ใน LINE Developers Console"
    )
    
    user_id = st.text_input(
        "2. Target User ID", 
        value="",
        placeholder="Uxxxxxxxxxxxxxxx...",
        help="User ID ของผู้ใช้งานที่ต้องการหาชื่อ (ต้องเป็นเพื่อนกับบอทตัวที่ใช้ Token นี้)"
    )

# 4. ปุ่มทำงาน
if st.button("ค้นหาข้อมูล", type="primary", use_container_width=True):
    if not access_token or not user_id:
        st.error("⚠️ กรุณากรอกทั้ง Access Token และ User ID ให้ครบถ้วน")
    else:
        with st.spinner('กำลังดึงข้อมูลจาก LINE API...'):
            url = f"https://api.line.me/v2/bot/profile/{user_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            try:
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ ค้นพบข้อมูล!")
                    
                    # ส่วนแสดงผล
                    st.divider()
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if data.get('pictureUrl'):
                            st.image(data.get('pictureUrl'), use_column_width=True)
                        else:
                            st.warning("ไม่มีรูปโปรไฟล์")
                            
                    with col2:
                        st.subheader(f"ชื่อ: {data.get('displayName')}")
                        st.text(f"Status: {data.get('statusMessage', '-')}")
                        st.code(f"ID: {user_id}", language="text")
                        
                elif response.status_code == 401:
                    st.error("❌ Token ไม่ถูกต้อง หรือหมดอายุ")
                elif response.status_code == 404:
                    st.error("❌ ไม่พบ User นี้ (ID ผิด หรือยังไม่ได้เพิ่มเพื่อนกับบอท)")
                else:
                    st.error(f"❌ Error {response.status_code}")
                    st.json(response.json())
                    
            except Exception as e:
                st.error(f"⚠️ การเชื่อมต่อผิดพลาด: {e}")

# 5. ส่วนท้าย
st.divider()
st.caption("แอปพลิเคชันนี้ไม่ได้เก็บข้อมูล Token หรือ User ID ของคุณ ข้อมูลจะถูกส่งไปยัง LINE API โดยตรงเท่านั้น")
