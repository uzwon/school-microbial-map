import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="MicroMap | 학교 미생물 분포 지도",
    page_icon="🦠",
    layout="wide"
)

# 디자인
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
}
.subtitle {
    color: #718078;
    margin-bottom: 24px;
}
.info-box {
    background: #EAF1EC;
    padding: 20px;
    border-radius: 15px;
    color: #263D35;
}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E2EAE4;
}
</style>
""", unsafe_allow_html=True)

# 파일 위치
BASE_DIR = Path(__file__).resolve().parent

# 실제 관찰 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv(
        BASE_DIR / "data.csv",
        encoding="utf-8-sig",
        keep_default_na=False
    )

try:
    df = load_data()
except Exception as e:
    st.error("data.csv 파일을 읽을 수 없습니다.")
    st.exception(e)
    st.stop()

# 배지 이미지
sample_images = {
    "sample1": "images/sample1.jpg",
    "sample2": "images/sample2.jpg",
    "sample3": "images/sample3.jpg"
}

def show_image(relative_path):
    path = BASE_DIR / relative_path

    if not path.exists():
        st.warning(f"이미지 파일이 없습니다: {relative_path}")
        return

    try:
        st.image(str(path), use_container_width=True)
    except Exception:
        st.error(f"이미지를 표시할 수 없습니다: {relative_path}")
        st.info("실제 JPEG 또는 PNG 형식인지 확인해 주세요.")

def show_location_result(location):
    row = df[df["조사장소"] == location].iloc[0]

    st.subheader(f"📍 {location}")

    sample = row["배지번호"]

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown("#### 🧫 실제 배지 사진")
        image_path = sample_images.get(sample)

        if image_path:
            show_image(image_path)
        else:
            st.warning("연결된 배지 사진이 없습니다.")

        st.caption(
            "하나의 배지를 여러 조사 구역으로 나누어 "
            "사용했습니다. 사진에 표시된 해당 구역을 "
            "확인해 주세요."
        )

    with col2:
        st.markdown("#### 🔬 관찰 결과")

        st.write(f"**배지 번호:** {sample}")
        st.write(f"**집락 수:** {row['집락수']}")
        st.write(f"**주요 색깔:** {row['주요색깔']}")
        st.write(f"**관찰 특징:** {row['관찰특징']}")

        st.markdown("#### 🧬 동정 후보")
        st.write(row["동정후보"])

        st.caption(
            "위 미생물 이름은 집락 외형을 바탕으로 "
            "고려한 후보이며, 실제 동정이 확인된 것은 아닙니다."
        )

# 제목
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
학교 내 미생물 집락의 분포와 형태적 특징을
관찰하고 시각화하는 탐구 프로젝트입니다.
</div>
""", unsafe_allow_html=True)

st.write("")

# 메뉴
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

locations = df["조사장소"].tolist()

# 학교 위생 지도
if menu == "🗺️ 학교 위생 지도":

    st.header("🗺️ 학교 미생물 분포 지도")

    c1, c2, c3 = st.columns(3)

    c1.metric("조사 장소", f"{len(df)}곳")
    c2.metric("배지 수", f"{df['배지번호'].nunique()}개")
    c3.metric("동정 상태", "미확정")

    st.divider()

    map_path = BASE_DIR / "school_map.png"

    if map_path.exists():
        show_image("school_map.png")
    else:
        st.warning("학교 평면도 파일을 찾을 수 없습니다.")

    st.divider()

    selected = st.selectbox(
        "📍 조사 장소 선택",
        locations
    )

    show_location_result(selected)

# 배지 갤러리
elif menu == "🧫 배지 관찰 갤러리":

    st.header("🧫 배지 관찰 갤러리")

    sample = st.selectbox(
        "배지 선택",
        list(sample_images.keys())
    )

    show_image(sample_images[sample])

    st.subheader("해당 배지의 조사 장소")

    sample_df = df[df["배지번호"] == sample]

    for location in sample_df["조사장소"]:
        st.write(f"• {location}")

    st.info(
        "배지 사진만으로 미생물의 종이나 "
        "병원성을 확정할 수 없습니다."
    )

# 동정 결과
elif menu == "🔬 미생물 동정 결과":

    st.header("🔬 미생물 관찰 및 동정 후보")

    selected = st.selectbox(
        "조사 장소 선택",
        locations
    )

    show_location_result(selected)

    st.divider()

    st.subheader("전체 관찰 데이터")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# 데이터 분석
elif menu == "📊 데이터 분석":

    st.header("📊 미생물 관찰 데이터 분석")

    st.subheader("조사 장소별 집락 수 기록")

    st.dataframe(
        df[["조사장소", "집락수"]],
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "집락이 겹쳐 정확한 계수가 어려운 장소가 "
        "있으므로 전체 장소의 집락 수를 "
        "하나의 수치 그래프로 직접 비교하지 않습니다."
    )

    st.divider()

    st.subheader("배지별 조사 장소 수")

    counts = (
        df.groupby("배지번호")
        .size()
        .reset_index(name="조사 장소 수")
    )

    st.bar_chart(
        counts.set_index("배지번호")
    )

    st.caption(
        "이 그래프는 집락 수가 아닌 "
        "배지별 조사 장소 수를 나타냅니다."
    )

    st.subheader("주요 관찰 특징")

    selected = st.selectbox(
        "분석할 장소",
        locations
    )

    row = df[df["조사장소"] == selected].iloc[0]

    st.write(f"**주요 색깔:** {row['주요색깔']}")
    st.write(f"**관찰 특징:** {row['관찰특징']}")

# 프로젝트 소개
elif menu == "📋 프로젝트 소개":

    st.header("📋 MicroMap 프로젝트")

    st.subheader("연구 목적")

    st.write(
        "학교 내 다양한 장소에서 채취한 시료의 "
        "미생물 집락을 관찰하고, 장소별 분포와 "
        "형태적 특징을 시각화하는 것을 목적으로 합니다."
    )

    st.subheader("연구 과정")

    steps = [
        "학교 내 조사 장소 선정",
        "시료 채취 및 배양",
        "집락의 형태적 특징 관찰",
        "동정 후보와 관찰 근거 정리",
        "MicroMap 데이터베이스 구축",
        "학교 미생물 분포 시각화",
        "장소별 차이 분석"
    ]

    for i, step in enumerate(steps, 1):
        st.write(f"{i}. {step}")

    st.subheader("연구의 한계")

    st.warning(
        "집락의 색깔과 형태만으로 미생물의 "
        "종이나 병원성을 확인할 수 없습니다. "
        "또한 배양된 집락 수가 해당 장소의 "
        "감염 위험을 직접 나타내지는 않습니다."
    )

st.divider()

st.caption(
    "MicroMap | School Microbial Distribution Project"
)
