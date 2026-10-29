import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# 1. 기본 설정
# ==========================================

st.set_page_config(
    page_title="MicroMap | 학교 미생물 분포 지도",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# 2. 디자인 설정
# ==========================================

st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #F8FAF8;
    color: #111111;
}

/* 제목 */
h1, h2, h3, h4 {
    color: #263D35 !important;
}

/* MicroMap 메인 제목 */
.main-title {
    font-size: 44px;
    font-weight: 800;
    color: #263D35 !important;
    letter-spacing: -1px;
}

/* 영어 부제목 */
.subtitle {
    color: #52645A !important;
    margin-bottom: 24px;
    font-size: 15px;
}

/* 프로젝트 소개 박스 */
.info-box {
    background-color: #EAF1EC;
    padding: 22px;
    border-radius: 15px;
    color: #111111 !important;
    font-weight: 500;
    line-height: 1.8;
    font-size: 15px;
}

/* 소개 박스 내부 글씨 */
.info-box,
.info-box * {
    color: #111111 !important;
    opacity: 1 !important;
}

/* 조사 장소, 배지 수, 동정 상태 카드 */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 13px;
    border: 1px solid #E2EAE4;
}

/* 카드 제목 */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p {
    color: #111111 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* 카드 숫자 */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div {
    color: #111111 !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* 카드 내부 텍스트 */
[data-testid="stMetric"] p,
[data-testid="stMetric"] span,
[data-testid="stMetric"] div {
    color: #111111 !important;
    opacity: 1 !important;
}

/* 일반 본문 */
[data-testid="stMainBlockContainer"] p {
    color: #111111;
}

/* 선택 박스 */
[data-baseweb="select"] {
    background-color: #FFFFFF;
}

[data-baseweb="select"] * {
    color: #111111 !important;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background-color: #252831;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* 구분선 */
hr {
    border-color: #DFE7E1;
}

/* 이미지 */
[data-testid="stImage"] img {
    border-radius: 12px;
}

/* 표 */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* 모바일 화면 */
@media (max-width: 768px) {

    .main-title {
        font-size: 36px;
    }

    .info-box {
        padding: 16px;
    }

    [data-testid="stMetric"] {
        padding: 12px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 데이터 불러오기
# ==========================================

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


# ==========================================
# 4. 이미지 파일 설정
# ==========================================

sample_images = {
    "sample1": "images/sample1.jpg",
    "sample2": "images/sample2.jpg",
    "sample3": "images/sample3.jpg"
}


# 학교 평면도 파일 자동 검색
def find_school_map():

    possible_names = [
        "school_map.png",
        "school_map.PNG",
        "school_map.jpg",
        "school_map.JPG",
        "school_map.jpeg",
        "school_map.JPEG"
    ]

    for name in possible_names:

        path = BASE_DIR / name

        if path.exists():
            return path

    return None


# 이미지 출력
def show_image(relative_path):

    path = BASE_DIR / relative_path

    if not path.exists():

        st.warning(
            f"이미지 파일을 찾을 수 없습니다: {relative_path}"
        )

        return

    try:

        st.image(
            str(path),
            use_container_width=True
        )

    except Exception:

        st.error(
            f"이미지를 표시할 수 없습니다: {relative_path}"
        )

        st.info(
            "이미지 파일이 실제 JPEG 또는 PNG 형식인지 확인해 주세요."
        )


# ==========================================
# 5. 조사 장소별 관찰 결과 출력
# ==========================================

def show_location_result(location):

    selected_data = df[
        df["조사장소"] == location
    ]

    if selected_data.empty:

        st.warning("해당 장소의 데이터가 없습니다.")
        return

    row = selected_data.iloc[0]

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
            "하나의 배지를 여러 조사 구역으로 나누어 사용했습니다. "
            "사진에 표시된 해당 구역을 확인해 주세요."
        )

    with col2:

        st.markdown("#### 🔬 관찰 결과")

        st.write(
            f"**배지 번호:** {sample}"
        )

        st.write(
            f"**집락 수:** {row['집락수']}"
        )

        st.write(
            f"**주요 색깔:** {row['주요색깔']}"
        )

        st.write(
            f"**관찰 특징:** {row['관찰특징']}"
        )

        st.divider()

        st.markdown("#### 🧬 미생물 동정 후보")

        st.write(
            row["동정후보"]
        )

        st.info(
            "위 미생물 이름은 집락의 외형을 바탕으로 "
            "고려한 후보입니다. 실제 동정이 확인된 "
            "미생물은 아닙니다."
        )


# ==========================================
# 6. 메인 화면
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
학교 내 미생물 집락의 분포와 형태적 특징을
관찰하고 시각화하는 탐구 프로젝트입니다.
</div>
""", unsafe_allow_html=True)

st.write("")


# ==========================================
# 7. 사이드바 메뉴
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

locations = df["조사장소"].tolist()


# ==========================================
# 8. 학교 위생 지도
# ==========================================

if menu == "🗺️ 학교 위생 지도":

    st.header("🗺️ 학교 미생물 분포 지도")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "조사 장소",
            f"{len(df)}곳"
        )

    with col2:
        st.metric(
            "배지 수",
            f"{df['배지번호'].nunique()}개"
        )

    with col3:
        st.metric(
            "동정 상태",
            "미확정"
        )

    st.divider()

    # 학교 평면도
    map_path = find_school_map()

    if map_path:

        try:

            st.image(
                str(map_path),
                use_container_width=True
            )

        except Exception:

            st.error(
                "학교 평면도를 표시할 수 없습니다."
            )

    else:

        st.warning(
            "학교 평면도 파일을 찾을 수 없습니다."
        )

    st.divider()

    st.markdown("### 📍 조사 장소 선택")

    selected_location = st.selectbox(
        "관찰 결과를 확인할 장소",
        locations
    )

    show_location_result(selected_location)


# ==========================================
# 9. 배지 관찰 갤러리
# ==========================================

elif menu == "🧫 배지 관찰 갤러리":

    st.header("🧫 배지 관찰 갤러리")

    sample = st.selectbox(
        "관찰할 배지를 선택하세요",
        list(sample_images.keys())
    )

    st.divider()

    show_image(
        sample_images[sample]
    )

    st.subheader("📍 해당 배지의 조사 장소")

    sample_df = df[
        df["배지번호"] == sample
    ]

    for location in sample_df["조사장소"]:

        st.write(
            f"• {location}"
        )

    st.info(
        "배지 사진만으로 미생물의 종이나 "
        "병원성을 확정할 수 없습니다."
    )


# ==========================================
# 10. 미생물 동정 결과
# ==========================================

elif menu == "🔬 미생물 동정 결과":

    st.header("🔬 미생물 관찰 및 동정 후보")

    selected_location = st.selectbox(
        "조사 장소를 선택하세요",
        locations
    )

    st.divider()

    show_location_result(
        selected_location
    )

    st.divider()

    st.subheader("📋 전체 관찰 데이터")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 11. 데이터 분석
# ==========================================

elif menu == "📊 데이터 분석":

    st.header("📊 미생물 관찰 데이터 분석")

    st.subheader("조사 장소별 집락 수")

    st.dataframe(
        df[
            ["조사장소", "집락수"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "일부 장소는 집락이 서로 겹쳐 "
        "정확한 계수가 어렵습니다. "
        "따라서 전체 장소의 집락 수를 "
        "하나의 수치 그래프로 직접 비교하지 않습니다."
    )

    st.divider()

    st.subheader("📊 배지별 조사 장소 수")

    counts = (
        df.groupby("배지번호")
        .size()
        .reset_index(name="조사 장소 수")
    )

    st.bar_chart(
        counts.set_index("배지번호")
    )

    st.caption(
        "이 그래프는 집락 수가 아니라 "
        "각 배지에 포함된 조사 장소 수를 나타냅니다."
    )

    st.divider()

    st.subheader("🔬 장소별 관찰 특징 분석")

    selected_location = st.selectbox(
        "분석할 장소를 선택하세요",
        locations
    )

    row = df[
        df["조사장소"] == selected_location
    ].iloc[0]

    st.write(
        f"**주요 색깔:** {row['주요색깔']}"
    )

    st.write(
        f"**관찰 특징:** {row['관찰특징']}"
    )

    st.write(
        f"**동정 후보:** {row['동정후보']}"
    )


# ==========================================
# 12. 프로젝트 소개
# ==========================================

elif menu == "📋 프로젝트 소개":

    st.header("📋 MicroMap 프로젝트")

    st.subheader("🎯 연구 목적")

    st.write(
        "학교 내 다양한 장소에서 채취한 시료의 "
        "미생물 집락을 관찰하고, 장소별 분포와 "
        "형태적 특징을 시각화하는 것을 목적으로 합니다."
    )

    st.divider()

    st.subheader("🔬 연구 과정")

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

        st.write(
            f"{i}. {step}"
        )

    st.divider()

    st.subheader("📌 연구의 한계")

    st.warning(
        "집락의 색깔과 형태만으로 미생물의 "
        "종이나 병원성을 확인할 수 없습니다. "
        "또한 배양된 집락 수가 해당 장소의 "
        "감염 위험을 직접 나타내지는 않습니다."
    )


# ==========================================
# 13. 하단 정보
# ==========================================

st.divider()

st.caption(
    "MicroMap | School Microbial Distribution Project"
)
