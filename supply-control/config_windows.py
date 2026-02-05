# ============================================================================
# CONFIGURAÇÃO - SUPPLY CONTROL PARA WINDOWS
# ============================================================================
# Arquivo para facilitar a configuração em servidor Windows
# Edite este arquivo conforme necessário
# ============================================================================

# CONFIGURAÇÕES BÁSICAS
# ============================================================================

# Porta do servidor
# Padrão: 5000
# Mude se a porta estiver em uso
PORT = 5000

# Host (IP a ouvir)
# 127.0.0.1  = Apenas localhost
# 0.0.0.0    = Qualquer máquina na rede
HOST = '0.0.0.0'

# Debug mode (NUNCA em produção)
# True  = Modo desenvolvimento (reinicia automaticamente)
# False = Modo produção (mais rápido e seguro)
DEBUG = False

# ============================================================================
# BANCO DE DADOS
# ============================================================================

# Localização do banco de dados
# Use caminho absoluto ou relativo
DB_FILE = 'supply.db'

# Conectar a outro banco de dados?
# SQLite:      sqlite:///supply.db
# PostgreSQL:  postgresql://user:password@localhost/supply
# MySQL:       mysql+pymysql://user:password@localhost/supply
DATABASE_URL = None  # Se None, usa SQLite padrão

# ============================================================================
# SEGURANÇA
# ============================================================================

# IMPORTANTE: Altere isso em produção!
# Gerar chave: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = 'dev-secret-change-in-prod'

# ============================================================================
# SESSÃO
# ============================================================================

# Tempo da sessão (em segundos)
SESSION_TIMEOUT = 3600  # 1 hora

# Manter logado?
REMEMBER_ME_COOKIE_DURATION = 2592000  # 30 dias

# ============================================================================
# UPLOAD DE ARQUIVOS
# ============================================================================

# Pasta para uploads
UPLOAD_FOLDER = 'uploads'

# Tamanho máximo (em MB)
MAX_UPLOAD_SIZE = 50

# ============================================================================
# RELATÓRIOS
# ============================================================================

# Pasta para relatórios PDF
REPORTS_FOLDER = 'reports'

# Pasta para códigos de barras
BARCODES_FOLDER = 'static/barcodes'

# ============================================================================
# LOGS
# ============================================================================

# Pasta para logs
LOG_FOLDER = 'logs'

# Nível de log
# DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# ============================================================================
# PERFORMANCE
# ============================================================================

# Usar cache?
CACHE_ENABLED = True

# Tamanho do cache (MB)
CACHE_SIZE = 100

# ============================================================================
# EMAIL (opcional - para notificações)
# ============================================================================

# Ativar envio de email?
MAIL_ENABLED = False

# Configuração de email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'seu_email@gmail.com'
MAIL_PASSWORD = 'sua_senha_app'
MAIL_FROM = 'noreply@supplyccontrol.local'

# ============================================================================
# BACKUP AUTOMÁTICO
# ============================================================================

# Ativar backup automático?
AUTO_BACKUP = True

# Hora do backup (formato 24h, ex: 23 = 23:00)
BACKUP_HOUR = 23

# Manter quantos backups?
BACKUP_RETENTION = 10

# ============================================================================
# MONITORAMENTO
# ============================================================================

# Ativar health check?
HEALTH_CHECK_ENABLED = True

# Verificar a cada N minutos
HEALTH_CHECK_INTERVAL = 5

# ============================================================================
# PERSONALIZAÇÃO
# ============================================================================

# Nome do hospital/empresa
ORGANIZATION_NAME = 'Hospital Exemplo'

# Logo (URL ou caminho local)
LOGO_URL = '/static/logo.png'

# Tema
# light = Claro
# dark  = Escuro
THEME = 'light'

# ============================================================================
# LIMITES DO SISTEMA
# ============================================================================

# Máximo de equipamentos por página
ITEMS_PER_PAGE = 20

# Máximo de resultados de busca
MAX_SEARCH_RESULTS = 1000

# Máximo de registros para exportação
MAX_EXPORT_RECORDS = 10000

# ============================================================================
# FUNCIONALIDADES
# ============================================================================

# Ativar empréstimos?
LOANS_ENABLED = True

# Ativar movimentações?
MOVEMENTS_ENABLED = True

# Ativar relatórios?
REPORTS_ENABLED = True

# Ativar importação em lote?
BULK_IMPORT_ENABLED = True

# ============================================================================
# NOTAS DE CONFIGURAÇÃO
# ============================================================================

"""
MUDANÇAS EM PRODUÇÃO:
=====================

1. SECRET_KEY
   Gere uma chave segura:
   python -c "import secrets; print(secrets.token_hex(32))"
   Coloque em: SECRET_KEY = '[sua_chave_aqui]'

2. DEBUG
   Altere para: DEBUG = False

3. DATABASE_URL
   Para PostgreSQL:
   DATABASE_URL = 'postgresql://user:password@localhost/supply'

4. HOST
   Para acessar de outro PC:
   HOST = '0.0.0.0'
   Configure firewall do Windows

5. PORT
   Mude para 80 ou 443 (requer admin):
   PORT = 80

6. HTTPS
   Obtenha certificado SSL
   Configure em app.py com ssl_context

7. BACKUP
   Ative backup automático:
   AUTO_BACKUP = True

8. EMAIL
   Configure SMTP para notificações:
   MAIL_ENABLED = True
   MAIL_SERVER = 'seu_smtp'
   MAIL_USERNAME = 'seu_email'
   MAIL_PASSWORD = 'sua_senha'

9. MONITORAMENTO
   Habilite health check:
   HEALTH_CHECK_ENABLED = True

10. LIMITES
    Ajuste conforme performance:
    ITEMS_PER_PAGE = 20
    MAX_SEARCH_RESULTS = 1000
"""
