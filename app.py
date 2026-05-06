import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="조관 성적서 입력", page_icon="🏗️")

st.title("🏗️ 조관 중간검사 성적서 입력 시스템")

# 2. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 입력 폼
with st.form("inspection_form"):
    st.subheader("1. 기본 정보")
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("검사일자", datetime.now())
    with col2:
        line = st.selectbox("라인(호기)", ["조관 1", "조관 2", "조관 3", "조관 4", "조관 5", "조관 6", "조관 7"])
    with col3:
        worker = st.text_input("검사자", value="신명재")

    st.subheader("2. 제품 규격")
    col4, col5, col6 = st.columns(3)
    with col4:
        customer = st.text_input("수요가", value="태창철강")
    with col5:
        lot = st.text_input("스탬프LotNo")
    with col6:
        spec = st.text_input("제품규격", value="HR 50*50*2.0*6M")
    
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

# 4. 저장 로직 (핵심 수정 부분)
if submit:
    try:
        # 데이터 생성 (한글 에러 방지를 위해 컬럼명과 데이터를 최대한 단순화 시도)
        new_data = pd.DataFrame([{
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

        # 1단계: 기존 시트 읽기
        # 만약 여기서 에러가 나면 시트 URL이나 Secrets 설정 문제임
        existing_data = conn.read(worksheet="데이터저장", ttl=0)
        
        # 2단계: 데이터 합치기
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # 3단계: 업데이트 (worksheet 인자를 직접 넣지 않고 시도)
        conn.update(worksheet="데이터저장", data=updated_df)
        
        st.success("✅ 저장 성공! 구글 시트를 확인하세요.")
        st.balloons()
        
    except Exception as e:
        st.error(f"⚠️ 저장 오류 발생: {str(e)}")
        st.warning("도움말: 구글 시트의 첫 번째 행(제목행)이 영어로 되어 있는지 확인해 보세요. (예: Date, Line, Worker...) 한글 제목행에서 인코딩 에러가 발생할 수 있습니다.")
