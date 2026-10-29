import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components
import base64
import json

# ==================================================
# 1. 기본 설정
# ==================================================

st.set_page_config(
    page_title="MicroMap | 학교 미생물 분포 지도",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent


# ==================================================
# 2. 디자인
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAF8;
    color: #111111;
}

h1, h2, h3, h4 {
    color: #263D35 !important;
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #263D35 !important;
    letter-spacing: -1px;
}

.subtitle {
    color: #52645A !important;
    margin-bottom: 24px;
    font-size: 15px;
}

.info-box {
    background-color: #EAF1EC;
    padding: 22px;
    border-radius: 16px;
    color: #111111 !important;
    line-height: 1.8;
}

.info-box * {
    color: #111111 !important;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E2EAE4;
}

[data-testid="stMetric"] *,
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] * {
    color: #111111 !important;
    opacity: 1 !important;
}

[data-testid="stMainBlockContainer"] p {
    color: #111111;
}

[data-testid="stSidebar"] {
    background-color: #252831;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-baseweb="select"] * {
    color: #111111 !important;
}

[data-testid="stImage"] img {
    border-radius: 12px;
}

.legend-box {
    background: white;
    border: 1px solid #E2EAE4;
    padding: 18px;
    border-radius: 14px;
    line-height: 2;
    color: #111111;
}

.criteria-box {
    background-color: #F0F4F1;
    border-left: 5px solid #718D7B;
    padding: 20px;
    border-radius: 10px;
    line-height: 1.9;
    color: #111111;
}

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


# ==================================================
# 3. 데이터 불러오기
# ==================================================

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
    st.error("data.csv 파일을 불러올 수 없습니다.")
    st.exception(e)
    st.stop()


required_columns = [
    "조사장소",
    "배지번호",
    "집락수",
    "주요색깔",
    "관찰특징",
    "동정후보"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "data.csv에 필요한 열이 없습니다: "
        + ", ".join(missing_columns)
    )
    st.stop()


locations = df["조사장소"].tolist()


# ==================================================
# 4. 이미지 설정
# ==================================================

sample_images = {
    "sample1": "images/sample1.jpg",
    "sample2": "images/sample2.jpg",
    "sample3": "images/sample3.jpg"
}


def find_school_map():

    for name in [
        "school_map.png",
        "school_map.PNG",
        "school_map.jpg",
        "school_map.JPG",
        "school_map.jpeg",
        "school_map.JPEG"
    ]:

        path = BASE_DIR / name

        if path.exists():
            return path

    return None


def show_image(relative_path):

    path = BASE_DIR / relative_path

    if not path.exists():
        st.warning(f"이미지가 없습니다: {relative_path}")
        return

    try:
        st.image(
            str(path),
            use_container_width=True
        )

    except Exception:
        st.error("이미지를 표시할 수 없습니다.")


# ==================================================
# 5. 색상 분류
# ==================================================

def get_colony_category(location):

    selected = df[df["조사장소"] == location]

    if selected.empty:
        return "unknown"

    count_text = str(
        selected.iloc[0]["집락수"]
    ).replace(" ", "")

    if (
        "계수어려움" in count_text
        or "계수불가" in count_text
        or "측정불가" in count_text
    ):
        return "unknown"

    if "20~30" in count_text:
        return "high"

    if "10~20" in count_text:
        return "medium"

    if "3~5" in count_text:
        return "low"

    return "unknown"


CATEGORY_INFO = {
    "high": {
        "color": "#E35D5B",
        "label": "집락 수 많음",
        "symbol": "🔴"
    },
    "medium": {
        "color": "#E7B94B",
        "label": "집락 수 중간",
        "symbol": "🟡"
    },
    "low": {
        "color": "#5DAA79",
        "label": "집락 수 적음",
        "symbol": "🟢"
    },
    "unknown": {
        "color": "#8B9690",
        "label": "계수 어려움",
        "symbol": "⚪"
    }
}


def get_colony_symbol(location):

    category = get_colony_category(location)

    return CATEGORY_INFO[category]["symbol"]


# ==================================================
# 6. 색상 기준 설명
# ==================================================

def show_color_criteria():

    st.markdown("### 🎨 미생물 분포 색상 기준")

    st.markdown("""
    <div class="legend-box">

    🔴 <b>빨강 — 집락 수 많음</b><br>
    약 20개 이상 관찰된 경우

    <br><br>

    🟡 <b>노랑 — 집락 수 중간</b><br>
    약 10~19개 관찰된 경우

    <br><br>

    🟢 <b>초록 — 집락 수 적음</b><br>
    약 9개 이하 관찰된 경우

    <br><br>

    ⚪ <b>회색 — 계수 어려움</b><br>
    집락이 겹치거나 넓게 퍼져
    정확한 개수 확인이 어려운 경우

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="criteria-box">

    <b>🔬 색상 분류의 과학적 기준</b>

    <br><br>

    본 지도는 배지에서 관찰된
    <b>미생물 집락 수</b>를 기준으로
    조사 장소를 구분한 시각화 자료입니다.

    <br><br>

    빨강·노랑·초록의 경계값은
    이번 탐구 결과를 비교하기 위해 설정한
    <b>프로젝트 자체 분류 기준</b>이며,
    공식적인 미생물 안전 기준은 아닙니다.

    <br><br>

    <b>⚠️ 색상은 인체 유해성이나
    감염 위험도를 의미하지 않습니다.</b>

    <br><br>

    집락 수가 많더라도 반드시
    병원성 미생물이 많다는 뜻은 아니며,
    집락 수가 적다고 해서
    안전한 장소라고 단정할 수도 없습니다.

    <br><br>

    시료 채취 면적과 배양 조건 등에 따라
    집락 수가 달라질 수 있으므로
    장소 간 차이를 해석할 때 주의가 필요합니다.

    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 7. 장소별 상세 결과
# ==================================================

def show_location_result(location):

    selected = df[df["조사장소"] == location]

    if selected.empty:
        st.warning("관찰 데이터가 없습니다.")
        return

    row = selected.iloc[0]

    category = get_colony_category(location)

    info = CATEGORY_INFO[category]

    st.subheader(
        f"{info['symbol']} {location}"
    )

    st.caption(
        f"집락 수 분류: {info['label']} "
        "| 인체 유해성 판정 아님"
    )

    col1, col2 = st.columns([1.1, 1])

    with col1:

        st.markdown("#### 🧫 실제 배지 사진")

        sample = row["배지번호"]

        image_path = sample_images.get(sample)

        if image_path:
            show_image(image_path)

        st.caption(
            "하나의 배지를 여러 조사 구역으로 "
            "나누어 사용했습니다. "
            "사진에서 해당 구역을 확인해 주세요."
        )

    with col2:

        st.markdown("#### 🔬 관찰 결과")

        st.write(f"**배지 번호:** {row['배지번호']}")
        st.write(f"**집락 수:** {row['집락수']}")
        st.write(f"**주요 색깔:** {row['주요색깔']}")
        st.write(f"**관찰 특징:** {row['관찰특징']}")

        st.divider()

        st.markdown("#### 🧬 미생물 동정 후보")

        st.write(row["동정후보"])

        st.info(
            "동정 후보는 집락 외형을 바탕으로 "
            "고려한 것으로, 실제 미생물의 "
            "종이 확인된 것은 아닙니다."
        )


# ==================================================
# 8. 지도 마커 위치
# ==================================================

# 평면도 이미지에 대한 백분율 좌표
# 정확한 채취 지점이 아닌 대략적인 초기 위치

MAP_POSITIONS = {

    "보건실": (28.5, 38.5),

    "중앙현관 손잡이": (67.0, 46.5),

    "중앙현관 우산꽂이": (70.5, 48.0),

    "1층 중앙현관 옆 거울": (65.5, 51.0),

    "학습도움실 문손잡이": (23.5, 84.5),

    "준비실 서랍장": (37.5, 84.5),

    "화장실 변기": (6.5, 33.0),

    "남자화장실 손잡이": (9.0, 30.0)

}


# ==================================================
# 9. 이미지를 HTML에서 표시할 수 있도록 변환
# ==================================================

@st.cache_data
def encode_image(path_string):

    path = Path(path_string)

    suffix = path.suffix.lower()

    if suffix in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "image/png"

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


# ==================================================
# 10. 클릭 가능한 지도 + 배지 사진
# ==================================================

def show_interactive_map():

    map_path = find_school_map()

    if map_path is None:
        st.warning("학교 평면도 파일을 찾을 수 없습니다.")
        return

    map_image_data = encode_image(str(map_path))

    marker_data = []

    for location, position in MAP_POSITIONS.items():

        selected = df[df["조사장소"] == location]

        if selected.empty:
            continue

        row = selected.iloc[0]

        category = get_colony_category(location)

        info = CATEGORY_INFO[category]

        sample = str(row["배지번호"])

        sample_path = sample_images.get(sample)

        sample_image_data = ""

        if sample_path:

            full_path = BASE_DIR / sample_path

            if full_path.exists():

                sample_image_data = encode_image(
                    str(full_path)
                )

        marker_data.append({
            "location": location,
            "x": position[0],
            "y": position[1],
            "color": info["color"],
            "category": info["label"],
            "count": str(row["집락수"]),
            "sample": sample,
            "sample_image": sample_image_data,
            "main_color": str(row["주요색깔"]),
            "features": str(row["관찰특징"]),
            "candidates": str(row["동정후보"])
        })

    markers_json = json.dumps(
        marker_data,
        ensure_ascii=False
    ).replace("<", "\\u003c")

    map_html = """
    <div class="map-app">

        <div class="map-container" id="map-container">

            <img
                class="floor-map"
                src="__MAP_IMAGE__"
                alt="학교 1층 평면도"
            >

            <div id="markers"></div>

        </div>

        <div class="map-help">
            ● 색깔 원을 누르면 해당 장소의
            실제 배지 사진과 관찰 결과가 나타납니다.
            <br>
            ● 마커 위치는 평면도를 기준으로 한
            대략적인 위치입니다.
        </div>

        <div class="result-card" id="result-card">

            <div class="result-title">
                📍 조사 장소를 선택하세요
            </div>

            <div class="result-body">
                지도 위의 색깔 원을 누르면
                해당 장소의 배지 사진과
                미생물 관찰 결과를 확인할 수 있습니다.
            </div>

        </div>

    </div>

    <style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Apple SD Gothic Neo",
            sans-serif;
        color: #111111;
        background: #F8FAF8;
    }

    .map-app {
        width: 100%;
    }

    .map-container {
        position: relative;
        width: 100%;
        border-radius: 14px;
        overflow: hidden;
        background: white;
        border: 1px solid #E0E7E1;
    }

    .floor-map {
        display: block;
        width: 100%;
        height: auto;
    }

    .marker {
        position: absolute;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        border: 3px solid white;
        transform: translate(-50%, -50%);
        cursor: pointer;
        box-shadow: 0 1px 6px #00000055;
        z-index: 5;
        padding: 0;
    }

    .marker:focus-visible {
        outline: 3px solid #263D35;
        outline-offset: 3px;
    }

    .marker.active {
        border: 3px solid #263D35;
        width: 27px;
        height: 27px;
        z-index: 10;
    }

    .map-help {
        padding: 12px 4px;
        font-size: 13px;
        color: #52645A;
        line-height: 1.8;
    }

    .result-card {
        background: white;
        border: 1px solid #DFE7E1;
        border-radius: 14px;
        padding: 20px;
        margin-top: 8px;
    }

    .result-title {
        font-size: 20px;
        font-weight: 750;
        color: #263D35;
        margin-bottom: 15px;
    }

    .result-body {
        font-size: 14px;
        line-height: 1.9;
        color: #111111;
        overflow-wrap: anywhere;
    }

    .result-row {
        margin-bottom: 8px;
    }

    .result-label {
        font-weight: 700;
        color: #263D35;
    }

    .sample-photo {
        display: block;
        width: 100%;
        max-width: 650px;
        height: auto;
        border-radius: 12px;
        margin-top: 12px;
        border: 1px solid #E0E7E1;
    }

    .photo-title {
        margin-top: 18px;
        font-size: 16px;
        font-weight: 700;
        color: #263D35;
    }

    .photo-caption {
        font-size: 12px;
        color: #52645A;
        line-height: 1.7;
        margin-top: 8px;
    }

    .caution {
        background: #F0F4F1;
        border-radius: 8px;
        padding: 12px;
        margin-top: 15px;
        font-size: 12px;
        line-height: 1.8;
    }

    @media (max-width: 500px) {

        .marker {
            width: 19px;
            height: 19px;
        }

        .marker.active {
            width: 24px;
            height: 24px;
        }

        .result-card {
            padding: 15px;
        }

    }

    </style>

    <script>

    const markers = __MARKERS_JSON__;

    const markerContainer =
        document.getElementById("markers");

    const resultCard =
        document.getElementById("result-card");

    function escapeHtml(value) {

        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");

    }

    function selectMarker(marker, button) {

        document.querySelectorAll(".marker")
            .forEach(item => {
                item.classList.remove("active");
            });

        button.classList.add("active");

        let photoHtml = "";

        if (marker.sample_image) {

            photoHtml = `
                <div class="photo-title">
                    🧫 실제 배지 사진
                </div>

                <img
                    class="sample-photo"
                    src="${marker.sample_image}"
                    alt="${escapeHtml(marker.location)}가 포함된 배지 사진"
                >

                <div class="photo-caption">
                    배지 번호: ${escapeHtml(marker.sample)}
                    <br>
                    하나의 배지를 여러 조사 구역으로
                    나누어 사용했습니다.
                    사진에서 해당 장소의 구역을
                    확인해 주세요.
                </div>
            `;

        } else {

            photoHtml = `
                <div class="photo-caption">
                    연결된 배지 사진을 찾을 수 없습니다.
                </div>
            `;

        }

        resultCard.innerHTML = `
            <div class="result-title">
                📍 ${escapeHtml(marker.location)}
            </div>

            <div class="result-body">

                <div class="result-row">
                    <span class="result-label">
                        집락 수 분류:
                    </span>
                    ${escapeHtml(marker.category)}
                </div>

                <div class="result-row">
                    <span class="result-label">
                        관찰된 집락 수:
                    </span>
                    ${escapeHtml(marker.count)}
                </div>

                <div class="result-row">
                    <span class="result-label">
                        주요 색깔:
                    </span>
                    ${escapeHtml(marker.main_color)}
                </div>

                <div class="result-row">
                    <span class="result-label">
                        관찰 특징:
                    </span>
                    ${escapeHtml(marker.features)}
                </div>

                <div class="result-row">
                    <span class="result-label">
                        미생물 동정 후보:
                    </span>
                    ${escapeHtml(marker.candidates)}
                </div>

                ${photoHtml}

                <div class="caution">
                    ⚠️ 이 색상은 관찰된 집락 수에 따른
                    분류이며 인체 유해성이나
                    감염 위험도를 의미하지 않습니다.
                    동정 후보도 확정된 결과가 아닙니다.
                </div>

            </div>
        `;

        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    }

    markers.forEach(marker => {

        const button =
            document.createElement("button");

        button.type = "button";

        button.className = "marker";

        button.style.left = marker.x + "%";
        button.style.top = marker.y + "%";
        button.style.backgroundColor = marker.color;

        button.title = marker.location;

        button.setAttribute(
            "aria-label",
            marker.location + " 관찰 결과 보기"
        );

        button.addEventListener("click", () => {
            selectMarker(marker, button);
        });

        markerContainer.appendChild(button);

    });

    </script>
    """

    map_html = map_html.replace(
        "__MAP_IMAGE__",
        map_image_data
    )

    map_html = map_html.replace(
        "__MARKERS_JSON__",
        markers_json
    )

    components.html(
        map_html,
        height=1350,
        scrolling=True
    )


# ==================================================
# 11. 메인 제목
# ==================================================

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


# ==================================================
# 12. 사이드바
# ==================================================

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


# ==================================================
# 13. 학교 위생 지도
# ==================================================

if menu == "🗺️ 학교 위생 지도":

    st.header("🗺️ 학교 미생물 분포 지도")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "조사 장소",
        f"{len(df)}곳"
    )

    col2.metric(
        "배지 수",
        f"{df['배지번호'].nunique()}개"
    )

    col3.metric(
        "동정 상태",
        "미확정"
    )

    st.divider()

    show_color_criteria()

    st.divider()

    st.markdown("### 🗺️ 학교 1층 미생물 관찰 지도")

    st.caption(
        "평면도 위 색깔 마커를 누르면 "
        "해당 장소의 실제 배지 사진과 "
        "관찰 결과를 확인할 수 있습니다."
    )

    show_interactive_map()

    st.info(
        "지도에 표시된 위치는 평면도를 기준으로 한 "
        "대략적인 위치입니다. 정확한 채취 지점이 "
        "확인되지 않은 장소는 지도 아래 목록에서 "
        "확인할 수 있습니다."
    )

    st.divider()

    st.markdown("### 📍 전체 조사 장소별 관찰 결과")

    selected_location = st.selectbox(
        "조사 장소 선택",
        locations,
        format_func=lambda x:
            f"{get_colony_symbol(x)} {x}"
    )

    show_location_result(selected_location)


# ==================================================
# 14. 배지 관찰 갤러리
# ==================================================

elif menu == "🧫 배지 관찰 갤러리":

    st.header("🧫 배지 관찰 갤러리")

    sample = st.selectbox(
        "배지 선택",
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
            f"• {get_colony_symbol(location)} {location}"
        )

    st.info(
        "집락의 외형만으로 미생물의 종이나 "
        "병원성을 확정할 수 없습니다."
    )


# ==================================================
# 15. 미생물 동정 결과
# ==================================================

elif menu == "🔬 미생물 동정 결과":

    st.header("🔬 미생물 관찰 및 동정 후보")

    selected_location = st.selectbox(
        "조사 장소 선택",
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


# ==================================================
# 16. 데이터 분석
# ==================================================

elif menu == "📊 데이터 분석":

    st.header("📊 미생물 관찰 데이터 분석")

    st.subheader("🎨 집락 수 분류 결과")

    category_counts = {
        "많음": 0,
        "중간": 0,
        "적음": 0,
        "계수 어려움": 0
    }

    for location in locations:

        category = get_colony_category(location)

        if category == "high":
            category_counts["많음"] += 1

        elif category == "medium":
            category_counts["중간"] += 1

        elif category == "low":
            category_counts["적음"] += 1

        else:
            category_counts["계수 어려움"] += 1

    chart_df = pd.DataFrame({
        "분류": list(category_counts.keys()),
        "조사 장소 수": list(category_counts.values())
    })

    st.bar_chart(
        chart_df.set_index("분류")
    )

    st.caption(
        "이 그래프는 집락 수 분류별 "
        "조사 장소의 개수를 나타냅니다."
    )

    st.divider()

    st.subheader("📋 조사 장소별 집락 수")

    st.dataframe(
        df[["조사장소", "집락수"]],
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "일부 장소는 집락이 겹치거나 넓게 퍼져 "
        "정확한 계수가 어렵습니다. "
        "장소별 집락 수를 동일한 조건에서 측정한 "
        "정량적 결과로 해석해서는 안 됩니다."
    )

    st.divider()

    st.subheader("🧫 배지별 조사 장소 수")

    counts = (
        df.groupby("배지번호")
        .size()
        .reset_index(name="조사 장소 수")
    )

    st.bar_chart(
        counts.set_index("배지번호")
    )


# ==================================================
# 17. 프로젝트 소개
# ==================================================

elif menu == "📋 프로젝트 소개":

    st.header("📋 MicroMap 프로젝트")

    st.subheader("🎯 연구 목적")

    st.write(
        "학교 내 다양한 장소에서 채취한 시료의 "
        "미생물 집락을 관찰하고, "
        "장소별 분포와 형태적 특징을 "
        "시각화하는 것을 목적으로 합니다."
    )

    st.divider()

    st.subheader("🔬 연구 과정")

    steps = [
        "학교 내 조사 장소 선정",
        "시료 채취 및 배양",
        "집락 수와 형태적 특징 관찰",
        "미생물 동정 후보 정리",
        "MicroMap 데이터베이스 구축",
        "학교 평면도 기반 분포 시각화",
        "장소별 관찰 결과 비교 및 한계 분석"
    ]

    for i, step in enumerate(steps, 1):
        st.write(f"{i}. {step}")

    st.divider()

    show_color_criteria()

    st.divider()

    st.subheader("📌 연구의 한계")

    st.write(
        "집락의 색깔과 형태만으로 미생물의 "
        "종이나 병원성을 확인할 수 없습니다."
    )

    st.write(
        "또한 집락 수는 채취 면적, 채취 방법, "
        "배양 조건 등에 따라 달라질 수 있으므로 "
        "실제 환경의 미생물 총량을 정확하게 "
        "나타내지 않을 수 있습니다."
    )

    st.write(
        "따라서 지도에서 사용하는 색상은 "
        "관찰된 집락 수를 구분하기 위한 것이며 "
        "인체 유해성이나 감염 위험도를 "
        "나타내는 지표가 아닙니다."
    )


# ==================================================
# 18. 하단
# ==================================================

st.divider()

st.caption(
    "MicroMap | School Microbial Distribution Project"
)
