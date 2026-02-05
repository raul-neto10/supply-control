@echo off
REM ============================================================================
REM  INICIAR SERVIDOR - SUPPLY CONTROL
REM  ============================================================================
REM  Execute este arquivo para iniciar a aplicação
REM ============================================================================

setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ============================================================================
echo  ^> INICIANDO SUPPLY CONTROL
echo ============================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Python não encontrado!
    echo.
    echo Instale Python 3.11+ e execute install_windows.bat primeiro
    echo.
    pause
    exit /b 1
)

echo [✓] Python verificado
echo.

REM Verificar dependências
echo [*] Verificando dependências...
pip list | findstr /i "Flask SQLAlchemy" >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Dependências não instaladas!
    echo.
    echo Execute: install_windows.bat
    echo.
    pause
    exit /b 1
)

echo [✓] Dependências verificadas
echo.

REM Criar diretório de logs
if not exist "logs" mkdir logs

REM Iniciar servidor
echo ============================================================================
echo  [✓] Iniciando servidor...
echo ============================================================================
echo.
echo Informações:
echo   - URL Local: http://localhost:5000
echo   - Para acessar de outro PC: http://[IP_DO_SERVIDOR]:5000
echo   - Usuário: superadmin
echo   - Senha: superadmin
echo.
echo Pressione CTRL+C para parar o servidor
echo.
echo ============================================================================
echo.

REM Tentar obter IP do servidor
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do set IP=%%a
set IP=%IP: =%
echo IP do servidor: %IP%
echo.


REM Iniciar aplicação usando o Python do ambiente virtual, se existir
if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" app.py
) else (
    python app.py
)

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERRO] Falha ao iniciar a aplicação
    echo.
    pause
    exit /b 1
)
