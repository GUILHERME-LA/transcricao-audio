# 🪟 GUIA WINDOWS - Passo a Passo

## 1️⃣ PREPARAÇÃO NO SEU PC

### A) Instalar Python
1. Vá para: https://www.python.org/downloads/
2. Baixe **Python 3.11** (Windows Installer)
3. Execute o .exe
4. ⚠️ **IMPORTANTE**: Marque "Add Python to PATH"
5. Clique "Install Now"

### B) Instalar FFmpeg
1. Vá para: https://ffmpeg.org/download.html
2. Clique em "Windows builds"
3. Escolha versão com "ffmpeg-release-full.7z"
4. Extraia em: `C:\ffmpeg`
5. Copie o caminho: `C:\ffmpeg\bin` 
6. Adicione ao PATH do Windows:
   - Pesquise: "Variáveis de ambiente"
   - Clique: "Editar variáveis de ambiente do sistema"
   - Clique: "Variáveis de ambiente"
   - Em PATH → Editar → Novo → Cole: `C:\ffmpeg\bin`
   - OK, OK, OK

### C) Testar instalação
Abra `cmd` e digite:
```cmd
python --version
ffmpeg -version
```

Se ambos funcionarem, está tudo certo! ✅

---

## 2️⃣ GERAR EXECUTÁVEL

### A) Preparar pasta
1. Crie uma pasta vazia: `C:\Meus Projetos\Transcritor`
2. Coloque nela:
   - `transcritor_melhorado.py`
   - `requirements.txt`
   - `build_windows.bat`

### B) Gerar EXE
1. Abra `cmd`
2. Navigate para a pasta:
   ```cmd
   cd C:\Meus Projetos\Transcritor
   ```
3. Execute o script:
   ```cmd
   build_windows.bat
   ```
4. Aguarde 2-5 minutos
5. Se tudo correr bem, verá:
   ```
   ===== PRONTO! =====
   Seu executável foi criado em: dist\Transcritor IA.exe
   ```

✅ Executável pronto em: `C:\Meus Projetos\Transcritor\dist\Transcritor IA.exe`

---

## 3️⃣ DISTRIBUIR PARA OUTRO PC

### A) Preparar pacote de entrega
```
Crie uma pasta chamada: Transcritor_IA_2025

Coloque nela:
├── Transcritor IA.exe  (copie de dist/)
├── INSTALAR_FFMPEG.txt (veja abaixo)
└── README.txt          (instruções)
```

### B) Arquivo INSTALAR_FFMPEG.txt
```
⚠️ IMPORTANTE - Leia antes de usar!

Este programa requer FFmpeg instalado.

1. Acesse: https://ffmpeg.org/download.html
2. Clique em "Windows builds"
3. Baixe: ffmpeg-release-full.7z
4. Extraia em: C:\ffmpeg
5. Adicione ao PATH:
   - Pesquise "Variáveis de ambiente"
   - Clique "Editar variáveis de ambiente do sistema"
   - Em "PATH" → Novo → Cole: C:\ffmpeg\bin
   - Reinicie o Windows

Depois disso, execute: Transcritor IA.exe
```

### C) Arquivo README.txt
```
╔════════════════════════════════════════╗
║   🎙️  TRANSCRITOR IA 2.0              ║
║   Converta Áudio em Texto com IA       ║
╚════════════════════════════════════════╝

REQUISITO: FFmpeg instalado
Veja: INSTALAR_FFMPEG.txt

COMO USAR:
1. Clique duplo em: Transcritor IA.exe
2. Clique em "Escolher Áudio"
3. Selecione um arquivo (MP3, MP4, MKV, etc)
4. Clique em "▶️ Iniciar Transcrição"
5. Aguarde processamento
6. Arquivos salvos na mesma pasta do áudio!

SAÍDAS:
- arquivo.txt  → Transcrição completa
- arquivo.srt  → Legendas com timing

DÚVIDAS?
Verifique o arquivo: transcritor.log
na mesma pasta do programa

Desenvolvido com Whisper (OpenAI)
```

---

## 4️⃣ INSTALAÇÃO NO OUTRO PC

### Para o usuário final:

**PASSO 1: Instalar FFmpeg**
1. Abra: `INSTALAR_FFMPEG.txt`
2. Siga as instruções
3. Reinicie o Windows

**PASSO 2: Usar o programa**
1. Clique duplo em: `Transcritor IA.exe`
2. Aguarde carregar (primeira vez pode levar 10s)
3. Clique em "Escolher Áudio"
4. Selecione um arquivo
5. Clique em "▶️ Iniciar Transcrição"

**PASSO 3: Resultados**
Os arquivos aparecem na mesma pasta do áudio original!

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### ❌ "FFmpeg não encontrado"
**Solução:**
1. Instale FFmpeg: https://ffmpeg.org/download.html
2. Abra `cmd` e digite: `ffmpeg -version`
3. Se não aparecer, adicione ao PATH:
   - Variáveis de ambiente → PATH → Novo
   - Cole: `C:\ffmpeg\bin`
   - Reinicie Windows

### ❌ "Python não encontrado"
**Solução:**
- Seu PC precisa de Python 3.10+
- [Download aqui](https://www.python.org/downloads/)
- ⚠️ Marque "Add Python to PATH" na instalação

### ❌ Executável não abre
**Solução 1:**
- FFmpeg pode estar faltando (veja acima)

**Solução 2:**
- Abra `cmd` na pasta do .exe e execute:
  ```cmd
  "Transcritor IA.exe"
  ```
  Você verá mensagens de erro claras

**Solução 3:**
- Verifique se não tem erro de permissão
- Clique direito → Executar como administrador

### ❌ Muito lento / Travando
**Solução:**
- Normal na primeira vez (modelo download = 140MB)
- Próximas vezes é mais rápido
- Sem GPU? Use CPU (mais lento, funciona)

### ❌ Arquivo SRT/TXT não criou
**Solução:**
1. Verifique pasta do áudio original
2. Procure por: `nome_do_arquivo.txt` e `.srt`
3. Se não encontrar, abra `transcritor.log` para ver erro

---

## 🎯 DICAS

### Performance
- Áudios **menores** = processamento **mais rápido**
- Com GPU: 10x mais rápido
- Sem GPU: Usa CPU (funciona, mas lento)

### Qualidade da transcrição
- Áudio **limpo** = melhor resultado
- Português é bem suportado
- Se tiver erros, tente modelo maior (edite .py)

### Segurança
- Todo processamento é **LOCAL**
- Nenhum dado é enviado para internet
- Arquivo log salva histórico

---

## 📝 CRIAR ATALHO NA ÁREA DE TRABALHO

1. Clique direito em: `Transcritor IA.exe`
2. Enviar para → Área de Trabalho (criar atalho)
3. Pronto! Clique duplo no atalho para abrir

---

## 🔧 CONFIGURAÇÃO AVANÇADA

**Mudar velocidade vs qualidade:**
1. Abra: `transcritor_melhorado.py` (com Notepad++)
2. Procure por: `MODEL: str = "base"`
3. Mude para:
   - `"tiny"` = MuitoRápido, MenosPreciso
   - `"base"` = Rápido, Preciso (padrão)
   - `"small"` = Normal, MaisPreciso
   - `"medium"` = Lento, MuitoPreciso
4. Salve e recrie o .exe

---

## ✅ CHECKLIST FINAL

Antes de distribuir, verifique:

- [ ] Python instalado e no PATH
- [ ] FFmpeg instalado e no PATH
- [ ] Executável criado sem erros
- [ ] Executável testa com um arquivo MP3
- [ ] Arquivo SRT criado corretamente
- [ ] Arquivo TXT criado corretamente
- [ ] Copiar texto funciona
- [ ] Cancelamento funciona
- [ ] Sem erros no transcritor.log

---

## 📧 SUPORTE

Se algo não funcionar:
1. Leia `transcritor.log` (salvo na pasta do .exe)
2. Verifique se FFmpeg está instalado: `ffmpeg -version`
3. Teste em um arquivo menor primeiro
4. Se persistir, pode ser erro do áudio (muito baixo, corrompido, etc)

---

**Pronto! Seu app está pronto para distribuição! 🚀**
