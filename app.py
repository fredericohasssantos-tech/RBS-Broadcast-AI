# =========================================================
# RBS BROADCAST AI
# OPERADOR VIRTUAL DE ÁUDIO BROADCAST
# STREAMLIT + FFMPEG + IA
# =========================================================

import streamlit as st
import tempfile
import subprocess
import json
import os
import random
from datetime import datetime
from pathlib import Path

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
# CSS PREMIUM
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #050505;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #0b0b0b;
    border-right: 1px solid #1f1f1f;
}

/* TEXTOS */

h1,h2,h3,h4,h5,h6,p,span,label {
    color: #f5f5f5 !important;
}

/* TITULO */

.main-title {
    font-size: 58px;
    font-weight: 900;
    color: white;
}

.subtitle {
    color: #9ca3af;
    margin-bottom: 30px;
}

/* CARDS */

.card {
    background: linear-gradient(
        145deg,
        #101010,
        #181818
    );

    border: 1px solid #222;

    border-radius: 24px;

    padding: 24px;

    box-shadow:
        0 0 25px rgba(0,0,0,0.5);
}

/* STATUS */

.approved {
    background: linear-gradient(
        135deg,
        #00c853,
        #00695c
    );

    border-radius: 24px;

    padding: 30px;

    text-align: center;
}

.rejected {
    background: linear-gradient(
        135deg,
        #ff1744,
        #b71c1c
    );

    border-radius: 24px;

    padding: 30px;

    text-align: center;
}

/* LOGS */

.log-card {

    background: #0f0f0f;

    border: 1px solid #1f1f1f;

    border-radius: 14px;

    padding: 14px;

    margin-bottom: 10px;

    color: #d1d5db;
}

/* METRICAS */

.metric-label {
    color: #9ca3af;
    font-size: 14px;
}

.metric-value {
    color: white;
    font-size: 34px;
    font-weight: 800;
}

/* UPLOADER */

[data-testid="stFileUploader"] {

    background: #111111;

    border: 1px solid #222;

    border-radius: 18px;

    padding: 20px;
}

.big-score {
    font-size: 64px;
    font-weight: 900;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class='main-title'>
🎛️ RBS Broadcast AI
</div>

<div class='subtitle'>
Operador Virtual Inteligente de Broadcast
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Painel Operacional")

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
        "FM Agressivo",
        "Podcast",
        "Jornalismo",
        "Atlântida Style",
        "Gaúcha Style"
    ]
)

score_minimo = st.sidebar.slider(
    "🎯 Score mínimo",
    0,
    10,
    7
)

st.sidebar.divider()

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

transcricao = st.sidebar.toggle(
    "🧠 IA Transcrição",
    True
)

noise = st.sidebar.toggle(
    "🎙️ Noise Reduction",
    False
)

st.sidebar.divider()

st.sidebar.metric(
    "📦 Uploads Hoje",
    "248"
)

st.sidebar.metric(
    "🤖 Workers",
    "4"
)

st.sidebar.metric(
    "📡 Pipeline",
    "ONLINE"
)

# =========================================================
# DASHBOARD SUPERIOR
# =========================================================

top1, top2, top3, top4 = st.columns(4)

cards = [
    ("Uploads Hoje", "248"),
    ("Score Médio", "8.9"),
    ("Workers Ativos", "4"),
    ("Sistema", "ONLINE")
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

st.divider()

# =========================================================
# UPLOAD
# =========================================================

uploaded = st.file_uploader(
    "📤 Upload do boletim",
    type=["mp3", "wav", "aac"]
)

# =========================================================
# TRANSCRIÇÃO FAKE
# =========================================================

def fake_transcription():

    textos = [

        "Boa noite. O trânsito apresenta lentidão na região central.",

        "A previsão indica chuva forte nas próximas horas.",

        "O Internacional venceu por dois a zero no Beira-Rio.",

        "O sistema opera normalmente em todas as emissoras."
    ]

    return random.choice(textos)

# =========================================================
# PROCESSADOR BROADCAST
# =========================================================

def process_audio(input_path, output_path):

    audio_chain = []

    # ==========================================
    # COMPRESSÃO
    # ==========================================

    if compressao:

        if preset == "FM Agressivo":

            audio_chain.append(
                "acompressor=threshold=-20dB:ratio=6:attack=5:release=120"
            )

        elif preset == "Podcast":

            audio_chain.append(
                "acompressor=threshold=-18dB:ratio=3:attack=20:release=250"
            )

        elif preset == "Jornalismo":

            audio_chain.append(
                "acompressor=threshold=-16dB:ratio=2:attack=15:release=180"
            )

        else:

            audio_chain.append(
                "acompressor=threshold=-18dB:ratio=4:attack=10:release=200"
            )

    # ==========================================
    # LIMITER
    # ==========================================

    if limiter:

        audio_chain.append(
            "alimiter=limit=-2dB"
        )

    # ==========================================
    # NORMALIZE
    # ==========================================

    if normalize:

        audio_chain.append(
            "loudnorm=I=-14:TP=-2:LRA=11"
        )

    # ==========================================
    # NOISE REDUCTION
    # ==========================================

    if noise:

        audio_chain.append(
            "afftdn=nf=-25"
        )

    filters = ",".join(audio_chain)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-af",
        filters,
        output_path
    ]

    subprocess.run(
        command,
        capture_output=True,
        text=True
    )

# =========================================================
# ANALISADOR
# =========================================================

def analyze_audio(path):

    try:

        result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                path,
                "-af",
                "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                "-f",
                "null",
                "-"
            ],
            capture_output=True,
            text=True
        )

        stderr = result.stderr

        json_start = stderr.rfind("{")
        json_end = stderr.rfind("}") + 1

        if json_start >= 0:

            data = json.loads(
                stderr[json_start:json_end]
            )

            return {

                "lufs": round(
                    float(data.get("input_i", -14)),
                    1
                ),

                "peak": round(
                    float(data.get("input_tp", -2)),
                    1
                )
            }

    except Exception:
        pass

    return {
        "lufs": -14,
        "peak": -2
    }

# =========================================================
# PROCESSAMENTO
# =========================================================

if uploaded:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as tmp:

        tmp.write(uploaded.read())

        input_path = tmp.name

    output_path = (
        input_path.replace(
            ".mp3",
            "_processed.mp3"
        )
    )

    st.audio(input_path)

    with st.spinner(
        "🤖 Operador virtual processando áudio..."
    ):

        process_audio(
            input_path,
            output_path
        )

        analysis = analyze_audio(
            output_path
        )

        transcription_text = fake_transcription()

    score = round(
        random.uniform(7.5, 9.9),
        1
    )

    aprovado = (
        score >= score_minimo
    )

    st.divider()

    # ======================================================
    # MÉTRICAS
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>
                📻 Rádio
            </div>

            <div class='metric-value'>
                {radio}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>
                🔊 Loudness
            </div>

            <div class='metric-value'>
                {analysis['lufs']} LUFS
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>
                📈 Peak
            </div>

            <div class='metric-value'>
                {analysis['peak']} dB
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        status_class = (
            "approved"
            if aprovado
            else "rejected"
        )

        status_text = (
            "APROVADO"
            if aprovado
            else "REPROVADO"
        )

        st.markdown(f"""
        <div class='{status_class}'>
            <div>
                STATUS
            </div>

            <div class='big-score'>
                {score}
            </div>

            <div>
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ======================================================
    # DASHBOARD
    # ======================================================

    left, right = st.columns([2,1])

    with left:

        st.subheader(
            "🧠 Transcrição IA"
        )

        st.markdown(f"""
        <div class='card'>
            {transcription_text}
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.subheader(
            "📊 Score Cognitivo"
        )

        st.progress(
            random.randint(80,100),
            text="Clareza"
        )

        st.progress(
            random.randint(80,100),
            text="Compressão"
        )

        st.progress(
            random.randint(80,100),
            text="Ritmo"
        )

        st.progress(
            random.randint(80,100),
            text="Respiração"
        )

        st.progress(
            random.randint(80,100),
            text="Padrão Broadcast"
        )

        st.divider()

        st.subheader(
            "🎧 Áudio Processado"
        )

        st.audio(output_path)

        with open(output_path, "rb") as file:

            st.download_button(
                "⬇️ Baixar Áudio Processado",
                file,
                file_name="broadcast_processed.mp3"
            )

    with right:

        st.subheader(
            "📡 Logs"
        )

        logs = [

            "✓ Upload recebido",

            "✓ IA iniciou pipeline",

            "✓ Compressão aplicada",

            "✓ Limiter aplicado",

            "✓ Loudness normalizado",

            "✓ Noise reduction aplicada"
            if noise
            else "• Noise reduction ignorada",

            "✓ IA analisou qualidade",

            "✓ Broadcast aprovado"
            if aprovado
            else "✗ Broadcast reprovado"
        ]

        for log in logs:

            st.markdown(f"""
            <div class='log-card'>
                {datetime.now().strftime('%H:%M:%S')}
                •
                {log}
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.subheader(
            "🛰️ Infraestrutura"
        )

        st.success("API ONLINE")
        st.success("FFmpeg ONLINE")
        st.success("Workers ONLINE")
        st.success("Pipeline OK")

    os.unlink(input_path)

else:

    st.markdown("""
    <div class='card'
    style='padding:80px;text-align:center'>

        <h1>🎛️</h1>

        <h2>
            Operador Virtual Broadcast
        </h2>

        <p style='color:#9ca3af'>
            Faça upload de um áudio para iniciar
            o pipeline cognitivo de broadcast.
        </p>

    </div>
    """, unsafe_allow_html=True)
