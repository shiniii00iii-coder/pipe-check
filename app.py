import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# ... 상단 설정 동일 ...

if submit:
    try:
        # 기존 데이터를 먼저 읽어옴 (이건 Public 링크로 가능)
        df = conn.read(worksheet="data")
        
        # 새 데이터 추가
        new_row = pd.DataFrame([{"Date": str(date), "Line": str(line), ...}]) # 모든 필드 채우기
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # 업데이트 시도
        conn.update(worksheet="data", data=updated_df)
        st.success("저장 성공!")
    except:
        st.error("역시나 구글 보안 정책상 '서비스 계정'이 필요해 보입니다.")
