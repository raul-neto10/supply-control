from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError
from datetime import datetime
import os
import csv
from io import StringIO, BytesIO
import requests
import json
import uuid
import barcode
from barcode.writer import ImageWriter

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'supply.db')
BARCODES_DIR = os.path.join(BASE_DIR, 'static', 'barcodes')

# Criar diretório de códigos de barras se não existir
if not os.path.exists(BARCODES_DIR):
    os.makedirs(BARCODES_DIR)

def generate_barcode_code():
    """Gera um código de barras único de 12 dígitos"""
    barcode_code = str(int(str(uuid.uuid4().int)[:12]))[:12]
    while Item.query.filter_by(barcode_code=barcode_code).first():
        barcode_code = str(int(str(uuid.uuid4().int)[:12]))[:12]
    return barcode_code

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-change-in-prod'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    location = db.Column(db.String(200), nullable=True)
    serial = db.Column(db.String(200), nullable=True)
    sector = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    barcode_code = db.Column(db.String(100), unique=True, nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Item {self.name}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superadmin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'entry' or 'exit'
    quantity = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.String(200), nullable=True)
    responsible = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    item = db.relationship('Item', backref=db.backref('movements', lazy='dynamic'))
    user = db.relationship('User')


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    borrowed_by = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(200), nullable=True)
    expected_return = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    item = db.relationship('Item', backref=db.backref('loans', lazy='dynamic'))
    user = db.relationship('User')


class Equipment(db.Model):
    """Modelo para equipamentos de TI"""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    localization = db.Column(db.String(255), nullable=False, index=True)  # LOCALIZAÇÃO/SETOR
    equipment_type = db.Column(db.String(100), nullable=False, index=True)  # TIPO
    host = db.Column(db.String(100), unique=True, nullable=True)  # HOST
    ip_address = db.Column(db.String(15), unique=True, nullable=True)  # IP
    processor = db.Column(db.String(100))  # PROCESSADOR
    memory_ram = db.Column(db.String(50))  # MEMÓRIA RAM
    storage = db.Column(db.String(100))  # ARMAZENAMENTO
    mac_address = db.Column(db.String(17), unique=True, nullable=True)  # MAC
    patrimony_code = db.Column(db.String(50), unique=True, nullable=True)  # PATRIMÔNIO
    operating_system = db.Column(db.String(50))  # SISTEMA OPERACIONAL
    monitor_code = db.Column(db.String(100))  # COD.MONITOR SIMPRESS
    status = db.Column(db.String(50), default='Ativo')  # Ativo, Inativo, Manutenção
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Equipment {self.host or self.ip_address}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'localization': self.localization,
            'equipment_type': self.equipment_type,
            'host': self.host,
            'ip_address': self.ip_address,
            'processor': self.processor,
            'memory_ram': self.memory_ram,
            'storage': self.storage,
            'mac_address': self.mac_address,
            'patrimony_code': self.patrimony_code,
            'operating_system': self.operating_system,
            'monitor_code': self.monitor_code,
            'status': self.status,
            'last_updated': self.last_updated.strftime('%d/%m/%Y %H:%M') if self.last_updated else '',
            'notes': self.notes
        }


class ItemForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    category = SelectField('Categoria', choices=[
        ('Computador','Computador'), ('Monitor','Monitor'), ('Impressora','Impressora'),
        ('Toner','Toner'), ('Cartucho','Cartucho'), ('Periférico','Periférico'), ('Outro','Outro')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    location = StringField('Local', validators=[Optional()])
    serial = StringField('Serial / Código', validators=[Optional()])
    sector = StringField('Setor / Centro de custo', validators=[Optional()])
    description = TextAreaField('Descrição', validators=[Optional()])


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])


class MovementForm(FlaskForm):
    type = SelectField('Tipo', choices=[('entry', 'Entrada'), ('exit', 'Saída')], validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    destination = StringField('Destino', validators=[Optional()])
    responsible = StringField('Responsável', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional()])


class LoanForm(FlaskForm):
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    borrowed_by = StringField('Emprestado por', validators=[DataRequired()])
    contact = StringField('Contato (telefone/email)', validators=[Optional()])
    expected_return = StringField('Data de devolução esperada (YYYY-MM-DD)', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional()])


class NewLoanForm(FlaskForm):
    item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    borrowed_by = StringField('Emprestado por', validators=[DataRequired()])
    contact = StringField('Contato (telefone/email)', validators=[Optional()])
    expected_return = StringField('Data de devolução esperada (YYYY-MM-DD)', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional()])


class ConfirmLoanForm(FlaskForm):
    password = PasswordField('Confirmar com senha', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha atual', validators=[DataRequired()])
    new_password = PasswordField('Nova senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar nova senha', validators=[DataRequired()])
    
    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('As senhas não conferem.')


class EditUserForm(FlaskForm):
    is_admin = SelectField('Permissão', choices=[
        ('user', 'Usuário (sem permissões especiais)'),
        ('admin', 'Admin (gerenciamento, sem deletar)'),
        ('superadmin', 'Superadmin (acesso total)')
    ], validators=[DataRequired()])


class CreateUserForm(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired()])
    is_admin = SelectField('Permissão', choices=[
        ('user', 'Usuário (sem permissões especiais)'),
        ('admin', 'Admin (gerenciamento, sem deletar)'),
        ('superadmin', 'Superadmin (acesso total)')
    ], validators=[DataRequired()])
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Este nome de usuário já existe.')
    
    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('As senhas não conferem.')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/api/search-product', methods=['GET'])
@login_required
def search_product_api():
    barcode = request.args.get('barcode', '').strip()
    if not barcode:
        return {'error': 'Código de barras não fornecido'}, 400
    
    try:
        # Consulta a API externa com o código de barras
        response = requests.get(
            f'https://api-produtos.seunegocionanuvem.com.br/produtos',
            params={'codigo_barras': barcode},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                product = data[0]
                return {
                    'success': True,
                    'name': product.get('nome') or product.get('descricao') or 'Produto desconhecido',
                    'description': product.get('descricao', ''),
                    'category': product.get('categoria') or 'Outro',
                    'barcode': product.get('codigo_barras', barcode),
                    'sku': product.get('sku', product.get('id', ''))
                }
            else:
                return {'error': 'Produto não encontrado na API'}, 404
        else:
            return {'error': f'Erro na API: {response.status_code}'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Timeout ao consultar a API'}, 500
    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao conectar à API: {str(e)}'}, 500
    except json.JSONDecodeError:
        return {'error': 'Resposta inválida da API'}, 500


def create_tables():
    with app.app_context():
        db.create_all()
        # create default admin and superadmin if not exists
        if User.query.count() == 0:
            superadmin = User(username='superadmin', is_admin=True, is_superadmin=True)
            superadmin.set_password('superadmin')
            db.session.add(superadmin)
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()



@app.route('/')
def index():
    if current_user.is_authenticated:
        items = Item.query.order_by(Item.added_at.desc()).all()
        categories = db.session.query(Item.category, db.func.count(Item.id)).group_by(Item.category).all()
        return render_template('index.html', items=items, categories=categories)
    return redirect(url_for('login'))


@app.route('/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        barcode_code = generate_barcode_code()
        item = Item(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            location=form.location.data,
            serial=form.serial.data,
            sector=form.sector.data,
            description=form.description.data,
            barcode_code=barcode_code
        )
        db.session.add(item)
        db.session.commit()
        flash('Item adicionado com sucesso.', 'success')
        return redirect(url_for('index'))
    return render_template('add_item.html', form=form)


@app.route('/item/<int:item_id>')
def view_item(item_id):
    item = Item.query.get_or_404(item_id)
    movements = item.movements.order_by(Movement.created_at.desc()).limit(10).all()
    return render_template('view_item.html', item=item, movements=movements)


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Item atualizado.', 'success')
        return redirect(url_for('view_item', item_id=item.id))
    return render_template('edit_item.html', form=form, item=item)


@app.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    if not current_user.is_superadmin:
        flash('Apenas superadmin pode deletar registros.', 'danger')
        return redirect(url_for('view_item', item_id=item_id))
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item removido.', 'info')
    return redirect(url_for('index'))


@app.route('/category/<name>')
def by_category(name):
    items = Item.query.filter_by(category=name).order_by(Item.added_at.desc()).all()
    return render_template('index.html', items=items, categories=[]) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logado com sucesso.', 'success')
            return redirect(url_for('dashboard'))
        # ensure no lingering session when login fails
        logout_user()
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('index'))


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Verificar se a senha atual está correta
        if not current_user.check_password(form.current_password.data):
            flash('Senha atual incorreta.', 'danger')
            return render_template('change_password.html', form=form)
        
        # Atualizar a senha
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('change_password.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    total_items = Item.query.count()
    total_types = db.session.query(Item.category).distinct().count()
    low_stock = Item.query.filter(Item.quantity <= 2).order_by(Item.quantity.asc()).all()
    recent = Item.query.order_by(Item.added_at.desc()).limit(8).all()
    categories = db.session.query(Item.category, db.func.count(Item.id)).group_by(Item.category).all()
    return render_template('dashboard.html', total_items=total_items, total_types=total_types,
                           low_stock=low_stock, recent=recent, categories=categories)


@app.route('/users')
@login_required
def list_users():
    if not current_user.is_superadmin:
        flash('Acesso negado. Apenas superadmin.', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.username).all()
    return render_template('users_list.html', users=users)


@app.route('/users/novo', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_superadmin:
        flash('Acesso negado. Apenas superadmin.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = CreateUserForm()
    if form.validate_on_submit():
        try:
            # Criar novo usuário
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            
            # Definir permissões
            if form.is_admin.data == 'superadmin':
                new_user.is_superadmin = True
                new_user.is_admin = True
            elif form.is_admin.data == 'admin':
                new_user.is_superadmin = False
                new_user.is_admin = True
            else:
                new_user.is_superadmin = False
                new_user.is_admin = False
            
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'Usuário "{form.username.data}" criado com sucesso!', 'success')
            return redirect(url_for('list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar usuário: {str(e)}', 'danger')
    
    return render_template('create_user.html', form=form)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_superadmin:
        flash('Acesso negado. Apenas superadmin.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    
    if form.validate_on_submit():
        # Atualizar permissões
        if form.is_admin.data == 'superadmin':
            user.is_superadmin = True
            user.is_admin = True
        elif form.is_admin.data == 'admin':
            user.is_superadmin = False
            user.is_admin = True
        else:
            user.is_superadmin = False
            user.is_admin = False
        
        db.session.commit()
        flash(f'Permissões de {user.username} atualizadas com sucesso!', 'success')
        return redirect(url_for('list_users'))
    
    # Pré-preencher o formulário
    if user.is_superadmin:
        form.is_admin.data = 'superadmin'
    elif user.is_admin:
        form.is_admin.data = 'admin'
    else:
        form.is_admin.data = 'user'
    
    return render_template('edit_user.html', form=form, user=user)


@app.route('/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
def reset_user_password(user_id):
    if not current_user.is_superadmin:
        flash('Acesso negado. Apenas superadmin.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Gerar senha temporária
    import string
    import secrets
    temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(12))
    
    user.set_password(temp_password)
    db.session.commit()
    
    flash(f'Senha de {user.username} resetada para: {temp_password}', 'success')
    return redirect(url_for('list_users'))


# ==================== EQUIPMENT MAPPING ROUTES ====================

from equipment_service import EquipmentMapping


ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/mapeamento')
@login_required
def equipment_mapping():
    """Página principal de mapeamento de equipamentos"""
    stats = EquipmentMapping.get_statistics(Equipment)
    localizations = EquipmentMapping.get_localizations(Equipment)
    operating_systems = EquipmentMapping.get_operating_systems(Equipment)
    
    return render_template('equipment_mapping.html', 
                         stats=stats, 
                         localizations=localizations,
                         operating_systems=operating_systems)


@app.route('/mapeamento/equipamentos', methods=['GET', 'POST'])
@login_required
def list_equipment():
    """Lista de equipamentos com filtros"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = Equipment.query
    
    # Filtros
    localization = request.args.get('localization')
    equipment_type = request.args.get('type')
    status_filter = request.args.get('status')
    search = request.args.get('search')
    
    if localization:
        query = query.filter_by(localization=localization)
    if equipment_type:
        query = query.filter_by(equipment_type=equipment_type)
    if status_filter:
        query = query.filter_by(status=status_filter)
    if search:
        query = Equipment.query.filter(
            (Equipment.host.ilike(f'%{search}%')) |
            (Equipment.ip_address.ilike(f'%{search}%')) |
            (Equipment.mac_address.ilike(f'%{search}%'))
        )
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return render_template('equipment_list.html', 
                         equipments=paginated.items,
                         pagination=paginated,
                         current_page=page)


@app.route('/mapeamento/equipamento/<int:equipment_id>')
@login_required
def view_equipment(equipment_id):
    """Visualiza detalhes de um equipamento"""
    equipment = Equipment.query.get_or_404(equipment_id)
    return render_template('equipment_detail.html', equipment=equipment)


@app.route('/mapeamento/novo', methods=['GET', 'POST'])
@login_required
def create_new_equipment():
    """Cria novo equipamento"""
    if not current_user.is_superadmin and not current_user.is_admin:
        flash('Acesso negado. Apenas admin.', 'danger')
        return redirect(url_for('equipment_mapping'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        result = EquipmentMapping.create_equipment(db, Equipment, **data)
        
        if request.is_json:
            return jsonify(result)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('list_equipment'))
        else:
            flash(result['message'], 'danger')
    
    localizations = EquipmentMapping.get_localizations(Equipment)
    operating_systems = EquipmentMapping.get_operating_systems(Equipment)
    return render_template('equipment_form.html', 
                          localizations=localizations,
                          operating_systems=operating_systems,
                          action='criar')


@app.route('/mapeamento/equipamento/<int:equipment_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_equipment(equipment_id):
    """Edita equipamento existente"""
    if not current_user.is_superadmin and not current_user.is_admin:
        flash('Acesso negado. Apenas admin.', 'danger')
        return redirect(url_for('equipment_mapping'))
    
    equipment = Equipment.query.get_or_404(equipment_id)
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        result = EquipmentMapping.update_equipment(db, Equipment, equipment_id, **data)
        
        if request.is_json:
            return jsonify(result)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('view_equipment', equipment_id=equipment_id))
        else:
            flash(result['message'], 'danger')
    
    localizations = EquipmentMapping.get_localizations(Equipment)
    operating_systems = EquipmentMapping.get_operating_systems(Equipment)
    return render_template('equipment_form.html', 
                          equipment=equipment,
                          localizations=localizations,
                          operating_systems=operating_systems,
                          action='editar')


@app.route('/mapeamento/equipamento/<int:equipment_id>/deletar', methods=['POST', 'DELETE'])
@login_required
def delete_equipment_route(equipment_id):
    """Deleta equipamento"""
    if not current_user.is_superadmin and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Acesso negado'}), 403
    
    result = EquipmentMapping.delete_equipment(db, Equipment, equipment_id)
    
    if request.is_json or request.method == 'DELETE':
        return jsonify(result)
    
    if result['success']:
        flash(result['message'], 'success')
        return redirect(url_for('list_equipment'))
    else:
        flash(result['message'], 'danger')
        return redirect(url_for('view_equipment', equipment_id=equipment_id))


@app.route('/mapeamento/importar', methods=['GET', 'POST'])
@login_required
def import_equipment():
    """Importa equipamentos de arquivo"""
    if not current_user.is_superadmin and not current_user.is_admin:
        flash('Acesso negado. Apenas admin.', 'danger')
        return redirect(url_for('equipment_mapping'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado.', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(BASE_DIR, 'uploads', filename)
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            file.save(filepath)
            
            result = EquipmentMapping.import_from_csv(filepath, db, Equipment)
            
            if result['success']:
                flash(f"Importados {result['imported']} equipamentos com sucesso!", 'success')
                if result['errors']:
                    flash(f"Alguns erros ocorreram: {', '.join(result['errors'][:5])}", 'warning')
            else:
                flash(f"Erro ao importar: {result['error']}", 'danger')
            
            # Limpar arquivo
            os.remove(filepath)
            return redirect(url_for('equipment_mapping'))
    
    return render_template('import_equipment.html')


@app.route('/mapeamento/exportar')
@login_required
def export_equipment():
    """Exporta equipamentos para CSV"""
    df = EquipmentMapping.export_to_csv(Equipment)
    
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'equipamentos_{datetime.now().strftime("%d_%m_%Y")}.csv'
    )


@app.route('/mapeamento/api/estatisticas')
@login_required
def api_statistics():
    """API para estatísticas em tempo real"""
    stats = EquipmentMapping.get_statistics(Equipment)
    return jsonify(stats)


@app.route('/mapeamento/buscar')
@login_required
def search_equipment():
    """Busca equipamentos (AJAX)"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    equipments = EquipmentMapping.search_equipment(query, Equipment)
    results = [equipment.to_dict() for equipment in equipments[:10]]
    
    return jsonify(results)


@app.route('/item/<int:item_id>/move', methods=['GET', 'POST'])
@login_required
def move_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = MovementForm()
    if form.validate_on_submit():
        qty = form.quantity.data
        if form.type.data == 'exit':
            if item.quantity < qty:
                flash('Quantidade insuficiente no estoque.', 'danger')
                return render_template('move_item.html', form=form, item=item)
            item.quantity -= qty
        else:
            item.quantity += qty

        mv = Movement(
            item_id=item.id,
            type=form.type.data,
            quantity=qty,
            destination=form.destination.data,
            responsible=form.responsible.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(mv)
        db.session.commit()
        flash('Movimentação registrada e estoque atualizado.', 'success')
        return redirect(url_for('view_item', item_id=item.id))
    return render_template('move_item.html', form=form, item=item)


@app.route('/item/<int:item_id>/loan', methods=['GET', 'POST'])
@login_required
def create_loan(item_id):
    item = Item.query.get_or_404(item_id)
    form = LoanForm()
    if form.validate_on_submit():
        qty = form.quantity.data
        if item.quantity < qty:
            flash('Quantidade insuficiente no estoque.', 'danger')
            return render_template('create_loan.html', form=form, item=item)
        return redirect(url_for('confirm_loan', item_id=item_id, qty=qty, borrowed_by=form.borrowed_by.data, contact=form.contact.data, expected_return=form.expected_return.data, notes=form.notes.data))
    return render_template('create_loan.html', form=form, item=item)


@app.route('/item/<int:item_id>/loan/confirm', methods=['GET', 'POST'])
@login_required
def confirm_loan(item_id):
    item = Item.query.get_or_404(item_id)
    qty = request.args.get('qty', type=int)
    borrowed_by = request.args.get('borrowed_by')
    contact = request.args.get('contact')
    expected_return = request.args.get('expected_return')
    notes = request.args.get('notes')
    
    if not qty or not borrowed_by:
        flash('Dados inválidos.', 'danger')
        return redirect(url_for('create_loan', item_id=item_id))
    
    form = ConfirmLoanForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash('Senha incorreta.', 'danger')
            return render_template('confirm_loan.html', form=form, item=item, qty=qty, borrowed_by=borrowed_by, contact=contact, expected_return=expected_return)
        
        item.quantity -= qty
        expected_return_dt = None
        if expected_return:
            try:
                expected_return_dt = datetime.strptime(expected_return, '%Y-%m-%d')
            except:
                pass
        
        loan = Loan(
            item_id=item.id,
            quantity=qty,
            borrowed_by=borrowed_by,
            contact=contact,
            expected_return=expected_return_dt,
            notes=notes,
            user_id=current_user.id
        )
        db.session.add(loan)
        db.session.commit()
        flash('Empréstimo registrado e estoque atualizado.', 'success')
        return redirect(url_for('view_item', item_id=item.id))
    
    return render_template('confirm_loan.html', form=form, item=item, qty=qty, borrowed_by=borrowed_by, contact=contact, expected_return=expected_return)


@app.route('/loan/confirm', methods=['GET', 'POST'])
@login_required
def confirm_loan_from_list(item_id=None, qty=None, borrowed_by=None, contact=None, expected_return=None, notes=None):
    item_id = item_id or request.args.get('item_id', type=int)
    qty = qty or request.args.get('qty', type=int)
    borrowed_by = borrowed_by or request.args.get('borrowed_by')
    contact = contact or request.args.get('contact')
    expected_return = expected_return or request.args.get('expected_return')
    notes = notes or request.args.get('notes')
    
    item = Item.query.get_or_404(item_id)
    
    if not qty or not borrowed_by:
        flash('Dados inválidos.', 'danger')
        return redirect(url_for('new_loan'))
    
    form = ConfirmLoanForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash('Senha incorreta.', 'danger')
            return render_template('confirm_loan.html', form=form, item=item, qty=qty, borrowed_by=borrowed_by, contact=contact, expected_return=expected_return)
        
        item.quantity -= qty
        expected_return_dt = None
        if expected_return:
            try:
                expected_return_dt = datetime.strptime(expected_return, '%Y-%m-%d')
            except:
                pass
        
        loan = Loan(
            item_id=item.id,
            quantity=qty,
            borrowed_by=borrowed_by,
            contact=contact,
            expected_return=expected_return_dt,
            notes=notes,
            user_id=current_user.id
        )
        db.session.add(loan)
        db.session.commit()
        flash('Empréstimo registrado e estoque atualizado.', 'success')
        return redirect(url_for('list_loans'))
    
    return render_template('confirm_loan.html', form=form, item=item, qty=qty, borrowed_by=borrowed_by, contact=contact, expected_return=expected_return)


@app.route('/loans')
@login_required
def list_loans():
    pending_loans = Loan.query.filter(Loan.returned_at == None).order_by(Loan.created_at.desc()).all()
    returned_loans = Loan.query.filter(Loan.returned_at != None).order_by(Loan.returned_at.desc()).limit(20).all()
    return render_template('loans_list.html', pending_loans=pending_loans, returned_loans=returned_loans, now=datetime.utcnow())


@app.route('/loan/new', methods=['GET', 'POST'])
@login_required
def new_loan():
    form = NewLoanForm()
    # Organizar itens por categoria
    items_by_category = {}
    for item in Item.query.filter(Item.quantity > 0).all():
        if item.category not in items_by_category:
            items_by_category[item.category] = []
        items_by_category[item.category].append(item)
    
    # Criar choices organizadas: (id, "Categoria | Nome (#ID) (Qtd disponível)")
    choices = []
    for category in sorted(items_by_category.keys()):
        for item in items_by_category[category]:
            choice_label = f"{category} | {item.name} (#{item.barcode_code or item.id}) ({item.quantity} disponível)"
            choices.append((item.id, choice_label))
    
    # Se não houver choices, adicionar um placeholder
    if not choices:
        choices = [(0, "Nenhum item disponível")]
    
    form.item_id.choices = choices
    
    if form.validate_on_submit():
        if form.item_id.data == 0:
            flash('Selecione um item válido.', 'danger')
            return render_template('new_loan.html', form=form)
        item = Item.query.get_or_404(form.item_id.data)
        qty = form.quantity.data
        if item.quantity < qty:
            flash('Quantidade insuficiente no estoque.', 'danger')
            return render_template('new_loan.html', form=form)
        return redirect(url_for('confirm_loan_from_list', item_id=item.id, qty=qty, borrowed_by=form.borrowed_by.data, contact=form.contact.data, expected_return=form.expected_return.data, notes=form.notes.data))
    return render_template('new_loan.html', form=form)


@app.route('/loan/<int:loan_id>/return', methods=['POST'])
@login_required
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.returned_at:
        flash('Este empréstimo já foi devolvido.', 'warning')
        return redirect(url_for('list_loans'))
    
    loan.returned_at = datetime.utcnow()
    loan.item.quantity += loan.quantity
    db.session.commit()
    flash('Empréstimo marcado como devolvido e estoque atualizado.', 'success')
    return redirect(url_for('list_loans'))


@app.route('/reports')
@login_required
def reports():
    return render_template('reports_index.html')


@app.route('/reports/stock')
@login_required
def report_stock():
    items = Item.query.order_by(Item.category, Item.name).all()
    total_value_estimate = sum(item.quantity for item in items)
    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = {'count': 0, 'items': []}
        categories[item.category]['count'] += item.quantity
        categories[item.category]['items'].append(item)
    
    export_format = request.args.get('export', 'html')
    if export_format == 'csv':
        return export_stock_csv(items)
    elif export_format == 'pdf':
        return export_stock_pdf(items)
    
    return render_template('report_stock.html', items=items, categories=categories, total_value_estimate=total_value_estimate)


@app.route('/reports/movements')
@login_required
def report_movements():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    item_id = request.args.get('item_id', type=int)
    
    query = Movement.query
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Movement.created_at >= start)
        except:
            pass
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Movement.created_at <= end)
        except:
            pass
    if item_id:
        query = query.filter(Movement.item_id == item_id)
    
    movements = query.order_by(Movement.created_at.desc()).all()
    items = Item.query.all()
    
    export_format = request.args.get('export', 'html')
    if export_format == 'csv':
        return export_movements_csv(movements)
    elif export_format == 'pdf':
        return export_movements_pdf(movements)
    
    return render_template('report_movements.html', movements=movements, items=items, start_date=start_date, end_date=end_date, item_id=item_id)


@app.route('/reports/loans')
@login_required
def report_loans():
    status = request.args.get('status', 'all')
    
    if status == 'pending':
        loans = Loan.query.filter(Loan.returned_at == None).order_by(Loan.created_at.desc()).all()
    elif status == 'returned':
        loans = Loan.query.filter(Loan.returned_at != None).order_by(Loan.returned_at.desc()).all()
    else:
        loans = Loan.query.order_by(Loan.created_at.desc()).all()
    
    export_format = request.args.get('export', 'html')
    if export_format == 'csv':
        return export_loans_csv(loans)
    elif export_format == 'pdf':
        return export_loans_pdf(loans)
    
    return render_template('report_loans.html', loans=loans, status=status)


@app.route('/reports/sector')
@login_required
def report_sector():
    items = Item.query.order_by(Item.sector, Item.name).all()
    sectors = {}
    for item in items:
        sector = item.sector or 'Sem setor'
        if sector not in sectors:
            sectors[sector] = {'count': 0, 'quantity': 0, 'items': []}
        sectors[sector]['count'] += 1
        sectors[sector]['quantity'] += item.quantity
        sectors[sector]['items'].append(item)
    
    export_format = request.args.get('export', 'html')
    if export_format == 'csv':
        return export_sector_csv(items, sectors)
    elif export_format == 'pdf':
        return export_sector_pdf(items, sectors)
    
    return render_template('report_sector.html', sectors=sectors)


def export_stock_csv(items):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nome', 'Categoria', 'Quantidade', 'Local', 'Setor', 'Serial'])
    for item in items:
        writer.writerow([item.name, item.category, item.quantity, item.location or '', item.sector or '', item.serial or ''])
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=estoque.csv'}
    )
    return response


def export_stock_pdf(items):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=20,
        alignment=1
    )
    
    elements.append(Paragraph('Relatório de Estoque', title_style))
    elements.append(Paragraph(f'Gerado em {datetime.utcnow().strftime("%d/%m/%Y %H:%M")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Nome', 'Categoria', 'Quantidade', 'Local', 'Setor']]
    for item in items:
        data.append([item.name, item.category, str(item.quantity), item.location or '', item.sector or ''])
    
    table = Table(data, colWidths=[2*inch, 1.2*inch, 1*inch, 1.2*inch, 1.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return app.response_class(
        response=buffer.getvalue(),
        status=200,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=estoque.pdf'}
    )


def export_movements_csv(movements):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Data', 'Item', 'Tipo', 'Quantidade', 'Destino', 'Responsável', 'Usuário'])
    for mv in movements:
        writer.writerow([
            mv.created_at.strftime('%Y-%m-%d %H:%M'),
            mv.item.name,
            'Entrada' if mv.type == 'entry' else 'Saída',
            mv.quantity,
            mv.destination or '',
            mv.responsible or '',
            mv.user.username if mv.user else ''
        ])
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=movimentacoes.csv'}
    )
    return response


def export_movements_pdf(movements):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=20,
        alignment=1
    )
    
    elements.append(Paragraph('Relatório de Movimentações', title_style))
    elements.append(Paragraph(f'Gerado em {datetime.utcnow().strftime("%d/%m/%Y %H:%M")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Data', 'Item', 'Tipo', 'Quantidade', 'Responsável']]
    for mv in movements:
        data.append([
            mv.created_at.strftime('%d/%m/%Y'),
            mv.item.name,
            'Entrada' if mv.type == 'entry' else 'Saída',
            str(mv.quantity),
            mv.responsible or ''
        ])
    
    table = Table(data, colWidths=[1.2*inch, 2*inch, 1*inch, 1*inch, 1.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return app.response_class(
        response=buffer.getvalue(),
        status=200,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=movimentacoes.pdf'}
    )


def export_loans_csv(loans):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Item', 'Quantidade', 'Emprestado por', 'Contato', 'Data empréstimo', 'Devolução esperada', 'Status'])
    for loan in loans:
        status = 'Devolvido' if loan.returned_at else 'Pendente'
        writer.writerow([
            loan.item.name,
            loan.quantity,
            loan.borrowed_by,
            loan.contact or '',
            loan.created_at.strftime('%Y-%m-%d'),
            loan.expected_return.strftime('%Y-%m-%d') if loan.expected_return else '',
            status
        ])
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=emprestimos.csv'}
    )
    return response


def export_loans_pdf(loans):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=20,
        alignment=1
    )
    
    elements.append(Paragraph('Relatório de Empréstimos', title_style))
    elements.append(Paragraph(f'Gerado em {datetime.utcnow().strftime("%d/%m/%Y %H:%M")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Item', 'Quantidade', 'Emprestado por', 'Data', 'Status']]
    for loan in loans:
        status = 'Devolvido' if loan.returned_at else 'Pendente'
        data.append([
            loan.item.name,
            str(loan.quantity),
            loan.borrowed_by,
            loan.created_at.strftime('%d/%m/%Y'),
            status
        ])
    
    table = Table(data, colWidths=[2*inch, 1*inch, 1.5*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return app.response_class(
        response=buffer.getvalue(),
        status=200,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=emprestimos.pdf'}
    )


def export_sector_csv(items, sectors):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Setor', 'Total de itens', 'Quantidade total', 'Itens'])
    for sector, data in sorted(sectors.items()):
        items_list = ', '.join([f'{it.name} ({it.quantity})' for it in data['items']])
        writer.writerow([sector, data['count'], data['quantity'], items_list])
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=setores.csv'}
    )
    return response


def export_sector_pdf(items, sectors):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=20,
        alignment=1
    )
    
    elements.append(Paragraph('Relatório por Setor', title_style))
    elements.append(Paragraph(f'Gerado em {datetime.utcnow().strftime("%d/%m/%Y %H:%M")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Setor', 'Itens', 'Quantidade']]
    for sector, sector_data in sorted(sectors.items()):
        data.append([sector, str(sector_data['count']), str(sector_data['quantity'])])
    
    table = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return app.response_class(
        response=buffer.getvalue(),
        status=200,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=setores.pdf'}
    )


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000, debug=False)
