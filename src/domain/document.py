from dataclasses import dataclass


@dataclass
class Document:
    """Representa um documento PDF processado pela aplicacao."""

    file_path: str
    file_name: str
    extracted_text: str
    total_pages: int | None
    total_characters: int
