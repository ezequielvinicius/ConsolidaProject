import os
import tkinter as tk
from tkinter import filedialog
from typing import Set, Dict

class ProjectAnalyzer:
    """
    Analisa e consolida a estrutura e o conteúdo de um projeto em um único arquivo.
    """
    def __init__(self, project_path: str, output_filename: str):
        self.project_path = project_path
        self.output_filename = output_filename
        self.ignore_patterns: Dict[str, Set[str]] = {}
        self.code_extensions: Set[str] = set()

    def set_profiles(self, profiles: list[str]):
        """Define os perfis de arquivos a serem ignorados e incluídos."""
        self.ignore_patterns = {
            'dirs': {
                '.git', '__pycache__', 'venv', '.idea', '.vscode', 
                'coverage', '.pytest_cache', '.mypy_cache', 'logs', 
                'tmp', 'temp', 'build', 'dist', 'target', 'out', 'bin', 'obj',
            },
            'files': {
                'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', '.gitignore',
                '.dockerignore', 'requirements.txt', 'pipfile', 'pipfile.lock',
                'poetry.lock', 'readme.md', 'license', 'changelog.md',
                'contributing.md', 'makefile', 'dockerfile', 'docker-compose.yml',
                'docker-compose.yaml',
            },
            'extensions': {
                '.log', '.tmp', '.cache', '.lock', '.pid', '.swp', '.swo',
                '.DS_Store', 'Thumbs.db', '.ico', '.png', '.jpg', '.jpeg', 
                '.gif', '.svg', '.webp', '.pdf', '.zip', '.tar', '.gz',
                '.exe', '.dll', '.so', '.dylib', '.deb', '.rpm',
                '.map', '.min.js', '.min.css',
            },
        }

        self.code_extensions = {
            # Web geral
            '.html', '.css', '.scss', '.sass', '.js', '.jsx', '.ts', '.tsx',
            '.vue', '.svelte', '.astro', '.json', '.yaml', '.yml', '.md',
            # Backend
            '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.rb', '.go',
            '.rs', '.swift', '.kt', '.scala', '.sh', '.bash', '.ps1', '.bat',
            '.cmd', '.sql', '.toml', '.ini',
        }

        if 'php' in profiles:
            self._add_php_patterns()
        if 'react' in profiles:
            self._add_react_patterns()
        if 'spring' in profiles:
            self._add_spring_patterns()

    def _add_php_patterns(self):
        """Adiciona padrões específicos de PHP."""
        self.ignore_patterns['dirs'].update({
            'vendor', 'storage/logs', 'storage/framework/cache',
            'storage/framework/sessions', 'storage/framework/views',
            'bootstrap/cache',
        })
        self.ignore_patterns['files'].update({
            'composer.json', 'composer.lock', 'composer.phar', 'phpunit.xml', 
            'phpunit.xml.dist', '.phpunit.result.cache', 'artisan', 
            'server.php', '.htaccess', 'web.config',
            '.env', '.env.local', '.env.example', '.env.testing',
            '.env.production', '.env.staging',
        })
        self.ignore_patterns['extensions'].add('.phar')
        self.code_extensions.update({'.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps'})
        
    def _add_react_patterns(self):
        """Adiciona padrões específicos de React e Node."""
        self.ignore_patterns['dirs'].update({'node_modules', '.next', '.nuxt', 'out', 'dist'})
        self.ignore_patterns['files'].update({
            'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            'webpack.config.js', 'vite.config.js', 'rollup.config.js',
            'babel.config.js', '.babelrc', 'tsconfig.json', 'jsconfig.json',
            'eslint.config.js', '.eslintrc', '.prettierrc', 'jest.config.js',
            'vitest.config.js',
        })

    def _add_spring_patterns(self):
        """Adiciona padrões específicos de Spring Boot e Java."""
        self.ignore_patterns['dirs'].update({'target', 'bin', 'obj'})
        self.ignore_patterns['files'].update({
            'pom.xml', 'build.gradle', 'mvnw', 'mvnw.cmd', 'gradlew', 
            'gradlew.bat', 'gradle-wrapper.jar',
        })
        self.code_extensions.update({'.java', '.xml', '.properties', '.sql'})
        
    def _should_ignore_file(self, file_name: str, relative_path: str) -> bool:
        """Verifica se um arquivo deve ser ignorado."""
        lower_name = file_name.lower()
        
        # Ignora arquivos baseados na lista de exclusão
        if lower_name in self.ignore_patterns['files']:
            return True
        
        # Ignora arquivos com extensões de exclusão
        _, ext = os.path.splitext(lower_name)
        if ext in self.ignore_patterns['extensions']:
            return True
            
        # Ignora arquivos que começam com ponto (exceto alguns)
        if lower_name.startswith('.') and lower_name not in ['.gitkeep', '.htaccess']:
            return True
        
        # Ignora arquivos que estão em pastas de exclusão
        for pattern in self.ignore_patterns['dirs']:
            # Lida com casos como 'storage/logs'
            if pattern in relative_path.replace(os.sep, '/'):
                return True
        
        return False

    def _generate_tree(self) -> str:
        """Gera a árvore de diretórios em estilo 'tree'."""
        lines = []
        for root, dirs, files in os.walk(self.project_path):
            relative_path = os.path.relpath(root, self.project_path)

            # Filtra diretórios a serem ignorados
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns['dirs'] and not self._should_ignore_file(d, os.path.join(relative_path, d))]
            
            level = relative_path.count(os.sep)
            indent = "│   " * level
            
            dir_name = os.path.basename(root)
            if root != self.project_path:
                lines.append(f"{indent}├── {dir_name}")
            
            sub_indent = "│   " * (level + 1)
            
            # Filtra arquivos a serem ignorados
            filtered_files = [f for f in files if not self._should_ignore_file(f, os.path.join(relative_path, f))]

            for file in filtered_files:
                lines.append(f"{sub_indent}└── {file}")
                
        return "\n".join(lines)

    def _consolidate_code(self) -> str:
        """Consolida o conteúdo dos arquivos de código."""
        content = []
        for root, dirs, files in os.walk(self.project_path):
            relative_path = os.path.relpath(root, self.project_path)

            # Filtra diretórios a serem ignorados
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns['dirs'] and not self._should_ignore_file(d, os.path.join(relative_path, d))]

            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.project_path)
                _, ext = os.path.splitext(file)

                # Pula arquivos ignorados ou que não são de código
                if self._should_ignore_file(file, rel_path) or ext.lower() not in self.code_extensions:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read().strip()
                        if file_content:
                            content.append(f"### `{rel_path}`\n\n```\n{file_content}\n```\n")
                except (IOError, OSError):
                    # Ignora arquivos binários ou sem permissão
                    pass

        return "\n".join(content)

    def generate_report(self):
        """Gera o arquivo de relatório final em Markdown."""
        if not os.path.isdir(self.project_path):
            print("Caminho do projeto inválido.")
            return

        print("Gerando estrutura e conteúdo do projeto...")
        tree = self._generate_tree()
        code_content = self._consolidate_code()

        with open(self.output_filename, 'w', encoding='utf-8') as out:
            out.write("# Análise de Projeto\n\n")
            out.write("## Estrutura de Pastas\n\n```\n")
            out.write(tree)
            out.write("```\n\n")
            out.write("---")
            out.write("\n\n## Conteúdo dos Arquivos de Código\n\n")
            out.write(code_content)

        print(f"Arquivo '{self.output_filename}' gerado com sucesso!")
        print("Pastas e arquivos de dependência e build foram ignorados.")

# --- Execução Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    project_folder = filedialog.askdirectory(title="Selecione a pasta do projeto")
    
    if project_folder:
        # Perfis: use uma lista para habilitar o que for necessário.
        # Ex: ['php', 'react', 'spring']
        analyzer = ProjectAnalyzer(project_folder, "projeto_unificado.md")
        analyzer.set_profiles(['react', 'spring', 'php']) 
        analyzer.generate_report()
    else:
        print("Nenhuma pasta selecionada. Encerrando o programa.")