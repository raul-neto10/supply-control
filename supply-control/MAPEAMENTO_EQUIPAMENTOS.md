# 📊 Mapeamento de Equipamentos - Documentação Completa

## 📋 Visão Geral

A funcionalidade de **Mapeamento de Equipamentos** foi criada para gerenciar e rastrear equipamentos de TI (computadores, impressoras, carrinhos beira-leito) em diferentes setores da instituição.

## ✨ Características Principais

### 1. **Dashboard Principal**
- 📊 Visualização de estatísticas em tempo real
- 📈 Gráficos de distribuição por localização
- 📉 Gráficos de distribuição por sistema operacional
- 🎯 Cards de status (Ativos, Manutenção, Inativos)

### 2. **Listagem de Equipamentos**
- 📄 Visualização em tabela com 20 itens por página
- 🔍 Filtros avançados:
  - Busca por localização, tipo, status
  - Busca de texto em HOST, IP, MAC, patrimônio
- 🏷️ Badges de status com cores diferenciadas
- 🔗 Links para visualizar detalhes completos

### 3. **Detalhes do Equipamento**
- 📋 Informações completas de cada equipamento:
  - Localização e setor
  - Tipo de equipamento
  - Identificadores de rede (HOST, IP, MAC)
  - Especificações técnicas (Processador, RAM, Armazenamento)
  - Sistema operacional
  - Código do monitor (se aplicável)
  - Status e última atualização

### 4. **Importação de Dados**
- 📁 Suporte para arquivos CSV, XLSX e XLS
- ⚡ Processamento automático com colunas mapeadas
- 🔄 Atualiza equipamentos existentes ou cria novos
- ✅ Validação automática de duplicatas

### 5. **Exportação de Dados**
- 📊 Baixar todos os equipamentos em formato CSV
- 💾 Mantém as colunas originais para compatibilidade
- 📱 Fácil importação em outras aplicações

## 🚀 Como Usar

### Acessar o Mapeamento

1. **Faça login** na aplicação
2. **Clique em "📊 Mapeamento"** no menu superior
3. Você verá o dashboard com as estatísticas

### Visualizar Equipamentos

**No Dashboard:**
- Veja as estatísticas resumidas
- Visualize os gráficos de distribuição
- Clique em "Ver lista completa" para mais detalhes

**Na Listagem:**
- Use os filtros na parte superior para refinar resultados
- Clique no ícone de visualização para ver detalhes
- Navegue entre páginas usando os controles de paginação

### Importar Novos Dados

1. **Acesse** "Mapeamento" → "Importar"
2. **Selecione** um arquivo (CSV, XLSX ou XLS)
3. **Aguarde** o processamento
4. **Verifique** a mensagem de confirmação com o número de equipamentos importados

#### Formato do Arquivo

O arquivo deve conter as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| LOCALIZAÇÃO / SETOR | Setor onde o equipamento está | AGENDAMENTO |
| TIPO | Tipo de equipamento | Computador, Impressora, Carrinho Beira-Leito |
| HOST | Nome do host | CSSMDSK117 |
| IP | Endereço IP | 10.53.0.44 |
| PROCESSADOR | Modelo do processador | CORE I3 |
| MEMÓRIA RAM | Quantidade de memória | 4GB, 8GB, 16GB |
| ARMAZENAMENTO | Tipo e tamanho | 120GB SSD, 240GB SSD |
| MAC | Endereço MAC | 00-E0-4C-04-04-DA |
| PATRIMÔNIO | Código de patrimônio | SIMPRESS (opcional) |
| SISTEMA OPERACIONAL | Sistema operacional | W10, W11 |
| COD.MONITOR SIMPRESS | Código do monitor | BRC44505FC (opcional) |

### Exportar Dados

1. **Acesse** "Mapeamento" → "Exportar"
2. O arquivo CSV será **baixado automaticamente**
3. Você pode **abrir em Excel ou Google Sheets**

### Buscar Equipamentos

**Método 1: Filtros**
- Use os filtros no topo da listagem
- Selecione localização, tipo, status
- Pressione Enter ou clique em Filtrar

**Método 2: Busca Rápida**
- Digite no campo de busca
- Procura em: HOST, IP, MAC, Localização, Patrimônio
- Resultados aparecem em tempo real

## 📊 Dados Carregados Inicialmente

A aplicação foi pré-configurada com **8 equipamentos de amostra**:

| Localização | Tipo | HOST | IP | Processador | RAM | S.O. |
|-------------|------|------|----|----|-----|------|
| AGENDAMENTO | Computador | CSSMDSK117 | 10.53.0.44 | CORE I3 | 4GB | W10 |
| ALMOXARIFADO | Computador | CSSMDSK014 | 10.52.0.104 | CORE I3 | 8GB | W10 |
| CENTRO CIRURGICO | Computador | CSSMDSK179 | 10.52.0.140 | CORE I3 | 8GB | W10 |
| CLINICA MÉDICA | Computador | CSSMDSK047 | 10.53.0.105 | CORE I3 | 8GB | W10 |
| UTI A | Computador | CSSMDSK124 | 10.53.0.102 | CORE I3 | 8GB | W10 |
| FATURAMENTO CONVENIOS | Impressora | - | 10.51.0.114 | - | - | - |
| CENTRO CIRURGICO | Impressora | - | 10.51.0.112 | - | - | - |
| CENTRO DE REAB. PSIQ. | Carrinho Beira-Leito | CSSMNTB007 | 10.51.0.11 | CORE I5 | 16GB | W11 |

### Importar Seus Dados

Para importar seus equipamentos (400+ registros):

1. **Prepare seu arquivo** (CSV ou XLSX) com o formato correto
2. **Acesse "Importar"** em Mapeamento
3. **Selecione seu arquivo**
4. **Aguarde** a importação
5. **Visualize** os dados no dashboard

## 🔐 Permissões de Acesso

- **Todos os usuários autenticados**: Podem visualizar mapeamento
- **Administradores/Superadmin**: Podem importar e exportar dados

## 📈 Estatísticas Disponíveis

O dashboard exibe:

- **Total de Equipamentos**: Quantidade total na base
- **Por Tipo**:
  - 💻 Computadores
  - 🖨️ Impressoras
  - 🛏️ Carrinhos Beira-Leito
- **Por Status**:
  - ✅ Ativos
  - 🔧 Em Manutenção
  - ❌ Inativos
- **Gráficos**:
  - Equipamentos por localização (Top 10)
  - Distribuição por sistema operacional

## 🛠️ Troubleshooting

### Problema: Arquivo não importa
- **Solução**: Verifique se o arquivo está em formato CSV, XLSX ou XLS
- **Solução**: Verifique se as colunas têm os nomes corretos
- **Solução**: Certifique-se de que há dados a partir da linha 2 (linha 1 é cabeçalho)

### Problema: Dados não aparecem
- **Solução**: Atualize a página (F5)
- **Solução**: Verifique se há filtros aplicados que ocultam os dados
- **Solução**: Verifique a console do navegador para erros

### Problema: Não consigo importar
- **Solução**: Verifique se é administrador ou superadmin
- **Solução**: Verifique o tamanho do arquivo (máximo ~100MB recomendado)

## 📞 Suporte

Para reportar problemas ou sugerir melhorias:
- Verifique os logs do servidor
- Contacte o administrador do sistema

## 📝 Histórico de Versão

**v1.0** - Implementação inicial
- Dashboard com estatísticas
- Listagem com paginação e filtros
- Importação de dados
- Exportação para CSV
- Gráficos de distribuição
- Busca avançada
