import json
from datetime import datetime
from pathlib import Path


class SummaryRepository:
    """Persistencia simples de resumos em arquivos JSON."""

    def __init__(self, output_dir: str = "data/summaries") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, result: dict) -> Path:
        """Salva um resultado de sumarizacao em disco."""

        file_stem = Path(result.get("file_name", "summary")).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"{file_stem}_{timestamp}.json"

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)

        return output_path
