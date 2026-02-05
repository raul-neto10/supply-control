# 🚀 GUIA RÁPIDO: Criar Novo Usuário

## Acesso Rápido

### 1️⃣ Login como Superadmin
```
URL: http://localhost:5000/login
Usuário: superadmin
Senha: superadmin
```

### 2️⃣ Ir para Gerenciamento de Usuários
```
URL: http://localhost:5000/users
OU
- Menu Principal → Gerenciamento de Usuários (se admin)
OU
- Clique em "Gerenciamento de Usuários" no dashboard
```

### 3️⃣ Criar Novo Usuário
```
Clique no botão "+ Novo Usuário"
```

### 4️⃣ Preencher Formulário

```
Nome do Usuário: [nome_único_aqui]
Senha: [senha_segura_aqui]
Confirmar Senha: [mesma_senha]
Permissão: [selecionar_nível]
```

**Exemplo:**
```
Nome do Usuário: joao.silva
Senha: Senha123!
Confirmar Senha: Senha123!
Permissão: Admin
```

### 5️⃣ Enviar
Clique em "Criar Usuário"

---

## ✅ Resultado Esperado

**Sucesso:**
```
✓ Mensagem: "Usuário 'joao.silva' criado com sucesso!"
✓ Redirecionamento automático para lista de usuários
✓ Novo usuário aparece na tabela com badge de permissão
```

**Erro (Usuário existe):**
```
✗ Mensagem: "Este nome de usuário já existe."
✗ Poder corrigir e tentar novamente
```

**Erro (Senhas diferentes):**
```
✗ Mensagem: "As senhas não conferem."
✗ Poder corrigir e tentar novamente
```

---

## 🔐 Níveis de Permissão

### 👑 Superadmin
- ✓ Acesso total ao sistema
- ✓ Gerencia usuários
- ✓ Pode deletar registros
- ✓ Acesso a todas as funcionalidades

**Use para:** Administrador do sistema

---

### 🛠️ Admin
- ✓ Gerencia itens
- ✓ Processa empréstimos
- ✓ Registra movimentações
- ✗ NÃO pode deletar registros
- ✗ NÃO pode gerenciar usuários

**Use para:** Gerente de estoque/inventário

---

### 👤 Usuário
- ✓ Visualiza itens
- ✓ Registra movimentações
- ✓ Vê empréstimos
- ✗ NÃO pode gerenciar
- ✗ NÃO pode deletar

**Use para:** Operador, auxiliar

---

## 📋 Lista de Usuários

Após criar, você verá na lista:

```
┌──────────────────┬─────────────────┬─────────────────┐
│ Usuário          │ Permissão       │ Ações           │
├──────────────────┼─────────────────┼─────────────────┤
│ joao.silva       │ Admin           │ [Editar] [Reset]│
│ maria.santos     │ Superadmin      │ [Editar] [Reset]│
│ pedro.costa      │ Usuário         │ [Editar] [Reset]│
└──────────────────┴─────────────────┴─────────────────┘
```

---

## 🔧 Ações Disponíveis

### Editar Permissões
- Clique em "Editar" próximo ao usuário
- Altere o nível de permissão
- Clique em "Salvar alterações"

### Resetar Senha
- Clique em "Reset Senha" próximo ao usuário
- Uma nova senha será gerada automaticamente
- A senha aparecerá em uma mensagem
- O usuário poderá usar para fazer login e depois trocar

---

## ⚙️ Configurações Importantes

### Senha Padrão
- Mínimo: Sem limite formal, mas recomenda-se 6+ caracteres
- Criptografia: PBKDF2 (segura)
- Armazenamento: Hash (não reversível)

### Validações
- ✓ Nome de usuário único
- ✓ Senhas coincidem antes de salvar
- ✓ Campos obrigatórios
- ✓ Sem acesso para não-Superadmin

---

## 🆘 Troubleshooting

### Problema: "Acesso negado"
```
Solução: Verifique se está logado como Superadmin
- Fazer logout: http://localhost:5000/logout
- Fazer login novamente com superadmin
```

### Problema: "Usuário já existe"
```
Solução: Escolha outro nome de usuário único
- Verifique a lista de usuários existentes
- Tente: joao.silva2, joao_silva, jsilva, etc.
```

### Problema: "Senhas não conferem"
```
Solução: Copie e cole a mesma senha em ambos os campos
- Verifique CAPS LOCK
- Cuidado com espaços em branco
```

### Problema: Botão não aparece
```
Solução: Página pode estar em cache
- Pressione F5 ou Ctrl+F5 para recarregar
- Limpar cookies do navegador se necessário
```

---

## 📊 Exemplo Completo

### Cenário: Criar usuário gerente de estoque

1. Login como superadmin
2. Ir para /users
3. Clicar "+ Novo Usuário"
4. Preencher:
   ```
   Nome: gerente.estoque
   Senha: EstoqueSegura2024!
   Confirmar: EstoqueSegura2024!
   Permissão: Admin
   ```
5. Clicar "Criar Usuário"
6. Sucesso! Novo gerente pode fazer login

---

## 💡 Dicas

- 📝 Anote o nome de usuário e senha antes de criar (será necessário para o novo usuário)
- 🔐 Use senhas fortes com números, letras maiúsculas e minúsculas
- 👥 Crie uma conta para cada pessoa (não compartilhe)
- 🔄 Resete senhas regularmente por segurança
- ✅ Confirme que o novo usuário consegue fazer login

---

**Status: ✅ FUNCIONALIDADE ATIVA E PRONTA PARA USO**

Perguntas? Consulte `FUNCIONALIDADE_CRIAR_USUARIOS.md` para detalhes técnicos.
