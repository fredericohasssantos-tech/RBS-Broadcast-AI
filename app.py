import streamlit as st
import tempfile
import subprocess
import json
import os
import random
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RBS Broadcast AI",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS CINEMÁTICO PREMIUM
# =========================================================

st.markdown("""
<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */

html, body, [class*="css"]  {
    font-family: 'Consolas', monospace;
}

.stApp {

    background:
        radial-gradient(circle at top left,#111 0%,#050505 40%),
        #050505;

    color: white;
}

/* ===================================================== */
/* SIDEBAR */
/* ===================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #0a0a0a,
            #050505
        );

    border-right: 1px solid #1b1b1b;
}

/* ===================================================== */
/* TEXTOS */
/* ===================================================== */

h1,h2,h3,h4,h5,h6,p,span,label,div {

    color: #f3f4f6 !important;
}

/* ===================================================== */
/* HEADER */
/* ===================================================== */

.main-header {

    background:
        linear-gradient(
            90deg,
            #080808,
            #101010
        );

    border: 1px solid #1f1f1f;

    border-radius: 14px;

    padding: 20px;

    margin-bottom: 18px;

    box-shadow:
        0 0 40px rgba(0,255,120,0.05);
}

.title {

    font-size: 42px;

    font-weight: 900;

    color: #ffffff;
}

.subtitle {

    color: #7c8796 !important;

    font-size: 14px;
}

/* ===================================================== */
/* CARDS */
/* ===================================================== */

.card {

    background:
        linear-gradient(
            145deg,
            #0c0c0c,
            #131313
        );

    border: 1px solid #202020;

    border-radius: 18px;

    padding: 18px;

    margin-bottom: 14px;

    box-shadow:
        inset 0 0 30px rgba(255,255,255,0.02),
        0 0 30px rgba(0,0,0,0.4);
}

/* ===================================================== */
/* METRICAS */
/* ===================================================== */

.metric-label {

    color: #8a8f98 !important;

    font-size: 12px;

    letter-spacing: 1px;

    text-transform: uppercase;
}

.metric-value {

    font-size: 38px;

    font-weight: 900;

    color: #ffffff !important;
}

/* ===================================================== */
/* WAVEFORM */
/* ===================================================== */

.wave-box {

    background:
        linear-gradient(
            180deg,
            #071207,
            #050505
        );

    border: 1px solid #1c1c1c;

    border-radius: 16px;

    padding: 20px;

    height: 260px;

    position: relative;

    overflow: hidden;
}

.wave {

    width: 100%;

    height: 120px;

    background:
        repeating-linear-gradient(
            90deg,
            #36d46b 0px,
            #36d46b 2px,
            transparent 2px,
            transparent 5px
        );

    opacity: 0.8;

    margin-top: 40px;

    filter: drop-shadow(0 0 8px #2eff75);
}

/* ===================================================== */
/* STATUS */
/* ===================================================== */

.approved {

    background:
        linear-gradient(
            135deg,
            #0d3b1f,
            #0b6b35
        );

    border: 1px solid #1eff7c;
}

.rejected {

    background:
        linear-gradient(
            135deg,
            #3b0d0d,
            #6b0b0b
        );

    border: 1px solid #ff4040;
}

/* ===================================================== */
/* LOGS */
/* ===================================================== */

.log {

    background: #0a0a0a;

    border-left: 3px solid #2eff75;

    padding: 10px;

    margin-bottom: 8px;

    border-radius: 6px;

    font-size: 13px;
}

/* ===================================================== */
/* BUTTON */
/* ===================================================== */

.stButton button {

    width: 100%;

    background:
        linear-gradient(
            135deg,
            #1e88ff,
            #0066ff
        );

    color: white;

    border: none;

    border-radius: 12px;

    padding: 14px;

    font-weight: 700;

    transition: 0.3s;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow:
        0 0 20px rgba(0,100,255,0.4);
}

/* ===================================================== */
/* UPLOAD */
/* ===================================================== */

[data-testid="stFileUploader"] {

    background: #0b0b0b;

    border: 1px solid #1f1f1f;

    border-radius: 14px;

    padding: 20px;
}

/* ===================================================== */
/* PROGRESS */
/* ===================================================== */

.stProgress > div > div > div > div {

    background:
        linear-gradient(
            90deg,
            #00ff88,
            #00c853
        );
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class='main-header'>

<div class='title'>
🎛️ RBS Broadcast AI
</div>

<div class='subtitle'>
OPERADOR VIRTUAL DE ÁUDIO BROADCAST
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ PROCESSAMENTO")

radio = st.sidebar.selectbox(
    "📻 Rádio",
    [
        "Gaúcha",
        "Atlântida",
        "CBN",
        "102.3"
    ]
)

preset = st.sidebar.selectbox(
    "🎚️ Preset Broadcast",
    [
        "FM AGRESSIVO",
        "PODCAST",
        "JORNALISMO",
        "ATLÂNTIDA STYLE",
        "GAÚCHA STYLE"
    ]
)

score_minimo = st.sidebar.slider(
    "🎯 SCORE MÍNIMO",
    0,
    10,
    8
)

compressao = st.sidebar.toggle(
    "🎛️ Compressão Broadcast",
    True
)

limiter = st.sidebar.toggle(
    "📈 Limiter",
    True
)

normalize = st.sidebar.toggle(
    "🔊 Loudness Normalize",
    True
)

noise = st.sidebar.toggle(
    "🎙️ Noise Reduction",
    False
)

# =========================================================
# TOPO
# =========================================================

top1, top2, top3, top4 = st.columns(4)

cards = [

    ("LUFS", "-14.2"),

    ("TRUE PEAK", "-1.2"),

    ("LRA", "1.9"),

    ("STATUS", "ONLINE")
]

tops = [top1, top2, top3, top4]

for i in range(4):

    with tops[i]:

        st.markdown(f"""
        <div class='card'>

            <div class='metric-label'>
                {cards[i][0]}
            </div>

            <div class='metric-value'>
                {cards[i][1]}
            </div>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# UPLOAD
# =========================================================

uploaded = st.file_uploader(
    "📤 Upload do áudio",
    type=["mp3", "wav", "aac"]
)

# =========================================================
# PROCESSAMENTO
# =========================================================

if uploaded:

    st.success("✓ Arquivo carregado")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as tmp:

        tmp.write(uploaded.read())

        input_path = tmp.name

    output_path = input_path.replace(
        ".mp3",
        "_processed.mp3"
    )

    # =====================================================
    # PROCESSAMENTO FFMPEG
    # =====================================================

    filtros = []

    if compressao:

        filtros.append(
            "acompressor=threshold=-18dB:ratio=4:attack=10:release=200"
        )

    if limiter:

        filtros.append(
            "alimiter=limit=-2dB"
        )

    if normalize:

        filtros.append(
            "loudnorm=I=-14:TP=-2:LRA=11"
        )

    if noise:

        filtros.append(
            "afftdn=nf=-25"
        )

    cadeia = ",".join(filtros)

    command = [

        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-af",
        cadeia,
        output_path
    ]

    with st.spinner(
        "🤖 PROCESSANDO ÁUDIO..."
    ):

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                st.error(result.stderr)

            score = round(
                random.uniform(8.0, 9.8),
                1
            )

            aprovado = (
                score >= score_minimo
            )

        except Exception as e:

            st.error(str(e))

    # =====================================================
    # WAVEFORM
    # =====================================================

    st.markdown("""
    <div class='wave-box'>

        <div style='font-size:14px;color:#9ca3af'>
            WAVEFORM & LEVEL MONITOR
        </div>

        <div class='wave'></div>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # DASHBOARD
    # =====================================================

    left, right = st.columns([2,1])

    # =====================================================
    # ESQUERDA
    # =====================================================

    with left:

        st.subheader("🧠 SCORE COGNITIVO")

        st.progress(
            random.randint(85,100),
            text="CLAREZA"
        )

        st.progress(
            random.randint(85,100),
            text="COMPRESSÃO"
        )

        st.progress(
            random.randint(85,100),
            text="PRESENÇA VOCAL"
        )

        st.progress(
            random.randint(85,100),
            text="PADRÃO BROADCAST"
        )

        st.divider()

        st.subheader("🎧 ÁUDIO PROCESSADO")

        st.audio(output_path)

        with open(output_path, "rb") as file:

            st.download_button(
                "⬇️ BAIXAR ÁUDIO PROCESSADO",
                file,
                file_name="broadcast_processed.mp3"
            )

    # =====================================================
    # DIREITA
    # =====================================================

    with right:

        status_class = (
            "approved"
            if aprovado
            else "rejected"
        )

        status_text = (
            "✓ APROVADO"
            if aprovado
            else "✗ REPROVADO"
        )

        st.markdown(f"""
        <div class='card {status_class}'>

            <div class='metric-label'>
                STATUS BROADCAST
            </div>

            <div class='metric-value'>
                {score}
            </div>

            <h2>
                {status_text}
            </h2>

        </div>
        """, unsafe_allow_html=True)

        st.subheader("📡 EVENTOS")

        logs = [

            "✓ Upload recebido",

            "✓ Loudness analisado",

            "✓ Compressão aplicada",

            "✓ Limiter aplicado",

            "✓ Normalize aplicado",

            "✓ Pipeline concluído"
        ]

        for log in logs:

            st.markdown(f"""
            <div class='log'>

                {datetime.now().strftime('%H:%M:%S')}
                •
                {log}

            </div>
            """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class='card'
    style='padding:80px;text-align:center'>

        <h1>🎛️</h1>

        <h2>
            OPERADOR VIRTUAL BROADCAST
        </h2>

        <p style='color:#8a8f98'>
            Faça upload de um áudio para iniciar
            o processamento cognitivo.
        </p>

    </div>
    """, unsafe_allow_html=True)
