import streamlit as st
import requests
import json
from datetime import datetime

# 페이지 설정 및 제목
st.set_page_config(page_title="조관 성적서 입력", page_icon="🏗️", layout="centered")

# --- 설정 (여기에 URL을 붙여넣으세요) ---
WEBAPP_URL = "https://script.google.com/macros/s/AKfycby9p3D_JPaMMjzizySaE5n8-jBzdu3DPK5zn3nnIPIs408XnmySBfnTjMazfGrimT9t/exec"

st.title("🏗️ 조관 중간검사 성적서 입력")
st.markdown("---")

# 폼 시작
with st.form("inspection_form", clear_on_submit=True):
    # 1. 기본 정보
    st.subheader("1. 기본 정보")
    c1, c2, c3 = st.columns(3)
    with c1:
        date = st.date_input("검사일자", datetime.now())
    with c2:
        line = st.selectbox("라인(호기)", ["조관 1", "조관 2", "조관 3", "조관 4", "조관 5", "조관 6", "조관 7"])
    with c3:
        worker = st.text_input("검사자", value="신명재")

    # 2. 제품 규격
    st.subheader("2. 제품 규격")
    c4, c5, c6 = st.columns(3)
    with c4:
        customer = st.text_input("수요가", value="태창철강")
    with c5:
        lot = st.text_input("스탬프LotNo")
    with c6:
        spec = st.text_input("제품규격", value="HR 50*50*2.0*6M")
    
    count = st.number_input("생산수량(본)", min_value=0, step=1)

    # 3. 주요 검사 및 판정
    st.subheader("3. 주요 검사 및 판정")
    c7, c8, c9 = st.columns(3)
    with c7:
        v1 = st.selectbox("육안_겉모양", ["양호", "불량"])
        v2 = st.selectbox("육안_방청유무", ["양호", "불량"])
    with c8:
        t1 = st.text_input("치수_두께(t)")
        t2 = st.text_input("치수_길이(mm)")
    with c9:
        final_res = st.selectbox("최종 판정", ["합격", "불합격"])
        remarks = st.text_input("비고")

    st.markdown("---")
    submit = st.form_submit_button("📋 구글 시트에 저장하기", use_container_width=True)

# 저장 로직
if submit:
    # 전송 데이터 생성
    payload = {
        "Date": str(date),
        "Line": str(line),
        "Worker": str(worker),
        "Customer": str(customer),
        "LotNo": str(lot),
        "Spec": str(spec),
        "Qty": str(count),
        "Visual1": str(v1),
        "Visual2": str(v2),
        "T": str(t1),
        "L": str(t2),
        "Result": str(final_res),
        "Note": str(remarks)
    }

    try:
        # 데이터 전송
        with st.spinner('데이터를 저장 중입니다...'):
            response = requests.post(WEBAPP_URL, data=json.dumps(payload))
        
        if response.text == "Success":
            st.success("✅ 구글 시트에 성공적으로 저장되었습니다!")
            st.balloons()
        else:
            st.error(f"❌ 저장 실패: {response.text}")
            
    except Exception as e:
        st.error(f"🚨 연결 오류 발생: {e}")
