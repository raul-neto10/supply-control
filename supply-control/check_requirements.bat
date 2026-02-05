@echo off
REM ============================================================================
REM  VERIFICAÇÃO PRÉ-INSTALAÇÃO - SUPPLY CONTROL
REM  ============================================================================
REM  Execute este script para verificar se o sistema está pronto
REM ============================================================================

setlocal enabledelayedexpansion

color 0E
cls

echo.
echo ============================================================================
echo  ^> VERIFICAÇÃO PRÉ-INSTALAÇÃO - SUPPLY CONTROL
echo ============================================================================
echo.

set STATUS_OK=0
set STATUS_ERROR=0

REM ============================================================================
REM VERIFICAR WINDOWS
REM ============================================================================

echo [*] Verificando Sistema Operacional...

for /f "tokens=3" %%A in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentVersion') do (
    set WIN_VERSION=%%A
)

for /f "tokens=3" %%A in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentBuild') do (
    set WIN_BUILD=%%A
)

echo [✓] Windows versão: %WIN_VERSION% (Build %WIN_BUILD%)
set /a STATUS_OK+=1

echo.

REM ============================================================================
REM VERIFICAR PYTHON
REM ============================================================================

echo [*] Verificando Python...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [✓] !PYTHON_VERSION! instalado
    set /a STATUS_OK+=1
) else (
    echo [X] Python NÃO encontrado
    echo    Download: https://www.python.org/downloads/
    echo    Importante: Marque "Add Python to PATH"
    set /a STATUS_ERROR+=1
)

echo.

REM ============================================================================
REM VERIFICAR PIP
REM ============================================================================

echo [*] Verificando pip...

pip --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
    echo [✓] !PIP_VERSION!
    set /a STATUS_OK+=1
) else (
    echo [X] pip NÃO encontrado
    echo    Instale ou adicione Python ao PATH
    set /a STATUS_ERROR+=1
)

echo.

REM ============================================================================
REM VERIFICAR ESPAÇO EM DISCO
REM ============================================================================

echo [*] Verificando espaço em disco...

for /f "tokens=3" %%a in ('dir C:\ ^| findstr /r "[0-9]"') do (
    set DISK_SPACE=%%a
)

if exist "C:\" (
    echo [✓] Espaço em disco disponível
    set /a STATUS_OK+=1
) else (
    echo [X] Erro ao verificar espaço em disco
    set /a STATUS_ERROR+=1
)

echo.

REM ============================================================================
REM VERIFICAR ARQUIVOS NECESSÁRIOS
REM ============================================================================

echo [*] Verificando arquivos necessários...

set ARQUIVO_COUNT=0
set ARQUIVO_OK=0

if exist "app.py" (
    echo [✓] app.py encontrado
    set /a ARQUIVO_OK+=1
) else (
    echo [X] app.py NÃO encontrado
)
set /a ARQUIVO_COUNT+=1

if exist "requirements.txt" (
    echo [✓] requirements.txt encontrado
    set /a ARQUIVO_OK+=1
) else (
    echo [X] requirements.txt NÃO encontrado
)
set /a ARQUIVO_COUNT+=1

if exist "templates\" (
    echo [✓] Pasta templates encontrada
    set /a ARQUIVO_OK+=1
) else (
    echo [X] Pasta templates NÃO encontrada
)
set /a ARQUIVO_COUNT+=1

if exist "static\" (
    echo [✓] Pasta static encontrada
    set /a ARQUIVO_OK+=1
) else (
    echo [X] Pasta static NÃO encontrada
)
set /a ARQUIVO_COUNT+=1

if !ARQUIVO_OK! equ !ARQUIVO_COUNT! (
    set /a STATUS_OK+=1
) else (
    set /a STATUS_ERROR+=1
)

echo.

REM ============================================================================
REM VERIFICAR PERMISSÕES
REM ============================================================================

echo [*] Verificando permissões de pasta...

REM Tentar criar arquivo temporário
set TEMP_FILE=.permission_test_%random%.tmp

echo test > !TEMP_FILE! 2>nul
if exist !TEMP_FILE! (
    echo [✓] Permissão de escrita OK
    del !TEMP_FILE! >nul 2>&1
    set /a STATUS_OK+=1
) else (
    echo [X] Sem permissão de escrita
    echo    Clique direito na pasta e marque "Controle Total"
    set /a STATUS_ERROR+=1
)

echo.

REM ============================================================================
REM VERIFICAR PORTAS
REM ============================================================================

echo [*] Verificando portas...

netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [!] Porta 5000 já está em uso
    echo    Será necessário mudar a porta em app.py
) else (
    echo [✓] Porta 5000 disponível
    set /a STATUS_OK+=1
)

echo.

REM ============================================================================
REM RESUMO
REM ============================================================================

echo ============================================================================
echo  ^> RESULTADO DA VERIFICAÇÃO
echo ============================================================================
echo.

if %STATUS_ERROR% equ 0 (
    color 0A
    echo [✓✓✓] SISTEMA PRONTO PARA INSTALAÇÃO [✓✓✓]
    echo.
    echo Próximos passos:
    echo   1. Execute: install_windows.bat
    echo   2. Execute: start_server.bat
    echo   3. Acesse: http://localhost:5000
    echo.
) else (
    color 0C
    echo [XXX] PROBLEMAS ENCONTRADOS [XXX]
    echo.
    echo Itens OK:    %STATUS_OK%
    echo Itens ERRO:  %STATUS_ERROR%
    echo.
    echo Resolva os problemas acima e tente novamente.
    echo.
)

echo ============================================================================
echo.

pause
