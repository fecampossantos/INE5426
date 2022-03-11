 # Variáveis
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

# Exemplo
filepath=src/examples/exemplo1.lcc 

run: 
		rm -rf venv/
		rm -rf semantic_analysis.json
		rm -rf intermediary_code.txt
		python3 -m venv $(VENV)
		. $(VENV)/bin/activate
		$(PIP) install -r requirements.txt
		$(PYTHON) src/main.py ${filepath}


clean:
		rm -rf __pycache__
		rm -rf $(VENV)