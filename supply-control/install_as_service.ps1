# ============================================================================
#  INSTALAÇÃO COMO SERVIÇO DO WINDOWS - SUPPLY CONTROL
# ============================================================================
#  Execute este script como administrador em PowerShell
# ============================================================================

# Requer permissões de administrador
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[ERRO] Este script deve ser executado como ADMINISTRADOR" -ForegroundColor Red
    Write-Host ""
    Write-Host "Clique direito no PowerShell e selecione 'Executar como administrador'"
    Write-Host ""
    pause
    exit
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host " > INSTALAÇÃO COMO SERVIÇO - SUPPLY CONTROL" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

# Verificar se NSSM está instalado
$nssm_path = "C:\nssm\nssm.exe"

if (-not (Test-Path $nssm_path)) {
    Write-Host "[!] NSSM não encontrado em C:\nssm\" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opções:" -ForegroundColor Cyan
    Write-Host "  1. Download manual em: https://nssm.cc/download" -ForegroundColor Cyan
    Write-Host "  2. Executar este script novamente após instalar" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Alternativa: Use Task Scheduler para iniciar na inicialização" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host "[✓] NSSM encontrado" -ForegroundColor Green
Write-Host ""

# Definir variáveis
$service_name = "SupplyControl"
$python_path = "C:\Python311\python.exe"
$app_path = Split-Path -Parent $MyInvocation.MyCommand.Path
$app_file = Join-Path $app_path "app.py"
$log_dir = Join-Path $app_path "logs"
$log_file = Join-Path $log_dir "app.log"

# Validar paths
Write-Host "[*] Verificando configurações..." -ForegroundColor Cyan

if (-not (Test-Path $python_path)) {
    Write-Host "[ERRO] Python não encontrado em: $python_path" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternativas:" -ForegroundColor Yellow
    Write-Host "  - Ajuste o caminho em: `$python_path = 'seu_caminho_python\python.exe'" -ForegroundColor Yellow
    Write-Host "  - Encontre o caminho: where python" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

if (-not (Test-Path $app_file)) {
    Write-Host "[ERRO] app.py não encontrado em: $app_file" -ForegroundColor Red
    pause
    exit
}

Write-Host "[✓] Python: $python_path" -ForegroundColor Green
Write-Host "[✓] App: $app_file" -ForegroundColor Green

# Criar diretório de logs
if (-not (Test-Path $log_dir)) {
    New-Item -ItemType Directory -Path $log_dir | Out-Null
    Write-Host "[✓] Diretório de logs criado: $log_dir" -ForegroundColor Green
}

Write-Host ""
Write-Host "[*] Instalando serviço 'SupplyControl'..." -ForegroundColor Cyan

# Verificar se serviço já existe
$service = Get-Service -Name $service_name -ErrorAction SilentlyContinue

if ($service) {
    Write-Host "[!] Serviço já existe. Removendo..." -ForegroundColor Yellow
    & $nssm_path stop $service_name 2>&1 | Out-Null
    & $nssm_path remove $service_name confirm 2>&1 | Out-Null
    Start-Sleep -Seconds 2
}

# Criar novo serviço
& $nssm_path install $service_name $python_path $app_file | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[✓] Serviço instalado com sucesso" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Falha ao instalar serviço" -ForegroundColor Red
    pause
    exit
}

# Configurar diretório
& $nssm_path set $service_name AppDirectory $app_path | Out-Null

# Configurar output
& $nssm_path set $service_name AppStdout $log_file | Out-Null
& $nssm_path set $service_name AppStderr $log_file | Out-Null

# Reiniciar automático
& $nssm_path set $service_name AppRestartDelay 5000 | Out-Null

Write-Host "[✓] Serviço configurado" -ForegroundColor Green
Write-Host ""

# Iniciar serviço
Write-Host "[*] Iniciando serviço..." -ForegroundColor Cyan
Start-Service -Name $service_name -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

$service = Get-Service -Name $service_name

if ($service.Status -eq 'Running') {
    Write-Host "[✓] Serviço iniciado com sucesso" -ForegroundColor Green
} else {
    Write-Host "[!] Serviço pode estar iniciando... aguarde" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host " [✓] INSTALAÇÃO CONCLUÍDA" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Informações do Serviço:" -ForegroundColor Cyan
Write-Host "  - Nome: SupplyControl" -ForegroundColor Cyan
Write-Host "  - Status: $($service.Status)" -ForegroundColor Cyan
Write-Host "  - Log: $log_file" -ForegroundColor Cyan
Write-Host ""

Write-Host "Comandos úteis:" -ForegroundColor Yellow
Write-Host "  - Iniciar:  net start SupplyControl" -ForegroundColor Yellow
Write-Host "  - Parar:    net stop SupplyControl" -ForegroundColor Yellow
Write-Host "  - Status:   Get-Service SupplyControl" -ForegroundColor Yellow
Write-Host "  - Remover:  nssm remove SupplyControl confirm" -ForegroundColor Yellow
Write-Host ""

Write-Host "Acessar aplicação:" -ForegroundColor Cyan
Write-Host "  - URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "  - Verificar logs: $log_file" -ForegroundColor Cyan
Write-Host ""

pause
