from openai import OpenAI

from src.config.settings import get_settings


class Summarizer:
    """Gera resumos de chunks e documentos completos usando a OpenAI API."""

    def __init__(self, model: str | None = None) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY não configurada. Crie um arquivo .env com sua chave."
            )

        self.model = model or settings.openai_model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def summarize_chunk(self, chunk: str) -> str:
        """Gera um resumo fiel em portugues para um trecho do documento."""

        prompt = (
            "Resuma o trecho a seguir em português, com linguagem acadêmica clara. "
            "Preserve os conceitos principais, não invente informações, não adicione "
            "fatos externos e mantenha fidelidade ao texto original.\n\n"
            f"Trecho:\n{chunk}"
        )

        return self._request_summary(prompt)

    def summarize_document(self, chunks: list[str]) -> str:
        """Combina resumos parciais em um resumo final estruturado."""

        partial_summaries = "\n\n".join(
            f"Resumo parcial {index}:\n{summary}"
            for index, summary in enumerate(chunks, start=1)
        )
        prompt = (
            "Com base nos resumos parciais abaixo, gere um resumo final estruturado "
            "em português, com linguagem acadêmica clara, sem inventar informações "
            "e sem acrescentar fatos externos. Organize exatamente nas secoes:\n"
            "1. Tema central\n"
            "2. Principais pontos\n"
            "3. Conclusao geral\n\n"
            f"Resumos parciais:\n{partial_summaries}"
        )

        return self._request_summary(prompt)

    def _request_summary(self, prompt: str) -> str:
        """Envia uma solicitacao de sumarizacao ao modelo configurado."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente acadêmico especializado em resumir "
                        "documentos com fidelidade ao conteudo original."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()
