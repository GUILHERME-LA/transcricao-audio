@echo off
REM Script para empacotar o Transcritor como executável
REM Requer: Python 3.10+ e pip

echo.
echo ===== CONSTRUTOR DE EXECUTAVEL - TRANSCRITOR IA =====
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! Instale Python 3.10+
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Atualizando pip...
python -m pip install --upgrade pip

echo.
echo [2/5] Instalando dependências...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [3/5] Criando executável...
echo (Isto pode levar 2-5 minutos, por favor aguarde)

pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=transcritor.ico ^
    --add-data "transcritor.ico;." ^
    --name "Transcritor IA" ^
    --specpath build ^
    --distpath dist ^
    --buildpath build ^
    transcritor_melhorado.py

echo.
echo [4/5] Verificando saída...
if exist "dist\Transcritor IA.exe" (
    echo [OK] Executável criado com sucesso!
    echo.
    echo Localização: dist\Transcritor IA.exe
) else (
    echo [ERRO] Falha ao criar executável
    pause
    exit /b 1
)

echo.
echo [5/5] Limpando arquivos temporários...
rmdir /s /q build 2>nul
rmdir /s /q "__pycache__" 2>nul
del /q "*.spec" 2>nul

echo.
echo ===== PRONTO! =====
echo.
echo Seu executável foi criado em: dist\Transcritor IA.exe
echo.
echo Para distribuir em outro PC:
echo 1. Copie: dist\Transcritor IA.exe
echo 2. Instale FFmpeg (https://ffmpeg.org/download.html)
echo 3. Execute o .exe
echo.
pause
