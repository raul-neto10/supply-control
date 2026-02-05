@echo off
REM ============================================================================
REM  BACKUP DO BANCO DE DADOS
REM  ============================================================================
REM  Execute este arquivo para fazer backup do supply.db
REM ============================================================================

setlocal enabledelayedexpansion

color 0B
cls

echo.
echo ============================================================================
echo  ^> BACKUP - SUPPLY CONTROL
echo ============================================================================
echo.

REM Criar diretório de backups
if not exist "backups" (
    echo [*] Criando pasta de backups...
    mkdir backups
    echo [✓] Pasta criada
) else (
    echo [✓] Pasta de backups existe
)

echo.
echo [*] Obtendo data/hora atual...

REM Gerar timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

set TIMESTAMP=%mydate%_%mytime%

echo [✓] Timestamp: %TIMESTAMP%

echo.
echo [*] Realizando backup...

if exist "supply.db" (
    copy "supply.db" "backups\supply_%TIMESTAMP%.db" >nul 2>&1
    
    if %errorlevel% equ 0 (
        color 0A
        echo [✓] Backup realizado com sucesso!
        echo.
        echo Arquivo: backups\supply_%TIMESTAMP%.db
    ) else (
        color 0C
        echo [ERRO] Falha ao realizar backup
        echo.
        pause
        exit /b 1
    )
) else (
    color 0C
    echo [ERRO] Banco de dados (supply.db) não encontrado!
    echo.
    pause
    exit /b 1
)

echo.
echo [*] Limpando backups antigos (mantendo últimos 10)...

REM Listar backups
dir /b "backups\supply_*.db" | find /c /v "" > backups_count.txt
set /p COUNT=<backups_count.txt
del backups_count.txt

if %COUNT% gtr 10 (
    REM Deletar os backups mais antigos
    for /f "skip=10 delims=" %%a in ('dir /b /o-d "backups\supply_*.db"') do (
        del "backups\%%a"
        echo   - Removido: %%a
    )
    echo [✓] Limpeza concluída
) else (
    echo [✓] Nenhuma limpeza necessária (backups: %COUNT%/10)
)

echo.
echo ============================================================================
echo  [✓] BACKUP CONCLUÍDO
echo ============================================================================
echo.

pause
