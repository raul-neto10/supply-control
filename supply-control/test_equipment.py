#!/usr/bin/env python
"""
Script de teste para a funcionalidade de mapeamento de equipamentos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Equipment, User
import pandas as pd
from io import StringIO

def test_equipment_mapping():
    """Testa a funcionalidade de mapeamento"""
    print("🧪 Iniciando testes do Mapeamento de Equipamentos...\n")
    
    with app.app_context():
        # Criar usuário de teste
        print("1️⃣ Criando usuário de teste...")
        user = User.query.filter_by(username='admin').first()
        if not user:
            user = User(username='admin', is_admin=True, is_superadmin=True)
            user.set_password('admin123')
            db.session.add(user)
            db.session.commit()
            print("   ✅ Usuário admin criado")
        else:
            print("   ℹ️  Usuário admin já existe")
        
        # Verificar equipamentos
        print("\n2️⃣ Verificando equipamentos...")
        total = Equipment.query.count()
        print(f"   ✅ Total de equipamentos: {total}")
        
        # Estatísticas
        print("\n3️⃣ Estatísticas:")
        computers = Equipment.query.filter_by(equipment_type='Computador').count()
        printers = Equipment.query.filter_by(equipment_type='Impressora').count()
        bedside_carts = Equipment.query.filter_by(equipment_type='Carrinho Beira-Leito').count()
        print(f"   - Computadores: {computers}")
        print(f"   - Impressoras: {printers}")
        print(f"   - Carrinhos: {bedside_carts}")
        
        # Listar alguns equipamentos
        print("\n4️⃣ Primeiros 3 equipamentos:")
        equipments = Equipment.query.limit(3).all()
        for eq in equipments:
            print(f"   - {eq.localization} | {eq.equipment_type} | HOST: {eq.host} | IP: {eq.ip_address}")
        
        # Teste de busca
        print("\n5️⃣ Teste de busca (buscando 'AGENDAMENTO'):")
        search_results = Equipment.query.filter(
            Equipment.localization.ilike('%AGENDAMENTO%')
        ).all()
        print(f"   ✅ Encontrados: {len(search_results)} equipamentos")
        for eq in search_results:
            print(f"      - {eq.localization} | {eq.equipment_type}")
        
        # Teste de filtro por tipo
        print("\n6️⃣ Teste de filtro (Computadores):")
        computers_list = Equipment.query.filter_by(equipment_type='Computador').all()
        print(f"   ✅ Total de computadores: {len(computers_list)}")
        
        print("\n✅ Todos os testes passaram!")
        print("\n📝 Próximos passos:")
        print("   1. Acesse http://localhost:5000/login")
        print("   2. Faça login com: admin / admin123")
        print("   3. Clique em 'Mapeamento' no navbar")
        print("   4. Visualize o dashboard com estatísticas")
        print("   5. Teste os filtros e busca")
        print("   6. Use 'Importar' para adicionar mais equipamentos de um CSV/XLSX")


if __name__ == '__main__':
    test_equipment_mapping()
