import sys
import os

# Adicione o diretório raiz do projeto ao sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

# Importe o módulo ORM
from database.infra.orm import ORM

def main():
    orm = ORM()
    orm.create_tables()

if __name__ == "__main__":
    main()