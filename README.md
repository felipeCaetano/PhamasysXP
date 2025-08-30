# PharmaSysXP 💊

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/status-development-orange.svg)](#)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](#)

> **Plataforma modular de gestão farmacêutica** desenvolvida em Python, com foco em controle de estoque, cadastro de fornecedores e integração com notas fiscais eletrônicas.

## 🎯 Visão do Produto

O **PharmaSysXP** é uma solução escalável, segura e de fácil manutenção para farmácias e distribuidoras, oferecendo uma plataforma completa de gestão que permite:

- **Cadastro completo** de produtos, fornecedores e notas fiscais
- **Controle de estoque** com rastreabilidade de movimentações
- **Integração** com sistemas de emissão de NF-e e DANFE
- **Geração de relatórios** gerenciais e operacionais
- **Segurança e conformidade** com regulamentos (LGPD)

## ✨ Funcionalidades Principais

### 📦 Gestão de Produtos e Estoque
- **Cadastro de medicamentos** com informações completas
- **Controle de lotes** e validade
- **Rastreabilidade** completa de movimentações
- **Alertas de estoque** crítico e vencimento

### 🏢 Gestão de Fornecedores
- **Cadastro completo** de fornecedores
- **Histórico de compras** e relacionamento
- **Avaliação de performance** de fornecedores
- **Controle de contratos** e condições

### 📄 Integração Fiscal
- **Importação automática** de NF-e
- **Geração de DANFE**
- **Controle fiscal** completo
- **Relatórios fiscais** automatizados

### 📊 Relatórios e Analytics
- **Relatórios gerenciais** personalizáveis
- **Análise de vendas** e estoque
- **Exportação** para PDF/Excel
- **Dashboards** interativos

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Interface**: Tkinter/CustomTkinter para desktop
- **Banco de Dados**: SQLite/PostgreSQL
- **Testes**: pytest com cobertura de código
- **Documentação**: Sphinx com diagramas C4/UML
- **Qualidade**: flake8, black para padronização
- **Integração**: APIs REST para NF-e e sistemas externos

## 📁 Estrutura do Projeto

```
PharmaSysXP/
├── src/
│   ├── main.py                 # Entrada principal da aplicação
│   └── app/
│       ├── models/             # Modelos de dados
│       ├── services/           # Lógica de negócio
│       ├── ui/                 # Telas e componentes de interface
│       ├── controllers/        # Integração entre UI e serviços
│       └── assets/            # Recursos estáticos (imagens, ícones)
├── experimental/              # Scripts experimentais ou POC
├── tests/                     # Testes unitários e de integração
├── docs/                      # Documentação e diagramas
├── requirements.txt           # Dependências Python
├── .gitignore
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## 📋 Requisitos do Sistema

### Requisitos Mínimos
- **Python**: 3.8 ou superior
- **Sistema Operacional**: Windows 10+, Linux Ubuntu 18.04+, macOS 10.15+
- **Memória RAM**: 4 GB
- **Espaço em disco**: 1 GB livre
- **Resolução**: 1024x768 ou superior

### Requisitos Recomendados
- **Python**: 3.10+ com pip atualizado
- **Memória RAM**: 8 GB ou mais
- **Espaço em disco**: 5 GB livres para dados e backups
- **SSD**: Para melhor performance do banco de dados
- **Conexão com internet**: Para integração fiscal e atualizações

## 🚀 Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/felipeCaetano/PhamasysXP.git
cd PhamasysXP
```

### 2. Crie e Ative um Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados
```bash
# Execute as migrações (se aplicável)
python src/setup_database.py
```

### 5. Execute a Aplicação
```bash
python src/main.py
```

## 🧪 Testes

Execute todos os testes unitários e de integração:

```bash
# Executar todos os testes
pytest tests/

# Executar testes com relatório de cobertura
pytest tests/ --cov=src

# Executar testes específicos
pytest tests/test_models.py -v
```

### Estrutura de Testes
```bash
tests/
├── test_models/          # Testes dos modelos de dados
├── test_services/        # Testes da lógica de negócio
├── test_controllers/     # Testes dos controllers
├── test_integration/     # Testes de integração
└── fixtures/            # Dados de teste
```

## 📖 Como Usar

### Primeiro Acesso
1. **Inicialização**: Execute `python src/main.py`
2. **Configuração Inicial**: Configure os dados da farmácia
3. **Cadastros Base**: Registre fornecedores e categorias
4. **Produtos**: Adicione medicamentos ao sistema
5. **Integração Fiscal**: Configure certificados e URLs

### Operações Principais
1. **Cadastro de Produtos**: Use o módulo de produtos para gerenciar medicamentos
2. **Controle de Estoque**: Monitore entradas, saídas e níveis
3. **Gestão de Fornecedores**: Mantenha base atualizada de fornecedores
4. **Relatórios**: Gere relatórios gerenciais e operacionais
5. **Backup**: Execute backups regulares dos dados

## 📈 Roadmap

### 🎯 **Q1 2026** - MVP Completo
- [x] Estrutura base do projeto
- [ ] Cadastro de produtos completo
- [ ] Gestão de fornecedores
- [ ] Sistema de notas fiscais
- [ ] Interface de usuário principal

### 🔗 **Q2 2026** - Integração Fiscal
- [ ] Integração automática com NF-e
- [ ] Geração de DANFE
- [ ] Validação fiscal automatizada
- [ ] API de consulta de produtos

### 📊 **Q3 2026** - Relatórios e Analytics
- [ ] Relatórios gerenciais avançados
- [ ] Exportação para PDF/Excel
- [ ] Dashboards interativos
- [ ] Análise de performance

### 🔐 **Q4 2026** - Segurança e Usuários
- [ ] Sistema de autenticação
- [ ] Controle de acesso por perfil
- [ ] Auditoria de operações
- [ ] Conformidade com LGPD

### 🚨 **Q1 2027** - Automação
- [ ] Alertas de estoque crítico
- [ ] Notificações de vencimento
- [ ] Automação de pedidos
- [ ] Integração com ERP

### 🏪 **Q2 2027** - Versão Comercial
- [ ] Preparação para comercialização
- [ ] Conformidade regulatória completa
- [ ] Suporte técnico estruturado
- [ ] Documentação de usuário final

## 📄 Documentação

A documentação técnica completa está disponível na pasta `docs/` e inclui:

- **Diagramas de Arquitetura**: C4 Model e UML
- **Especificação de APIs**: Endpoints e contratos
- **Manual de Instalação**: Guias detalhados
- **Documentação de Código**: Docstrings e comentários
- **Guias de Contribuição**: Padrões e práticas

### Gerando Documentação
```bash
# Gerar documentação com Sphinx
cd docs/
make html

# Visualizar documentação
open _build/html/index.html
```

## 🤝 Contribuindo

Agradecemos sua contribuição! Para contribuir com o projeto:

### Padrões de Desenvolvimento
- **Estrutura**: Use `src/app/` para código principal
- **Experimentação**: Scripts experimentais em `experimental/`
- **Testes**: Crie/atualize testes em `tests/`
- **Qualidade**: Use `flake8` e `black` para padronização

### Fluxo de Contribuição
1. Fork do projeto
2. Crie uma branch feature (`git checkout -b feature/nova-funcionalidade`)
3. Implemente as mudanças seguindo os padrões
4. Execute os testes (`pytest tests/`)
5. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
6. Push para a branch (`git push origin feature/nova-funcionalidade`)
7. Abra um Pull Request detalhado

### Padrões de Código
```bash
# Verificar qualidade do código
flake8 src/

# Formatar código automaticamente
black src/

# Verificar tipos (se usando)
mypy src/
```

## 🐛 Reportar Problemas

Encontrou um bug? Abra uma [issue](https://github.com/felipeCaetano/PhamasysXP/issues) incluindo:

- **Descrição detalhada** do problema
- **Passos para reproduzir** o erro
- **Ambiente** (SO, versão Python, dependências)
- **Screenshots** se aplicável
- **Logs de erro** relevantes

## 📊 Capturas de Tela

### Dashboard Principal
![Dashboard](docs/screenshots/dashboard.png)

### Gestão de Produtos
![Produtos](docs/screenshots/produtos.png)

### Controle de Estoque
![Estoque](docs/screenshots/estoque.png)

### Relatórios
![Relatórios](docs/screenshots/relatorios.png)

## 🛡️ Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes completos.

## ✨ Reconhecimentos

- **Comunidade farmacêutica brasileira** pelas sugestões e feedback
- **Desenvolvedores contribuidores** do projeto
- **Bibliotecas Python** de código aberto utilizadas
- **Reguladores e órgãos** que definem padrões do setor

## 📞 Contato

**Felipe Caetano** - Desenvolvedor Principal

- 🐙 GitHub: [@felipeCaetano](https://github.com/felipeCaetano)
- 📧 Email: [seu-email@exemplo.com]
- 💼 LinkedIn: [Seu Perfil LinkedIn]

## 🌟 Apoie o Projeto

Se este projeto foi útil para você:

- ⭐ **Dê uma estrela** no repositório
- 🐛 **Reporte bugs** ou sugira melhorias
- 📢 **Compartilhe** com outros profissionais
- 💻 **Contribua** com código
- 📖 **Melhore** a documentação

---

<div align="center">

**Desenvolvido com ❤️ para revolucionar a gestão farmacêutica brasileira**

[⬆ Voltar ao topo](#pharmasysxp-)

</div>
