from flask import Flask, request
from flask_restful import Resource, Api
from models import Despesas

app = Flask(__name__)
api = Api(app)


class Despesa(Resource):
    def get(self, nome):
        despesa = Despesas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': despesa.nome,
                'data': despesa.data,
                'tipo': despesa.tipo,
                'valor': despesa.valor,
                'observacao': despesa.observacao
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Despesa não encontrada'
            }
        return response

    def put(self, nome):
        despesa = Despesas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            despesa.nome = dados['nome']

        if 'data' in dados:
            despesa.data = dados['data']

        if 'tipo' in dados:
            despesa.tipo = dados['tipo']

        if 'valor' in dados:
            despesa.valor = dados['valor']

        if 'observacao' in dados:
            despesa.observacao = dados['observacao']

        despesa.save()
        response = {
            'id': despesa.id,
            'nome': despesa.nome,
            'data': despesa.data,
            'tipo': despesa.tipo,
            'valor': despesa.valor,
            'observacao': despesa.observacao
        }
        return response

    def delete(self, nome):
        despesa = Despesas.query.filter_by(nome=nome).first()
        mensagem = 'Despesa {} excluida com sucesso'.format(despesa)
        despesa.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaDespesas(Resource):
    def get(self):
        despesas = Despesas.query.all()
        response = [{'id': i.id,
                     'nome': i.nome,
                     'data': i.data,
                     'tipo': i.tipo,
                     'valor': i.valor,
                     'observacao': i.observacao
                     } for i in despesas]
        return response

    def post(self):
        dados = request.json
        despesa = Despesas(nome=dados['nome'],
                           data=dados['data'],
                           tipo=dados['tipo'],
                           valor=dados['valor'],
                           observacao=dados['observacao'])
        despesa.save()
        response = {
            'id': despesa.id,
            'nome': despesa.nome,
            'data': despesa.data,
            'tipo': despesa.tipo,
            'valor': despesa.valor,
            'observacao': despesa.observacao
        }
        return response


api.add_resource(Despesa, '/despesa/<string:nome>/')
api.add_resource(ListaDespesas, '/despesas/')

if __name__ == '__main__':
    app.run(debug=True)
