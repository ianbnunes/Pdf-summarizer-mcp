import argparse
from pathlib import Path

from src.services.pipeline import PDFSummaryPipeline


def main() -> None:
    """Executa a sumarizacao de um PDF via terminal."""

    parser = argparse.ArgumentParser(
        description="Sumariza um documento PDF com texto selecionável."
    )
    parser.add_argument("pdf_path", help="Caminho do arquivo PDF")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)

    try:
        pipeline = PDFSummaryPipeline()
        result = pipeline.run(str(pdf_path))
    except Exception as exc:
        print(f"Erro ao processar PDF: {exc}")
        raise SystemExit(1) from exc

    print(f"Arquivo: {result['file_name']}")
    print(f"Total de chunks: {result['total_chunks']}")
    print("\nResumo final:\n")
    print(result["final_summary"])


if __name__ == "__main__":
    main()
