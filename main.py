import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (제목, 아이콘, 레이아웃)
st.set_page_config(
    page_title="나만의 MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 따뜻한 크림/노랑 톤 Custom CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background-color: #FFFDF0;
        font-family: 'Pretendard', 'Noto Sans KR', -apple-system, sans-serif;
        color: #4A3B32;
    }
    
    /* 상단 타이틀 상자 */
    .header-box {
        background: linear-gradient(135deg, #FFF5C0 0%, #FFE082 100%);
        padding: 2rem 1.5rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.12);
        margin-bottom: 2rem;
        border: 2px solid #FCD34D;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #78350F;
        margin-bottom: 0.4rem;
    }
    
    .header-subtitle {
        font-size: 1.15rem;
        color: #92400E;
        font-weight: 600;
    }

    /* 포켓몬 결과 카드 스타일 */
    .pokemon-card {
        background-color: #FFFFFF;
        border: 3px solid #FCD34D;
        border-radius: 28px;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: 0 12px 30px rgba(217, 119, 6, 0.15);
        margin-top: 1.5rem;
    }

    /* MBTI 배지 */
    .mbti-badge {
        display: inline-block;
        background-color: #FEF3C7;
        color: #B45309;
        font-weight: 800;
        font-size: 1.25rem;
        padding: 0.4rem 1.3rem;
        border-radius: 50px;
        border: 2px solid #FBBF24;
        margin-bottom: 1rem;
    }

    /* 포켓몬 이름 */
    .pokemon-name {
        font-size: 2.3rem;
        font-weight: 900;
        color: #451A03;
        margin-bottom: 0.2rem;
    }

    .pokemon-english {
        font-size: 1.2rem;
        color: #D97706;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* 타입 태그 */
    .type-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        font-size: 1.05rem;
        font-weight: 700;
        border-radius: 20px;
        color: white;
        margin: 0.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    /* 특징 및 어울리는 이유 박스 */
    .info-section {
        background-color: #FFFBEB;
        border-radius: 20px;
        padding: 1.3rem 1.5rem;
        margin-top: 1.2rem;
        text-align: left;
        border: 1px solid #FDE68A;
    }

    .info-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #78350F;
        margin-bottom: 0.5rem;
    }

    .info-text {
        font-size: 1.15rem;
        line-height: 1.75;
        color: #451A03;
        font-weight: 500;
    }

    .reason-list {
        margin: 0;
        padding-left: 1.3rem;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #451A03;
    }

    /* 선택 상자 및 버튼 스타일 */
    div[data-baseweb="select"] > div {
        background-color: #FFFBEB !important;
        border-color: #FBBF24 !important;
        border-radius: 16px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #78350F !important;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        font-size: 1.35rem;
        font-weight: 800;
        padding: 0.8rem 1.5rem;
        border-radius: 20px;
        border: none;
        box-shadow: 0 6px 18px rgba(217, 119, 6, 0.3);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(217, 119, 6, 0.4);
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 3. 타입별 배지 색상 테이블
TYPE_COLORS = {
    "불꽃": "#EF4444",
    "물": "#3B82F6",
    "풀": "#10B981",
    "전기": "#F59E0B",
    "에스퍼": "#EC4899",
    "격투": "#D97706",
    "강철": "#6B7280",
    "노말": "#A8A29E",
    "페어리": "#F472B6",
    "고스트": "#8B5CF6",
    "독": "#A855F7",
    "비행": "#60A5FA",
    "드래곤": "#6366F1",
    "바위": "#78350F",
    "악": "#475569"
}

# 4. 16가지 MBTI별 포켓몬 데이터베이스
MBTI_POKEMON = {
    "ISTJ": {
        "name": "거북왕",
        "english_name": "Blastoise",
        "id": 9,
        "types": ["물"],
        "features": "묵묵하고 단단하며 신뢰를 최우선으로 생각하는 보디가드",
        "reasons": [
            "원칙을 지키며 책임감이 강한 ISTJ의 신뢰감을 꼭 닮아 있습니다.",
            "어떤 단단한 시련이 찾아와도 흔들리지 않고 팀을 든든하게 지켜줍니다.",
            "말보다 확실한 행동과 실력으로 최고의 파트너십을 발휘합니다."
        ]
    },
    "ISFJ": {
        "name": "해피너스",
        "english_name": "Blissey",
        "id": 242,
        "types": ["노말"],
        "features": "타인의 행복과 건강을 세심하게 보살피는 헌신적인 포켓몬",
        "reasons": [
            "주변 사람들을 온화하고 세심하게 챙기는 ISFJ의 다정함과 꼭 맞닿아 있습니다.",
            "지친 일상 속에서 따뜻한 안식처가 되어 마음의 평화를 선물해 줍니다.",
            "진심 어린 공감과 보살핌으로 서로의 마음에 큰 위안을 줍니다."
        ]
    },
    "INFJ": {
        "name": "뮤",
        "english_name": "Mew",
        "id": 151,
        "types": ["에스퍼"],
        "features": "깊은 통찰력과 신비로운 이상을 품고 있는 포켓몬",
        "reasons": [
            "내면의 깊은 가치와 통찰력을 중시하는 INFJ와 영혼의 결이 어울립니다.",
            "조용하지만 세상을 긍정적으로 변화시키고자 하는 선한 지향점을 공유합니다.",
            "말하지 않아도 마음 깊이 서로의 직관을 알아채는 신비로운 콤비입니다."
        ]
    },
    "INTJ": {
        "name": "후딘",
        "english_name": "Alakazam",
        "id": 65,
        "types": ["에스퍼"],
        "features": "비범한 지능과 전략적 사고를 바탕으로 해결책을 찾는 지성파",
        "reasons": [
            "복잡한 문제를 명확하게 분석하고 철저히 계획하는 INTJ의 모범적인 파트너입니다.",
            "감정에 휘둘리지 않고 합리적이며 가장 효율적인 길을 함께 개척합니다.",
            "긴 설명 없이도 명확한 전략적 판단으로 함께 승리를 만들어냅니다."
        ]
    },
    "ISTP": {
        "name": "루카리오",
        "english_name": "Lucario",
        "id": 448,
        "types": ["격투", "강철"],
        "features": "침착한 관찰력과 정교한 기민함을 겸비한 과묵한 해결사",
        "reasons": [
            "상황을 냉철하게 파악하고 깔끔하게 임무를 완수하는 ISTP와 스타일이 맞아떨어집니다.",
            "군더더기 없는 차분함과 강인한 실천력으로 깔끔한 호흡을 과시합니다.",
            "위기의 순간일수록 한층 더 빛나는 기량을 보여주는 든든한 조력자입니다."
        ]
    },
    "ISFP": {
        "name": "피카츄",
        "english_name": "Pikachu",
        "id": 25,
        "types": ["전기"],
        "features": "자유롭고 감성적이며 주변에 기분 좋은 순수함을 전하는 파트너",
        "reasons": [
            "자신만의 감성을大切히 여기는 ISFP에게 솔직하고 매력적인 온기를 더해줍니다.",
            "강요 없이 자연스러운 일상 속 행복과 자유로움을 선사합니다.",
            "함께 있는 것만으로도 잔잔한 상쾌함과 소소한 기쁨이 피어납니다."
        ]
    },
    "INFP": {
        "name": "님피아",
        "english_name": "Sylveon",
        "id": 700,
        "types": ["페어리"],
        "features": "상대방의 마음을 어루만지고 따뜻한 유대감을 나누는 낭만 포켓몬",
        "reasons": [
            "풍부한 감수성과 따뜻한 마음을 가진 INFP의 정서를 누구보다 잘 감싸줍니다.",
            "세상을 다정하고 아름다운 시선으로 바라보는 순수한 이상을 나눕니다.",
            "지친 마음을 보듬으며 서로에게 세상에 하나뿐인 친구가 되어줍니다."
        ]
    },
    "INTP": {
        "name": "팬텀",
        "english_name": "Gengar",
        "id": 94,
        "types": ["고스트", "독"],
        "features": "엉뚱하고 기발하며 독창적인 관점으로 세상을 탐구하는 호기심 대장",
        "reasons": [
            "고정관념을 벗어나 늘 새로운 아이디어를 탐구하는 INTP에게 시원한 영감을 줍니다.",
            "남들과 다른 관점에서도 마음이 통해서 지루할 틈이 없는 만남입니다.",
            "엉뚱하지만 시원시원하고 독창적인 사고방식을 진심으로 지지합니다."
        ]
    },
    "ESTP": {
        "name": "리자몽",
        "english_name": "Charizard",
        "id": 6,
        "types": ["불꽃", "비행"],
        "features": "망설임 없는 도전 정신과 화끈한 에너지를 자랑하는 행동파",
        "reasons": [
            "스릴 넘치는 모험과 거침없는 현장 실행력을 지닌 ESTP의 열정을 닮았습니다.",
            "어떤 역경도 직면해서 돌파해내는 화끈하고 당당한 자신감을 선사합니다.",
            "망설임 없이 즉각 도전하여 최고의 결과를 이끌어내는 승부사 조합입니다."
        ]
    },
    "ESFP": {
        "name": "푸린",
        "english_name": "Jigglypuff",
        "id": 39,
        "types": ["노말", "페어리"],
        "features": "무대 위의 스타처럼 밝은 에너지를 전파하는 매력 만점 무드메이커",
        "reasons": [
            "흥이 넘치고 사람들에게 웃음을 건네는 ESFP의 밝은 분위기와 천생연분입니다.",
            "어디서나 존재감을 드러내며 주위 분위기를 환하게 만들어 줍니다.",
            "매 순간을 즐거운 축제로 바꾸는 신나는 유쾌함의 대명사입니다."
        ]
    },
    "ENFP": {
        "name": "토게피",
        "english_name": "Togepi",
        "id": 175,
        "types": ["페어리"],
        "features": "긍정 에너지와 행운을 유발하는 무한한 상상력의 소유자",
        "reasons": [
            "세상을 호기심 가득하고 긍정적으로 바라보는 ENFP의 순수한 열정과 통합니다.",
            "통통 튀는 아이디어와 맑은 에너지를 모아 뜻밖의 행운을 불러옵니다.",
            "바라보기만 해도 기분이 올라가며 새로운 희망을 품게 만듭니다."
        ]
    },
    "ENTP": {
        "name": "로토무",
        "english_name": "Rotom",
        "id": 479,
        "types": ["전기", "고스트"],
        "features": "끊임없이 변화하며 새로운 형태를 시도하는 창의력 브레인",
        "reasons": [
            "다방면에 관심이 많고 틀에 갇히길 거부하는 ENTP에게 완벽한 자극을 줍니다.",
            "상상 이상의 변화무쌍함으로 질릴 겨를이 없는 재기발랄한 관계입니다.",
            "새로운 가능성을 끝없이 탐구하며 번뜩이는 지적 아이디어를 뿜어냅니다."
        ]
    },
    "ESTJ": {
        "name": "윈디",
        "english_name": "Arcanine",
        "id": 59,
        "types": ["불꽃"],
        "features": "위풍당당한 용맹함과 확고한 책임감을 갖춘 대장 포켓몬",
        "reasons": [
            "질서와 체계를 지키며 단체를 이끄는 ESTJ의 당당한 리더십에 꼭 맞습니다.",
            "깊은 신뢰와 흔들림 없는 충성심으로 주어진 과업을 정확히 완성해냅니다.",
            "누구도 가볍게 보지 못할 카리스마와 안정감을 보여주는 조합입니다."
        ]
    },
    "ESFJ": {
        "name": "다부니",
        "english_name": "Audino",
        "id": 531,
        "types": ["노말"],
        "features": "상대방의 마음을 먼저 헤아리고 화합을 이루어내는 친절 왕",
        "reasons": [
            "사람들을 따뜻하게 챙기고 친화력이 높은 ESFJ의 다정함을 배로 만들어줍니다.",
            "모임 내부의 분위기를 매끄럽고 따뜻하게 이어주는 다리 역할을 맡습니다.",
            "서로에 대한 깊은 유대와 친절로 늘 조화로운 시너지를 만듭니다."
        ]
    },
    "ENFJ": {
        "name": "망나뇽",
        "english_name": "Dragonite",
        "id": 149,
        "types": ["드래곤", "비행"],
        "features": "크고 포근한 마음으로 타인을 이끌고 돕는 든든한 멘토",
        "reasons": [
            "주변 사람들의 가능성을 꽃피우고 진심으로 돕는 ENFJ의 헌신과 닮아 있습니다.",
            "온화하면서도 강인한 기상으로 모임 전체를 포근히 감싸 안습니다.",
            "타인을 향한 선한 영향력과 용기를 크게 북돋아 주는 최고의 파트너입니다."
        ]
    },
    "ENTJ": {
        "name": "마기라스",
        "english_name": "Tyranitar",
        "id": 248,
        "types": ["바위", "악"],
        "features": "압도적인 포스와 당당한 추진력으로 정상을 목표로 하는 비전가",
        "reasons": [
            "높은 비전을 설정하고 원대하게 목표를 이뤄내는 ENTJ의 결단력과 어울립니다.",
            "어떠한 거친 장애물도 담대하게 파헤쳐 나가는 엄청난 존재감을 가집니다.",
            "확고한 의지와 카리스마로 목표를 정복해 내는 압도적 라이벌이자 동반자입니다."
        ]
    }
}

# 5. 메인 레이아웃 구성
st.markdown("""
<div class="header-box">
    <div class="header-title">⚡ MBTI 단짝 포켓몬 찾기 ⚡</div>
    <div class="header-subtitle">나의 성격 유형과 가장 완벽하게 어울리는 포켓몬 친구를 만나보세요!</div>
</div>
""", unsafe_allow_html=True)

# 6. MBTI 선택 섹션
mbti_list = list(MBTI_POKEMON.keys())
selected_mbti = st.selectbox(
    "👉 당신의 MBTI 유형을 선택해 주세요:",
    mbti_list,
    index=0
)

# 7. 버튼 클릭 시 결과 표시
if st.button("✨ 내 단짝 포켓몬 찾아보기 ✨"):
    # 폭죽 효과 실행 (Streamlit 기본 축하 효과)
    st.balloons()
    
    # HTML/JS 커스텀 파티클 연출 포함
    js_confetti = """
    <script>
    function createParticle(x, y) {
        const particle = document.createElement('div');
        const colors = ['#F59E0B', '#EF4444', '#10B981', '#3B82F6', '#EC4899', '#FBBF24'];
        const size = Math.random() * 12 + 8;
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        particle.style.borderRadius = Math.random() > 0.5 ? '50%' : '3px';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '999999';
        
        document.body.appendChild(particle);

        const destX = (Math.random() - 0.5) * 350;
        const destY = (Math.random() - 0.5) * 350 - 100;

        particle.animate([
            { transform: 'translate(0, 0) scale(1)', opacity: 1 },
            { transform: `translate(${destX}px, ${destY}px) scale(0)`, opacity: 0 }
        ], {
            duration: 1200 + Math.random() * 800,
            easing: 'cubic-bezier(0, .9, .57, 1)',
            fill: 'forwards'
        });

        setTimeout(() => particle.remove(), 2000);
    }
    for(let i=0; i<45; i++) {
        setTimeout(() => {
            createParticle(window.innerWidth / 2, window.innerHeight / 3);
        }, i * 20);
    }
    </script>
    """
    components.html(js_confetti, height=0)

    # 데이터 추출
    poke_info = MBTI_POKEMON[selected_mbti]
    poke_id = poke_info["id"]
    # PokeAPI 공식 이미지 고화질 URL
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{poke_id}.png"

    # 타입 배지 HTML 구성
    type_badges_html = ""
    for t in poke_info["types"]:
        bg_col = TYPE_COLORS.get(t, "#F59E0B")
        type_badges_html += f'<span class="type-badge" style="background-color:{bg_col};">{t}</span>'

    # 이유 리스트 HTML 구성
    reasons_html = "".join([f"<li>{r}</li>" for r in poke_info["reasons"]])

    # 결과 카드 출력
    st.markdown(f"""
    <div class="pokemon-card">
        <div class="mbti-badge">{selected_mbti}의 단짝</div>
        <div class="pokemon-name">{poke_info['name']}</div>
        <div class="pokemon-english">({poke_info['english_name']})</div>
        <div>{type_badges_html}</div>
        <div style="margin: 1.5rem 0;">
            <img src="{img_url}" width="240" alt="{poke_info['name']}" style="filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.12));">
        </div>
        <div class="info-section">
            <div class="info-title">🌟 단짝 포켓몬의 특징</div>
            <div class="info-text">{poke_info['features']}</div>
        </div>
        <div class="info-section">
            <div class="info-title">🤝 우리는 왜 최고의 단짝일까요?</div>
            <ul class="reason-list">
                {reasons_html}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
