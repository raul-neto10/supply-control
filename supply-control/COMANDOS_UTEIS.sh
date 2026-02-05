#!/bin/bash
# COMANDOS ÚTEIS - Mapeamento de Equipamentos

# ==================== INICIAR/PARAR SERVIDOR ====================

# Iniciar servidor Flask
alias start-server='cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python app.py'

# Iniciar servidor em background
alias start-server-bg='cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python app.py > flask_server.log 2>&1 &'

# Parar servidor
alias stop-server='pkill -f "python app.py"'

# Ver status do servidor
alias status-server='ps aux | grep "python app.py" | grep -v grep'

# ==================== TESTAR E VERIFICAR ====================

# Executar testes
alias test-equipment='cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python test_equipment.py'

# Ver últimas linhas do log
alias log-tail='tail -50 /home/rps1002/Documentos/Projects/supply-control/flask_server.log'

# Ver erro específico
alias log-errors='grep -i "error\|traceback" /home/rps1002/Documentos/Projects/supply-control/flask_server.log'

# ==================== BANCO DE DADOS ====================

# Reinicializar banco de dados
alias reinit-db='cd /home/rps1002/Documentos/Projects/supply-control && rm supply.db && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python init_equipment_mapping.py'

# Backup do banco
alias backup-db='cp /home/rps1002/Documentos/Projects/supply-control/supply.db /home/rps1002/Documentos/Projects/supply-control/supply.db.backup'

# Restaurar backup
alias restore-db='cp /home/rps1002/Documentos/Projects/supply-control/supply.db.backup /home/rps1002/Documentos/Projects/supply-control/supply.db'

# ==================== LIMPEZA E MANUTENÇÃO ====================

# Limpar cache Python
alias clean-cache='cd /home/rps1002/Documentos/Projects/supply-control && find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; find . -name "*.pyc" -delete 2>/dev/null'

# Remover arquivos de upload antigos
alias clean-uploads='rm -rf /home/rps1002/Documentos/Projects/supply-control/uploads/*'

# ==================== ACESSO DIRETO ====================

# Ir para diretório do projeto
alias go-project='cd /home/rps1002/Documentos/Projects/supply-control'

# Abrir projeto em VS Code
alias open-vscode='code /home/rps1002/Documentos/Projects/supply-control'

# ==================== DADOS E CONFIGURAÇÃO ====================

# Listar todos os equipamentos
alias list-equipment='cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python -c "from app import app, db, Equipment; ctx = app.app_context(); ctx.push(); [print(f\"{e.localization} | {e.equipment_type} | {e.host} | {e.ip_address}\") for e in Equipment.query.all()]; ctx.pop()"'

# Contar equipamentos
alias count-equipment='cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python -c "from app import app, db, Equipment; ctx = app.app_context(); ctx.push(); print(f\"Total: {Equipment.query.count()}\"); ctx.pop()"'

# ==================== DOCUMENTAÇÃO ====================

# Ver documentação de uso
alias doc-uso='cat /home/rps1002/Documentos/Projects/supply-control/MAPEAMENTO_EQUIPAMENTOS.md'

# Ver documentação técnica
alias doc-tech='cat /home/rps1002/Documentos/Projects/supply-control/IMPLEMENTACAO_MAPEAMENTO.md'

# Ver resumo
alias doc-resumo='cat /home/rps1002/Documentos/Projects/supply-control/RESUMO_IMPLEMENTACAO.txt'

# Ver quick start
alias doc-quick='cat /home/rps1002/Documentos/Projects/supply-control/README_MAPEAMENTO.txt'

# ==================== IMPORTAR/EXPORTAR ====================

# Exportar dados para backup
alias export-csv='cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python -c "from app import app, db, Equipment; import csv; ctx = app.app_context(); ctx.push(); equipments = Equipment.query.all(); f = open(\"equipments_backup.csv\", \"w\"); w = csv.DictWriter(f, fieldnames=equipments[0].to_dict().keys()); w.writeheader(); [w.writerow(e.to_dict()) for e in equipments]; f.close(); print(\"Exportado: equipments_backup.csv\"); ctx.pop()"'

# ==================== EXEMPLOS DE USO ====================

# EXEMPLO 1: Iniciar servidor e acessar
# $ start-server-bg
# $ sleep 2
# Abra: http://localhost:5000

# EXEMPLO 2: Executar testes
# $ test-equipment
# Verá: ✅ Todos os testes passaram!

# EXEMPLO 3: Ver estatísticas
# $ count-equipment
# Verá: Total: 8

# EXEMPLO 4: Limpar e reinicializar
# $ clean-cache
# $ reinit-db
# $ test-equipment

# EXEMPLO 5: Fazer backup
# $ backup-db
# $ clean-cache
# $ reinit-db
# $ restore-db

# ==================== SCRIPTS ÚTEIS ====================

# Script para reiniciar tudo
restart-all() {
    echo "🔄 Reiniciando..."
    stop-server
    sleep 1
    clean-cache
    start-server-bg
    sleep 2
    status-server
    echo "✅ Servidor reiniciado!"
}

# Script para verificar saúde do sistema
health-check() {
    echo "🏥 Verificando saúde do sistema..."
    
    echo "1️⃣ Status do servidor:"
    ps aux | grep "python app.py" | grep -v grep && echo "   ✅ Rodando" || echo "   ❌ Parado"
    
    echo -e "\n2️⃣ Conexão com banco:"
    cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python -c "from app import app, db, Equipment; ctx = app.app_context(); ctx.push(); count = Equipment.query.count(); print(f\"   ✅ {count} equipamentos\"); ctx.pop()" 2>/dev/null || echo "   ❌ Erro no banco"
    
    echo -e "\n3️⃣ Teste de conexão HTTP:"
    curl -s http://localhost:5000/login > /dev/null && echo "   ✅ Conectado" || echo "   ❌ Desconectado"
    
    echo -e "\n✅ Verificação concluída!"
}

# Script para ver logs em tempo real
tail-logs() {
    tail -f /home/rps1002/Documentos/Projects/supply-control/flask_server.log
}

# ==================== COMBINAÇÕES ÚTEIS ====================

# Fazer setup completo
setup-complete() {
    echo "📦 Setup Completo"
    clean-cache
    reinit-db
    start-server-bg
    sleep 2
    test-equipment
    echo "✅ Setup concluído!"
}

# Gerar relatório
report() {
    echo "📊 RELATÓRIO DO SISTEMA"
    echo "======================="
    echo ""
    echo "Versão: 1.0"
    echo "Status: $(status-server | wc -l) processo(s)"
    echo "Equipamentos: $(cd /home/rps1002/Documentos/Projects/supply-control && /home/rps1002/Documentos/Projects/supply-control/.venv-1/bin/python -c "from app import app, db, Equipment; ctx = app.app_context(); ctx.push(); print(Equipment.query.count()); ctx.pop()" 2>/dev/null)"
    echo "Data: $(date '+%d/%m/%Y %H:%M:%S')"
    echo ""
    echo "Arquivos principais:"
    echo "  • app.py"
    echo "  • equipment_service.py"
    echo "  • supply.db"
    echo ""
    echo "Documentação:"
    ls -1 /home/rps1002/Documentos/Projects/supply-control/*.md /home/rps1002/Documentos/Projects/supply-control/*.txt 2>/dev/null | grep -i "mapeamento\|equipment" | xargs -I {} basename {}
}

# ==================== INSTRU ÇÕES ====================

cat << 'INSTRUCTIONS'

📚 INSTRUÇÕES DE USO DOS COMANDOS

Para usar os aliases, primeiro source este arquivo:
  $ source COMANDOS_UTEIS.sh

Ou adicione a seu ~/.bashrc:
  $ cat COMANDOS_UTEIS.sh >> ~/.bashrc
  $ source ~/.bashrc

COMANDOS PRINCIPAIS:
  start-server         - Inicia servidor em foreground
  start-server-bg      - Inicia servidor em background
  stop-server          - Para o servidor
  status-server        - Verifica status do servidor
  
TESTES:
  test-equipment       - Executa testes da funcionalidade
  health-check         - Verifica saúde completa
  
BANCO DE DADOS:
  reinit-db            - Reinicializa banco com dados de amostra
  backup-db            - Faz backup do banco
  restore-db           - Restaura backup
  
UTILITÁRIOS:
  clean-cache          - Limpa cache Python
  clean-uploads        - Remove uploads antigos
  count-equipment      - Conta equipamentos no banco
  list-equipment       - Lista todos os equipamentos
  export-csv           - Exporta para CSV
  
DOCUMENTAÇÃO:
  doc-uso              - Abre guia de uso
  doc-tech             - Abre detalhes técnicos
  doc-resumo           - Abre resumo de implementação
  doc-quick            - Abre quick start
  
SCRIPTS ESPECIAIS:
  restart-all          - Reinicia tudo
  tail-logs            - Acompanha logs em tempo real
  report               - Gera relatório do sistema
  setup-complete       - Setup completo do zero
  
EXEMPLOS:
  $ start-server-bg && test-equipment
  $ health-check
  $ restart-all
  $ setup-complete

INSTRUCTIONS
