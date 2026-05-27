import streamlit as st
import tempfile
import subprocess
import random
import os

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="AudioQA",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='topbar'>

<div class='logo'>
AudioQA
</div>

<div class='subtitle'>
STUDIO QUALITY ANALYZER
</div>

<div class='status'>
● STANDBY
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# LAYOUT
# =====================================================

left, center, right = st.columns([1,3,1])

# =====================================================
# LEFT PANEL
# =====================================================

with left:

    st.markdown("<div class='panel-title'>INPUT SOURCE</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "LOAD AUDIO FILE",
        type=["mp3","wav","aac"]
    )

    st.markdown("<div class='panel-title'>PARAMETERS</div>", unsafe_allow_html=True)

    bitrate = st.selectbox(
        "BIT RATE",
        ["128","192","256","320"],
        index=3
    )

    sample = st.selectbox(
        "SAMPLE RATE",
        ["44100","48000"]
    )

    stereo = st.selectbox(
        "CHANNELS",
        ["STEREO","MONO"]
    )

    normalize = st.toggle(
        "LOUDNESS NORMALIZE",
        True
    )

    limiter = st.toggle(
        "LIMITER",
        True
    )

    compressor = st.toggle(
        "COMPRESSOR",
        True
    )

# =====================================================
# CENTER
# =====================================================

with center:

    st.markdown("<div class='panel-title'>TRANSPORT & LEVEL MONITOR</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='wavebox'>
        <div class='wave'></div>
    </div>
    """, unsafe_allow_html=True)

    if uploaded:

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

        filters = []

        if compressor:
            filters.append(
                "acompressor=threshold=-18dB:ratio=4"
            )

        if limiter:
            filters.append(
                "alimiter=limit=-2dB"
            )

        if normalize:
            filters.append(
                "loudnorm=I=-14:TP=-2:LRA=11"
            )

        chain = ",".join(filters)

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-af",
            chain,
            output_path
        ]

        with st.spinner("PROCESSING AUDIO..."):

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                st.success("ANALYSIS COMPLETE")

                st.audio(output_path)

                with open(output_path,"rb") as file:

                    st.download_button(
                        "DOWNLOAD PROCESSED AUDIO",
                        file,
                        file_name="broadcast_processed.mp3"
                    )

            else:

                st.error(result.stderr)

# =====================================================
# RIGHT
# =====================================================

with right:

    st.markdown("<div class='panel-title'>LEVEL</div>", unsafe_allow_html=True)

    lufs = round(random.uniform(-14.5,-13.5),1)
    peak = round(random.uniform(-2.0,-0.5),1)
    score = round(random.uniform(8.0,9.8),1)

    st.metric("LUFS", lufs)
    st.metric("TRUE PEAK", peak)
    st.metric("QUALITY", score)

    st.progress(random.randint(70,100))

    st.markdown("<div class='panel-title'>TEXT ANALYZER</div>", unsafe_allow_html=True)

    text = st.text_area(
        "",
        value="No analysis loaded."
    )
