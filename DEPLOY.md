# 🚀 Guia de Deploy no Render

Este guia detalha como fazer o deploy do projeto Banco Digital no Render usando Gunicorn.

## 📋 Pré-requisitos

- Conta no [Render.com](https://render.com)
- Código no GitHub (repositório público ou privado)
- Python 3.7+ (configurado no projeto)

## 🔧 Arquivos de Configuração

O projeto já inclui todos os arquivos necessários para deploy:

- `requirements.txt` - Dependências Python
- `gunicorn.conf.py` - Configuração do Gunicorn
- `render.yaml` - Configuração automática do Render
- `Procfile` - Comando de inicialização
- `runtime.txt` - Versão do Python
- `.gitignore` - Arquivos ignorados

## 🌐 Passo a Passo do Deploy

### 1. Preparar o Repositório

```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparando para deploy no Render"
git push origin main
```

### 2. Acessar o Render

1. Vá para [render.com](https://render.com)
2. Faça login ou crie uma conta
3. Clique em "New +" → "Web Service"

### 3. Conectar o Repositório

1. **Conecte seu GitHub**
   - Clique em "Connect account" se necessário
   - Autorize o acesso ao GitHub

2. **Selecione o repositório**
   - Escolha o repositório do projeto
   - Clique em "Connect"

### 4. Configurar o Serviço

**Configurações Básicas:**
- **Name**: `banco-digital-flask` (ou nome de sua preferência)
- **Environment**: `Python 3`
- **Region**: Escolha a região mais próxima
- **Branch**: `main` (ou sua branch principal)
- **Root Directory**: Deixe vazio (raiz do projeto)

**Configurações de Build:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Configurações Avançadas:**
- **Plan**: Free (para começar)
- **Auto-Deploy**: Yes (deploy automático)

### 5. Variáveis de Ambiente

Adicione as seguintes variáveis:

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `SECRET_KEY` | `sua_chave_secreta_muito_segura` | Chave para sessões Flask |
| `DATABASE_URL` | (deixe vazio) | URL do banco (opcional) |

**Para gerar uma SECRET_KEY segura:**
```python
import secrets
print(secrets.token_hex(32))
```

### 6. Deploy

1. Clique em "Create Web Service"
2. Aguarde o build (pode levar alguns minutos)
3. O serviço ficará disponível em: `https://seu-app-name.onrender.com`

## 🔍 Verificando o Deploy

### Logs de Build
- Acesse a aba "Logs" no dashboard do Render
- Verifique se não há erros durante o build
- Confirme que o Gunicorn iniciou corretamente

### Teste da Aplicação
1. Acesse a URL fornecida pelo Render
2. Teste o registro de usuário
3. Teste o login
4. Teste a criação de contas
5. Teste depósitos e saques

## 🛠️ Solução de Problemas

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Confirme que o build command está correto

### Erro: "Port already in use"
- O Render gerencia a porta automaticamente
- Use `gunicorn app:app` sem especificar porta

### Erro: "Database connection failed"
- Para desenvolvimento, o SQLite é usado automaticamente
- Para produção, considere usar PostgreSQL

### Erro: "SECRET_KEY not set"
- Adicione a variável de ambiente `SECRET_KEY`
- Gere uma chave segura usando Python

## 🔧 Configurações Avançadas

### Usando PostgreSQL

1. **Crie um banco PostgreSQL no Render**
   - New + → PostgreSQL
   - Configure o banco

2. **Conecte o banco ao serviço**
   - Vá para as configurações do Web Service
   - Adicione a variável `DATABASE_URL`
   - Use a URL fornecida pelo PostgreSQL

### Configuração Personalizada do Gunicorn

Edite o `gunicorn.conf.py`:

```python
# Mais workers para melhor performance
workers = 4

# Timeout maior para operações lentas
timeout = 60

# Logs mais detalhados
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

### Domínio Personalizado

1. **Configure DNS**
   - Aponte seu domínio para o Render
   - Use CNAME para `seu-app-name.onrender.com`

2. **Adicione no Render**
   - Settings → Custom Domains
   - Adicione seu domínio

## 📊 Monitoramento

### Logs
- Acesse a aba "Logs" no dashboard
- Monitore erros e performance

### Métricas
- Render fornece métricas básicas
- CPU, memória, requisições

### Health Checks
- Configure endpoints de health check
- Monitore a disponibilidade

## 🔄 Atualizações

### Deploy Automático
- Push para a branch principal
- Render fará deploy automático

### Deploy Manual
- Vá para o dashboard do serviço
- Clique em "Manual Deploy"

## 💰 Custos

### Plano Free
- 750 horas/mês
- 512MB RAM
- 0.1 CPU
- Ideal para desenvolvimento/teste

### Plano Pago
- $7/mês por serviço
- Mais recursos
- Sem limite de horas

## 🎯 Próximos Passos

1. **Teste completamente** a aplicação
2. **Configure monitoramento** se necessário
3. **Considere PostgreSQL** para produção
4. **Configure domínio personalizado**
5. **Implemente CI/CD** se necessário

## 📞 Suporte

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Render Support**: [render.com/support](https://render.com/support)
- **GitHub Issues**: Para problemas específicos do projeto

---

**🎉 Parabéns!** Sua aplicação está no ar e pronta para uso! 