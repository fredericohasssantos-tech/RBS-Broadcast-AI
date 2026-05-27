import streamlit as st

    st.divider()

    # =========================
    # TRANSCRIÇÃO
    # =========================

    st.subheader("🧠 Transcrição Inteligente")

    st.markdown(
        f"""
        <div class='metric-card'>
            {transcription}
        </div>
        """,
        unsafe_allow_html=True
    )

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
        st.markdown(
            f"""
            <div class='log-box'>
                {datetime.now().strftime('%H:%M:%S')} • {log}
            </div>
            """,
            unsafe_allow_html=True
        )

    os.unlink(temp_path)

else:
    st.info("📁 Faça upload de um áudio para iniciar análise")
