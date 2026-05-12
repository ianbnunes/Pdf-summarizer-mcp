from src.services.text_cleaner import TextCleaner


def test_text_cleaner_remove_espacos_extras() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean("Texto     com     muitos       espacos.")

    assert result == "Texto com muitos espacos."
