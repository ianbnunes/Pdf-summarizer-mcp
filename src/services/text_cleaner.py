import re


class TextCleaner:
    """Realiza limpeza simples no texto extraido do PDF."""

    def clean(self, text: str) -> str:
        """Remove espacos excessivos, quebras repetidas e residuos comuns."""

        if not text:
            return ""

        cleaned = text.replace("\x00", " ")
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r" *\n *", "\n", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        cleaned = re.sub(r"[_]{3,}", "", cleaned)
        cleaned = re.sub(r"[-]{4,}", "---", cleaned)

        return cleaned.strip()
