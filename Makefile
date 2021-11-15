# Variáveis
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# Exemplo
filepath=programas/prog1.lcc 

run: 
		python3 -m venv $(VENV)
		. $(VENV)/bin/activate
		$(PIP) install -r requirements.txt
		$(PYTHON) main.py $(filepath)


clean:
		rm -rf __pycache__
		rm -rf $(VENV)