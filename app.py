import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정: 가로로 넓게 사용
st.set_page_config(page_title="조관 중간검사 성적서", layout="wide")

st.title("🏗️ 조관 중간검사 성적서 입력 시스템")
st.markdown("---")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 입력 폼 시작
with st.form("inspection_form"):
    # 첫 번째 줄: 기본 정보
    st.subheader("📍 1. 기본 정보")
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        date = st.date_input("검사일자", datetime.now())
    with row1_col2:
        line = st.text_input("라인(호기)")
    with row1_col3:
        worker = st.text_input("검사자")
    
    st.markdown("---")
    
    # 두 번째 줄: 제품 규격 및 수량
    st.subheader("📦 2. 제품 규격")
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        customer = st.text_input("수요가")
    with row2_col2:
        lot = st.text_input("스탬프LotNo")
    with row2_col3:
        spec = st.text_input("제품규격(종류_등급_외경x두께x길이)")
        count = st.number_input("생산수량(본)", min_value=0, step=1)

    st.markdown("---")

    # 세 번째 줄: 검사 항목 (일부 요약)
    st.subheader("🔍 3. 주요 검사 및 판정")
    row3_col1, row3_col2, row3_col3 = st.columns(3)
    with row3_col1:
        v1 = st.selectbox("육안_겉모양", ["양호", "불량"])
        v2 = st.selectbox("육안_방청유무", ["양호", "불량"])
    with row3_col2:
        t1 = st.text_input("치수_두께(t)")
        t2 = st.text_input("치수_길이(mm)")
    with row3_col3:
        final_res = st.selectbox("최종 판정", ["합격", "불합격", "보수"])
        remarks = st.text_input("비고")

    # 저장 버튼
    submit = st.form_submit_button("📋 구글 시트에 저장하기")

# 저장 로직
if submit:
    # 시트의 가로 제목 순서와 데이터 연결
    new_data = pd.DataFrame([{
        "검사일자": date.strftime("%Y-%m-%d"),
        "라인(호기)": line,
        "검사자": worker,
        "수요가": customer,
        "스탬프LotNo": lot,
        "제품규격(종류_등급_외경x두께x길이)": spec,
        "생산수량(본)": count,
        "육안_겉모양": v1,
        "육안_방청유무": v2,
        "치수_두께": t1,
        "치수_길이": t2,
        "판정": final_res,
        "비고": remarks
    }])
    
    try:
        # 기존 시트 데이터 가져오기
        existing_df = conn.read(worksheet="데이터저장", ttl=0)
        # 데이터 합치기
        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
        # 시트에 쓰기
        conn.update(worksheet="데이터저장", data=updated_df.astype(str))
        st.success("✅ 데이터가 구글 시트에 실시간으로 저장되었습니다!")
        st.balloons()
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
