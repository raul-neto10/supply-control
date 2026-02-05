# 🪟 GUIA DE INSTALAÇÃO EM SERVIDOR WINDOWS

## 📋 Pré-requisitos

- **Windows Server 2016+** ou **Windows 10/11 Pro**
- **Python 3.11+** (não incluído - precisa instalar)
- **SQLite3** (já incluído no Python)
- **Permissões de Administrador**
- **Mínimo 500MB de espaço livre**

---

## 🚀 PASSO 1: Instalar Python

### 1.1 Download
Acesse: https://www.python.org/downloads/
- Versão: **Python 3.11** ou superior
- **Importante:** Marque "Add Python to PATH" durante instalação

### 1.2 Verificar instalação
Abra **PowerShell** como administrador:
```powershell
python --version
pip --version
```

Saída esperada:
```
Python 3.11.x
pip 23.x
```

---

## 📦 PASSO 2: Preparar Projeto

### 2.1 Copiar arquivos
1. Crie pasta no servidor:
   ```
   C:\webapp\supply-control\
   ```

2. Copie TODOS os arquivos do projeto para essa pasta:
   - `app.py`
   - `equipment_service.py`
   - `bulk_import.py`
   - `requirements.txt`
   - `templates/` (pasta inteira)
   - `static/` (pasta inteira)
   - `supply.db` (se já tem dados)
   - `import_data.txt` (opcional)

### 2.2 Estrutura esperada
```
C:\webapp\supply-control\
├── app.py
├── equipment_service.py
├── bulk_import.py
├── requirements.txt
├── supply.db
├── templates\
│   ├── layout.html
│   ├── dashboard.html
│   ├── login.html
│   ├── ... (outros .html)
├── static\
│   └── ... (CSS, JS, imagens)
└── install_windows.bat (será criado)
```

---

## ⚙️ PASSO 3: Instalar Dependências

### 3.1 Opção A: Instalação Automática (Recomendado)
1. Na pasta `C:\webapp\supply-control\`
2. Execute: **`install_windows.bat`**
3. Aguarde conclusão (2-3 minutos)

### 3.2 Opção B: Instalação Manual
1. Abra **PowerShell** como administrador
2. Navegue até a pasta:
   ```powershell
   cd C:\webapp\supply-control
   ```
3. Execute:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 🎯 PASSO 4: Iniciar Servidor

### 4.1 Opção A: Inicializar Manualmente
1. Abra **PowerShell** como administrador
2. Na pasta do projeto:
   ```powershell
   python app.py
   ```
3. Saída esperada:
   ```
   * Running on http://127.0.0.1:5000
   * Press CTRL+C to quit
   ```

### 4.2 Opção B: Como Serviço do Windows (Recomendado para servidor)

#### Método 1: Usando NSSM (Non-Sucking Service Manager)
1. Download: https://nssm.cc/download
2. Extraia `nssm.exe` para `C:\nssm\`
3. Abra **PowerShell** como administrador:
   ```powershell
   cd C:\nssm
   .\nssm.exe install SupplyControl "C:\Python311\python.exe" "C:\webapp\supply-control\app.py"
   ```
4. Configure:
   - AppDirectory: `C:\webapp\supply-control`
   - Output: `C:\webapp\supply-control\logs\app.log`
5. Inicie o serviço:
   ```powershell
   net start SupplyControl
   ```

#### Método 2: Usando Task Scheduler (Simples)
1. Abra **Task Scheduler**
2. Crie nova tarefa:
   - **Nome:** SupplyControl
   - **Trigger:** "At startup"
   - **Action:** 
     - Program: `C:\Python311\python.exe`
     - Arguments: `C:\webapp\supply-control\app.py`
   - **Advanced:** "Run with highest privileges"

---

## 🌐 PASSO 5: Acessar a Aplicação

### 5.1 Acesso Local
- URL: `http://localhost:5000`
- Para acessar de outro computador:
  - Encontre o IP do servidor Windows:
    ```powershell
    ipconfig
    ```
  - Acesse: `http://[IP_DO_SERVIDOR]:5000`

### 5.2 Credenciais Padrão
```
Usuário: superadmin
Senha: superadmin
```

⚠️ **MUDE ESSA SENHA IMEDIATAMENTE NA PRODUÇÃO**

---

## 🔧 PASSO 6: Configurar Firewall

Para aceitar conexões de outros computadores:

### Opção A: PowerShell (Recomendado)
```powershell
netsh advfirewall firewall add rule name="Flask Supply Control" dir=in action=allow protocol=tcp localport=5000
```

### Opção B: Manualmente
1. Abra **Windows Defender Firewall**
2. Clique "Allow app through firewall"
3. Clique "Allow another app"
4. Selecione `python.exe`
5. Marque as caixas "Private" e "Public"

---

## 📊 PASSO 7: Verificar Banco de Dados

### 7.1 Se está restaurando de Linux
O arquivo `supply.db` funcionará identicamente no Windows (SQLite é multi-plataforma)

### 7.2 Se é nova instalação
Banco será criado automaticamente na primeira execução

---

## 🛡️ SEGURANÇA EM PRODUÇÃO

### 1. Alterar Secret Key
Edit `app.py` (linha ~45):
```python
# ❌ NÃO USE ISSO
app.config['SECRET_KEY'] = 'dev-secret-change-in-prod'

# ✅ USE ISSO (gerado aleatoriamente)
app.config['SECRET_KEY'] = 'sua-chave-super-secreta-muito-longa-e-aleatoria'
```

Gerar chave segura:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. HTTPS (SSL/TLS)
Instale certificado e configure:
```powershell
pip install pyopenssl
```

Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443)
```

### 3. Backup do Banco de Dados
Crie tarefa agendada para backup diário:
```batch
@echo off
REM Backup diário
FOR /F "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
copy "C:\webapp\supply-control\supply.db" "C:\webapp\backups\supply_%mydate%.db"
```

---

## 🐛 TROUBLESHOOTING

### Problema: "Python não encontrado"
```
Solução: 
1. Reinstale Python
2. Marque "Add Python to PATH"
3. Reinicie o computador
4. Tente: python --version
```

### Problema: "Port 5000 already in use"
```powershell
# Encontre o processo usando porta 5000
netstat -ano | findstr :5000

# Mate o processo (substitua PID)
taskkill /PID 1234 /F

# Ou mude a porta no app.py
app.run(host='0.0.0.0', port=8000)
```

### Problema: "Module not found"
```powershell
# Reinstale dependências
pip install --upgrade -r requirements.txt

# Ou instale manualmente
pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Login reportlab python-barcode
```

### Problema: "Permissão negada ao escrever no banco"
```
Solução:
1. Clique direito na pasta C:\webapp\supply-control
2. Propriedades → Segurança
3. Selecione "Usuários" → Editar
4. Marque "Controle Total"
5. Aplique
```

### Problema: "Aplicação não inicia como serviço"
```
Solução:
1. Verifique caminhos absolutos (não use C:\, use C:\\)
2. Verifique permissões do usuário do serviço
3. Veja logs: C:\webapp\supply-control\logs\app.log
```

---

## 📈 ESCALABILIDADE

### Para Produção com Alto Tráfego:

#### 1. Use Gunicorn (WSGI Server)
```powershell
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

#### 2. Use Nginx como Reverse Proxy
Download: https://nginx.org/en/download.html

Config `/nginx/conf/nginx.conf`:
```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. Use PostgreSQL ao invés de SQLite
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/supply'
```

---

## ✅ CHECKLIST FINAL

- [ ] Python 3.11+ instalado
- [ ] Arquivos copiados para `C:\webapp\supply-control\`
- [ ] Dependências instaladas (`requirements.txt`)
- [ ] Aplicação inicia com `python app.py`
- [ ] Acessível em `http://localhost:5000`
- [ ] Login funciona (superadmin / superadmin)
- [ ] Banco de dados carregado
- [ ] Firewall configurado
- [ ] Secret key alterada
- [ ] Backup agendado
- [ ] Serviço Windows criado (opcional)

---

## 📞 SUPORTE

Erros comuns e soluções em: **README.md**

Para logs detalhados:
```powershell
# Veja eventos do Windows
Get-EventLog -LogName Application -Newest 20
```

---

**Versão:** 1.0 | **Data:** 02/02/2026 | **Status:** Pronto para instalação
