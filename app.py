from pathlib import Path

import streamlit as st

from src.services.pipeline import PDFSummaryPipeline


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


st.set_page_config(
    page_title="Sumarizacao Inteligente de PDFs",
    layout="wide",
)

st.title("Sumarização Inteligente de Documentos PDF com LLMs")

uploaded_file = st.file_uploader("Selecione um arquivo PDF", type=["pdf"])

if uploaded_file is not None:
    pdf_path = UPLOAD_DIR / uploaded_file.name
    pdf_path.write_bytes(uploaded_file.getbuffer())

    st.success(f"Arquivo enviado: {uploaded_file.name}")

    if st.button("Gerar resumo", type="primary"):
        with st.spinner("Processando PDF e gerando resumo..."):
            try:
                pipeline = PDFSummaryPipeline()
                result = pipeline.run(str(pdf_path))

                st.subheader("Resumo final")
                st.write(result["final_summary"])

                col1, col2 = st.columns(2)
                col1.metric("Chunks", result["total_chunks"])
                col2.metric("Caracteres", result["total_characters"])

                with st.expander("Resumos parciais"):
                    for index, summary in enumerate(result["partial_summaries"], start=1):
                        st.markdown(f"**Resumo parcial {index}**")
                        st.write(summary)

                with st.expander("Texto extraido"):
                    st.text(result["extracted_text"])

            except ValueError as exc:
                st.warning(str(exc))
            except FileNotFoundError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Ocorreu um erro ao processar o PDF: {exc}")
else:
    st.info("Envie um PDF com texto selecionável para iniciar.")
