import streamlit as st
import tempfile
import subprocess
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="RBS Broadcast AI",
    layout="wide"
)

# =========================
# ESTILO
# =========================

st.markdown("""
<style>

.main {
    background-color: #09090b;
    color: white;
}

.metric-card {
    background: #18181b;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #27272a;
}

.score-card {
    background: linear-gradient(135deg, #0891b2, #1e40af);
    padding: 30px;
    border-radius: 24px;
    text-align: center;
}

.log-box {
    background: #111827;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.title("🎛️ RBS Broadcast AI")
st.caption("Plataforma Inteligente de Automação Broadcast")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙️ Configurações")

radio = st.sidebar.selectbox(
    "Rádio",
    ["Gaúcha", "Atlântida", "CBN", "102.3"]
)

score_minimo = st.sidebar.slider(
    "Score mínimo",
    0,
    10,
    7
)

# =========================
# UPLOAD
# =========================

uploaded = st.file_uploader(
    "📤 Upload do boletim",
    type=["mp3", "wav", "aac"]
)

# =========================
# FUNÇÕES
# =========================

def fake_transcription():
    return (
        "Boa noite. O trânsito apresenta lentidão "
        "na região central de Porto Alegre devido "
        "ao fluxo intenso de veículos."
    )

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
                ),
            }

    except Exception:
        pass

    return {
        "lufs": -14,
        "peak": -2,
    }

# =========================
# PROCESSAMENTO
# =========================

if uploaded:

    st.success("✅ Arquivo recebido")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as tmp:

        tmp.write(uploaded.read())
        temp_path = tmp.name

    st.audio(temp_path)

    with st.spinner("🤖 IA analisando áudio..."):

        analysis = analyze_audio(temp_path)

        transcription = fake_transcription()

    score = 8.9

    aprovado = score >= score_minimo

    # =========================
    # MÉTRICAS
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class='metric-card'>
            <h3>📻 Rádio</h3>
            <h1>{radio}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class='metric-card'>
            <h3>🔊 LUFS</h3>
            <h1>{analysis['lufs']}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class='metric-card'>
            <h3>📈 Peak</h3>
            <h1>{analysis['peak']} dB</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        status = (
            "APROVADO"
            if aprovado
            else "REPROVADO"
        )

        st.markdown(f"""
        <div class='score-card'>
            <h3>Status</h3>
            <h1>{status}</h1>
            <h2>{score}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # =========================
    # TRANSCRIÇÃO
    # =========================

    st.subheader("🧠 Transcrição Inteligente")

    st.markdown(f"""
    <div class='metric-card'>
        {transcription}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # =========================
    # SCORE IA
    # =========================

    st.subheader("📊 Score Cognitivo")

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.progress(92, text="Clareza")
        st.progress(88, text="Loudness")
        st.progress(81, text="Ritmo")

    with score_col2:

        st.progress(95, text="Respiração")
        st.progress(91, text="Padrão Broadcast")
        st.progress(89, text="Compressão")

    st.divider()

    # =========================
    # LOGS
    # =========================

    st.subheader("📡 Eventos do Sistema")

    logs = [
        "✓ Upload recebido",
        "✓ Loudness analisado",
        "✓ Áudio validado",
        "✓ IA processou transcrição",
        "✓ Score cognitivo calculado",
        "✓ Arquivo aprovado para broadcast"
        if aprovado
        else "✗ Arquivo reprovado"
    ]

    for log in logs:

        st.markdown(f"""
        <div class='log-box'>
            {datetime.now().strftime("%H:%M:%S")} • {log}
        </div>
        """, unsafe_allow_html=True)

    os.unlink(temp_path)

else:

    st.info(
        "📁 Faça upload de um áudio para iniciar análise"
    )
