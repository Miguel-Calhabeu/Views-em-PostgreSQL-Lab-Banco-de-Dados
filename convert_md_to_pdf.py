import os
import subprocess

def run():
    md_path = 'Relatorio_T5_Indices.md'
    temp_html_path = 'temp_corpo.html'
    html_path = 'Relatorio_T5_Indices.html'
    pdf_path = 'Relatorio_T5_Indices.pdf'
    screenshot_path = 'Relatorio_Screenshot.png'
    
    if not os.path.exists(md_path):
        print(f"Erro: {md_path} não encontrado!")
        return
        
    print("Processando conversão do Markdown para HTML robusto via npx marked...")
    try:
        subprocess.run([
            'npx', '-y', 'marked',
            '-i', md_path,
            '-o', temp_html_path,
            '--gfm'
        ], check=True)
    except Exception as e:
        print(f"Erro ao rodar npx marked: {e}")
        return

    if not os.path.exists(temp_html_path):
        print("Erro: Fragmento HTML temporário não foi gerado!")
        return

    with open(temp_html_path, 'r', encoding='utf-8') as f:
        html_body = f.read()

    try:
        os.remove(temp_html_path)
    except:
        pass

    # Injeta a regra CSS pre-wrap e break-word no @media print pre/code
    # Isso faz com que no PDF (versão impressa) o código quebre as linhas longas de forma elegante e nativa,
    # enquanto na tela (HTML) continua com scroll horizontal caso o usuário visualize na web
    css_style = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    @page {
        size: A4;
        margin: 20mm 15mm 20mm 15mm; /* Margens nativas reais repetidas em todas as páginas */
    }
    
    body {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
        padding: 40px 20px;
        background-color: #ffffff;
    }
    
    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 600;
        margin-top: 1.8em;
        margin-bottom: 0.6em;
        page-break-after: avoid; /* Evita quebra de página logo após títulos (órfãos) */
        break-after: avoid;
    }
    
    h1 {
        font-size: 2.2em;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 15px;
        margin-top: 0;
    }
    
    h2 {
        font-size: 1.6em;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 8px;
    }
    
    h3 {
        font-size: 1.25em;
    }
    
    p {
        margin-bottom: 1.2em;
        font-size: 1.05em;
        color: #334155;
    }
    
    strong {
        color: #0f172a;
        font-weight: 600;
    }
    
    code {
        font-family: 'JetBrains Mono', monospace;
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.9em;
    }
    
    pre {
        background-color: #0f172a;
        border-radius: 8px;
        padding: 20px;
        overflow-x: auto; /* Mantém o scroll horizontal elegante no navegador */
        margin: 1.5em 0;
        border: 1px solid #1e293b;
        page-break-inside: avoid; /* Evita quebrar blocos de código no meio */
        break-inside: avoid;
    }
    
    pre code {
        font-family: 'JetBrains Mono', monospace;
        background-color: transparent;
        color: #f8fafc;
        padding: 0;
        border-radius: 0;
        font-size: 0.95em;
        line-height: 1.5;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 2em 0;
        font-size: 1em;
        page-break-inside: avoid; /* Evita quebrar tabelas no meio */
        break-inside: avoid;
    }
    
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }
    
    th {
        background-color: #f8fafc;
        color: #0f172a;
        font-weight: 600;
    }
    
    tr:hover {
        background-color: #f8fafc;
    }
    
    hr {
        border: 0;
        border-top: 1px solid #e2e8f0;
        margin: 2.5em 0;
    }
    
    ul, ol {
        margin-bottom: 1.5em;
        padding-left: 20px;
        page-break-inside: avoid; /* Evita quebrar listas no meio se possível */
        break-inside: avoid;
    }
    
    li {
        margin-bottom: 0.6em;
        color: #334155;
    }
    
    a {
        color: #2563eb;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    @media print {
        body {
            padding: 0; /* Margem nativa do @page cuida do espaçamento em todas as folhas */
            max-width: 100%;
            font-size: 11pt;
            background-color: #ffffff;
        }
        
        pre {
            background-color: #f8fafc;
            color: #0f172a;
            border: 1px solid #e2e8f0;
            page-break-inside: avoid;
            break-inside: avoid;
            white-space: pre-wrap;       /* Força a quebra de linha de código longa no papel */
            word-wrap: break-word;       /* Força a quebra de palavras no limite lateral */
            overflow-x: visible;         /* Desativa scroll no PDF final */
        }
        
        pre code {
            color: #0f172a;
            white-space: pre-wrap;       /* Força o código interno a quebrar linha */
        }
        
        table {
            page-break-inside: avoid;
            break-inside: avoid;
        }
        
        tr, td, th {
            page-break-inside: avoid;
            break-inside: avoid;
        }
    }
    """
    
    html_content = f"""<!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório Técnico T5 — Índices em PostgreSQL</title>
        <style>
            {css_style}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML completo e validado gerado em: {html_path}")
    
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    # PDF
    try:
        subprocess.run([
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--print-to-pdf-no-header",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path
        ], check=True)
        print(f"PDF gerado com sucesso em: {pdf_path}")
    except Exception as e:
        print(f"Erro ao gerar o PDF com o Chrome: {e}")
        
    # Screenshot para validação visual total
    try:
        subprocess.run([
            chrome_path,
            "--headless",
            "--disable-gpu",
            f"--screenshot={screenshot_path}",
            "--window-size=1000,2000",
            html_path
        ], check=True)
        print(f"Screenshot gerado em: {screenshot_path}")
    except Exception as e:
        print(f"Erro ao gerar screenshot: {e}")

if __name__ == '__main__':
    run()
