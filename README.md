# 🏦 Banco Digital - Projeto Flask

Um sistema bancário simples desenvolvido em Flask com funcionalidades básicas de gerenciamento de contas e transações.

## ✨ Funcionalidades

- **Cadastro e Login de Usuários**: Sistema de autenticação seguro
- **Gerenciamento de Contas**: Criação de contas corrente e poupança
- **Operações Bancárias**: Depósitos e saques
- **Extrato de Transações**: Histórico completo de movimentações
- **Interface Moderna**: Design responsivo com Bootstrap 5
- **Segurança**: Senhas criptografadas e sessões seguras

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite com SQLAlchemy (local) / PostgreSQL (produção)
- **Frontend**: Bootstrap 5, Font Awesome
- **Segurança**: Werkzeug para hash de senhas
- **Deploy**: Gunicorn + Render

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação Local

1. **Clone ou baixe o projeto**
   ```bash
   # Se estiver usando git
   git clone <url-do-repositorio>
   cd banco-digital
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**
   ```bash
   python app.py
   ```

4. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 🌐 Deploy no Render

### Opção 1: Deploy Automático (Recomendado)

1. **Faça push do código para o GitHub**
   ```bash
   git add .
   git commit -m "Preparando para deploy no Render"
   git push origin main
   ```

2. **Acesse o Render Dashboard**
   - Vá para [render.com](https://render.com)
   - Faça login ou crie uma conta

3. **Crie um novo Web Service**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório do projeto

4. **Configure o serviço**
   - **Name**: `banco-digital-flask`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. **Configure as variáveis de ambiente**
   - **SECRET_KEY**: Gere uma chave secreta aleatória
   - **DATABASE_URL**: (opcional) URL do PostgreSQL se quiser usar banco externo

6. **Deploy**
   - Clique em "Create Web Service"
   - Aguarde o build e deploy automático

### Opção 2: Deploy Manual

1. **Crie um Web Service no Render**
2. **Configure manualmente**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**:
     - `SECRET_KEY`: sua_chave_secreta_aqui
     - `DATABASE_URL`: (opcional)

## 📁 Estrutura do Projeto

```
banco-digital/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências do projeto
├── gunicorn.conf.py      # Configuração do Gunicorn
├── render.yaml           # Configuração do Render (opcional)
├── Procfile              # Configuração do Render (alternativo)
├── runtime.txt           # Versão do Python
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Este arquivo
├── banco.db              # Banco de dados SQLite (local)
└── templates/            # Templates HTML
    ├── base.html         # Template base
    ├── index.html        # Página inicial
    ├── login.html        # Página de login
    ├── registro.html     # Página de registro
    ├── dashboard.html    # Dashboard principal
    ├── criar_conta.html  # Criação de contas
    ├── deposito.html     # Página de depósito
    ├── saque.html        # Página de saque
    └── extrato.html      # Página de extrato
```

## 🎯 Como Usar

### 1. Primeiro Acesso
- Acesse a página inicial
- Clique em "Criar Conta"
- Preencha seus dados (nome, email, senha)
- Faça login com suas credenciais

### 2. Criando Contas Bancárias
- No dashboard, clique em "Criar" na seção "Nova Conta"
- Escolha o tipo: Conta Corrente ou Conta Poupança
- Confirme a criação

### 3. Realizando Operações
- **Depósito**: Clique em "Depositar" na conta desejada
- **Saque**: Clique em "Sacar" na conta desejada
- **Extrato**: Clique em "Extrato" para ver o histórico

### 4. Navegação
- Use o menu superior para navegar entre as páginas
- O dashboard mostra um resumo de todas suas contas
- Cada conta tem botões para as operações disponíveis

## 🔒 Segurança

- Senhas são criptografadas usando hash bcrypt
- Sessões seguras para autenticação
- Validação de dados em todas as operações
- Proteção contra acesso não autorizado
- Variáveis de ambiente para configurações sensíveis

## 🗄️ Modelo de Dados

### Usuário
- ID, Nome, Email, Senha (hash), Saldo, Data de Criação

### Conta
- ID, Tipo (corrente/poupança), Saldo, ID do Usuário

### Transação
- ID, Tipo (depósito/saque), Valor, Descrição, Data, ID da Conta

## 🚧 Funcionalidades Futuras

- [ ] Transferências entre contas
- [ ] Pagamentos e boletos
- [ ] Relatórios e gráficos
- [ ] Notificações por email
- [ ] API REST para integração
- [ ] Autenticação de dois fatores

## 🔧 Configurações de Produção

### Variáveis de Ambiente
- `SECRET_KEY`: Chave secreta para sessões
- `DATABASE_URL`: URL do banco de dados (PostgreSQL recomendado)
- `PORT`: Porta do servidor (gerenciada pelo Render)

### Gunicorn
- Workers: 2 (configurável)
- Timeout: 30 segundos
- Preload: True para melhor performance

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como projeto de estudo em Flask.

---

**⚠️ Nota**: Este é um projeto educacional. Não use para operações bancárias reais.

## 🌟 Status do Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**URL do Deploy**: https://seu-app-name.onrender.com 