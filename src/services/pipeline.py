from pathlib import Path

from src.config.settings import get_settings
from src.domain.document import Document
from src.domain.summary import SummaryResult
from src.services.chunker import TextChunker
from src.services.pdf_extractor import PDFExtractor
from src.services.summarizer import Summarizer
from src.services.text_cleaner import TextCleaner


class PDFSummaryPipeline:
    """Orquestra extracao, limpeza, segmentacao e sumarizacao de PDFs."""

    def __init__(
        self,
        extractor: PDFExtractor | None = None,
        cleaner: TextCleaner | None = None,
        chunker: TextChunker | None = None,
        summarizer: Summarizer | None = None,
    ) -> None:
        settings = get_settings()
        self.extractor = extractor or PDFExtractor()
        self.cleaner = cleaner or TextCleaner()
        self.chunker = chunker or TextChunker(settings.chunk_size)
        self.summarizer = summarizer or Summarizer()

    def run(self, pdf_path: str) -> dict:
        """Executa o pipeline completo de sumarizacao."""

        path = Path(pdf_path)
        extracted_text = self.extractor.extract_text(pdf_path)
        total_pages = self.extractor.count_pages(pdf_path)
        cleaned_text = self.cleaner.clean(extracted_text)
        chunks = self.chunker.split(cleaned_text)

        if not chunks:
            raise ValueError(
                "Este PDF parece não possuir texto selecionável. "
                "Uma versão futura poderá incluir OCR."
            )

        partial_summaries = [
            self.summarizer.summarize_chunk(chunk) for chunk in chunks
        ]
        final_summary = self.summarizer.summarize_document(partial_summaries)

        document = Document(
            file_path=str(path),
            file_name=path.name,
            extracted_text=cleaned_text,
            total_pages=total_pages,
            total_characters=len(cleaned_text),
        )
        summary = SummaryResult(
            file_name=path.name,
            total_chunks=len(chunks),
            partial_summaries=partial_summaries,
            final_summary=final_summary,
        )

        return {
            "pdf_path": document.file_path,
            "file_name": document.file_name,
            "extracted_text": document.extracted_text,
            "total_pages": document.total_pages,
            "total_characters": document.total_characters,
            "total_chunks": summary.total_chunks,
            "partial_summaries": summary.partial_summaries,
            "final_summary": summary.final_summary,
        }
