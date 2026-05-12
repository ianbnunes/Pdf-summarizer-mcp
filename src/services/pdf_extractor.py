from pathlib import Path

import fitz


class PDFExtractor:
    """Extrai texto selecionavel de documentos PDF usando PyMuPDF."""

    MIN_TEXT_LENGTH = 20

    def extract_text(self, pdf_path: str) -> str:
        """Extrai o texto de todas as paginas de um PDF.

        Args:
            pdf_path: Caminho local do arquivo PDF.

        Returns:
            Texto extraido com marcadores de pagina.

        Raises:
            FileNotFoundError: Quando o arquivo informado nao existe.
            ValueError: Quando o PDF nao possui texto selecionavel suficiente.
            RuntimeError: Quando o arquivo nao pode ser lido como PDF.
        """

        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo PDF nao encontrado: {pdf_path}")

        try:
            with fitz.open(path) as pdf_document:
                pages_text: list[str] = []

                for page_index, page in enumerate(pdf_document, start=1):
                    page_text = page.get_text("text").strip()
                    pages_text.append(f"--- Página {page_index} ---\n{page_text}")

        except Exception as exc:
            raise RuntimeError(f"Nao foi possivel ler o arquivo PDF: {exc}") from exc

        full_text = "\n\n".join(pages_text).strip()
        text_without_markers = "\n".join(
            line for line in full_text.splitlines() if not line.startswith("--- Página")
        ).strip()

        if len(text_without_markers) < self.MIN_TEXT_LENGTH:
            raise ValueError(
                "Este PDF parece não possuir texto selecionável. "
                "Uma versão futura poderá incluir OCR."
            )

        return full_text

    def count_pages(self, pdf_path: str) -> int:
        """Conta o total de paginas de um arquivo PDF."""

        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo PDF nao encontrado: {pdf_path}")

        with fitz.open(path) as pdf_document:
            return pdf_document.page_count
