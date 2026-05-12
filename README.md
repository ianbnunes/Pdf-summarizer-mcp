# PDF Summarizer MCP

Projeto MVP para o TCC **"Sumarizacao Inteligente de Documentos PDF com Modelos de Linguagem (LLMs)"**.

A solucao recebe arquivos PDF com texto selecionavel, extrai o conteudo com PyMuPDF, limpa e segmenta o texto em chunks, gera resumos com LLMs pela OpenAI API, expoe ferramentas via FastMCP e oferece uma interface web simples em Streamlit.

> Nesta primeira versao nao ha OCR. PDFs escaneados ou baseados apenas em imagem nao serao processados.

## Tecnologias

- Python
- PyMuPDF
- Streamlit
- FastMCP
- OpenAI API
- python-dotenv
- pytest

## Estrutura do projeto

```text
pdf-summarizer-mcp/
├── app.py
├── mcp_server.py
├── main.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── domain/
│   ├── services/
│   ├── repositories/
│   └── config/
├── data/
│   ├── uploads/
│   └── summaries/
└── tests/
```

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
CHUNK_SIZE=4000
```

## Executar com Streamlit

```bash
streamlit run app.py
```

A interface permite enviar um PDF, gerar o resumo, visualizar os metadados, os resumos parciais e o texto extraido.

## Executar o servidor MCP

```bash
python mcp_server.py
```

Ferramentas expostas:

- `extrair_texto_pdf(caminho_pdf: str) -> str`
- `resumir_pdf(caminho_pdf: str) -> dict`
- `dividir_texto_em_chunks(texto: str, limite: int = 4000) -> list[str]`

## Executar via terminal

```bash
python main.py caminho/do/arquivo.pdf
```

O script imprime o nome do arquivo, o total de chunks e o resumo final.

## Relação com o TCC

O projeto adapta a arquitetura de um sistema ETL com agente IA e servidor MCP para o dominio de documentos PDF. Em vez de coletar e transformar dados estruturados, a aplicacao processa texto nao estruturado de PDFs e utiliza LLMs para produzir resumos academicos, mantendo separacao clara entre dominio, servicos, interface e exposicao de ferramentas.

## Limitações da versão atual

- Nao implementa OCR.
- Processa apenas PDFs com texto selecionavel.
- Depende da OpenAI API para gerar resumos.
- Nao avalia automaticamente a qualidade dos resumos.

Quando um PDF nao possui texto selecionavel, a aplicacao informa que uma versao futura podera incluir OCR.

## Trabalhos futuros

- OCR para PDFs escaneados.
- RAG com banco vetorial.
- Avaliacao automatica dos resumos.
- Historico com SQLite.
- Comparacao entre modelos LLM.

## Testes

```bash
pytest
```
