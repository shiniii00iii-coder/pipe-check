import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="조관 성적서 입력", page_icon="🏗️")

st.title("🏗️ 조관 중간검사 성적서 입력 시스템")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 입력 폼
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

# 저장 로직
if submit:
    # 에러 방지를 위해 모든 데이터를 문자열로 변환
    new_row = {
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
    }
    
    try:
        # 기존 데이터를 읽어오되, 오류 방지를 위해 ttl=0 설정
        df = conn.read(worksheet="데이터저장", ttl=0)
        
        # 새 행 추가
        new_data_df = pd.DataFrame([new_row])
        updated_df = pd.concat([df, new_data_df], ignore_index=True)
        
        # [핵심] 시트 업데이트 시 탭 이름을 생략하거나 명시적으로 전달
        # 데이터프레임 전체를 다시 쓸 때 발생하는 인코딩 문제를 피하기 위해 astype(str) 사용
        conn.update(worksheet="데이터저장", data=updated_df.astype(str))
        
        st.success("✅ 성공적으로 저장되었습니다!")
        st.balloons()
    except Exception as e:
        # 에러 메시지 분석을 위해 상세 출력
        st.error(f"저장 중 오류 발생: {e}")
        st.info("팁: 구글 시트의 탭 이름이 '데이터저장'이 맞는지 확인해 주세요.")
