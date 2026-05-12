from dataclasses import dataclass


@dataclass
class SummaryResult:
    """Representa o resultado da sumarizacao de um documento."""

    file_name: str
    total_chunks: int
    partial_summaries: list[str]
    final_summary: str
