import re


class TextChunker:
    """Divide textos longos em blocos menores para envio ao LLM."""

    def __init__(self, max_characters: int = 4000) -> None:
        if max_characters <= 0:
            raise ValueError("O limite de caracteres deve ser maior que zero.")
        self.max_characters = max_characters

    def split(self, text: str) -> list[str]:
        """Divide o texto preservando paragrafos sempre que possivel."""

        cleaned_text = text.strip()
        if not cleaned_text:
            return []

        paragraphs = [paragraph.strip() for paragraph in re.split(r"\n{2,}", cleaned_text)]
        chunks: list[str] = []
        current_chunk = ""

        for paragraph in paragraphs:
            if not paragraph:
                continue

            if len(paragraph) > self.max_characters:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                chunks.extend(self._split_large_paragraph(paragraph))
                continue

            candidate = f"{current_chunk}\n\n{paragraph}".strip()
            if len(candidate) <= self.max_characters:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_large_paragraph(self, paragraph: str) -> list[str]:
        """Divide paragrafos grandes tentando preservar frases."""

        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        chunks: list[str] = []
        current_chunk = ""

        for sentence in sentences:
            if len(sentence) > self.max_characters:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                chunks.extend(self._hard_split(sentence))
                continue

            candidate = f"{current_chunk} {sentence}".strip()
            if len(candidate) <= self.max_characters:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _hard_split(self, text: str) -> list[str]:
        """Divide trechos que excedem o limite mesmo sem pontuacao."""

        return [
            text[index : index + self.max_characters].strip()
            for index in range(0, len(text), self.max_characters)
            if text[index : index + self.max_characters].strip()
        ]
