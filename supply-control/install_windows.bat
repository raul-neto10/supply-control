@echo off
REM ============================================================================
REM  INSTALAÇÃO AUTOMÁTICA - SUPPLY CONTROL PARA WINDOWS
REM  ============================================================================
REM  Este script instala todas as dependências necessárias
REM  Execute como ADMINISTRADOR
REM ============================================================================

setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ============================================================================
echo  ^> SUPPLY CONTROL - INSTALAÇÃO WINDOWS
echo ============================================================================
echo.

REM Verificar se está executando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Este script deve ser executado como ADMINISTRADOR
    echo.
    echo Abra PowerShell como administrador e tente novamente
    pause
    exit /b 1
)

echo [✓] Permissões de administrador confirmadas
echo.

REM Verificar Python
echo [*] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Python não encontrado!
    echo.
    echo Instale Python 3.11+ de: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante instalação
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [✓] %PYTHON_VERSION% encontrado

REM Verificar pip
echo.
echo [*] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] pip não encontrado!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('pip --version') do set PIP_VERSION=%%i
echo [✓] %PIP_VERSION% encontrado

REM Criar diretórios
echo.
echo [*] Criando estrutura de diretórios...
if not exist "logs" mkdir logs
if not exist "static\barcodes" mkdir static\barcodes
if not exist "templates" mkdir templates
echo [✓] Diretórios criados

REM Upgrade pip
echo.
echo [*] Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1
echo [✓] pip atualizado

REM Instalar dependências
echo.
echo [*] Instalando dependências (pode levar alguns minutos)...
echo.

pip install Flask==3.0.0 ^
    Flask-SQLAlchemy==3.1.1 ^
    Flask-WTF==1.2.1 ^
    WTForms==3.1.1 ^
    Flask-Login==0.6.3 ^
    reportlab==4.0.7 ^
    python-barcode==0.15.1 ^
    requests==2.31.0

if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Falha ao instalar dependências
    echo.
    pause
    exit /b 1
)

echo.
echo [✓] Todas as dependências instaladas com sucesso!

REM Criar banco de dados
echo.
echo [*] Verificando banco de dados...
if not exist "supply.db" (
    echo [*] Banco de dados não encontrado, será criado na primeira execução
) else (
    echo [✓] Banco de dados existente encontrado
)

REM Resumo
echo.
echo ============================================================================
echo  ^> INSTALAÇÃO CONCLUÍDA COM SUCESSO
echo ============================================================================
echo.
echo Próximos passos:
echo.
echo 1. Para iniciar a aplicação, execute:
echo    python app.py
echo.
echo 2. Acesse em seu navegador:
echo    http://localhost:5000
echo.
echo 3. Credenciais padrão:
echo    Usuário: superadmin
echo    Senha: superadmin
echo.
echo IMPORTANTE: Mude a senha imediatamente!
echo.
echo Para mais informações, consulte INSTALACAO_WINDOWS.md
echo.
echo ============================================================================

pause
