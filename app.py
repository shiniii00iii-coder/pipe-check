import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="조관 성적서 입력", page_icon="🏗️")
st.title("🏗️ 조관 중간검사 성적서 입력")

# 아까 복사한 구글 웹 앱 URL을 여기에 넣으세요
WEBAPP_URL = "여러분의_웹앱_URL_주소"

# --- 입력 폼 (이전과 동일) ---
with st.form("inspection_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1: date = st.date_input("검사일자", datetime.now())
    with col2: line = st.selectbox("라인(호기)", ["조관 1", "조관 2", "조관 3", "조관 4", "조관 5", "조관 6", "조관 7"])
    with col3: worker = st.text_input("검사자", value="신명재")
    
    # ... (기타 입력 필드들: customer, lot, spec, count, v1, v2, t1, t2, final_res, remarks) ...

    submit = st.form_submit_button("📋 구글 시트에 저장하기")

if submit:
    # 전송할 데이터 정리
    data = {
        "Date": str(date), "Line": str(line), "Worker": str(worker),
        "Customer": str(customer), "LotNo": str(lot), "Spec": str(spec),
        "Qty": str(count), "Visual1": str(v1), "Visual2": str(v2),
        "T": str(t1), "L": str(t2), "Result": str(final_res), "Note": str(remarks)
    }

    try:
        # 구글 앱스 스크립트로 데이터 전송
        response = requests.post(WEBAPP_URL, data=json.dumps(data))
        
        if response.status_code == 200:
            st.success("✅ 구글 시트에 데이터가 기록되었습니다!")
            st.balloons()
        else:
            st.error("전송 실패 (상태 코드 에러)")
    except Exception as e:
        st.error(f"에러 발생: {e}")
