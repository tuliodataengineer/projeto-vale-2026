# 🏗️ Projeto Vale 2026

Projeto de análise de dados, machine learning e dashboard para a Vale — 2026.

---

## 📁 Estrutura de Pastas

```
projeto-vale-2026/
├── data/
│   ├── raw/          → Dados brutos (nunca editar)
│   └── processed/    → Dados tratados e prontos para uso
├── notebooks/        → Análises exploratórias (Jupyter Notebooks)
├── src/              → Scripts Python (pipeline, modelos, utilitários)
├── dashboard/        → Arquivos Power BI e templates
├── relatorio/        → Relatórios finais gerados
└── README.md
```

---

## ⚙️ Como Configurar o Ambiente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/projeto-vale-2026.git
cd projeto-vale-2026
```

### 2. Crie o ambiente virtual Python
```bash
# Com venv
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Ou com conda
conda create -n vale2026 python=3.10
conda activate vale2026
```

### 3. Instale as dependências
```bash
pip install pandas numpy scikit-learn xgboost shap matplotlib seaborn
```

---

## 🚀 Como Rodar o Pipeline

```bash
# 1. Coloque os dados brutos em /data/raw/
# 2. Execute o pipeline de processamento
python src/pipeline.py

# 3. Execute o modelo
python src/modelo.py

# 4. Gere o relatório
python src/relatorio.py
```

---

## 📐 Convenção de Nomenclatura

### Arquivos
| Tipo | Formato | Exemplo |
|------|---------|---------|
| Notebooks | `XX_descricao.ipynb` | `01_exploracao.ipynb` |
| Scripts | `snake_case.py` | `pipeline_dados.py` |
| Dados brutos | `YYYYMMDD_descricao.csv` | `20260101_vendas.csv` |
| Dados processados | `descricao_processed.csv` | `vendas_processed.csv` |

### Branches
| Branch | Uso |
|--------|-----|
| `main` | Versão estável e final |
| `dev` | Desenvolvimento ativo |
| `feature/nome` | Nova funcionalidade |
| `fix/nome` | Correção de bug |

---

## 🛠️ Tecnologias Utilizadas

- **Python** — pandas, numpy, scikit-learn, xgboost, shap, matplotlib, seaborn
- **Power BI Desktop** — dashboards e visualizações
- **Git/GitHub** — controle de versão
- **Jupyter Notebook** — análise exploratória

---

## 👤 Contato

Projeto desenvolvido para análise de dados — Vale 2026.
