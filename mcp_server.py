from fastmcp import FastMCP

from src.config.settings import get_settings
from src.services.chunker import TextChunker
from src.services.pdf_extractor import PDFExtractor
from src.services.pipeline import PDFSummaryPipeline


mcp = FastMCP("PDF Summarizer MCP")


@mcp.tool()
def extrair_texto_pdf(caminho_pdf: str) -> str:
    """Extrai texto selecionavel de um arquivo PDF."""

    extractor = PDFExtractor()
    return extractor.extract_text(caminho_pdf)


@mcp.tool()
def resumir_pdf(caminho_pdf: str) -> dict:
    """Executa o pipeline completo de sumarizacao de PDF."""

    pipeline = PDFSummaryPipeline()
    result = pipeline.run(caminho_pdf)
    return {
        "pdf_path": result["pdf_path"],
        "file_name": result["file_name"],
        "total_pages": result["total_pages"],
        "total_characters": result["total_characters"],
        "total_chunks": result["total_chunks"],
        "final_summary": result["final_summary"],
        "partial_summaries": result["partial_summaries"],
    }


@mcp.tool()
def dividir_texto_em_chunks(texto: str, limite: int = 4000) -> list[str]:
    """Divide um texto em chunks usando o limite informado."""

    settings = get_settings()
    chunker = TextChunker(limite or settings.chunk_size)
    return chunker.split(texto)


if __name__ == "__main__":
    mcp.run()
