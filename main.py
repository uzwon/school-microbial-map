import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# 기본 설정
# -----------------------------

st.set_page_config(
    page_title="MicroMap | 학교 미생물 분포 지도",
    page_icon="🦠",
    layout="wide"
)

# -----------------------------
# 디자인
# -----------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F8FAF8;
    }

    h1, h2, h3 {
        color: #263D35;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #263D35;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #718078;
        margin-bottom: 30px;
    }

    .info-box {
        background-color: #EAF1EC;
        padding: 20px;
        border-radius: 15px;
        color: #263D35;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------

st.markdown(
    '<div class="main-title">MicroMap</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">학교 미생물 분포 분석 시스템</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
학교 내 여러 장소에서 관찰된 미생물 집락의
분포와 형태적 특징을 분석하는 프로젝트입니다.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 메뉴
# -----------------------------

menu = st.sidebar.radio(
    "MENU",
    [
        "🗺️ 학교 위생 지도",
        "🔬 미생물 관찰 결과",
        "📊 데이터 분석",
        "📋 프로젝트 소개"
    ]
)

# -----------------------------
# 조사 장소
# -----------------------------

locations = [
    "화장실",
    "복도",
    "계단",
    "보건실",
    "교실",
    "중앙 정원",
    "기타 장소"
]

# -----------------------------
# 학교 지도
# -----------------------------

if menu == "🗺️ 학교 위생 지도":

    st.header("🗺️ 학교 미생물 분포 지도")

    st.write(
        "학교 내 조사 장소를 선택하여 "
        "미생물 관찰 결과를 확인할 수 있습니다."
    )

    map_path = Path("school_map.png")

    if map_path.exists():
        st.image(
            str(map_path),
            caption="학교 1층 평면도",
            use_container_width=True
        )
    else:
        st.warning(
            "학교 평면도 파일을 찾을 수 없습니다. "
            "school_map.png 파일을 확인해 주세요."
        )

    st.divider()

    st.subheader("📍 조사 장소 선택")

    selected_location = st.selectbox(
        "미생물 관찰 결과를 확인할 장소",
        locations
    )

    st.success(f"선택한 장소: {selected_location}")

    st.info(
        "해당 장소의 미생물 관찰 데이터는 "
        "동정 결과표가 완성된 후 연결됩니다."
    )

# -----------------------------
# 미생물 관찰 결과
# -----------------------------

elif menu == "🔬 미생물 관찰 결과":

    st.header("🔬 미생물 관찰 결과")

    st.write(
        "배양된 미생물의 집락 형태와 "
        "관찰 결과를 기록하는 공간입니다."
    )

    selected_location = st.selectbox(
        "조사 장소 선택",
        locations
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("배지 앞면")
        st.info("배지 앞면 사진이 표시될 예정입니다.")

    with col2:
        st.subheader("배지 뒷면")
        st.info("배지 뒷면 사진이 표시될 예정입니다.")

    st.divider()

    st.subheader("미생물 관찰 정보")

    result = pd.DataFrame({
        "분석 항목": [
            "조사 장소",
            "집락 수",
            "집락 색깔",
            "집락 형태",
            "미생물 동정 결과"
        ],
        "관찰 결과": [
            selected_location,
            "분석 예정",
            "분석 예정",
            "분석 예정",
            "미동정"
        ]
    })

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# 데이터 분석
# -----------------------------

elif menu == "📊 데이터 분석":

    st.header("📊 장소별 미생물 분포 분석")

    st.info(
        "동정 결과표가 완성되면 "
        "장소별 집락 수와 형태적 특징을 "
        "그래프로 시각화할 예정입니다."
    )

    st.subheader("분석 예정 항목")

    st.write("① 장소별 미생물 집락 수 비교")
    st.write("② 장소별 집락 형태 다양성 비교")
    st.write("③ 상대적 집락 분포 분석")

# -----------------------------
# 프로젝트 소개
# -----------------------------

elif menu == "📋 프로젝트 소개":

    st.header("📋 MicroMap 프로젝트")

    st.subheader("연구 목적")

    st.write(
        "학교 내 다양한 장소에서 채취한 시료의 "
        "미생물 배양 결과를 분석하고, "
        "장소별 집락 분포를 시각화하여 "
        "학교 환경의 미생물 분포 특성을 탐구합니다."
    )

    st.subheader("연구 과정")

    st.write("1. 학교 내 조사 장소 선정")
    st.write("2. 시료 채취 및 배양")
    st.write("3. 미생물 집락의 형태적 특징 관찰")
    st.write("4. 관찰 결과 데이터 정리")
    st.write("5. 학교 미생물 분포 지도 제작")
    st.write("6. 장소별 차이 분석 및 위생 개선 방안 탐색")

    st.subheader("연구의 한계")

    st.warning(
        "배양된 집락 수만으로 병원성 미생물의 "
        "존재 여부나 감염 위험을 판단할 수 없습니다. "
        "본 프로그램은 미생물 관찰 결과를 "
        "시각화하기 위한 교육용 시스템입니다."
    )

# -----------------------------
# 하단
# -----------------------------

st.divider()

st.caption(
    "MicroMap | School Microbial Distribution Project"
)
