import os
import json
import openai

from flask import Blueprint, jsonify, request
from Pyro5.api import Proxy

recipes_routes = Blueprint('recipes', __name__)

@recipes_routes.route('/recipes', methods=["POST"])
def create_recipe():
    name = request.json["name"]
    description = request.json["description"]
    ingredients = request.json["ingredients"]
    userId = request.json["userId"]
    fileId = request.json["fileId"]
    diveId = request.json["diveId"]

    try:
        recipe = Proxy("PYRONAME:adapters.create_recipe_adapter").execute(
            name=name,
            description=description,
            ingredients=ingredients,
            userId=userId,
            fileId=fileId,
            diveId=diveId
        )

        return jsonify({'data': recipe}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@recipes_routes.route('/recipes', methods=["GET"])
def list_recipes():
    try:
        recipes = Proxy("PYRONAME:adapters.list_recipe_adapter").execute()

        return jsonify({'data': recipes}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@recipes_routes.route('/recipes/<id>/react', methods=["PUT"])
def react(id):
    user_id = request.json["user_id"]
    typeR = request.json["type"]
    
    try:
        recipes = Proxy("PYRONAME:adapters.reaction_recipe_adapter").execute(
            recipe_id=id,
            user_id=user_id,
            type=typeR
        )

        return jsonify({'data': recipes}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@recipes_routes.route('/recipes/search', methods=["GET"])
def search():
    name = request.args.get("name")
    
    try:
        recipes = Proxy("PYRONAME:adapters.search_recipe_adapter").execute(
            name=name
        )

        return jsonify({'data': recipes}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@recipes_routes.route("/recipes/openai/description", methods=['GET'])
def description_recipe():
    nome_receita = request.args.get("name")

    # Prompt inicial para a geração de descrição da receita
    prompt = f"Aqui está uma descrição da receita de {nome_receita} com no máximo 40 caracteres, querendo convencer outras pessoas a fazerem a receita:"

    # Parâmetros para a chamada da API do ChatGPT
    params = {
        'engine': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 40,  # Defina o número máximo de tokens na resposta
        # Controla a aleatoriedade das respostas (0.2 é mais determinístico, 0.8 é mais criativo)
        'temperature': 0.8,
        'n': 1,  # Gere apenas uma resposta
        'stop': None  # Não defina uma palavra de parada para a resposta
    }

    try:
        openai.api_key = os.getenv('OPENAI_KEY')
        # Fazendo a chamada para a API do ChatGPT
        response = openai.Completion.create(**params)

        # Obtendo a descrição gerada
        descricao = response.choices[0].text.strip()

        return jsonify({'description': descricao}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_routes.route("/recipes/openai/ingredients", methods=['GET'])
def ingredients_recipe():
    nome_receita = request.args.get("name")
    descricao_receita = request.args.get("description")

    prompt = f"Sendo uma receita culinária de nome {nome_receita}, com a seguinte descrição: '{descricao_receita}',"
    prompt += "informe a lista de ingredientes possíveis da receita\n. Cada ingrediente é uma tripla com os campos:"
    prompt += "'name' (String), 'amount' (Integer) e 'unit' (String).\n"
    prompt += "A lista de unidades possíveis é a seguinte:\n\n"
    prompt += "['Unidade','Miligrama (mg)','Copo','Fio','Grama (g)','Pitada','Litro (l)','Raspas',"
    prompt += "'Tablete','Ramo','Colher de chá (c.c.)','Mililitro (ml)','Xícara (xíc.)',"
    prompt += "'Filete','Colher de sopa (c.s.)','Quilograma (kg)','Punhado']."
    prompt += "Retorne a lista de ingredientes como uma string JSON contendo em cada objeto os campos 'name', 'amount' e 'unit'."
    prompt += "Certifique-se de que a string JSON esteja corretamente formatada, com cada objeto de ingredientes separado por vírgula e o array de ingredientes devidamente fechado com colchetes no final."
    # Parâmetros para a chamada da API do ChatGPT
    params = {
        'engine': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 400,  # Defina o número máximo de tokens na resposta
        # Controla a aleatoriedade das respostas (0.2 é mais determinístico, 0.8 é mais criativo)
        'temperature': 0.1,
        'n': 1,  # Gere apenas uma resposta
        'stop': None  # Não defina uma palavra de parada para a resposta
    }

    try:

        openai.api_key = os.getenv('OPENAI_KEY')
        # Fazendo a chamada para a API do ChatGPT
        response = openai.Completion.create(**params)

        # Obtendo a descrição gerada
        ingredients = response.choices[0].text.strip()

        ingredients_json = json.loads(ingredients)

        return jsonify({'ingredients': ingredients_json}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500