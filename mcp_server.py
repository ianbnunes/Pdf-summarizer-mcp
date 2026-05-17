from fastmcp import FastMCP

from src.config.settings import get_settings
from src.services.chunker import TextChunker
from src.services.pdf_extractor import PDFExtractor
from src.services.pipeline import PDFSummaryPipeline


mcp = FastMCP("PDF Summarizer MCP")


@mcp.tool()
def extrair_texto_pdf(caminho_pdf: str) -> str:
    """
    Extrai o texto selecionável de um arquivo PDF usando PyMuPDF.

    Use esta ferramenta quando o usuário quiser:
    - visualizar o texto bruto extraído de um PDF;
    - verificar se um PDF possui texto selecionável;
    - analisar o conteúdo textual antes de gerar um resumo;
    - depurar problemas de extração textual.

    Parâmetros:
    - caminho_pdf: caminho local do arquivo PDF que será processado.

    Retorno:
    - Uma string contendo o texto extraído do PDF, organizado por páginas.
    - Cada página pode ser identificada no texto retornado por marcações como:
      "--- Página 1 ---".

    Observações:
    - Esta ferramenta não realiza OCR.
    - Caso o PDF seja escaneado ou composto apenas por imagens, o texto extraído
      poderá estar vazio ou incompleto.
    - Se o texto retornado for muito pequeno, é provável que o documento precise
      de uma etapa futura de OCR.
    """

    extractor = PDFExtractor()
    return extractor.extract_text(caminho_pdf)


@mcp.tool()
def resumir_pdf(caminho_pdf: str) -> dict:
    """
    Executa o pipeline completo de sumarização inteligente de um documento PDF.

    Use esta ferramenta quando o usuário quiser:
    - gerar um resumo completo de um PDF;
    - obter uma visão geral rápida do conteúdo de um documento;
    - resumir artigos, relatórios, materiais acadêmicos ou documentos técnicos;
    - testar o fluxo completo do sistema de TCC;
    - demonstrar a integração entre PyMuPDF, limpeza textual, chunking e LLM.

    Fluxo executado:
    1. Abre o arquivo PDF informado.
    2. Extrai o texto selecionável usando PyMuPDF.
    3. Limpa o texto extraído, removendo ruídos simples.
    4. Divide o conteúdo em chunks menores.
    5. Gera resumos parciais para cada chunk.
    6. Combina os resumos parciais em um resumo final estruturado.

    Parâmetros:
    - caminho_pdf: caminho local do arquivo PDF que será resumido.

    Retorno:
    Um dicionário contendo:
    - pdf_path: caminho original do arquivo PDF;
    - file_name: nome do arquivo processado;
    - total_pages: quantidade de páginas identificadas no PDF;
    - total_characters: quantidade total de caracteres extraídos;
    - total_chunks: quantidade de blocos textuais gerados;
    - final_summary: resumo final consolidado;
    - partial_summaries: lista com os resumos parciais de cada chunk.

    Observações:
    - Esta ferramenta é indicada para PDFs com texto selecionável.
    - Esta versão não executa OCR.
    - Para PDFs escaneados, o resultado pode ser vazio ou insuficiente.
    - O resumo deve ser interpretado como apoio à leitura, não como substituto
      da análise completa do documento.
    """

    pipeline = PDFSummaryPipeline()
    result = pipeline.run(caminho_pdf)

    return {
        "pdf_path": result["pdf_path"],
        "file_name": result["file_name"],
        "total_pages": result["total_pages"],
        "total_characters": result["total_characters"],
        "total_chunks": result["total_chunks"],
        "final_summary": result["final_summary"],
        "partial_summaries": result["partial_summaries"],
    }


@mcp.tool()
def dividir_texto_em_chunks(texto: str, limite: int = 4000) -> list[str]:
    """
    Divide um texto longo em blocos menores chamados chunks.

    Use esta ferramenta quando o usuário quiser:
    - dividir um texto grande antes de enviar para um LLM;
    - testar a etapa de chunking isoladamente;
    - verificar como o sistema segmenta documentos longos;
    - preparar textos extensos para sumarização parcial;
    - evitar ultrapassar limites de contexto do modelo de linguagem.

    Parâmetros:
    - texto: conteúdo textual que será dividido.
    - limite: número máximo aproximado de caracteres por chunk.
      Caso não seja informado, será usado o valor padrão configurado no sistema.

    Retorno:
    - Uma lista de strings.
    - Cada item da lista representa um chunk textual.

    Comportamento esperado:
    - A divisão tenta preservar parágrafos sempre que possível.
    - O objetivo é evitar cortes bruscos no meio de ideias ou frases.
    - Textos pequenos retornam uma lista com apenas um chunk.

    Observações:
    - Esta ferramenta não gera resumo.
    - Esta ferramenta apenas prepara o texto para processamento posterior.
    - Para gerar um resumo completo de PDF, use a ferramenta resumir_pdf.
    """

    settings = get_settings()
    chunker = TextChunker(limite or settings.chunk_size)
    return chunker.split(texto)


if __name__ == "__main__":
    mcp.run()
