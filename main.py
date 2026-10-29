import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# 1. 기본 설정
# ==========================================

st.set_page_config(
    page_title="MicroMap | 학교 미생물 분포 지도",
    page_icon="🦠",
    layout="wide"
)

# ==========================================
# 2. 디자인
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F8FAF8;
}

h1, h2, h3 {
    color: #263D35;
}

.main-title {
    font-size: 44px;
    font-weight: 800;
    color: #263D35;
    letter-spacing: -1px;
}

.subtitle {
    color: #718078;
    font-size: 16px;
    margin-bottom: 25px;
}

.info-box {
    background-color: #EAF1EC;
    padding: 22px;
    border-radius: 16px;
    color: #263D35;
    margin-bottom: 20px;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E2EAE4;
}

div.stButton > button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 실제 조사 데이터
# ==========================================

# 배지 사진 한 장에 여러 조사 장소가 포함됨

samples = {
    "sample1": {
        "image": "images/sample1.jpg",
        "locations": [
            "남자화장실 손잡이",
            "1층 중앙현관 옆 거울",
            "중앙현관 우산꽂이",
            "학습도움실 문손잡이"
        ]
    },

    "sample2": {
        "image": "images/sample2.jpg",
        "locations": [
            "중앙현관 손잡이",
            "보건실",
            "화장실 변기",
            "3학년 신발장"
        ]
    },

    "sample3": {
        "image": "images/sample3.jpg",
        "locations": [
            "탐구1실 쪽 복도 천장",
            "준비실 서랍장",
            "학습도움실 내부용 실내화"
        ]
    }
}

# 장소와 배지 연결

location_data = {}

for sample_name, sample_info in samples.items():

    for location in sample_info["locations"]:

        location_data[location] = {
            "sample": sample_name,
            "image": sample_info["image"],
            "colony_count": None,
            "morphology": "분석 예정",
            "identification": "미동정"
        }

locations = list(location_data.keys())

# ==========================================
# 4. 공통 함수
# ==========================================

def show_sample_image(image_path):

    path = Path(image_path)

    if path.exists():

        st.image(
            str(path),
            use_container_width=True
        )

    else:

        st.warning(
            f"이미지 파일을 찾을 수 없습니다: {image_path}"
        )


def show_location_result(location):

    data = location_data[location]

    st.subheader(f"📍 {location}")

    st.caption(
        f"연결된 배지: {data['sample']}"
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:

        show_sample_image(data["image"])

        st.caption(
            "사진에 표시된 구역을 확인해 주세요. "
            "하나의 배지에 여러 조사 장소가 포함되어 있습니다."
        )

    with col2:

        st.markdown("### 🔬 미생물 관찰 정보")

        result = pd.DataFrame({
            "분석 항목": [
                "조사 장소",
                "배지 번호",
                "집락 수",
                "집락 형태",
                "미생물 동정 결과"
            ],

            "관찰 결과": [
                location,
                data["sample"],
                "분석 예정",
                data["morphology"],
                data["identification"]
            ]
        })

        st.dataframe(
            result,
            hide_index=True,
            use_container_width=True
        )

        st.info(
            "미생물 동정 결과표가 완성되면 "
            "관찰 정보를 업데이트할 예정입니다."
        )

# ==========================================
# 5. 제목
# ==========================================

st.markdown(
    '<div class="main-title">MicroMap</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'School Microbial Distribution Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
학교 내 다양한 장소에서 관찰된 미생물 집락의
분포와 형태적 특징을 분석하고 시각화하는
학교 미생물 분포 탐구 프로젝트입니다.
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. 사이드바 메뉴
# ==========================================

menu = st.sidebar.radio(
    "MICROMAP",
    [
        "🗺️ 학교 위생 지도",
        "🧫 배지 관찰 갤러리",
        "🔬 미생물 동정 결과",
        "📊 데이터 분석",
        "📋 프로젝트 소개"
    ]
)

# ==========================================
# 7. 학교 위생 지도
# ==========================================

if menu == "🗺️ 학교 위생 지도":

    st.header("🗺️ 학교 미생물 분포 지도")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("조사 장소", f"{len(locations)}곳")

    with col2:
        st.metric("배지 수", f"{len(samples)}개")

    with col3:
        st.metric("동정 진행 상태", "분석 중")

    st.divider()

    map_path = Path("school_map.png")

    if map_path.exists():

        st.image(
            str(map_path),
            caption="학교 1층 평면도",
            use_container_width=True
        )

    else:

        st.warning(
            "학교 평면도 파일을 찾을 수 없습니다."
        )

    st.divider()

    st.subheader("📍 조사 장소 선택")

    selected_location = st.selectbox(
        "미생물 관찰 결과를 확인할 장소",
        locations
    )

    show_location_result(selected_location)

# ==========================================
# 8. 배지 관찰 갤러리
# ==========================================

elif menu == "🧫 배지 관찰 갤러리":

    st.header("🧫 배지 관찰 갤러리")

    st.write(
        "실제 학교 환경에서 채취한 시료의 "
        "배양 결과를 확인할 수 있습니다."
    )

    selected_sample = st.selectbox(
        "배지 선택",
        list(samples.keys())
    )

    sample_info = samples[selected_sample]

    st.subheader(
        f"배지 {selected_sample[-1]}"
    )

    show_sample_image(
        sample_info["image"]
    )

    st.markdown("### 📍 해당 배지의 조사 장소")

    for location in sample_info["locations"]:

        st.write(f"• {location}")

    st.warning(
        "사진에 나타난 집락의 색깔이나 형태만으로 "
        "미생물의 종 또는 병원성을 확정할 수 없습니다."
    )

# ==========================================
# 9. 미생물 동정 결과
# ==========================================

elif menu == "🔬 미생물 동정 결과":

    st.header("🔬 미생물 동정 결과")

    st.write(
        "조사 장소별 미생물 집락의 형태적 특징과 "
        "동정 결과를 확인하는 공간입니다."
    )

    selected_location = st.selectbox(
        "조사 장소",
        locations
    )

    show_location_result(selected_location)

# ==========================================
# 10. 데이터 분석
# ==========================================

elif menu == "📊 데이터 분석":

    st.header("📊 미생물 분포 데이터 분석")

    st.info(
        "동정 결과표가 완성되면 "
        "실제 관찰 데이터를 활용한 "
        "통계 분석 기능이 활성화됩니다."
    )

    st.subheader("현재 조사 현황")

    sample_counts = {
        sample: len(info["locations"])
        for sample, info in samples.items()
    }

    df = pd.DataFrame({
        "배지": list(sample_counts.keys()),
        "조사 장소 수": list(sample_counts.values())
    })

    st.bar_chart(
        df.set_index("배지")
    )

    st.caption(
        "위 그래프는 미생물 집락 수가 아니라 "
        "각 배지에 포함된 조사 장소 수를 나타냅니다."
    )

    st.divider()

    st.subheader("추가 예정 분석")

    st.write("① 장소별 집락 수 비교")
    st.write("② 집락 형태적 다양성 비교")
    st.write("③ 장소별 상대적 집락 분포 분석")

# ==========================================
# 11. 프로젝트 소개
# ==========================================

elif menu == "📋 프로젝트 소개":

    st.header("📋 MicroMap 프로젝트")

    st.subheader("연구 목적")

    st.write(
        "학교 내 여러 장소에서 채취한 시료의 "
        "미생물 배양 결과를 분석하고, "
        "관찰된 집락의 형태적 특징과 "
        "분포 차이를 시각화하는 것을 목적으로 합니다."
    )

    st.subheader("연구 과정")

    steps = [
        "학교 내 조사 장소 선정",
        "시료 채취 및 배양",
        "미생물 집락 관찰",
        "미생물 동정 결과 정리",
        "학교 미생물 분포 지도 제작",
        "장소별 차이 분석",
        "위생 개선 방안 탐색"
    ]

    for i, step in enumerate(steps, 1):

        st.write(f"{i}. {step}")

    st.subheader("연구의 한계")

    st.warning(
        "배양된 미생물 집락의 수와 형태만으로 "
        "해당 장소의 위생 안전성이나 감염 위험을 "
        "직접 판단할 수 없습니다. "
        "본 시스템은 교육 및 탐구 목적으로 제작되었습니다."
    )

# ==========================================
# 12. 하단
# ==========================================

st.divider()

st.caption(
    "MicroMap | School Microbial Distribution Project"
)
