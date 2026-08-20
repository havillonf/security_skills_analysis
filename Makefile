.PHONY: setup download notebook clean clean-data help

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
JUPYTER := $(VENV)/bin/jupyter
KERNEL_NAME := security-skills

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: $(VENV)/bin/activate ## Cria venv, instala dependências e registra kernel Jupyter
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PYTHON) -m ipykernel install --user --name $(KERNEL_NAME) --display-name "Security Skills Analysis"
	@echo ""
	@echo "✅ Setup concluído! Ative o ambiente com: source $(VENV)/bin/activate"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	@touch $(VENV)/bin/activate

download: $(VENV)/bin/activate ## Baixa o dataset do HuggingFace para data/
	$(PYTHON) scripts/download_dataset.py
	@echo ""
	@echo "✅ Dataset baixado em data/"

notebook: ## Abre o Jupyter Notebook
	$(JUPYTER) notebook notebooks/

clean: ## Remove o ambiente virtual
	rm -rf $(VENV)
	@echo "🗑️  Ambiente virtual removido."

clean-data: ## Remove os dados locais do dataset
	rm -rf data/*.parquet data/*.db
	@echo "🗑️  Dados locais removidos."
