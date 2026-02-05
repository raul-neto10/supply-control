# 🖥️ SUPPLY CONTROL - DEPLOYMENT WINDOWS - GUIA DEFINITIVO

**Versão:** 1.0 | **Data:** 02/02/2026 | **Status:** ✅ PRONTO PARA SERVIDOR

---

## 📋 ÍNDICE

1. [O que está incluído](#o-que-está-incluído)
2. [Começar Rápido](#começar-rápido)
3. [Instalação Completa](#instalação-completa)
4. [Configuração Avançada](#configuração-avançada)
5. [Troubleshooting](#troubleshooting)
6. [Produção](#produção)

---

## 🎁 O QUE ESTÁ INCLUÍDO

### Arquivos Principais
- **`app.py`** - Aplicação Flask completa
- **`equipment_service.py`** - Serviço de equipamentos
- **`bulk_import.py`** - Importação em lote
- **`supply.db`** - Banco de dados com 201 equipamentos

### Scripts Windows (Novos)
| Script | Função | Uso |
|--------|--------|-----|
| `check_requirements.bat` | ✅ Verifica pré-requisitos | Executar primeiro |
| `install_windows.bat` | 📦 Instala dependências | Após Python |
| `start_server.bat` | 🚀 Inicia servidor | Desenvolvimento |
| `backup_database.bat` | 💾 Faz backup | Manutenção |
| `install_as_service.ps1` | ⚙️ Instala como serviço | Produção |

### Documentação
- **`README_WINDOWS.md`** - Guia rápido (este arquivo expandido)
- **`INSTALACAO_WINDOWS.md`** - Guia completo (60+ páginas)
- **`GUIA_CRIAR_USUARIOS.md`** - Gerenciar usuários
- **`config_windows.py`** - Configurações

### Web Files
- **`templates/`** - 27 páginas HTML
- **`static/`** - CSS, JavaScript, imagens
- **`requirements.txt`** - Lista de dependências

---

## ⚡ COMEÇAR RÁPIDO (10 MINUTOS)

### 1. Verificar Requisitos
```batch
check_requirements.bat
```

Resultado esperado:
```
[✓] Windows versão: 10.0
[✓] Python 3.11.x instalado
[✓] pip instalado
[✓] Porta 5000 disponível
[✓] SISTEMA PRONTO PARA INSTALAÇÃO
```

### 2. Instalar Dependências
```batch
install_windows.bat
```

Espere 2-3 minutos. Resultado:
```
[✓] pip atualizado
[✓] Todas as dependências instaladas com sucesso!
```

### 3. Iniciar Servidor
```batch
start_server.bat
```

Resultado:
```
[✓] Iniciando servidor...
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 4. Acessar
- **URL:** http://localhost:5000
- **Usuário:** superadmin
- **Senha:** superadmin

---

## 🔧 INSTALAÇÃO COMPLETA

### Pré-requisitos

#### 1. Python 3.11+
- Download: https://www.python.org/downloads/
- **CRÍTICO:** Marque ☑️ "Add Python to PATH"
- Clique "Install Now"
- Reinicie o Windows

Verificar:
```powershell
python --version
# Resultado esperado: Python 3.11.x ou superior
```

#### 2. PowerShell (Executar como Admin)
- Pressione: `Win + X`
- Clique: "Windows PowerShell (Admin)"
- OU procure: "PowerShell" → Clique direito → "Run as administrator"

#### 3. Permissões de Escrita
A pasta `C:\webapp\supply-control\` precisa ser gravável pelo usuário

### Passos de Instalação

#### Passo 1: Preparar Pasta
```powershell
# Criar pasta
mkdir C:\webapp\supply-control
cd C:\webapp\supply-control

# Copiar TODOS os arquivos do projeto aqui
# Deve conter: app.py, requirements.txt, templates/, static/, supply.db, etc.
```

#### Passo 2: Verificar Requisitos
```powershell
.\check_requirements.bat
```

Todos os ✓ devem aparecer

#### Passo 3: Instalar Dependências
```powershell
.\install_windows.bat
```

Aguarde conclusão (2-3 minutos)

#### Passo 4: Iniciar Servidor
```powershell
.\start_server.bat
```

Veja:
```
IP do servidor: 192.168.x.x
[✓] Iniciando servidor...
 * Running on http://127.0.0.1:5000
```

#### Passo 5: Testar Acesso
Abra navegador → http://localhost:5000

Login:
- Usuário: `superadmin`
- Senha: `superadmin`

✅ Tudo funcionando!

---

## ⚙️ CONFIGURAÇÃO AVANÇADA

### 1. Mudar Porta Padrão

Se porta 5000 estiver em uso:

**Opção A: Automaticamente**
```powershell
# Encontrar processo na porta
netstat -ano | findstr :5000

# Matar processo (substituir PID)
taskkill /PID 1234 /F
```

**Opção B: Mudar Porta**
Editar `app.py` (última linha):
```python
# Mude de: app.run(host='0.0.0.0', port=5000)
# Para:
app.run(host='0.0.0.0', port=8000)
```

Reiniciar servidor

### 2. Acessar de Outro Computador

#### Passo 1: Encontrar IP
```powershell
ipconfig
# Procure por: IPv4 Address: 192.168.x.x
```

#### Passo 2: Configurar Firewall
```powershell
# PowerShell (Admin)
netsh advfirewall firewall add rule name="Supply Control" dir=in action=allow protocol=tcp localport=5000
```

#### Passo 3: Acessar
De outro PC:
```
http://192.168.1.100:5000
```
(Substitua pelo IP real)

### 3. Mudar Senha Padrão

1. Login com `superadmin / superadmin`
2. Menu → "Minha Conta"
3. Clique "Alterar Senha"
4. Digite nova senha
5. Salvar

### 4. Gerar Secret Key Segura

Para produção:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Resultado exemplo:
```
a3f8c2d9e7b1f4c6a8e2d5f9c1b3a7e4
```

Editar `app.py` (linha ~45):
```python
# De:
app.config['SECRET_KEY'] = 'dev-secret-change-in-prod'

# Para:
app.config['SECRET_KEY'] = 'a3f8c2d9e7b1f4c6a8e2d5f9c1b3a7e4'
```

### 5. Ativar HTTPS (SSL/TLS)

Para comunicação segura (produção):

```powershell
# Instalar OpenSSL
pip install pyopenssl

# Gerar certificado (auto-assinado)
# Usar serviço como Let's Encrypt em produção
```

Editar `app.py`:
```python
if __name__ == '__main__':
    app.run(
        ssl_context=('cert.pem', 'key.pem'),
        host='0.0.0.0',
        port=443
    )
```

### 6. Usar PostgreSQL (em vez de SQLite)

Para sistemas maiores:

```powershell
# Instalar driver
pip install psycopg2-binary

# Criar banco em PostgreSQL
# CREATE DATABASE supply;
```

Editar `app.py`:
```python
# Mudar:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supply.db'

# Para:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/supply'
```

---

## 🚀 INSTALAR COMO SERVIÇO DO WINDOWS

Para servidor de produção (inicia automaticamente):

### Opção A: NSSM (Recomendado)

1. **Download NSSM**
   - Acesse: https://nssm.cc/download
   - Versão: `nssm-2.24-101-g897c7ad`

2. **Extrair**
   - Extraia para: `C:\nssm\`

3. **Instalar Serviço**
   ```powershell
   # PowerShell (Admin)
   cd C:\webapp\supply-control
   
   # Rodar script
   .\install_as_service.ps1
   ```

4. **Verificar**
   ```powershell
   Get-Service SupplyControl
   
   # Status: Running
   ```

### Opção B: Task Scheduler (Simples)

1. **Abrir Agendador**
   - Win + R
   - Digite: `taskschd.msc`
   - Enter

2. **Criar Tarefa**
   - Lado direito: "Criar Tarefa Básica..."
   - Nome: `SupplyControl`
   - Descrição: `Inicia aplicação de mapeamento`

3. **Definir Gatilho**
   - Abas → "Disparadores"
   - Novo → "Ao iniciar o sistema"
   - OK

4. **Definir Ação**
   - Aba "Ações"
   - Novo
   - Programa: `C:\Python311\python.exe`
   - Argumentos: `app.py`
   - Iniciar em: `C:\webapp\supply-control`
   - OK

5. **Permissões**
   - Aba "Geral"
   - ☑️ "Executar independentemente de qualquer logon do usuário"
   - ☑️ "Executar com privilégios mais altos"
   - OK

### Gerenciar Serviço

```powershell
# Status
Get-Service SupplyControl

# Iniciar
Start-Service SupplyControl

# Parar
Stop-Service SupplyControl

# Reiniciar
Restart-Service SupplyControl

# Ver logs (se usando NSSM)
Get-Content C:\webapp\supply-control\logs\app.log -Tail 50
```

---

## 💾 BACKUP E RESTAURAÇÃO

### Backup Automático

```batch
backup_database.bat
```

Cria em: `backups\supply_[data]_[hora].db`

### Agendar Backup Diário

Usando Task Scheduler:

1. Criar tarefa: `Daily Backup Supply`
2. Gatilho: 23:00 (todos os dias)
3. Ação: `C:\webapp\supply-control\backup_database.bat`

### Restaurar Backup

```powershell
# 1. Parar servidor
Stop-Service SupplyControl
# ou
# Ctrl+C (se rodando manualmente)

# 2. Copiar backup
copy C:\webapp\supply-control\backups\supply_20260102_1430.db C:\webapp\supply-control\supply.db

# 3. Reiniciar
Start-Service SupplyControl
# ou
# .\start_server.bat
```

---

## 🔍 TROUBLESHOOTING

### ❌ "Python não encontrado"

**Solução:**
1. Reinstale Python 3.11+
2. **CRÍTICO:** Marque "Add Python to PATH"
3. Reinicie o Windows
4. Verifique: `python --version`

---

### ❌ "Módulo não encontrado"

Exemplo: `ModuleNotFoundError: No module named 'flask'`

**Solução:**
```powershell
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Ou instalar individualmente
pip install Flask Flask-SQLAlchemy Flask-WTF WTForms Flask-Login reportlab python-barcode
```

---

### ❌ "Porta 5000 já está em uso"

**Solução:**
```powershell
# Encontrar processo
netstat -ano | findstr :5000
# Resultado: TCP    127.0.0.1:5000    LISTENING    1234

# Matar processo
taskkill /PID 1234 /F

# Ou usar porta diferente
# Editar app.py: port=8000
```

---

### ❌ "Permission denied"

Ao escrever no banco de dados

**Solução:**
1. Clique direito em `C:\webapp\supply-control`
2. Propriedades
3. Segurança
4. Editar
5. Selecione seu usuário
6. Marque ☑️ "Controle Total"
7. Aplicar → OK

---

### ❌ "Não consegue conectar de outro PC"

**Solução:**
```powershell
# 1. Configurar firewall
netsh advfirewall firewall add rule name="Supply" dir=in action=allow protocol=tcp localport=5000

# 2. Verificar IP
ipconfig

# 3. Acessar
# http://[IP_ENCONTRADO]:5000
```

---

### ❌ "Erro ao fazer login"

**Solução:**
1. Verifique usuário/senha (padrão: superadmin/superadmin)
2. Verifique se banco está acessível
3. Veja logs: `C:\webapp\supply-control\logs\app.log`

---

### ❌ "Aplicação muito lenta"

**Solução:**
1. Verificar uso de CPU/RAM:
   ```powershell
   Get-Process python | Format-Table
   ```
2. Reiniciar aplicação
3. Para produção, use Gunicorn:
   ```powershell
   pip install gunicorn
   gunicorn --workers 4 app:app
   ```

---

## 🏭 PRODUÇÃO

### Checklist de Produção

- [ ] Python 3.11+ instalado
- [ ] Dependências instaladas (`requirements.txt`)
- [ ] Banco de dados migrado/restaurado
- [ ] Secret Key alterada (não usar padrão)
- [ ] DEBUG = False em app.py
- [ ] HTTPS configurado (certificado SSL)
- [ ] Firewall configurado
- [ ] Backup automático agendado
- [ ] Monitoramento ativo
- [ ] Logs configurados
- [ ] Senha padrão (superadmin) alterada
- [ ] Serviço do Windows criado
- [ ] Teste de restauração de backup realizado

### Otimizações para Alta Carga

#### 1. Usar Gunicorn (WSGI Server)
```powershell
pip install gunicorn

# Executar com múltiplos workers
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

#### 2. Usar Nginx (Reverse Proxy)
- Download: https://nginx.org
- Distribui requisições
- Cache de arquivos estáticos

#### 3. Banco PostgreSQL
```python
# Melhor performance que SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/supply'
```

#### 4. Cache Redis
```powershell
# Instalar
pip install redis flask-caching

# Usar cache em memória
```

### Monitoramento

```powershell
# Ver processo
Get-Process python

# Ver portas em uso
netstat -ano | findstr :5000

# Ver logs de eventos
Get-EventLog -LogName Application -Newest 20

# Ver arquivo de log
Get-Content C:\webapp\supply-control\logs\app.log -Tail 100
```

---

## 📞 SUPORTE

### Documentação Completa
- **[INSTALACAO_WINDOWS.md](INSTALACAO_WINDOWS.md)** - 60+ páginas
- **[README_WINDOWS.md](README_WINDOWS.md)** - Guia rápido
- **[GUIA_CRIAR_USUARIOS.md](GUIA_CRIAR_USUARIOS.md)** - Usuários

### Logs
```powershell
# Ver últimas 50 linhas
Get-Content C:\webapp\supply-control\logs\app.log -Tail 50

# Ver todos os logs com erro
Select-String "ERROR" C:\webapp\supply-control\logs\app.log
```

### Testes de Conectividade
```powershell
# Testar porta
Test-NetConnection -ComputerName localhost -Port 5000

# Testar URL
Invoke-WebRequest http://localhost:5000
```

---

## ✅ RESUMO

| Etapa | Comando | Tempo |
|-------|---------|-------|
| 1. Verificar | `check_requirements.bat` | 1 min |
| 2. Instalar | `install_windows.bat` | 3 min |
| 3. Iniciar | `start_server.bat` | 1 min |
| 4. Testar | Acessar http://localhost:5000 | 1 min |
| **TOTAL** | | **6 min** |

---

## 🎉 PRONTO!

O Supply Control está instalado e funcionando no seu servidor Windows!

**Próximos passos:**
1. Criar usuários: Menu → Gerenciamento de Usuários
2. Importar dados: Menu → Mapeamento → Importar
3. Configurar backup: `backup_database.bat`
4. Instalar como serviço: `install_as_service.ps1`

---

**Versão:** 1.0 | **Data:** 02/02/2026 | **Status:** ✅ PRONTO

Para suporte adicional, consulte a documentação completa ou verifique os logs.
