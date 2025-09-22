# ConsolidaProjeto

Uma ferramenta em Python para analisar e consolidar a estrutura e conteúdo de projetos de desenvolvimento em um único arquivo Markdown.

## Funcionalidades

- **Análise de estrutura**: Gera uma árvore visual da estrutura de diretórios do projeto
- **Consolidação de código**: Extrai e organiza o conteúdo de todos os arquivos de código em um documento único
- **Perfis personalizáveis**: Suporte para diferentes tipos de projeto (PHP, React, Spring Boot)
- **Filtros inteligentes**: Ignora automaticamente arquivos e pastas de dependências, build e cache
- **Interface gráfica**: Seleção de pasta através de dialog box

## Requisitos

- Python 3.6+
- Tkinter (geralmente incluído com Python)

## Como usar

### Execução simples

```bash
python project_analyzer.py
```

1. Execute o script
2. Selecione a pasta do projeto através da interface gráfica
3. O arquivo `projeto_unificado.md` será gerado no diretório atual

### Uso programático

```python
from project_analyzer import ProjectAnalyzer

# Criar instância do analisador
analyzer = ProjectAnalyzer("/caminho/do/projeto", "relatorio.md")

# Configurar perfis do projeto
analyzer.set_profiles(['react', 'php'])

# Gerar relatório
analyzer.generate_report()
```

## Perfis suportados

### React/Node.js (`'react'`)
- Ignora: `node_modules`, `.next`, `dist`, `package-lock.json`
- Inclui: `.js`, `.jsx`, `.ts`, `.tsx`, `.json`, `.md`

### PHP (`'php'`)
- Ignora: `vendor`, `storage/logs`, `composer.lock`, `.env`
- Inclui: `.php`, `.phtml`, arquivos de configuração

### Spring Boot (`'spring'`)
- Ignora: `target`, `bin`, `pom.xml`, `mvnw`
- Inclui: `.java`, `.xml`, `.properties`, `.sql`

## Estrutura do arquivo gerado

O arquivo de saída contém:

```markdown
# Análise de Projeto

## Estrutura de Pastas
```
├── src/
│   ├── components/
│   └── pages/
└── package.json
```

---

## Conteúdo dos Arquivos de Código

### `src/App.js`
```
// Conteúdo do arquivo...
```
```

## Arquivos e pastas ignorados

### Diretórios gerais
- `.git`, `__pycache__`, `venv`, `.idea`, `.vscode`
- `node_modules`, `vendor`, `target`, `dist`, `build`
- `logs`, `tmp`, `cache`, `.pytest_cache`

### Arquivos gerais
- `package-lock.json`, `yarn.lock`, `.gitignore`
- `requirements.txt`, `composer.lock`
- Arquivos de configuração de IDE e build

### Extensões ignoradas
- `.log`, `.tmp`, `.cache`, `.lock`, `.pid`
- Imagens: `.png`, `.jpg`, `.svg`, `.ico`
- Arquivos binários: `.exe`, `.dll`, `.zip`
- Arquivos minificados: `.min.js`, `.min.css`

## Personalização

Para adicionar novos perfis ou modificar os existentes, edite os métodos `_add_*_patterns()` na classe `ProjectAnalyzer`.

### Exemplo: Adicionar suporte para Python/Django

```python
def _add_django_patterns(self):
    self.ignore_patterns['dirs'].update({
        '__pycache__', 'migrations', 'static/admin'
    })
    self.ignore_patterns['files'].update({
        'manage.py', 'db.sqlite3', 'settings.py'
    })
    self.code_extensions.update({'.py', '.html', '.css'})
```
## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

***

**Nota**: Esta ferramenta é ideal para documentação de projetos, revisões de código, backup de desenvolvimento ou preparação de contexto para LLMs e assistentes de código.
