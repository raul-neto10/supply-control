#!/usr/bin/env python
"""
Script para inicializar o banco de dados de equipamentos e importar dados
"""

import sys
import os

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Equipment
import pandas as pd
from io import StringIO

def init_database():
    """Inicializa o banco de dados de equipamentos"""
    with app.app_context():
        print("🔧 Criando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas!")


def import_sample_data():
    """Importa dados de amostra"""
    with app.app_context():
        print("\n📥 Importando dados de amostra...")
        
        # Dados de amostra
        sample_data = """LOCALIZAÇÃO / SETOR,TIPO,HOST,IP,PROCESSADOR,MEMÓRIA RAM,ARMAZENAMENTO,MAC,PATRIMÔNIO,SISTEMA OPERACIONAL,COD.MONITOR SIMPRESS
AGENDAMENTO,Computador,CSSMDSK117,10.53.0.44,CORE I3,4GB,120GB SSD,00-E0-4C-04-04-DA,,W10,
ALMOXARIFADO,Computador,CSSMDSK014,10.52.0.104,CORE I3,8GB,120GB SSD,64-1C-67-7A-00-2D,,W10,
CENTRO CIRURGICO,Computador,CSSMDSK179,10.52.0.140,CORE I3,8GB,120GBSSD,64:1C:67:69:B7:E3,,W10,
CLINICA MÉDICA,Computador,CSSMDSK047,10.53.0.105,CORE I3,8GB,120GB SSD,64-1C-67-7C-72-FA,SIMPRESS,W10,BRC44505FC
UTI A,Computador,CSSMDSK124,10.53.0.102,CORE I3,8GB,120GB SSD,00-E0-4C-D2-03-90,,W10,
FATURAMENTO CONVENIOS,Impressora,,10.51.0.114,,,,58-38-79-69-63-66,,,
CENTRO CIRURGICO,Impressora,,10.51.0.112,,,,58:38:79:69:29:DF,,,.
CENTRO DE REABILITAÇÃO PSQUIATRICO,Carrinho Beira-Leito,CSSMNTB007,10.51.0.11,CORE I5,16GB,240GBSSD,28:C5:C8:FB:FE:E9,,W11,"""
        
        # Converter para DataFrame
        df = pd.read_csv(StringIO(sample_data))
        
        imported = 0
        for index, row in df.iterrows():
            try:
                existing = Equipment.query.filter_by(host=row['HOST']).first() if pd.notna(row['HOST']) else None
                
                if not existing:
                    equipment = Equipment(
                        localization=row.get('LOCALIZAÇÃO / SETOR', ''),
                        equipment_type=row.get('TIPO', ''),
                        host=row.get('HOST') if pd.notna(row['HOST']) else None,
                        ip_address=row.get('IP') if pd.notna(row['IP']) else None,
                        processor=row.get('PROCESSADOR', ''),
                        memory_ram=row.get('MEMÓRIA RAM', ''),
                        storage=row.get('ARMAZENAMENTO', ''),
                        mac_address=row.get('MAC') if pd.notna(row['MAC']) else None,
                        patrimony_code=row.get('PATRIMÔNIO') if pd.notna(row['PATRIMÔNIO']) else None,
                        operating_system=row.get('SISTEMA OPERACIONAL', ''),
                        monitor_code=row.get('COD.MONITOR SIMPRESS') if pd.notna(row['COD.MONITOR SIMPRESS']) else None,
                        status='Ativo'
                    )
                    db.session.add(equipment)
                    imported += 1
            except Exception as e:
                print(f"⚠️  Erro na linha {index + 1}: {str(e)}")
        
        db.session.commit()
        print(f"✅ {imported} equipamentos importados!")


def show_statistics():
    """Mostra estatísticas"""
    with app.app_context():
        total = Equipment.query.count()
        
        computers = Equipment.query.filter_by(equipment_type='Computador').count()
        printers = Equipment.query.filter_by(equipment_type='Impressora').count()
        bedside_carts = Equipment.query.filter_by(equipment_type='Carrinho Beira-Leito').count()
        
        active = Equipment.query.filter_by(status='Ativo').count()
        maintenance = Equipment.query.filter_by(status='Manutenção').count()
        inactive = Equipment.query.filter_by(status='Inativo').count()
        
        print("\n📊 Estatísticas do Mapeamento:")
        print(f"  Total de equipamentos: {total}")
        print(f"  Computadores: {computers}")
        print(f"  Impressoras: {printers}")
        print(f"  Carrinhos Beira-Leito: {bedside_carts}")
        print(f"  Ativos: {active}")
        print(f"  Em Manutenção: {maintenance}")
        print(f"  Inativos: {inactive}")


if __name__ == '__main__':
    print("🚀 Inicializando mapeamento de equipamentos...\n")
    
    init_database()
    
    # Verificar se há dados
    with app.app_context():
        count = Equipment.query.count()
        if count == 0:
            print("Nenhum equipamento encontrado. Importando dados de amostra...")
            import_sample_data()
        
        show_statistics()
    
    print("\n✅ Inicialização concluída!")
