from flask import Flask, jsonify , request
from flask_pymongo import PyMongo
import requests
import random



app = Flask(__name__)
app.config["MONGO_DBNAME"]='universo'
app.config["MONGO_URI"]='mongodb://localhost:27017/universo'
mongo = PyMongo(app)


#- Adicionar um planeta (com nome, clima e terreno) - Listar planetas - Buscar por nome - Buscar por ID - Remover planeta
"""
dado um planeta aleatório da franquia, perguntar como
seria o clima, o terreno e em quantos filmes da franquia ele apareceu.

Para auxiliar quem for apresentar a brincadeira, queremos desenvolver uma aplicação
que pegue aleatoriamente um planeta da franquia e exiba seus dados para servir como
col
"""


def CriandoPlanetaBd():
    planeta = mongo.db.planeta
    cod = input(" Digite um ID :")
    planets = input(" Digite um nome :")
    clima = input(" Digite um clima :")
    terreno = input(" Digite um terreno :")
    print("\n Por favor , aguarde alguns minutos. pode demorar")


    for cont in range(1,62,1) :
      requ = requests.get("https://swapi.co/api/planets/"+ str(cont) +"/?format=json")
      planeta_list = requ.json()
      nome = planeta_list['name']
      filmes = planeta_list['films']

      if(nome == planets):
             qtd_filmes = len(filmes)
             inserindo = planeta.insert_one({'cod':cod,'nome':nome,'clima':clima,'terreno':terreno,'qtd_filmes':qtd_filmes})
             print("\n Inserido com sucesso")
             break
      elif(nome != planets and cont == 61):
            print("\n Infelizmente quantidadeds de aparições não existe \n\n")
            break


def ExcluindoPlanetaBd():
    planeta = mongo.db.planeta
    nome = input(" Digite o nome do Planeta : ")
    excluindo = planeta.delete_one({"nome":nome})



def SortearPlanetas():
    planeta = mongo.db.planeta
    list_planetas = []
    for i in planeta.find():
        list_planetas.append({'cod':i['cod'],'nome':i['nome'],'clima': i['clima'],'terreno':i['terreno'],'qtd_filmes':i['qtd_filmes']})

    secure_random = random.SystemRandom()
    sorteio = []
    sorteio = secure_random.choice(list_planetas)
    print("\n  Planeta Sorteado foi : \n")
    print(" \n  ID :" + sorteio['cod'] +"\n")
    print(" \n  Nome :" +sorteio['nome']+"\n")
    print(" \n  Clima :" + sorteio['clima']+"\n")
    print(" \n  Terreno :"+ sorteio['terreno']+"\n \n")



@app.route('/planetas', methods=['GET'])
def ObterPlanetasBd():
    planeta = mongo.db.planeta
    planetas = []
    for d in planeta.find():
      planetas.append({'cod':d['cod'],'nome':d['nome'],'clima': d['clima'],'terreno':d['terreno'],'qtd_filmes':d['qtd_filmes']})
    return jsonify({'result': planetas})


@app.route('/planetas/<nome>', methods=['GET'])
def BuscarPlanetaNome(nome):
   planeta = mongo.db.planeta
   planetas = []
   achar_nome = planeta.find_one({'nome': nome})
   planetas = {'cod': achar_nome['cod'],'nome': achar_nome['nome'] ,'clima':achar_nome['clima'],'terreno': achar_nome['terreno'],'qtd_filmes':achar_nome['qtd_filmes'] }
   return jsonify({'result':planetas })

@app.route('/planetas/<int:cod>',methods=['GET'])
def BuscarPlanetaID(cod):
    planeta = mongo.db.planeta
    planetas = []
    achar_d = planeta.find_one({'cod':cod})
    planetas = {'cod': achar_d['cod'],'nome': achar_d['nome'] ,'clima':achar_d['clima'],'terreno': achar_d['terreno'],'qtd_filmes':achar_d['qtd_filmes'] }
    return jsonify({'result':planetas})

@app.route('/planetas/',methods=['POST'])
def ObterPlanetaApi():
    planeta = mongo.db.planeta

    cod = request.json['cod']
    nome = request.json['nome']
    clima = request.json['clima']
    terreno = request.json['terreno']
    qtd_filmes = request.json['qtd_filmes']

    planeta_id = planeta.insert({'cod':cod,'nome':nome,'clima':clima,'terreno':terreno,'qtd_filmes':qtd_filmes})
    achar_id = planeta.find_one({'_id':planeta_id})

    planetas = {'cod': achar_id['cod'] ,'nome': achar_id['nome'] ,'clima': achar_id['clima'],'terreno': achar_id['terreno'],'qtd_filmes':achar_id['qtd_filmes']}

    return jsonify({'result':planetas})


@app.route('/planetas/<nome>', methods=['DELETE'])
def ExcluirPlanetas(nome):
    planeta = mongo.db.planeta
    planeta.delete_one({"nome":nome})




if __name__ =='__main__':
  app.run(debug=True, use_reloader=False)
