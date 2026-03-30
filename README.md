# 🎙️ Transcritor IA - Guia Completo

## 📋 Visão Geral

App profissional para transcrição de áudio e vídeo usando **Whisper IA** da OpenAI. Converte mídia em texto com timestamps (formato SRT) e transcrição completa em .txt.

**Características:**
- ✅ Suporta: MP3, WAV, M4A, MP4, MKV, FLAC, OGG
- ✅ GPU (CUDA) ou CPU automático
- ✅ Saída em TXT e SRT (legendas)
- ✅ Interface moderna e responsiva
- ✅ Processamento em chunks para arquivos grandes
- ✅ Logging completo
- ✅ Cancelamento em tempo real

---

## 🚀 Instalação Rápida (Seu PC)

### Pré-requisitos
- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **FFmpeg** → [Download](https://ffmpeg.org/download.html)

### Passo 1: Clone/Copie os arquivos
```bash
# Pasta com:
# - transcritor_melhorado.py
# - requirements.txt
# - build_windows.bat (ou build_linux_mac.sh)
```

### Passo 2: Instale as dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Execute o app
```bash
python transcritor_melhorado.py
```

---

## 📦 Gerar Executável (Para outro PC)

### Windows
1. Abra `cmd` na pasta do projeto
2. Execute: `build_windows.bat`
3. Aguarde (2-5 minutos)
4. Arquivo criado em: `dist/Transcritor IA.exe`

### Linux/Mac
1. Abra terminal na pasta do projeto
2. Execute: `chmod +x build_linux_mac.sh && ./build_linux_mac.sh`
3. Aguarde (2-5 minutos)
4. Arquivo criado em: `dist/Transcritor IA`

---

## 💻 Distribuindo para Outro PC

### Requisito do PC destino
- **Windows**: FFmpeg instalado ([Download](https://ffmpeg.org/download.html))
- **Linux**: `sudo apt-get install ffmpeg`
- **Mac**: `brew install ffmpeg`

### Passo 1: Copie o executável
```
Copie: dist/Transcritor IA.exe (Windows)
       ou dist/Transcritor IA (Linux/Mac)
```

### Passo 2: Instale FFmpeg no outro PC
- [Windows: Download Portable](https://ffmpeg.org/download.html)
- [Linux: `sudo apt-get install ffmpeg`]
- [Mac: `brew install ffmpeg`]

### Passo 3: Execute
- **Windows**: Clique duplo em `Transcritor IA.exe`
- **Linux/Mac**: Terminal: `./Transcritor\ IA` ou clique duplo

---

## 🎯 Como Usar

### Passo 1️⃣: Selecionar Arquivo
- Clique em "Escolher Áudio"
- Selecione um arquivo de mídia

### Passo 2️⃣: Iniciar Transcrição
- Clique em "▶️ Iniciar Transcrição"
- Acompanhe o progresso em tempo real

### Passo 3️⃣: Resultados
- **Arquivo TXT**: Transcrição completa
- **Arquivo SRT**: Legendas com timestamps
- Ambos salvos na mesma pasta do arquivo original

### ⏹️ Cancelar
- Clique em "⛔ Cancelar" para parar o processamento

---

## 📊 Melhorias vs Código Original

### Backend
| Aspecto | Original | Melhorado |
|---------|----------|-----------|
| **Estrutura** | Funções soltas | Classe OOP completa |
| **Erros** | Try/except genéricos | Tratamento robusto |
| **Logging** | Nenhum | Arquivo + console |
| **Validação** | Mínima | Completa |
| **Limpeza** | Manual | Automática |
| **Documentação** | Comentários simples | Docstrings completas |

### Frontend
| Aspecto | Original | Melhorado |
|---------|----------|-----------|
| **Layout** | Básico | Frames estruturados |
| **Cores** | Tema único | Paleta profissional |
| **Feedback** | Status genérico | Detalhado e contextual |
| **Responsividade** | Fixa | Redimensionável |
| **Acessibilidade** | Limitada | Melhorada |
| **Botões** | Simples | Estados, hover, cores |
| **Informações** | Mínimas | Tempo, chunk, dispositivo |

### Funcionalidades Novas
- ✅ Cópia de texto para clipboard
- ✅ Verificação de FFmpeg na inicialização
- ✅ Detecção automática de GPU
- ✅ Exibição de tempo estimado
- ✅ Informação de chunk processado
- ✅ Suporte a mais formatos
- ✅ Limpeza automática de arquivos temporários
- ✅ Mensagens de sucesso com caminho do arquivo

---

## 🔧 Solução de Problemas

### ❌ "FFmpeg não encontrado"
**Solução:**
- Windows: [Baixe FFmpeg](https://ffmpeg.org/download.html) e adicione ao PATH
- Linux: `sudo apt-get install ffmpeg`
- Mac: `brew install ffmpeg`

### ❌ Muito lento
- Modelo padrão: `"base"` (rápido, menos preciso)
- Edite em `transcritor_melhorado.py`: `MODEL: str = "small"` (mais lento, mais preciso)
- Modelos: `tiny` < `base` < `small` < `medium` < `large`

### ❌ Erro de CUDA/GPU
- Normal em PC sem GPU
- Automaticamente usa CPU
- Mais lento, mas funciona

### ❌ Arquivo TXT vazio
- Áudio pode estar muito baixo
- Tente aumentar volume do arquivo original
- Use modelo maior (`"medium"` ou `"large"`)

### ❌ Executável muito grande
- Normal (~2GB com modelos Whisper)
- Use versão em pasta em vez de `--onefile`:
  ```bash
  pyinstaller --onedir transcritor_melhorado.py
  ```

---

## 📝 Configuração Avançada

### Editar `transcritor_melhorado.py`

**Mudar tempo do chunk** (linha ~20):
```python
CHUNK_TIME: int = 600  # 10 minutos ao invés de 5
```

**Mudar modelo** (mais preciso = mais lento):
```python
MODEL: str = "small"  # Opções: tiny, base, small, medium, large
```

**Mudar pasta temporária**:
```python
TEMP_DIR: str = "temp_audio"  # ao invés de "chunks"
```

---

## 🎬 Exemplos de Saída

### Arquivo SRT
```
1
00:00:00,000 --> 00:00:05,000
Olá, este é um teste de transcrição.

2
00:00:05,000 --> 00:00:10,500
O áudio está sendo convertido para texto.
```

### Arquivo TXT
```
Olá, este é um teste de transcrição.
O áudio está sendo convertido para texto.
Whisper é muito preciso com português.
```

---

## 📞 Suporte

- **Logs**: Verifique `transcritor.log` na pasta do app
- **GitHub Issues**: Se usar como base de projeto
- **Documentação Whisper**: https://github.com/openai/whisper

---

## 📄 Licença

Uso livre para fins pessoais e comerciais. Baseado em Whisper (OpenAI - MIT License).

---

## 🚀 Próximas Melhorias Possíveis

- [ ] Interface com tema claro/escuro
- [ ] Suporte a múltiplos idiomas
- [ ] Edição de transcrição no app
- [ ] Export para DOCX, PDF
- [ ] Fila de processamento (vários arquivos)
- [ ] Compressão de áudio antes de processar
- [ ] Busca no histórico de transcrições

---

**Versão**: 2.0  
**Última atualização**: Março 2025  
**Autor**: Seu Nome / Equipe  
**Python**: 3.10+
