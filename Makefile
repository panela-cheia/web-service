MAIN = src/main.py

all:
	python3 -B $(MAIN)

pyro:
	pyro5-ns -n localhost

server:
	python3 -B src/server.py

venv:
	python3 -m venv . 

run_venv_pyro:
	source bin/activate && make pyro

run_venv_server:
	source bin/activate && make

clean:
	true || deactivate && rm -rf bin/ lib/ lib64/ lib64 include/ share/ pyvenv.cfg

create_database:
	python3 -B database/create.py

populate:
	python3 -B prisma/seed.py

test:
	python3 -B src/test-server.py