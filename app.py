import streamlit as st
import numpy as np
from functools import reduce
from operator import mul
import pandas as pd

st.title("🎲 로또 조합 생성기")

# 6개 칸 입력 위젯
cols = st.columns(6)
inputs = []
for i in range(6):
    with cols[i]:
        input_str = st.text_input(
            f"{i+1}번째 숫자",
            placeholder="쉼표로 구분 (예: 1,5,10)",
            key=f"col_{i}"
        )
        try:
            numbers = sorted({int(n.strip()) for n in input_str.split(',') if n.strip()})
        except:
            numbers = []
        inputs.append(numbers)

# 최대 조합 수 계산
if all(len(col) > 0 for col in inputs):
    max_combinations = reduce(mul, [len(col) for col in inputs], 1)
else:
    max_combinations = 0

st.info(f"🎲 최대 조합 수: **{max_combinations:,}개**")

count = st.number_input(
    "생성할 조합 수",
    min_value=1,
    max_value=10000,
    value=5
)

if 'selections' not in st.session_state:
    st.session_state.selections = []

if st.button("🎲 번호 생성하기", use_container_width=True):
    if max_combinations == 0:
        st.error("❗모든 칸에 숫자를 입력해주세요!")
    else:
        valid_combos = []
        attempt = 0
        max_attempts = count * 10

        while len(valid_combos) < count and attempt < max_attempts:
            combo = tuple(sorted([np.random.choice(col) for col in inputs]))
            if combo not in valid_combos:
                valid_combos.append(combo)
            attempt += 1

        st.session_state.selections = valid_combos
        st.success(f"✅ {len(valid_combos)}개 조합 생성")

if st.session_state.selections:
    df = pd.DataFrame(
        st.session_state.selections,
        columns=[f"row {i+1}" for i in range(6)]
    )

    st.dataframe(df, height=400)  # 포맷팅 없이 자연스럽게 표시

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name="lotto_combinations.csv",
        mime="text/csv",
        use_container_width=True
    )
