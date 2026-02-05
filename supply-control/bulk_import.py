"""
Script para importar dados em lote (bulk import) de equipamentos
Processa dados tab-separated e insere no banco de dados
"""

import sys
import os
from io import StringIO
from datetime import datetime

# Adicionar o diretório do projeto ao path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app import app, db, Equipment


def normalize_mac_address(mac):
    """Normaliza endereço MAC para o formato padrão XX-XX-XX-XX-XX-XX"""
    if not mac or mac.strip() == '':
        return None
    
    mac = mac.strip().upper()
    
    # Remover caracteres especiais
    import re
    mac = re.sub(r'[^0-9A-F]', '', mac)
    
    if len(mac) != 12:
        return None
    
    # Formatar com hífens
    return '-'.join(mac[i:i+2] for i in range(0, 12, 2))


def normalize_memory(memory):
    """Normaliza valor de memória"""
    if not memory or memory.strip() == '':
        return None
    
    memory = str(memory).strip().upper()
    
    # Remover caracteres extra
    import re
    memory = re.sub(r'\s+', '', memory)
    
    return memory


def normalize_storage(storage):
    """Normaliza valor de armazenamento"""
    if not storage or storage.strip() == '':
        return None
    
    storage = str(storage).strip().upper()
    
    # Remover espaços extras, manter formato
    import re
    storage = re.sub(r'\s+', '', storage)
    
    return storage


def normalize_operating_system(os_str):
    """Normaliza sistema operacional"""
    if not os_str or os_str.strip() == '':
        return None
    
    os_str = str(os_str).strip().upper()
    
    # Mapeamento de valores comuns
    os_map = {
        'W10': 'Windows 10',
        'W11': 'Windows 11',
        'W7': 'Windows 7',
        'WINDOWS 10': 'Windows 10',
        'WINDOWS 11': 'Windows 11',
        'WINDOWS 7': 'Windows 7',
    }
    
    return os_map.get(os_str, os_str)


def normalize_equipment_type(eq_type):
    """Normaliza tipo de equipamento"""
    if not eq_type:
        return None
    
    eq_type = str(eq_type).strip()
    
    # Mapeamento de tipos válidos
    valid_types = [
        'Computador',
        'Notebook',
        'Impressora',
        'Carrinho Beira-Leito'
    ]
    
    for vtype in valid_types:
        if vtype.lower() in eq_type.lower():
            return vtype
    
    return eq_type


def normalize_ip_address(ip):
    """Normaliza endereço IP"""
    if not ip or ip.strip() == '':
        return None
    
    ip = str(ip).strip()
    
    # Validação básica de IP
    parts = ip.split('.')
    if len(parts) == 4:
        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return None
            return ip
        except ValueError:
            return None
    
    return None


def parse_equipment_data(data_text):
    """
    Parseia dados tab-separated do equipamento
    Retorna lista de dicionários com os dados normalizados
    """
    lines = data_text.strip().split('\n')
    equipment_list = []
    errors = []
    
    for line_num, line in enumerate(lines, 1):
        # Pular linhas vazias ou que contenham apenas espaços
        if not line.strip():
            continue
        
        # Última linha pode ser a mensagem do usuário
        if 'insira todos' in line.lower():
            continue
        
        # Dividir por tab
        fields = line.split('\t')
        
        # Esperamos pelo menos 10 campos
        if len(fields) < 10:
            # Pode ser uma linha incompleta, verificar se tem dados importantes
            if len(fields) < 2:
                continue
        
        try:
            # Mapear campos conforme o padrão
            localization = fields[0].strip() if len(fields) > 0 else None
            equipment_type = fields[1].strip() if len(fields) > 1 else None
            host = fields[2].strip() if len(fields) > 2 else None
            ip_address = fields[3].strip() if len(fields) > 3 else None
            processor = fields[4].strip() if len(fields) > 4 else None
            memory_ram = fields[5].strip() if len(fields) > 5 else None
            storage = fields[6].strip() if len(fields) > 6 else None
            mac_address = fields[7].strip() if len(fields) > 7 else None
            monitor_code = fields[8].strip() if len(fields) > 8 else None
            operating_system = fields[9].strip() if len(fields) > 9 else None
            patrimony_code = fields[10].strip() if len(fields) > 10 else None
            notes = fields[11].strip() if len(fields) > 11 else None
            
            # Pular se não tem localização ou tipo
            if not localization or not equipment_type:
                continue
            
            # Normalizar valores
            equipment_type = normalize_equipment_type(equipment_type)
            if not equipment_type:
                errors.append(f"Linha {line_num}: Tipo de equipamento inválido")
                continue
            
            mac_address = normalize_mac_address(mac_address)
            memory_ram = normalize_memory(memory_ram)
            storage = normalize_storage(storage)
            operating_system = normalize_operating_system(operating_system)
            ip_address = normalize_ip_address(ip_address)
            
            # Pular campos vazios
            host = host if host else None
            monitor_code = monitor_code if monitor_code else None
            patrimony_code = patrimony_code if patrimony_code else None
            notes = notes if notes else None
            
            # Criar dicionário de equipamento
            equipment = {
                'localization': localization,
                'equipment_type': equipment_type,
                'host': host,
                'ip_address': ip_address,
                'processor': processor if processor else None,
                'memory_ram': memory_ram,
                'storage': storage,
                'mac_address': mac_address,
                'monitor_code': monitor_code,
                'operating_system': operating_system,
                'patrimony_code': patrimony_code,
                'status': 'Ativo',
                'notes': notes
            }
            
            equipment_list.append(equipment)
            
        except Exception as e:
            errors.append(f"Linha {line_num}: Erro ao processar - {str(e)}")
    
    return equipment_list, errors


def check_duplicate_equipment(equipment_data, app_context=None):
    """
    Verifica se equipamento já existe no banco de dados
    Retorna True se duplicado, False caso contrário
    """
    # Verificar por host
    if equipment_data.get('host'):
        if Equipment.query.filter_by(host=equipment_data['host']).first():
            return True
    
    # Verificar por IP
    if equipment_data.get('ip_address'):
        if Equipment.query.filter_by(ip_address=equipment_data['ip_address']).first():
            return True
    
    # Verificar por MAC
    if equipment_data.get('mac_address'):
        if Equipment.query.filter_by(mac_address=equipment_data['mac_address']).first():
            return True
    
    # Verificar por código de patrimônio
    if equipment_data.get('patrimony_code'):
        if Equipment.query.filter_by(patrimony_code=equipment_data['patrimony_code']).first():
            return True
    
    return False


def bulk_import_equipment(data_text):
    """
    Importa todos os equipamentos do texto tab-separated
    Retorna relatório de importação
    """
    print("=" * 70)
    print("INICIANDO IMPORTAÇÃO EM LOTE DE EQUIPAMENTOS")
    print("=" * 70)
    
    # Parser dados
    print("\n1. Parsing dos dados...")
    equipment_list, parse_errors = parse_equipment_data(data_text)
    print(f"   ✓ {len(equipment_list)} registros processados com sucesso")
    
    if parse_errors:
        print(f"   ⚠ {len(parse_errors)} erros encontrados durante parsing:")
        for error in parse_errors[:5]:  # Mostrar primeiros 5
            print(f"     - {error}")
        if len(parse_errors) > 5:
            print(f"     ... e mais {len(parse_errors) - 5} erros")
    
    # Abrir contexto da aplicação
    with app.app_context():
        # Verificar duplicatas
        print(f"\n2. Verificando duplicatas...")
        duplicates = 0
        unique_equipment = []
        
        for equip in equipment_list:
            if check_duplicate_equipment(equip):
                duplicates += 1
            else:
                unique_equipment.append(equip)
        
        print(f"   ✓ {len(unique_equipment)} registros únicos para inserir")
        if duplicates > 0:
            print(f"   ⚠ {duplicates} duplicatas encontradas (não serão importadas)")
        
        # Inserir dados
        print(f"\n3. Inserindo dados no banco de dados...")
        inserted = 0
        errors_on_insert = []
        batch_size = 20
        
        for idx, equip_data in enumerate(unique_equipment, 1):
            try:
                # Criar equipamento
                equipment = Equipment(
                    localization=equip_data['localization'],
                    equipment_type=equip_data['equipment_type'],
                    host=equip_data.get('host'),
                    ip_address=equip_data.get('ip_address'),
                    processor=equip_data.get('processor'),
                    memory_ram=equip_data.get('memory_ram'),
                    storage=equip_data.get('storage'),
                    mac_address=equip_data.get('mac_address'),
                    monitor_code=equip_data.get('monitor_code'),
                    operating_system=equip_data.get('operating_system'),
                    patrimony_code=equip_data.get('patrimony_code'),
                    status=equip_data.get('status', 'Ativo'),
                    notes=equip_data.get('notes'),
                    last_updated=datetime.utcnow()
                )
                
                db.session.add(equipment)
                
                # Commit a cada N registros ou no final
                if idx % batch_size == 0 or idx == len(unique_equipment):
                    try:
                        db.session.commit()
                        inserted = idx
                        if idx % (batch_size * 5) == 0 or idx == len(unique_equipment):
                            print(f"   ✓ {idx}/{len(unique_equipment)} registros inseridos...")
                    except Exception as commit_error:
                        db.session.rollback()
                        # Registrar o erro mas continuar
                        errors_on_insert.append(f"Erro ao inserir equipamento(s) no batch {idx}: {str(commit_error)[:80]}")
                        print(f"   ⚠ Erro ao inserir equipamento {idx}: {str(commit_error)[:60]}...")
                
            except Exception as e:
                # Se houver erro ao criar o objeto, apenas registra e continua
                errors_on_insert.append(f"Erro ao preparar equipamento {idx}: {str(e)[:80]}")
                continue
    
        print(f"   ✓ Total de {inserted} registros inseridos com sucesso")
    
    # Relatório final
    print(f"\n" + "=" * 70)
    print("RELATÓRIO DE IMPORTAÇÃO")
    print("=" * 70)
    print(f"Total de registros processados: {len(equipment_list)}")
    print(f"Registros únicos: {len(unique_equipment)}")
    print(f"Duplicatas ignoradas: {duplicates}")
    print(f"Registros inseridos: {inserted}")
    print(f"Erros durante parse: {len(parse_errors)}")
    print(f"Erros durante insert: {len(errors_on_insert)}")
    
    # Listar erros se houver
    if errors_on_insert:
        print(f"\nErros encontrados:")
        for error in errors_on_insert[:10]:
            print(f"  - {error}")
        if len(errors_on_insert) > 10:
            print(f"  ... e mais {len(errors_on_insert) - 10} erros")
    
    print("\n" + "=" * 70)
    
    return {
        'processed': len(equipment_list),
        'unique': len(unique_equipment),
        'duplicates': duplicates,
        'inserted': inserted,
        'parse_errors': len(parse_errors),
        'insert_errors': len(errors_on_insert),
        'success': inserted > 0
    }


if __name__ == '__main__':
    # Se os dados forem passados como argumento
    if len(sys.argv) > 1:
        data = sys.argv[1]
    else:
        # Ler do stdin
        print("Cole os dados tab-separated e pressione Ctrl+D (Linux/Mac) ou Ctrl+Z+Enter (Windows):")
        data = sys.stdin.read()
    
    if data.strip():
        # Inicializar banco de dados
        with app.app_context():
            db.create_all()
        
        result = bulk_import_equipment(data)
        
        # Retornar código de saída apropriado
        sys.exit(0 if result['success'] else 1)
    else:
        print("Nenhum dado fornecido!")
        sys.exit(1)
