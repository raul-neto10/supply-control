# 🪟 SUPPLY CONTROL - INSTALAÇÃO WINDOWS

## ⚡ INÍCIO RÁPIDO (5 MINUTOS)

### 1️⃣ Instalar Python
- Download: https://www.python.org/downloads/ (Python 3.11+)
- **IMPORTANTE:** Marque ☑️ "Add Python to PATH"
- Reinicie o PC após instalação

### 2️⃣ Executar Instalação
```
1. Abra PowerShell como administrador
2. Navegue até: cd C:\caminho\supply-control
3. Execute: .\install_windows.bat
```

### 3️⃣ Iniciar Servidor
```
1. Execute: .\start_server.bat
2. Abra navegador: http://localhost:5000
3. Login: superadmin / superadmin
```

---

## 📦 O QUE ESTÁ INCLUÍDO

```
supply-control/
├── 📄 app.py                      # Aplicação principal
├── 📄 equipment_service.py        # Serviços de equipamento
├── 📄 bulk_import.py              # Importação em lote
├── 📋 requirements.txt            # Dependências
├── 📂 templates/                  # 27 páginas HTML
├── 📂 static/                     # CSS, JS, imagens
├── 🗄️  supply.db                   # Banco de dados (201 equipamentos)
│
├── 🪟 WINDOWS - SCRIPTS
├── 📜 install_windows.bat         # Instalar dependências
├── 📜 start_server.bat            # Iniciar servidor
├── 📜 backup_database.bat         # Fazer backup
├── 📜 install_as_service.ps1      # Instalar como serviço
│
├── 📚 DOCUMENTAÇÃO
├── 📖 INSTALACAO_WINDOWS.md       # Guia completo
├── 📖 README_WINDOWS.md           # Este arquivo
├── 📖 GUIA_CRIAR_USUARIOS.md      # Criar usuários
├── 📖 FUNCIONALIDADE_CRIAR_USUARIOS.md
└── 📖 Outros .md
```

---

## 🚀 SCRIPTS DISPONÍVEIS

| Script | Função | Como usar |
|--------|--------|-----------|
| `install_windows.bat` | Instala todas as dependências | Duplo clique ou execute no PowerShell |
| `start_server.bat` | Inicia a aplicação | Duplo clique para iniciar servidor |
| `backup_database.bat` | Faz backup do banco de dados | Executa backup automático com timestamp |
| `install_as_service.ps1` | Instala como serviço do Windows | Execute em PowerShell (Admin) |

---

## 💻 REQUISITOS MÍNIMOS

- **Windows:** Server 2016+, Win10/11 Pro
- **Python:** 3.11+ (não incluído)
- **RAM:** 512 MB
- **Espaço:** 500 MB
- **Acesso:** Permissões de Administrador

---

## 🎯 PASSOS DETALHADOS

### Passo 1: Preparar Pasta
```
C:\webapp\supply-control\
```
Cole TODOS os arquivos do projeto aqui

### Passo 2: Instalar Python
https://www.python.org/downloads/

```powershell
# Verificar após instalar
python --version
```

### Passo 3: Executar Instalação
```powershell
cd C:\webapp\supply-control
.\install_windows.bat
```

### Passo 4: Iniciar Servidor
```powershell
.\start_server.bat
```

Resultado:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Passo 5: Acessar Aplicação
- **URL:** http://localhost:5000
- **Usuário:** superadmin
- **Senha:** superadmin

---

## 🔐 SEGURANÇA

### Mudar Senha Padrão (OBRIGATÓRIO)
1. Login com: superadmin / superadmin
2. Menu → Minha Conta
3. Alterar senha

### Gerar Secret Key Segura
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Editar `app.py` (linha ~45):
```python
app.config['SECRET_KEY'] = '[copie_a_chave_gerada_aqui]'
```

---

## 🌐 ACESSAR DE OUTRO PC

1. Encontre IP do servidor:
```powershell
ipconfig
```

2. Procure por "IPv4 Address", ex: `192.168.1.100`

3. Configure Firewall (PowerShell Admin):
```powershell
netsh advfirewall firewall add rule name="Flask Supply" dir=in action=allow protocol=tcp localport=5000
```

4. Acesse de outro PC:
```
http://192.168.1.100:5000
```

---

## ⚙️ INSTALAR COMO SERVIÇO (Opcional)

Para servidor de produção, instale como serviço do Windows:

### Opção A: NSSM (Recomendado)
1. Download: https://nssm.cc/download
2. Extrair para: `C:\nssm\`
3. PowerShell (Admin):
```powershell
cd C:\webapp\supply-control
.\install_as_service.ps1
```

### Opção B: Task Scheduler (Simples)
1. Abra **Task Scheduler**
2. Crie nova tarefa:
   - **Nome:** SupplyControl
   - **Trigger:** "At Startup"
   - **Action:** 
     - Program: `C:\Python311\python.exe`
     - Arguments: `app.py`
     - Start in: `C:\webapp\supply-control`
   - **Advanced:** "Run with highest privileges"

### Gerenciar Serviço
```powershell
# Status
Get-Service SupplyControl

# Iniciar
Start-Service SupplyControl

# Parar
Stop-Service SupplyControl

# Ver logs
Get-Content -Path C:\webapp\supply-control\logs\app.log -Tail 50
```

---

## 🛠️ TROUBLESHOOTING

### ❌ "Python não encontrado"
```
✓ Instale Python 3.11+
✓ Reinicie o PC
✓ Marque "Add Python to PATH" na instalação
```

### ❌ "Port 5000 already in use"
```powershell
# Encontrar processo
netstat -ano | findstr :5000

# Matar processo (substituir 1234 pelo PID)
taskkill /PID 1234 /F

# Ou mudar porta em app.py:
# app.run(host='0.0.0.0', port=8000)
```

### ❌ "Module not found"
```powershell
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### ❌ "Permission denied"
```
Clique direito na pasta C:\webapp\supply-control
→ Propriedades → Segurança
→ Selecione "Usuários" → Editar
→ Marque "Controle Total"
```

### ❌ "Não consegue conectar"
```powershell
# Configurar firewall
netsh advfirewall firewall add rule name="Flask" dir=in action=allow protocol=tcp localport=5000

# Verificar se servidor está rodando
netstat -ano | findstr :5000
```

---

## 📊 BANCO DE DADOS

### Backup Automático
```
Duplo clique em: backup_database.bat
```

Cria em: `backups\supply_[data_hora].db`

### Restaurar Backup
```powershell
# Parar servidor
Ctrl+C

# Copiar backup antigo para supply.db
copy backups\supply_20260101_1430.db supply.db

# Reiniciar
.\start_server.bat
```

### SQLite em Windows
- Já incluído no Python
- Arquivo: `supply.db` (1 arquivo)
- Sincronizável com Linux/Mac

---

## 📈 PRODUÇÃO

### Otimizações
1. **Gunicorn** (WSGI Server)
```powershell
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

2. **Nginx** (Reverse Proxy)
- Download: https://nginx.org
- Distribui carga
- Cache estático

3. **PostgreSQL** (ao invés de SQLite)
```python
# Em app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/supply'
```

---

## 📝 LOGS

### Ver Logs
```powershell
# Logs da aplicação
Get-Content -Path C:\webapp\supply-control\logs\app.log -Tail 50

# Ou abra arquivo: C:\webapp\supply-control\logs\app.log
```

### Logs do Serviço
```powershell
# Eventos do Windows
Get-EventLog -LogName Application -Newest 20 | Format-List
```

---

## ✅ CHECKLIST

- [ ] Python 3.11+ instalado
- [ ] Arquivos copiados para `C:\webapp\supply-control\`
- [ ] `install_windows.bat` executado
- [ ] `start_server.bat` iniciado
- [ ] Acessível em `http://localhost:5000`
- [ ] Login funciona (superadmin)
- [ ] Senha alterada
- [ ] Firewall configurado
- [ ] Backup agendado (opcional)
- [ ] Serviço criado (opcional)

---

## 🆘 SUPORTE

### Documentação Completa
- [INSTALACAO_WINDOWS.md](INSTALACAO_WINDOWS.md) - Guia detalhado
- [GUIA_CRIAR_USUARIOS.md](GUIA_CRIAR_USUARIOS.md) - Criar usuários
- [README.md](README.md) - Funcionalidades gerais

### Erro Específico?
Verifique: `C:\webapp\supply-control\logs\app.log`

---

## 📞 INFORMAÇÕES DO SISTEMA

**Supply Control v1.0**
- Framework: Flask 3.0.0
- Python: 3.11+
- Banco: SQLite
- Servidor: Flask Development
- Data: 02/02/2026

---

**Pronto para usar! 🚀**
