import os
import tkinter as tk
from tkinter import filedialog

def gerar_arvore(caminho_base):
    """Gera a árvore de diretórios no estilo 'tree'."""
    linhas = []
    for root, dirs, files in os.walk(caminho_base):
        # Ignorar pastas indesejadas
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__', 'venv', '.idea')]
        nivel = root.replace(caminho_base, "").count(os.sep)
        indent = "│   " * nivel
        pasta = os.path.basename(root)
        if pasta:  # não mostra linha vazia para a raiz
            linhas.append(f"{indent}├── {pasta}")
        sub_indent = "│   " * (nivel + 1)
        for f in files:
            linhas.append(f"{sub_indent}└── {f}")
    return "\n".join(linhas)

def consolidar_projeto(caminho_projeto, arquivo_saida="projeto_unificado.txt"):
    with open(arquivo_saida, 'w', encoding='utf-8') as out:
        # 1️⃣ Estrutura completa do sistema
        out.write("### Estrutura de pastas\n\n")
        out.write(gerar_arvore(caminho_projeto))
        out.write("\n\n### Conteúdo dos arquivos\n\n")

        # 2️⃣ Conteúdo de cada arquivo
        for root, dirs, files in os.walk(caminho_projeto):
            dirs[:] = [d for d in dirs if d not in ('.git','node_modules','__pycache__','venv','.idea')]
            for file in files:
                caminho_completo = os.path.join(root, file)
                rel_path = os.path.relpath(caminho_completo, caminho_projeto)
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as f:
                        out.write(f"\n=== {rel_path} ===\n")
                        out.write(f.read())
                        out.write("\n\n")
                except UnicodeDecodeError:
                    out.write(f"\n=== {rel_path} (binário ignorado) ===\n")

def escolher_pasta():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Selecione a pasta do projeto")

if __name__ == "__main__":
    pasta = escolher_pasta()
    if pasta:
        consolidar_projeto(pasta)
        print("Arquivo 'projeto_unificado.txt' gerado com sucesso!")
    else:
        print("Nenhuma pasta selecionada.")
