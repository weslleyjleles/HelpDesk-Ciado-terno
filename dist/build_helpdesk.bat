@echo off
echo ===== COMPILANDO HELP DESK =====

REM Caminho para o executável principal
set MAIN_SCRIPT=main.py

REM Verifica se o arquivo principal existe
if not exist %MAIN_SCRIPT% (
    echo ERRO: Arquivo %MAIN_SCRIPT% não encontrado.
    pause
    exit /b
)

REM Executa o PyInstaller com os parâmetros corretos
pyinstaller --noconfirm --windowed ^
--add-data "usuarios.json;." ^
--add-data "chamados.json;." ^
--add-data "anexos;anexos" ^
--add-data "imagens;imagens" ^
--icon=icone.ico %MAIN_SCRIPT%

echo ===== CONCLUÍDO =====
echo O executável está em: dist\main\
pause
