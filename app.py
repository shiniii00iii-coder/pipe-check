import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="조관 성적서 입력", page_icon="🏗️")
st.title("🏗️ 조관 중간검사 성적서 입력")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 입력 폼
with st.form("inspection_form", clear_on_submit=True):
    st.subheader("1. 기본 정보")
    col1, col2, col3 = st.columns(3)
    with col1: date = st.date_input("검사일자", datetime.now())
    with col2: line = st.selectbox("라인(호기)", ["조관 1", "조관 2", "조관 3", "조관 4", "조관 5", "조관 6", "조관 7"])
    with col3: worker = st.text_input("검사자", value="신명재")

    st.subheader("2. 제품 규격")
    col4, col5, col6 = st.columns(3)
    with col4: customer = st.text_input("수요가", value="태창철강")
    with col5: lot = st.text_input("스탬프LotNo")
    with col6: spec = st.text_input("제품규격", value="HR 50*50*2.0*6M")
    count = st.number_input("생산수량(본)", min_value=0, step=1)

    st.subheader("3. 주요 검사 및 판정")
    col7, col8, col9 = st.columns(3)
    with col7:
        v1 = st.selectbox("육안_겉모양", ["양호", "불량"])
        v2 = st.selectbox("육안_방청유무", ["양호", "불량"])
    with col8:
        t1 = st.text_input("치수_두께(t)")
        t2 = st.text_input("치수_길이(mm)")
    with col9:
        final_res = st.selectbox("최종 판정", ["합격", "불합격"])
        remarks = st.text_input("비고")

    submit = st.form_submit_button("📋 구글 시트에 저장하기")

if submit:
    try:
        # 모든 필드를 빠짐없이 채운 데이터프레임 생성
        new_row = pd.DataFrame([{
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
        }])

        # 기존 데이터 읽기
        existing_df = conn.read(worksheet="data", ttl=0)
        
        # 새 데이터 합치기
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        
        # 저장 시도
        conn.update(worksheet="data", data=updated_df)
        
        st.success("✅ 성공적으로 저장되었습니다!")
        st.balloons()
    except Exception as e:
        st.error(f"저장 중 에러 발생: {e}")
        st.info("여전히 400 에러나 'Public Spreadsheet' 에러가 난다면, 앞에서 설명드린 '구글 서비스 계정' 설정이 필요합니다.")
