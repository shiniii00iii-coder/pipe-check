import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="조관 성적서 입력", page_icon="🏗️")

st.title("🏗️ 조관 중간검사 성적서 입력 시스템")
st.markdown("데이터를 입력하면 실시간으로 구글 스프레드시트에 저장됩니다.")

# 2. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 입력 폼 시작
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
        spec = st.text_input("제품규격(종류_등급_외경x두께x길이)", value="HR 50*50*2.0*6M")
    
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

# 4. 저장 로직
if submit:
    # 한글 에러 방지를 위해 모든 데이터를 문자열(str)로 강제 변환
    new_data = pd.DataFrame([{
        "검사일자": str(date),
        "라인(호기)": str(line),
        "검사자": str(worker),
        "수요가": str(customer),
        "스탬프LotNo": str(lot),
        "제품규격(종류_등급_외경x두께x길이)": str(spec),
        "생산수량(본)": str(count),
        "육안_겉모양": str(v1),
        "육안_방청유무": str(v2),
        "치수_두께": str(t1),
        "치수_길이": str(t2),
        "판정": str(final_res),
        "비고": str(remarks)
    }])

    try:
        # 데이터 불러오기 (캐시 없이 신선하게)
        existing_data = conn.read(worksheet="데이터저장", ttl=0)
        
        # 기존 데이터와 새 데이터 합치기
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # 저장 시 모든 컬럼을 한 번 더 문자열로 변환 (에러 원천 차단)
        conn.update(worksheet="데이터저장", data=updated_df.astype(str))
        
        st.success("✅ 저장 성공! 구글 시트를 확인하세요.")
        st.balloons()
    except Exception as e:
        st.error(f"⚠️ 저장 중 오류가 발생했습니다: {str(e)}")
        st.info("시트의 탭 이름이 '데이터저장'이 맞는지, 혹은 Secrets 설정이 올바른지 확인해 주세요.")
