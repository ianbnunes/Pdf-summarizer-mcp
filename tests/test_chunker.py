from src.services.chunker import TextChunker


def test_text_chunker_divide_textos_grandes() -> None:
    chunker = TextChunker(max_characters=50)
    text = "Primeira frase. " * 20

    chunks = chunker.split(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= 50 for chunk in chunks)


def test_text_chunker_retorna_chunk_para_texto_pequeno() -> None:
    chunker = TextChunker(max_characters=4000)

    chunks = chunker.split("Texto pequeno para teste.")

    assert len(chunks) == 1
    assert chunks[0] == "Texto pequeno para teste."
