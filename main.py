
import streamlit as st
import random

st.set_page_config(
    page_title="MBTI 포켓몬 단짝 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    background: linear-gradient(180deg, #FFF9E9 0%, #FFF4D3 100%);
    color: #493B28;
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    text-align: center;
    background: #FFFFFF;
    border: 2px solid #F7D875;
    border-radius: 28px;
    padding: 32px 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 0 #F4DDA1;
}
.hero-label {
    display: inline-block;
    background: #FFF0B8;
    color: #8A641A;
    padding: 7px 15px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 900;
}
.hero h1 {
    font-family: 'Jua', sans-serif;
    font-size: clamp(30px, 6vw, 45px);
    line-height: 1.4;
    margin: 18px 0 10px;
    color: #4B3A23;
}
.hero h1 span { color: #E5A900; }
.hero p {
    color: #8B7A60;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 0;
}
.section-title {
    font-size: 22px;
    font-weight: 900;
    margin: 25px 0 15px;
}
.stButton > button {
    min-height: 54px;
    border-radius: 15px;
    border: 2px solid #F2DDA2;
    background: #FFFFFF;
    color: #66502D;
    font-size: 17px;
    font-weight: 900;
    transition: all .15s ease;
}
.stButton > button:hover {
    border-color: #E9B92D;
    background: #FFF0B8;
    color: #614600;
}
.stButton > button[kind="primary"] {
    background: #F3C943;
    color: #4B3810;
    border-color: #E5B82F;
}
.result-card {
    background: #FFFFFF;
    border: 2px solid #F4D77C;
    border-radius: 28px;
    padding: 25px;
    box-shadow: 0 9px 0 #F4DDA1;
    text-align: center;
    margin-top: 18px;
}
.result-label {
    display: inline-block;
    background: #FFF0B8;
    border-radius: 30px;
    padding: 8px 15px;
    color: #8A641A;
    font-size: 14px;
    font-weight: 900;
}
.pokemon-name {
    font-family: 'Jua', sans-serif;
    font-size: clamp(27px, 5vw, 36px);
    margin: 12px 0;
    color: #4B3A23;
}
.pokemon-subtitle {
    color: #A07C34;
    font-size: 17px;
    font-weight: 700;
}
.type-pill {
    display: inline-block;
    padding: 8px 15px;
    background: #FFF4D3;
    border: 1px solid #F0D58A;
    border-radius: 30px;
    margin: 5px;
    font-size: 15px;
    font-weight: 800;
}
.reason {
    background: #FFFAED;
    border-radius: 17px;
    padding: 18px;
    text-align: left;
    line-height: 1.9;
    font-size: 16px;
    margin-top: 20px;
}
.trait {
    display: inline-block;
    background: #FFF0B8;
    color: #74551A;
    border-radius: 30px;
    padding: 8px 13px;
    margin: 4px;
    font-size: 14px;
    font-weight: 800;
}
.small-note {
    text-align: center;
    color: #9A896C;
    font-size: 12px;
    margin-top: 25px;
    line-height: 1.8;
}
div[data-testid="stImage"] img {
    object-fit: contain;
    border-radius: 20px;
}
@media (max-width: 600px) {
    .hero { padding: 25px 14px; }
    .result-card { padding: 18px 13px; }
    .section-title { font-size: 20px; }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 포켓몬 데이터
# 이미지: PokéAPI 공개 스프라이트 저장소
# -----------------------------
POKEMON = {
    "ISTJ": {
        "name": "꼬부기", "english": "Squirtle", "dex": 7,
        "type": "물", "emoji": "🐢",
        "traits": ["책임감", "꾸준함", "신중함"],
        "reason": "꼬부기처럼 차분하고 성실한 편이에요. "
                  "계획한 일을 꾸준히 해내고, 믿을 수 있는 단짝이 되어 주는 모습이 닮았어요."
    },
    "ISFJ": {
        "name": "이브이", "english": "Eevee", "dex": 133,
        "type": "노말", "emoji": "🦊",
        "traits": ["배려심", "다정함", "헌신"],
        "reason": "이브이처럼 부드럽고 따뜻한 매력이 있어요. "
                  "친구의 작은 변화도 알아차리고 소중한 관계를 정성껏 가꾸는 모습이 잘 어울려요."
    },
    "INFJ": {
        "name": "가디안", "english": "Gardevoir", "dex": 282,
        "type": "에스퍼 · 페어리", "emoji": "✨",
        "traits": ["통찰력", "공감", "이상주의"],
        "reason": "가디안처럼 다른 사람의 마음을 깊이 이해하려고 해요. "
                  "자신만의 가치관을 소중히 여기고 주변에 좋은 영향을 주려는 점이 닮았어요."
    },
    "INTJ": {
        "name": "뮤츠", "english": "Mewtwo", "dex": 150,
        "type": "에스퍼", "emoji": "🧠",
        "traits": ["전략적", "분석력", "독립성"],
        "reason": "뮤츠처럼 독립적으로 생각하고 큰 그림을 바라봐요. "
                  "복잡한 문제를 분석하고 자신만의 전략으로 해결하는 모습이 잘 어울려요."
    },
    "ISTP": {
        "name": "루카리오", "english": "Lucario", "dex": 448,
        "type": "격투 · 강철", "emoji": "🐺",
        "traits": ["실용적", "침착함", "독립적"],
        "reason": "루카리오처럼 침착하게 상황을 파악하는 타입이에요. "
                  "말보다 행동을 중요하게 여기고 문제가 생기면 실용적인 해결책을 찾아요."
    },
    "ISFP": {
        "name": "이상해씨", "english": "Bulbasaur", "dex": 1,
        "type": "풀 · 독", "emoji": "🌱",
        "traits": ["감각적", "여유로움", "진솔함"],
        "reason": "이상해씨처럼 편안하고 자연스러운 매력이 있어요. "
                  "자신만의 취향을 소중히 여기며 주변에 잔잔한 안정감을 전해 줘요."
    },
    "INFP": {
        "name": "님피아", "english": "Sylveon", "dex": 700,
        "type": "페어리", "emoji": "🎀",
        "traits": ["상상력", "공감력", "순수함"],
        "reason": "님피아처럼 다정하고 감수성이 풍부해요. "
                  "마음속의 꿈과 상상력을 소중히 여기고 진심이 통하는 관계를 원해요."
    },
    "INTP": {
        "name": "폴리곤", "english": "Porygon", "dex": 137,
        "type": "노말", "emoji": "💠",
        "traits": ["호기심", "논리력", "독창성"],
        "reason": "폴리곤처럼 새로운 지식과 원리를 탐구하는 걸 좋아해요. "
                  "궁금한 것을 깊이 파고들고 남들이 놓친 새로운 관점을 발견해요."
    },
    "ESTP": {
        "name": "리자몽", "english": "Charizard", "dex": 6,
        "type": "불꽃 · 비행", "emoji": "🔥",
        "traits": ["추진력", "모험심", "순발력"],
        "reason": "리자몽처럼 에너지가 넘치고 도전을 즐겨요. "
                  "생각에만 머무르지 않고 직접 경험하며 기회를 잡는 모습이 닮았어요."
    },
    "ESFP": {
        "name": "피카츄", "english": "Pikachu", "dex": 25,
        "type": "전기", "emoji": "⚡",
        "traits": ["사교성", "긍정적", "활발함"],
        "reason": "피카츄처럼 밝고 생기 넘치는 에너지를 가지고 있어요. "
                  "친구들과 즐거운 추억을 만들고 주변 분위기를 환하게 밝혀 줘요."
    },
    "ENFP": {
        "name": "파치리스", "english": "Pachirisu", "dex": 417,
        "type": "전기", "emoji": "🐿️",
        "traits": ["창의력", "열정", "자유로움"],
        "reason": "파치리스처럼 밝고 호기심이 많아요. "
                  "새로운 경험을 즐기고 어디서든 재미있는 가능성을 발견하는 모습이 잘 어울려요."
    },
    "ENTP": {
        "name": "팬텀", "english": "Gengar", "dex": 94,
        "type": "고스트 · 독", "emoji": "👻",
        "traits": ["기발함", "재치", "도전 정신"],
        "reason": "팬텀처럼 장난기와 기발한 아이디어가 넘쳐요. "
                  "뻔한 방식보다는 새로운 방법을 찾고 재치 있는 대화를 즐기는 편이에요."
    },
    "ESTJ": {
        "name": "괴력몬", "english": "Machamp", "dex": 68,
        "type": "격투", "emoji": "💪",
        "traits": ["실행력", "리더십", "책임감"],
        "reason": "괴력몬처럼 실행력이 뛰어나고 맡은 일을 확실하게 처리해요. "
                  "체계적으로 계획을 세우고 팀이 목표를 달성하도록 이끌어요."
    },
    "ESFJ": {
        "name": "푸린", "english": "Jigglypuff", "dex": 39,
        "type": "노말 · 페어리", "emoji": "🎤",
        "traits": ["친화력", "배려", "따뜻함"],
        "reason": "푸린처럼 함께하는 시간을 소중히 여겨요. "
                  "친구들의 기분을 살피고 모두가 편안하게 어울릴 수 있도록 분위기를 만들어요."
    },
    "ENFJ": {
        "name": "루카리오", "english": "Lucario", "dex": 448,
        "type": "격투 · 강철", "emoji": "🐺",
        "traits": ["리더십", "공감", "격려"],
        "reason": "루카리오처럼 주변 사람의 마음을 살피고 응원해요. "
                  "함께 성장하는 것을 중요하게 여기며 친구들의 가능성을 믿어 주는 타입이에요."
    },
    "ENTJ": {
        "name": "망나뇽", "english": "Dragonite", "dex": 149,
        "type": "드래곤 · 비행", "emoji": "🐲",
        "traits": ["리더십", "전략적", "추진력"],
        "reason": "망나뇽처럼 넓은 시야와 강한 추진력을 가지고 있어요. "
                  "높은 목표를 향해 효율적인 방법을 찾고 사람들과 함께 성과를 만들어 가요."
    }
}

# -----------------------------
# 제목
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-label">⭐ MY POKEMON PARTNER ⭐</div>
    <h1>내 MBTI의<br><span>운명의 포켓몬</span>은?</h1>
    <p>
        나와 찰떡궁합인 포켓몬을 찾아봐요!<br>
        MBTI를 선택하고 나만의 단짝을 만나 보세요.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">🧩 나의 MBTI를 골라 주세요</div>',
            unsafe_allow_html=True)

TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 4열 MBTI 버튼
for row_start in range(0, len(TYPES), 4):
    cols = st.columns(4)
    for col, mbti in zip(cols, TYPES[row_start:row_start + 4]):
        with col:
            if st.button(
                mbti,
                key=f"mbti_{mbti}",
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.get("selected_mbti") == mbti
                    else "secondary"
                )
            ):
                st.session_state.selected_mbti = mbti
                st.session_state.celebrate = True
                st.rerun()

st.markdown(
    '<p style="text-align:center;color:#9A896C;font-size:14px;">'
    '👇 버튼을 누르면 단짝 포켓몬이 나타나요!</p>',
    unsafe_allow_html=True
)

# -----------------------------
# 결과 화면
# -----------------------------
if "selected_mbti" in st.session_state:
    mbti = st.session_state.selected_mbti
    p = POKEMON[mbti]

    if st.session_state.get("celebrate", False):
        st.balloons()
        st.session_state.celebrate = False

    st.markdown(
        '<div class="result-card">'
        '<div class="result-label">🎉 운명의 단짝 발견!</div>'
        f'<div class="pokemon-name">{p["name"]} '
        f'({p["english"]})</div>'
        f'<div class="pokemon-subtitle">'
        f'{mbti} 유형과 어울리는 포켓몬</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # PokéAPI 스프라이트 이미지
    image_url = (
        "https://raw.githubusercontent.com/PokeAPI/sprites/"
        "master/sprites/pokemon/other/official-artwork/"
        f'{p["dex"]}.png'
    )

    left, center, right = st.columns([1, 2, 1])
    with center:
        try:
            st.image(
                image_url,
                width=270,
                caption=f'{p["name"]} / {p["english"]}'
            )
        except Exception:
            st.markdown(
                f'<div style="text-align:center;font-size:90px;">'
                f'{p["emoji"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        f'<div style="text-align:center;margin:8px 0 18px;">'
        f'<span class="type-pill">타입: {p["type"]}</span>'
        f'<span class="type-pill">MBTI: {mbti}</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">💛 포켓몬의 특징</div>',
        unsafe_allow_html=True
    )

    traits_html = "".join(
        f'<span class="trait">{trait}</span>'
        for trait in p["traits"]
    )
    st.markdown(traits_html, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">💌 우리가 잘 어울리는 이유</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="reason">{p["reason"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄 다른 MBTI로 다시 찾기", use_container_width=True):
        del st.session_state["selected_mbti"]
        st.rerun()

else:
    st.info("✨ 위에서 자신의 MBTI를 선택해 주세요!")

st.markdown("""
<div class="small-note">
    🍯 따뜻한 마음으로 만든 MBTI × 포켓몬 매칭<br>
    이 결과는 재미를 위한 창작 콘텐츠이며 공식 성격 진단은 아닙니다.<br>
    포켓몬 이미지 출처: PokéAPI 공개 스프라이트 저장소
</div>
""", unsafe_allow_html=True)
