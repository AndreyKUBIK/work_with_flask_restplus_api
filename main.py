from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, title="Exhibition API", description="API для выставок")

ns = api.namespace('exibitions', description='Операции с выставками')

exhibitions = {}

exhibiton_model = api.model('Exhibition', {
    'name': fields.String(required=True, description='Название выставки'),
    'author': fields.String(required=True, description='Компания-организатор'),
    'theme': fields.String(required=True, description='Тематика выставки'),
    'price': fields.Integer(required=True, description='Стоимость билета'),
    'available': fields.Boolean(required=True, description='Билеты в наличии или нет')
})


@ns.route('/<int:exibition_id>')
class Exhibition(Resource):

    @ns.expect(exhibiton_model)
    def put(self, exhibition_id):
        """
        Добавить или обновить выставку по ID
        """
        exhibitions[exhibition_id] = api.payload
        return {
            "message": "Выставка сохранена",
            "id": exhibition_id,
            "Exhibition": exhibitions[exhibition_id]
        }, 200

    def get(self, exhibition_id):
        """
        Получить выставку по ID
        """
        if exhibition_id not in exhibitions:
            api.abort(404, "Выставка не найдена")
        return exhibitions[exhibition_id]

    def delete(self, exhibition_id):
        """
        Удаление выставки
        """
        deleted_exhibition = exhibitions.pop(exhibition_id)
        return {
            "message": "Выставка удалена",
            "id": exhibition_id,
            "exhibition": deleted_exhibition
        }, 200
    
@ns.route('/')
class ExhibitionList(Resource):

    def get(self):
        """
        Получить список всех выставок
        """
        return exhibitions


if __name__ == '__main__':
    app.run(debug=True)