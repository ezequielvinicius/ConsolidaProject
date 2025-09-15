# Projeto: Consolidador de Projeto em Arquivo Único

Este script em **Python** gera um único arquivo de texto contendo: 1.
**Estrutura de pastas** do projeto, no estilo do comando `tree`. 2.
**Conteúdo completo** de cada arquivo de texto presente na pasta
selecionada.

## ✨ Funcionalidades

-   Geração da árvore de diretórios ignorando pastas comuns como `.git`,
    `node_modules`, `__pycache__`, `venv` e `.idea`.
-   Consolidação de todo o conteúdo dos arquivos de texto em um único
    arquivo `projeto_unificado.txt`.
-   Interface gráfica simples para seleção da pasta do projeto usando
    `tkinter`.

## 🚀 Como Usar

1.  Certifique-se de ter o **Python 3** instalado.

2.  Instale as dependências padrão (nenhuma dependência externa além do
    Python).

3.  Execute o script:

    ``` bash
    python nome_do_script.py
    ```

4.  Escolha a pasta do projeto quando a janela de seleção abrir.

5.  O arquivo `projeto_unificado.txt` será gerado na mesma pasta onde o
    script foi executado.

## 📂 Estrutura do Código

-   `gerar_arvore(caminho_base)`: Gera a árvore de diretórios em formato
    de texto.
-   `consolidar_projeto(caminho_projeto, arquivo_saida)`: Cria o arquivo
    consolidado com a estrutura e o conteúdo dos arquivos.
-   `escolher_pasta()`: Abre a janela para seleção da pasta via
    `tkinter`.

## 🛡️ Observações

-   Arquivos binários são ignorados automaticamente para evitar erros de
    leitura.
-   O script mantém a formatação do conteúdo original dos arquivos de
    texto.

## 📝 Licença

Este projeto está licenciado sob a licença MIT. Sinta-se à vontade para
usar e modificar.
