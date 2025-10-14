import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Set, Dict, List, Tuple
from pathlib import Path
import traceback
from datetime import datetime
import threading
import time

class ProjectAnalyzer:
    """
    Analisador de projetos ultra-robusto e à prova de falhas.
    Protegido contra todos os cenários possíveis.
    """
    def __init__(self, project_path: str, output_filename: str):
        self.project_path = self._validate_path(project_path)
        self.output_filename = self._sanitize_filename(output_filename)
        self.ignore_patterns: Dict[str, Set[str]] = {}
        self.code_extensions: Set[str] = set()
        self.debug = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.timeout_seconds = 300  # 5 minutos
        self.start_time = None
        self.files_processed = 0
        self.files_skipped = 0
        self.cancelled = False

    def _validate_path(self, path: str) -> str:
        """Valida e normaliza o caminho do projeto."""
        try:
            if not path or not isinstance(path, str):
                raise ValueError("Caminho inválido ou vazio")
            
            path = os.path.abspath(os.path.normpath(path))
            
            if not os.path.exists(path):
                raise ValueError(f"Caminho não existe: {path}")
            
            if not os.path.isdir(path):
                raise ValueError(f"Caminho não é um diretório: {path}")
            
            if not os.access(path, os.R_OK):
                raise PermissionError(f"Sem permissão de leitura: {path}")
            
            return path
        except Exception as e:
            self._log_error(f"Erro ao validar caminho: {e}")
            raise

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza o nome do arquivo de saída."""
        try:
            if not filename or not isinstance(filename, str):
                filename = "projeto_unificado.md"
            
            forbidden_chars = '<>:"|?*\x00'
            for char in forbidden_chars:
                filename = filename.replace(char, '_')
            
            if not filename.lower().endswith('.md'):
                filename += '.md'
            
            if len(filename) > 200:
                name, ext = os.path.splitext(filename)
                filename = name[:196] + ext
            
            return filename
        except Exception:
            return "projeto_unificado.md"

    def _log_error(self, message: str):
        """Registra um erro."""
        self.errors.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        if self.debug:
            print(f"❌ ERRO: {message}", file=sys.stderr)

    def _log_warning(self, message: str):
        """Registra um aviso."""
        self.warnings.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        if self.debug:
            print(f"⚠️  AVISO: {message}")

    def _check_timeout(self) -> bool:
        """Verifica se excedeu o timeout."""
        if self.start_time and self.timeout_seconds:
            elapsed = time.time() - self.start_time
            if elapsed > self.timeout_seconds:
                self._log_error(f"Timeout excedido ({self.timeout_seconds}s)")
                return True
        return False

    def set_profiles(self, profiles: list):
        """Define os perfis de arquivos de forma segura."""
        try:
            if not profiles or not isinstance(profiles, (list, tuple)):
                profiles = []
            
            profiles = [str(p).lower() for p in profiles if p]
            
            self.ignore_patterns = {
                'dirs': {
                    '.git', '__pycache__', 'venv', 'env', '.venv', '.env',
                    '.idea', '.vscode', 'coverage', '.pytest_cache', 
                    '.mypy_cache', '.tox', '.nox',
                },
                'dirs_exact': {
                    'build', 'dist', 'target', 'out', 'bin', 'obj',
                    'logs', 'tmp', 'temp', '.gradle', '.mvn',
                    'node_modules', 'bower_components', 'jspm_packages',
                    'vendor',
                },
                'files': {
                    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                    '.ds_store', 'thumbs.db', 'desktop.ini',
                },
                'extensions': {
                    '.log', '.tmp', '.cache', '.lock', '.pid', '.swp', '.swo',
                    '.bak', '.backup', '.old', '.orig',
                    '.DS_Store', '.ico', '.png', '.jpg', '.jpeg', 
                    '.gif', '.svg', '.webp', '.bmp', '.tiff',
                    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
                    '.exe', '.dll', '.so', '.dylib', '.a', '.lib',
                    '.deb', '.rpm', '.apk', '.dmg', '.iso',
                    '.map', '.min.js', '.min.css',
                    '.pyc', '.pyo', '.pyd', '.class', '.o', '.obj',
                },
                'paths': set(),
            }

            self.code_extensions = {
                '.html', '.htm', '.css', '.scss', '.sass', '.less',
                '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
                '.vue', '.svelte', '.astro',
                '.json', '.json5', '.jsonc', '.yaml', '.yml', '.toml', 
                '.xml', '.ini', '.cfg', '.conf', '.config',
                '.md', '.markdown', '.txt', '.text',
                '.py', '.pyw', '.pyi',
                '.java', '.kt', '.kts', '.scala',
                '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hh', '.hxx',
                '.cs', '.vb', '.fs', '.fsx',
                '.rb', '.rake', '.go', '.rs',
                '.swift', '.m', '.mm',
                '.lua', '.pl', '.pm', '.r',
                '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
                '.sql', '.psql', '.mysql', '.sqlite',
                '.env.example', '.gitignore', '.dockerignore',
                'dockerfile', 'makefile', 'rakefile',
            }

            if 'php' in profiles:
                self._add_php_patterns()
            if 'react' in profiles:
                self._add_react_patterns()
            if 'spring' in profiles:
                self._add_spring_patterns()
            if 'python' in profiles:
                self._add_python_patterns()
            if 'node' in profiles or 'nodejs' in profiles:
                self._add_node_patterns()
                
        except Exception as e:
            self._log_error(f"Erro ao configurar perfis: {e}")

    def _add_php_patterns(self):
        """Adiciona padrões PHP."""
        try:
            self.ignore_patterns['dirs_exact'].update({'vendor', 'cache'})
            self.ignore_patterns['paths'].update({
                'storage/logs', 'storage/framework/cache',
                'storage/framework/sessions', 'storage/framework/views',
                'bootstrap/cache',
            })
            self.ignore_patterns['files'].update({
                'composer.lock', 'composer.phar', '.phpunit.result.cache',
            })
            self.ignore_patterns['extensions'].add('.phar')
            self.code_extensions.update({
                '.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps'
            })
        except Exception as e:
            self._log_warning(f"Erro ao adicionar padrões PHP: {e}")

    def _add_react_patterns(self):
        """Adiciona padrões React."""
        try:
            self.ignore_patterns['dirs_exact'].update({
                'node_modules', '.next', '.nuxt', 'coverage'
            })
            self.ignore_patterns['files'].update({
                'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            })
        except Exception as e:
            self._log_warning(f"Erro ao adicionar padrões React: {e}")

    def _add_spring_patterns(self):
        """Adiciona padrões Spring."""
        try:
            self.ignore_patterns['dirs_exact'].update({'target', '.mvn', '.gradle'})
            self.ignore_patterns['files'].update({
                'mvnw', 'mvnw.cmd', 'gradlew', 'gradlew.bat', 
                'gradle-wrapper.jar', 'maven-wrapper.jar',
            })
            self.code_extensions.update({
                '.java', '.kt', '.xml', '.properties', '.gradle', '.sql'
            })
        except Exception as e:
            self._log_warning(f"Erro ao adicionar padrões Spring: {e}")

    def _add_python_patterns(self):
        """Adiciona padrões Python."""
        try:
            self.ignore_patterns['dirs_exact'].update({
                '__pycache__', '.pytest_cache', '.mypy_cache', 
                '.tox', '.nox', 'htmlcov', '.coverage',
            })
            self.ignore_patterns['extensions'].update({
                '.pyc', '.pyo', '.pyd', '.whl', '.egg',
            })
            self.ignore_patterns['files'].update({
                'poetry.lock', 'pipfile.lock',
            })
        except Exception as e:
            self._log_warning(f"Erro ao adicionar padrões Python: {e}")

    def _add_node_patterns(self):
        """Adiciona padrões Node.js."""
        try:
            self.ignore_patterns['dirs_exact'].update({
                'node_modules', '.npm', '.yarn', '.pnpm-store',
            })
            self.ignore_patterns['files'].update({
                'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            })
        except Exception as e:
            self._log_warning(f"Erro ao adicionar padrões Node: {e}")

    def _should_ignore_dir(self, dir_name: str, full_path: str) -> bool:
        """Verifica se deve ignorar diretório."""
        try:
            if not dir_name or not isinstance(dir_name, str):
                return True
            
            if dir_name.startswith('.') and dir_name not in {'.github', '.gitlab'}:
                return True
            
            if dir_name in self.ignore_patterns.get('dirs', set()):
                return True
            
            if dir_name in self.ignore_patterns.get('dirs_exact', set()):
                return True
            
            try:
                if not os.access(full_path, os.R_OK | os.X_OK):
                    self._log_warning(f"Sem permissão para acessar: {dir_name}")
                    return True
            except (OSError, PermissionError):
                return True
            
            try:
                if os.path.islink(full_path):
                    self._log_warning(f"Link simbólico ignorado: {dir_name}")
                    return True
            except (OSError, ValueError):
                return True
            
            return False
            
        except Exception as e:
            self._log_warning(f"Erro ao verificar diretório {dir_name}: {e}")
            return True

    def _should_ignore_file(self, file_name: str, relative_path: str) -> bool:
        """Verifica se deve ignorar arquivo."""
        try:
            if not file_name or not isinstance(file_name, str):
                return True
            
            lower_name = file_name.lower()
            
            if lower_name in self.ignore_patterns.get('files', set()):
                return True
            
            try:
                _, ext = os.path.splitext(lower_name)
                if ext and ext in self.ignore_patterns.get('extensions', set()):
                    return True
            except Exception:
                pass
            
            if lower_name.startswith('.') and lower_name not in {
                '.gitkeep', '.htaccess', '.env.example', '.editorconfig'
            }:
                return True
            
            try:
                if 'paths' in self.ignore_patterns:
                    normalized_path = relative_path.replace(os.sep, '/')
                    for ignore_path in self.ignore_patterns['paths']:
                        if ignore_path in normalized_path:
                            return True
            except Exception:
                pass
            
            return False
            
        except Exception as e:
            self._log_warning(f"Erro ao verificar arquivo {file_name}: {e}")
            return True

    def _is_binary_file(self, file_path: str) -> bool:
        """Detecta se arquivo é binário."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
                if not chunk:
                    return False
                
                if b'\x00' in chunk:
                    return True
                
                text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
                non_text = sum(1 for byte in chunk if byte not in text_chars)
                
                return non_text / len(chunk) > 0.3
                
        except Exception:
            return True

    def _read_file_safely(self, file_path: str) -> Tuple[str, bool]:
        """Lê arquivo de forma segura."""
        try:
            try:
                file_size = os.path.getsize(file_path)
                if file_size > self.max_file_size:
                    self._log_warning(f"Arquivo muito grande ignorado ({file_size} bytes): {file_path}")
                    return "", False
                if file_size == 0:
                    return "", False
            except (OSError, ValueError):
                return "", False
            
            if self._is_binary_file(file_path):
                self._log_warning(f"Arquivo binário ignorado: {file_path}")
                return "", False
            
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        content = f.read()
                        
                    if content and len(content.strip()) > 0:
                        content = ''.join(char for char in content if char.isprintable() or char in '\n\r\t')
                        return content.strip(), True
                        
                except (UnicodeDecodeError, UnicodeError):
                    continue
                except Exception:
                    break
            
            return "", False
            
        except PermissionError:
            self._log_warning(f"Sem permissão para ler: {file_path}")
            return "", False
        except (OSError, IOError) as e:
            self._log_warning(f"Erro de I/O ao ler {file_path}: {e}")
            return "", False
        except Exception as e:
            self._log_error(f"Erro inesperado ao ler {file_path}: {e}")
            return "", False

    def _generate_tree(self) -> str:
        """Gera árvore de diretórios."""
        lines = []
        try:
            for root, dirs, files in os.walk(self.project_path, topdown=True, onerror=None, followlinks=False):
                try:
                    if self._check_timeout() or self.cancelled:
                        break
                    
                    relative_path = os.path.relpath(root, self.project_path)
                    
                    original_dirs = dirs.copy()
                    dirs[:] = []
                    for d in original_dirs:
                        try:
                            full_dir_path = os.path.join(root, d)
                            if not self._should_ignore_dir(d, full_dir_path):
                                dirs.append(d)
                        except Exception as e:
                            self._log_warning(f"Erro ao processar diretório {d}: {e}")
                    
                    level = relative_path.count(os.sep) if relative_path != '.' else 0
                    indent = "│   " * level
                    
                    dir_name = os.path.basename(root)
                    if root != self.project_path:
                        lines.append(f"{indent}├── {dir_name}/")
                    
                    sub_indent = "│   " * (level + 1)
                    
                    for file in files:
                        try:
                            if not self._should_ignore_file(file, os.path.join(relative_path, file)):
                                lines.append(f"{sub_indent}└── {file}")
                        except Exception as e:
                            self._log_warning(f"Erro ao processar arquivo {file}: {e}")
                            
                except Exception as e:
                    self._log_warning(f"Erro ao processar pasta {root}: {e}")
                    continue
                    
        except Exception as e:
            self._log_error(f"Erro ao gerar árvore: {e}")
        
        return "\n".join(lines) if lines else "├── (vazio ou sem permissão)"

    def _consolidate_code(self) -> str:
        """Consolida código de forma segura."""
        content = []
        
        try:
            for root, dirs, files in os.walk(self.project_path, topdown=True, onerror=None, followlinks=False):
                try:
                    if self._check_timeout():
                        self._log_error("Processo cancelado por timeout")
                        break
                    
                    if self.cancelled:
                        self._log_warning("Processo cancelado pelo usuário")
                        break
                    
                    relative_path = os.path.relpath(root, self.project_path)
                    
                    original_dirs = dirs.copy()
                    dirs[:] = []
                    for d in original_dirs:
                        try:
                            full_dir_path = os.path.join(root, d)
                            if not self._should_ignore_dir(d, full_dir_path):
                                dirs.append(d)
                        except Exception:
                            pass
                    
                    for file in files:
                        try:
                            if self._check_timeout() or self.cancelled:
                                break
                            
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, self.project_path)
                            
                            if self._should_ignore_file(file, rel_path):
                                self.files_skipped += 1
                                continue
                            
                            try:
                                _, ext = os.path.splitext(file.lower())
                                if ext not in self.code_extensions and file.lower() not in self.code_extensions:
                                    self.files_skipped += 1
                                    continue
                            except Exception:
                                self.files_skipped += 1
                                continue
                            
                            file_content, success = self._read_file_safely(file_path)
                            
                            if success and file_content:
                                lang = ext[1:] if ext and len(ext) > 1 else ''
                                
                                content.append(
                                    f"### `{rel_path}`\n\n"
                                    f"```{lang}\n{file_content}\n```\n"
                                )
                                self.files_processed += 1
                                
                                if self.debug and self.files_processed % 10 == 0:
                                    print(f"📝 Processados: {self.files_processed} arquivos...")
                            else:
                                self.files_skipped += 1
                                
                        except Exception as e:
                            self._log_warning(f"Erro ao processar {file}: {e}")
                            self.files_skipped += 1
                            
                except Exception as e:
                    self._log_warning(f"Erro ao processar pasta {root}: {e}")
                    continue
                    
        except Exception as e:
            self._log_error(f"Erro crítico ao consolidar código: {e}")
            self._log_error(traceback.format_exc())
        
        return "\n".join(content) if content else "_Nenhum arquivo de código encontrado ou processado._\n"

    def _generate_statistics(self) -> str:
        """Gera estatísticas do processo."""
        stats = [
            "## 📊 Estatísticas da Análise\n",
            f"- **Arquivos processados:** {self.files_processed}",
            f"- **Arquivos ignorados/pulados:** {self.files_skipped}",
            f"- **Erros encontrados:** {len(self.errors)}",
            f"- **Avisos gerados:** {len(self.warnings)}",
            f"- **Data/Hora:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        ]
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            stats.append(f"- **Tempo de execução:** {elapsed:.2f}s")
        
        return "\n".join(stats)

    def _generate_error_section(self) -> str:
        """Gera seção de erros e avisos."""
        sections = []
        
        if self.errors:
            sections.append("\n## ❌ Erros Encontrados\n")
            for i, error in enumerate(self.errors[:50], 1):
                sections.append(f"{i}. {error}")
            if len(self.errors) > 50:
                sections.append(f"\n_... e mais {len(self.errors) - 50} erros_")
        
        if self.warnings and self.debug:
            sections.append("\n## ⚠️ Avisos\n")
            for i, warning in enumerate(self.warnings[:30], 1):
                sections.append(f"{i}. {warning}")
            if len(self.warnings) > 30:
                sections.append(f"\n_... e mais {len(self.warnings) - 30} avisos_")
        
        return "\n".join(sections)

    def generate_report(self) -> bool:
        """Gera relatório completo."""
        self.start_time = time.time()
        success = False
        
        try:
            print("🚀 Iniciando análise do projeto...")
            print(f"📁 Projeto: {self.project_path}")
            print(f"📄 Saída: {self.output_filename}\n")
            
            if not os.path.isdir(self.project_path):
                raise ValueError("Caminho do projeto inválido ou não é um diretório")
            
            print("📂 Gerando estrutura de diretórios...")
            tree = self._generate_tree()
            
            print("📝 Consolidando arquivos de código...")
            code_content = self._consolidate_code()
            
            stats = self._generate_statistics()
            error_section = self._generate_error_section()
            
            print(f"\n💾 Salvando arquivo '{self.output_filename}'...")
            
            try:
                with open(self.output_filename, 'w', encoding='utf-8', errors='replace') as out:
                    out.write("# 📋 Análise de Projeto\n\n")
                    out.write(f"**Projeto:** `{os.path.basename(self.project_path)}`  \n")
                    out.write(f"**Caminho:** `{self.project_path}`\n\n")
                    out.write("---\n\n")
                    out.write(stats)
                    out.write("\n\n---\n\n")
                    out.write("## 📁 Estrutura de Pastas\n\n```\n")
                    out.write(tree)
                    out.write("\n```\n\n")
                    out.write("---\n\n")
                    out.write("## 💻 Conteúdo dos Arquivos de Código\n\n")
                    out.write(code_content)
                    
                    if error_section:
                        out.write("\n\n---\n")
                        out.write(error_section)
                    
                    out.write("\n\n---\n\n")
                    out.write("_Relatório gerado automaticamente pelo ProjectAnalyzer_\n")
                
                success = True
                
            except PermissionError:
                raise PermissionError(f"Sem permissão para escrever: {self.output_filename}")
            except (OSError, IOError) as e:
                raise IOError(f"Erro ao escrever arquivo: {e}")
            
            print("\n" + "="*60)
            print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
            print("="*60)
            print(f"📄 Arquivo gerado: {self.output_filename}")
            print(f"📊 Arquivos processados: {self.files_processed}")
            print(f"⏭️  Arquivos ignorados: {self.files_skipped}")
            
            if self.errors:
                print(f"❌ Erros: {len(self.errors)}")
            if self.warnings:
                print(f"⚠️  Avisos: {len(self.warnings)}")
            
            elapsed = time.time() - self.start_time
            print(f"⏱️  Tempo total: {elapsed:.2f}s")
            print("="*60)
            
            return True
            
        except KeyboardInterrupt:
            self._log_error("Processo interrompido pelo usuário")
            print("\n⚠️  Processo cancelado pelo usuário")
            return False
            
        except Exception as e:
            self._log_error(f"Erro crítico: {e}")
            self._log_error(traceback.format_exc())
            print(f"\n❌ ERRO CRÍTICO: {e}")
            print("Verifique as permissões e o caminho do projeto")
            return False
        
        finally:
            if not success and self.files_processed > 0:
                try:
                    print("\n⚠️  Tentando salvar relatório parcial...")
                    with open(f"parcial_{self.output_filename}", 'w', encoding='utf-8') as out:
                        out.write("# Relatório Parcial (Processo Interrompido)\n\n")
                        out.write(self._generate_statistics())
                        out.write(self._generate_error_section())
                    print(f"💾 Relatório parcial salvo como: parcial_{self.output_filename}")
                except Exception:
                    pass


class AnalyzerGUI:
    """Interface gráfica para o analisador."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Analyzer - Exportador para IA")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.project_path = tk.StringVar()
        self.output_name = tk.StringVar(value="projeto_para_ia.md")
        self.selected_profiles = []
        self.analyzer = None
        self.analysis_thread = None
        
        self._create_widgets()
        self._center_window()
        
    def _center_window(self):
        """Centraliza janela na tela."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Cria interface gráfica."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title = ttk.Label(main_frame, text="🚀 Project Analyzer", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de pasta
        ttk.Label(main_frame, text="Pasta do Projeto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.project_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="📁 Buscar", command=self._select_folder).grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Nome do arquivo
        ttk.Label(main_frame, text="Nome do Arquivo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_name, width=50).grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Perfis
        ttk.Label(main_frame, text="Perfis do Projeto:", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        
        profiles_frame = ttk.Frame(main_frame)
        profiles_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.profile_vars = {}
        profiles = [
            ('Python', 'python'),
            ('React/Node.js', 'react'),
            ('PHP/Laravel', 'php'),
            ('Spring/Java', 'spring'),
            ('Node.js', 'node')
        ]
        
        for i, (label, value) in enumerate(profiles):
            var = tk.BooleanVar()
            self.profile_vars[value] = var
            ttk.Checkbutton(profiles_frame, text=label, variable=var).grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=3)
        
        # Barra de progresso
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.grid(row=5, column=0, columnspan=3, pady=(20, 5))
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="▶️  Iniciar Análise", command=self._start_analysis)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.cancel_btn = ttk.Button(button_frame, text="⏹️  Cancelar", command=self._cancel_analysis, state='disabled')
        self.cancel_btn.grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="ℹ️  Ajuda", command=self._show_help).grid(row=0, column=2, padx=5)
        
        # Log
        ttk.Label(main_frame, text="Log de Execução:", font=('Arial', 10, 'bold')).grid(row=8, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(9, weight=1)
        
        self.log_text = tk.Text(log_frame, height=12, width=70, wrap=tk.WORD, state='disabled')
        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def _select_folder(self):
        """Abre diálogo para selecionar pasta."""
        try:
            folder = filedialog.askdirectory(
                title="Selecione a pasta do projeto",
                mustexist=True
            )
            if folder:
                self.project_path.set(folder)
                self._log(f"✅ Pasta selecionada: {folder}")
        except Exception as e:
            self._log(f"❌ Erro ao selecionar pasta: {e}")
            messagebox.showerror("Erro", f"Erro ao selecionar pasta:\n{e}")
    
    def _log(self, message: str):
        """Adiciona mensagem ao log."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def _show_help(self):
        """Mostra janela de ajuda."""
        help_text = """
🚀 Project Analyzer - Guia de Uso

📋 O que faz:
Exporta todo o código do seu projeto para um único arquivo Markdown, 
ideal para enviar para IAs como ChatGPT, Claude, etc.

📝 Como usar:
1. Selecione a pasta do seu projeto
2. Escolha um nome para o arquivo de saída
3. Marque os perfis relevantes (opcional)
4. Clique em "Iniciar Análise"

🔧 Perfis:
- Python: Ignora venv, __pycache__, .pyc
- React/Node: Ignora node_modules, build
- PHP: Ignora vendor, cache
- Spring: Ignora target, .mvn
- Node.js: Ignora dependências NPM

⚙️ O que é ignorado automaticamente:
- Arquivos binários (imagens, PDFs, executáveis)
- Dependências (node_modules, vendor, etc)
- Arquivos de build e cache
- Logs e arquivos temporários
- Diretórios .git, .vscode, .idea

✅ Arquivos incluídos:
- Código fonte (.py, .js, .java, .php, etc)
- Arquivos de configuração (.json, .yaml, .env.example)
- Documentação (.md, .txt)
- Scripts (.sh, .bat)

💡 Dicas:
- O arquivo gerado pode ser grande para projetos complexos
- Use perfis para otimizar a análise
- Revise o log para ver avisos e erros
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Ajuda - Project Analyzer")
        help_window.geometry("600x500")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        ttk.Button(help_window, text="Fechar", command=help_window.destroy).pack(pady=10)
    
    def _validate_inputs(self) -> bool:
        """Valida entradas do usuário."""
        if not self.project_path.get():
            messagebox.showerror("Erro", "Selecione uma pasta do projeto!")
            return False
        
        if not os.path.isdir(self.project_path.get()):
            messagebox.showerror("Erro", "A pasta selecionada não existe!")
            return False
        
        if not self.output_name.get():
            messagebox.showerror("Erro", "Digite um nome para o arquivo de saída!")
            return False
        
        return True
    
    def _start_analysis(self):
        """Inicia análise em thread separada."""
        if not self._validate_inputs():
            return
        
        # Desabilita botão iniciar
        self.start_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        
        # Limpa log
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')
        
        # Inicia progresso
        self.progress.start(10)
        self.progress_label.config(text="⏳ Analisando projeto...")
        
        # Coleta perfis selecionados
        selected = [key for key, var in self.profile_vars.items() if var.get()]
        
        # Inicia thread
        self.analysis_thread = threading.Thread(
            target=self._run_analysis,
            args=(self.project_path.get(), self.output_name.get(), selected),
            daemon=True
        )
        self.analysis_thread.start()
        
        # Monitora thread
        self._check_thread()
    
    def _run_analysis(self, project_path: str, output_name: str, profiles: list):
        """Executa análise (roda em thread separada)."""
        try:
            self.analyzer = ProjectAnalyzer(project_path, output_name)
            self.analyzer.set_profiles(profiles)
            
            # Redireciona stdout para capturar prints
            import io
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            success = self.analyzer.generate_report()
            
            # Restaura stdout
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Atualiza GUI
            self.root.after(0, self._analysis_complete, success, output)
            
        except Exception as e:
            error_msg = f"Erro crítico: {e}\n{traceback.format_exc()}"
            self.root.after(0, self._analysis_error, error_msg)
    
    def _check_thread(self):
        """Verifica se thread ainda está rodando."""
        if self.analysis_thread and self.analysis_thread.is_alive():
            self.root.after(100, self._check_thread)
        else:
            self.progress.stop()
    
    def _analysis_complete(self, success: bool, output: str):
        """Callback quando análise completa."""
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        
        # Mostra output no log
        for line in output.split('\n'):
            if line.strip():
                self._log(line)
        
        if success:
            self.progress_label.config(text="✅ Análise concluída com sucesso!")
            messagebox.showinfo(
                "Sucesso",
                f"Análise concluída!\n\n"
                f"Arquivo gerado: {self.output_name.get()}\n"
                f"Arquivos processados: {self.analyzer.files_processed}\n"
                f"Arquivos ignorados: {self.analyzer.files_skipped}"
            )
        else:
            self.progress_label.config(text="❌ Análise concluída com erros")
            messagebox.showwarning(
                "Aviso",
                "A análise foi concluída mas houve erros.\n"
                "Verifique o log para mais detalhes."
            )
    
    def _analysis_error(self, error_msg: str):
        """Callback quando há erro na análise."""
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        self.progress_label.config(text="❌ Erro durante análise")
        
        self._log(f"\n❌ ERRO CRÍTICO:\n{error_msg}")
        messagebox.showerror("Erro", f"Erro durante análise:\n\n{error_msg[:200]}")
    
    def _cancel_analysis(self):
        """Cancela análise em andamento."""
        if self.analyzer:
            self.analyzer.cancelled = True
            self._log("⏹️  Cancelamento solicitado...")
            self.progress_label.config(text="⏹️  Cancelando...")
    
    def run(self):
        """Inicia interface gráfica."""
        self.root.mainloop()


def main():
    """Função principal com múltiplas opções de execução."""
    try:
        # Verifica se foi passado argumento de linha de comando
        if len(sys.argv) > 1:
            # Modo linha de comando
            project_folder = sys.argv[1]
            output_file = sys.argv[2] if len(sys.argv) > 2 else "projeto_para_ia.md"
            profiles = sys.argv[3:] if len(sys.argv) > 3 else []
            
            print("🚀 Project Analyzer - Modo Linha de Comando\n")
            
            try:
                analyzer = ProjectAnalyzer(project_folder, output_file)
                analyzer.set_profiles(profiles)
                success = analyzer.generate_report()
                
                sys.exit(0 if success else 1)
                
            except Exception as e:
                print(f"\n❌ ERRO: {e}")
                sys.exit(1)
        
        else:
            # Modo GUI
            try:
                app = AnalyzerGUI()
                app.run()
            except Exception as e:
                print(f"❌ Erro ao inicializar interface gráfica: {e}")
                print("\n💡 Tentando modo de seleção simples...\n")
                
                # Fallback: modo simples com tkinter básico
                root = tk.Tk()
                root.withdraw()
                
                project_folder = filedialog.askdirectory(
                    title="Selecione a pasta do projeto",
                    mustexist=True
                )
                
                root.destroy()
                
                if not project_folder:
                    print("⚠️  Nenhuma pasta selecionada. Encerrando.")
                    return
                
                output_file = "projeto_para_ia.md"
                
                print(f"\n📁 Pasta selecionada: {project_folder}")
                print(f"📄 Arquivo de saída: {output_file}")
                print("\n🔧 Selecione perfis (separados por espaço) ou Enter para pular:")
                print("   Opções: python, react, php, spring, node")
                
                profiles_input = input("Perfis: ").strip()
                profiles = profiles_input.split() if profiles_input else []
                
                print("\n🚀 Iniciando análise...\n")
                
                analyzer = ProjectAnalyzer(project_folder, output_file)
                analyzer.set_profiles(profiles)
                success = analyzer.generate_report()
                
                if success:
                    print("\n✅ Pressione Enter para sair...")
                    input()
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()