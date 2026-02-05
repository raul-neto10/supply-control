"""
Equipment Mapping Service
Serviço para mapeamento e rastreamento de equipamentos de TI
"""

import pandas as pd
from io import StringIO
from sqlalchemy import func


class EquipmentMapping:
    """Classe para gerenciar operações de equipamentos"""
    
    @staticmethod
    def import_from_csv(file_path, db, Equipment):
        """
        Importa equipamentos de arquivo CSV ou XLSX
        
        Args:
            file_path: Caminho do arquivo
            db: Instância do SQLAlchemy
            Equipment: Modelo de Equipment
        
        Returns:
            Dict com resultado da importação
        """
        try:
            # Suporta CSV e XLSX
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # Normalizar nomes das colunas
            column_mapping = {
                'LOCALIZAÇÃO / SETOR': 'localization',
                'LOCALIZAÇÃO': 'localization',
                'SETOR': 'localization',
                'TIPO': 'equipment_type',
                'HOST': 'host',
                'IP': 'ip_address',
                'PROCESSADOR': 'processor',
                'MEMÓRIA RAM': 'memory_ram',
                'MEMÓRIA': 'memory_ram',
                'ARMAZENAMENTO': 'storage',
                'MAC': 'mac_address',
                'PATRIMÔNIO': 'patrimony_code',
                'SISTEMA OPERACIONAL': 'operating_system',
                'SO': 'operating_system',
                'COD.MONITOR SIMPRESS': 'monitor_code',
                'COD MONITOR': 'monitor_code',
            }
            
            imported = 0
            updated = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Verificar se existe
                    host = row.get('HOST')
                    existing = None
                    
                    if pd.notna(host):
                        existing = Equipment.query.filter_by(host=str(host).strip()).first()
                    
                    if existing:
                        # Atualizar
                        for col, field in column_mapping.items():
                            if col in df.columns and pd.notna(row.get(col)):
                                setattr(existing, field, str(row.get(col)).strip())
                        updated += 1
                    else:
                        # Criar novo
                        data = {}
                        for col, field in column_mapping.items():
                            if col in df.columns:
                                value = row.get(col)
                                if pd.notna(value):
                                    data[field] = str(value).strip()
                        
                        if 'localization' in data and 'equipment_type' in data:
                            data['status'] = 'Ativo'
                            equipment = Equipment(**data)
                            db.session.add(equipment)
                            imported += 1
                except Exception as e:
                    errors.append(f"Linha {index + 2}: {str(e)}")
            
            db.session.commit()
            
            return {
                'success': True,
                'imported': imported,
                'updated': updated,
                'errors': errors,
                'message': f'{imported} equipamentos importados, {updated} atualizados'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao importar: {str(e)}',
                'errors': [str(e)]
            }
    
    @staticmethod
    def get_statistics(Equipment):
        """Retorna estatísticas do mapeamento"""
        from sqlalchemy import func
        
        total = Equipment.query.count()
        
        computers = Equipment.query.filter_by(equipment_type='Computador').count()
        notebooks = Equipment.query.filter_by(equipment_type='Notebook').count()
        printers = Equipment.query.filter_by(equipment_type='Impressora').count()
        bedside_carts = Equipment.query.filter_by(equipment_type='Carrinho Beira-Leito').count()
        
        active = Equipment.query.filter_by(status='Ativo').count()
        maintenance = Equipment.query.filter_by(status='Manutenção').count()
        inactive = Equipment.query.filter_by(status='Inativo').count()
        
        # Agregações por localização
        by_localization_rows = Equipment.query.with_entities(
            Equipment.localization,
            func.count(Equipment.id)
        ).group_by(Equipment.localization).all()
        by_localization = [(row[0], row[1]) for row in by_localization_rows]
        
        # Agregações por S.O.
        by_os_rows = Equipment.query.with_entities(
            Equipment.operating_system,
            func.count(Equipment.id)
        ).group_by(Equipment.operating_system).all()
        by_os = [(row[0], row[1]) for row in by_os_rows]
        
        return {
            'total_equipment': total,
            'computers': computers,
            'notebooks': notebooks,
            'printers': printers,
            'bedside_carts': bedside_carts,
            'active': active,
            'maintenance': maintenance,
            'inactive': inactive,
            'by_localization': by_localization,
            'by_os': by_os,
        }
    
    @staticmethod
    def get_localizations(Equipment):
        """Retorna lista de localizações únicas"""
        from sqlalchemy import distinct
        results = Equipment.query.with_entities(distinct(Equipment.localization)).all()
        return [r[0] for r in results if r[0]]
    
    @staticmethod
    def get_equipment_by_localization(localization, Equipment):
        """Filtra por localização"""
        return Equipment.query.filter_by(localization=localization).all()
    
    @staticmethod
    def get_equipment_by_type(equipment_type, Equipment):
        """Filtra por tipo"""
        return Equipment.query.filter_by(equipment_type=equipment_type).all()
    
    @staticmethod
    def search_equipment(query, Equipment):
        """Busca em múltiplos campos"""
        if not query:
            return []
        
        search_term = f"%{query}%"
        from sqlalchemy import or_
        results = Equipment.query.filter(
            or_(
                Equipment.host.ilike(search_term),
                Equipment.ip_address.ilike(search_term),
                Equipment.mac_address.ilike(search_term),
                Equipment.localization.ilike(search_term),
                Equipment.patrimony_code.ilike(search_term)
            )
        ).all()
        return results
    
    @staticmethod
    def get_operating_systems(Equipment):
        """Retorna lista de SOs únicos"""
        from sqlalchemy import distinct
        results = Equipment.query.with_entities(distinct(Equipment.operating_system)).all()
        return [r[0] for r in results if r[0]]
    
    @staticmethod
    def export_to_csv(Equipment):
        """Exporta dados para CSV"""
        try:
            equipments = Equipment.query.all()
            data = [e.to_dict() for e in equipments]
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Erro ao exportar: {str(e)}")
    
    @staticmethod
    def create_equipment(db, Equipment, **kwargs):
        """Cria novo equipamento"""
        try:
            equipment = Equipment(
                localization=kwargs.get('localization'),
                equipment_type=kwargs.get('equipment_type'),
                host=kwargs.get('host'),
                ip_address=kwargs.get('ip_address'),
                processor=kwargs.get('processor'),
                memory_ram=kwargs.get('memory_ram'),
                storage=kwargs.get('storage'),
                mac_address=kwargs.get('mac_address'),
                patrimony_code=kwargs.get('patrimony_code'),
                operating_system=kwargs.get('operating_system'),
                monitor_code=kwargs.get('monitor_code'),
                status=kwargs.get('status', 'Ativo'),
                notes=kwargs.get('notes')
            )
            db.session.add(equipment)
            db.session.commit()
            return {'success': True, 'id': equipment.id, 'message': 'Equipamento criado com sucesso'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Erro ao criar: {str(e)}'}
    
    @staticmethod
    def update_equipment(db, Equipment, equipment_id, **kwargs):
        """Atualiza equipamento existente"""
        try:
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                return {'success': False, 'message': 'Equipamento não encontrado'}
            
            for key, value in kwargs.items():
                if hasattr(equipment, key) and value is not None:
                    setattr(equipment, key, value)
            
            db.session.commit()
            return {'success': True, 'message': 'Equipamento atualizado com sucesso'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Erro ao atualizar: {str(e)}'}
    
    @staticmethod
    def delete_equipment(db, Equipment, equipment_id):
        """Deleta equipamento"""
        try:
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                return {'success': False, 'message': 'Equipamento não encontrado'}
            
            db.session.delete(equipment)
            db.session.commit()
            return {'success': True, 'message': 'Equipamento deletado com sucesso'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Erro ao deletar: {str(e)}'}
            return None
