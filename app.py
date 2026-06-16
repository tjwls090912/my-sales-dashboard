# app.py -- 지점 매출 분석 대시보드 (화면)
import streamlit as st
import json
import os
from utils import (total_sales, average_sales, to_grade, grade_to_incentive,
                   quarter_average, quarter_top, grade_distribution,
                   rank_list, achievement_rate)

# 페이지 설정
st.set_page_config(page_title="지점 매출 분석 대시보드", layout="wide")

# 로컬 JSON 파일명 설정 (영구 저장용 데이터베이스 역할)
DB_FILE = "branches.json"

# 데이터 로드 함수
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # 파일이 없거나 오류 발생 시 기본 샘플 데이터 제공 후 자동 저장
    default_data = [
        {"지점": "강남점", "1분기": 150, "2분기": 130, "3분기": 140},
        {"지점": "홍대점", "1분기": 90,  "2분기": 110, "3분기": 100},
        {"지점": "판교점", "1분기": 120, "2분기": 100, "3분기": 95},
        {"지점": "부산점", "1분기": 80,  "2분기": 90,  "3분기": 85},
        {"지점": "대전점", "1분기": 50,  "2분기": 55,  "3분기": 45},
    ]
    save_data(default_data)
    return default_data

# 데이터 저장 함수
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 고급스러운 다크/글래스모피즘 테마 스타일링 적용 (글자색 흰색 강조)
st.markdown("""
<style>
    /* 폰트 및 기본 다크 테마 배경 */
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #0b0f19;
        color: #ffffff !important;
    }
    
    /* 일반 텍스트, 설명, 목록 등을 모두 선명한 흰색으로 강제 오버라이드 */
    [data-testid="stMarkdownContainer"] p, 
    [data-testid="stMarkdownContainer"] span, 
    [data-testid="stMarkdownContainer"] li, 
    label, 
    span {
        color: #ffffff !important;
    }
    
    /* 타이틀 그라데이션 */
    h1 {
        font-family: 'Pretendard', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        font-weight: 700;
        color: #ffffff !important;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    /* 프리미엄 요약 카드 디자인 (지점 수, 평균, 달성률) */
    div[data-testid="metric-container"] {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border-color: rgba(96, 165, 250, 0.5);
        box-shadow: 0 12px 40px -10px rgba(96, 165, 250, 0.25);
    }
    
    div[data-testid="stMetricValue"] > div {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -1px;
    }
    
    div[data-testid="stMetricLabel"] > label {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff !important; /* 메트릭 레이블 흰색으로 선명하게 */
        letter-spacing: 0.5px;
    }
    
    /* 커스텀 탭 스타일링 */
    div[data-testid="stTabs"] {
        background: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 25px;
    }
    
    div[data-testid="stTabs"] button {
        font-size: 16px;
        font-weight: 600;
        color: #cbd5e1 !important; /* 비활성 탭 글자도 연회색으로 더 밝게 */
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease;
        padding: 12px 24px;
    }
    
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #60a5fa !important; /* 활성 탭 글자 강조색 */
        font-weight: 700;
        border-bottom: 2px solid #60a5fa !important;
    }
    
    /* 입력 필드 */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        background-color: #111827;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 14px;
    }
    
    div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
    }
    
    /* 추가 버튼 */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff !important;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
    }
    
    /* 테이블 스타일 */
    div[data-testid="stTable"] table {
        background-color: rgba(17, 24, 39, 0.5);
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    div[data-testid="stTable"] th {
        background-color: rgba(31, 41, 55, 0.8) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 14px 16px !important;
    }
    
    div[data-testid="stTable"] td {
        padding: 12px 16px !important;
        color: #ffffff !important; /* 테이블 셀 텍스트 흰색 */
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. 상단 배너 이미지
st.image("banner.png", width="stretch")
st.title("지점 매출 분석 대시보드")

QUARTERS = ["1분기", "2분기", "3분기"]

# 앱 시작 시 또는 세션에 데이터가 없을 시 로컬 JSON 파일로부터 데이터 로드
if "branches" not in st.session_state:
    st.session_state.branches = load_data()

branches = st.session_state.branches

# 2. 상단 요약 지표 (지점 수, 전체 평균, 목표 달성률)
col1, col2, col3 = st.columns(3)
col1.metric("지점 수 전체", f"{len(branches)}개")

# 지점이 하나도 없을 때 ZeroDivisionError 예방
if len(branches) > 0:
    avgs = [average_sales(b) for b in branches]
    overall = sum(avgs) / len(avgs)
    col2.metric("전체 평균 (분기)", f"{overall:.2f} 백만원")
    col3.metric("목표 달성률 (평균 90M 이상)", f"{achievement_rate(branches):.1f}%")
else:
    col2.metric("전체 평균 (분기)", "0.00 백만원")
    col3.metric("목표 달성률 (평균 90M 이상)", "0.0%")

st.write("---")

# 3. 4개 탭 (지점 입력 / 지점별 실적 / 분기별 통계 / 순위, 등급 분포)
tab1, tab2, tab3, tab4 = st.tabs(["지점 입력", "지점별 실적", "분기별 통계", "순위, 등급 분포"])

# --- Tab 1 : 지점 입력 ---
with tab1:
    st.header("🏢 신규 지점 입력 및 추가")
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        name = st.text_input("지점명", placeholder="예: 서초점")
        q1 = st.number_input("1분기 매출 (백만원)", 0, 1000, 0)
    with col_input2:
        q2 = st.number_input("2분기 매출 (백만원)", 0, 1000, 0)
        q3 = st.number_input("3분기 매출 (백만원)", 0, 1000, 0)
        
    st.write("")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("지점 추가 완료"):
            if name.strip() == "":
                st.error("지점명을 입력해주세요.")
            elif any(b["지점"] == name.strip() for b in branches):
                st.error("이미 존재하는 지점명입니다.")
            else:
                new_branch = {"지점": name.strip(), "1분기": q1, "2분기": q2, "3분기": q3}
                branches.append(new_branch)
                save_data(branches) # 로컬 JSON 파일에 영구 저장
                st.success(f"🎉 '{name}' 지점이 성공적으로 추가되었습니다!")
                st.rerun()
                
    with col_btn2:
        # 데이터 초기화 기능 추가 (샘플 데이터 상태로 복구)
        if st.button("샘플 데이터로 초기화"):
            default_data = [
                {"지점": "강남점", "1분기": 150, "2분기": 130, "3분기": 140},
                {"지점": "홍대점", "1분기": 90,  "2분기": 110, "3분기": 100},
                {"지점": "판교점", "1분기": 120, "2분기": 100, "3분기": 95},
                {"지점": "부산점", "1분기": 80,  "2분기": 90,  "3분기": 85},
                {"지점": "대전점", "1분기": 50,  "2분기": 55,  "3분기": 45},
            ]
            st.session_state.branches = default_data
            save_data(default_data)
            st.success("데이터가 기본 샘플 데이터로 복구되었습니다.")
            st.rerun()

# --- Tab 2 : 지점별 실적표 ---
with tab2:
    st.header("📊 지점별 실적 및 성과 분석")
    if len(branches) > 0:
        table = []
        for b in branches:
            avg = average_sales(b)
            grade = to_grade(avg)
            table.append({
                "지점": b["지점"],
                "1분기": f"{b['1분기']} M",
                "2분기": f"{b['2분기']} M",
                "3분기": f"{b['3분기']} M",
                "총매출": f"{total_sales(b)} M",
                "평균": f"{avg:.2f} M",
                "등급": grade,
                "성과급률": f"{grade_to_incentive(grade):.1f}%",
            })
        st.table(table)
    else:
        st.info("등록된 지점 정보가 없습니다. '지점 입력' 탭에서 지점을 추가해 주세요.")

# --- Tab 3 : 분기별 통계 (분기 평균 막대그래프 포함) ---
with tab3:
    st.header("📈 분기별 매출 통계 및 추이")
    if len(branches) > 0:
        cols = st.columns(3)
        for i in range(len(QUARTERS)):
            quarter = QUARTERS[i]
            with cols[i]:
                avg_val = quarter_average(branches, quarter)
                top_val = quarter_top(branches, quarter)
                
                st.subheader(f"📍 {quarter}")
                st.metric("평균 매출", f"{avg_val:.2f} M")
                st.metric("최고 매출", f"{top_val} M")

        st.write("")
        st.subheader("📊 분기별 평균 매출 비교 그래프")
        chart_data = []
        for quarter in QUARTERS:
            chart_data.append({"분기": quarter, "평균": quarter_average(branches, quarter)})
        # 원래대로 horizontal=True 로 변경하여 막대와 텍스트 정렬 복구
        st.bar_chart(chart_data, x="분기", y="평균", horizontal=True, height=400)
    else:
        st.info("등록된 지점 정보가 없습니다. '지점 입력' 탭에서 지점을 추가해 주세요.")

# --- Tab 4 : 순위 & 등급 분포 (등급 분포 막대그래프 포함) ---
with tab4:
    if len(branches) > 0:
        col_rank, col_dist = st.columns(2)
        
        with col_rank:
            st.header("🥇 지점별 누적 매출 순위")
            ranked = rank_list(branches)
            rank_table = []
            for rank, b in enumerate(ranked, 1):
                rank_table.append({
                    "순위": f"{rank}위",
                    "지점": b["지점"],
                    "총매출": f"{total_sales(b)} 백만원"
                })
            st.table(rank_table)

        with col_dist:
            st.header("🎯 등급별 지점 분포")
            dist = grade_distribution(branches)
            dist_data = [{"등급": g, "지점수": dist[g]} for g in ["A", "B", "C", "D", "F"]]
            
            # 원래대로 horizontal=True 로 변경하여 막대와 텍스트 정렬 복구
            st.bar_chart(dist_data, x="등급", y="지점수", horizontal=True, height=400)
    else:
        st.info("등록된 지점 정보가 없습니다. '지점 입력' 탭에서 지점을 추가해 주세요.")
