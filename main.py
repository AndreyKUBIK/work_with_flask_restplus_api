#Библиотеки
from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
import statistics

#Заголовки
app = Flask(__name__)
api = Api(app, title="Exhibition API", description="API для выставок")

ns = api.namespace('exhibitions', description='Операции с выставками')

#Оперативная память
exhibitions = {}

#Модель выставок
exhibition_model = api.model('Exhibition', {
    'name': fields.String(required=True, description='Название выставки'),
    'Company': fields.String(required=True, description='Компания-организатор'),
    'theme': fields.String(required=True, description='Тематика выставки'),
    'price': fields.Integer(required=True, description='Стоимость билета'),
    'available': fields.Boolean(required=True, description='Билеты в наличии или нет')
})

#Скелет сортировки и фильтрации
exhibition_list_parser = reqparse.RequestParser()
exhibition_list_parser.add_argument('name', type=str, help='Название')
exhibition_list_parser.add_argument('company', type=str, help='Компания-организатор')
exhibition_list_parser.add_argument('theme', type=str, help='Тематика')
exhibition_list_parser.add_argument('price', type=int, help='Стоимость билета')
exhibition_list_parser.add_argument('available', type=bool, help='В наличии')

exhibition_list_parser.add_argument(
    'sort_by',
    type=str,
    choices=('name', 'company', 'theme', 'price', 'available'),
    help='Поле сортировки'
)

exhibition_list_parser.add_argument(
    'order',
    type=str,
    choices=('asc', 'desc'),
    default='asc',
    help='Порядок сортировки'
)

#Функции для работы с добавлением/изменением/удалением выставок
@ns.route('/<int:exhibition_id>')
class Exhibition(Resource):

    @ns.expect(exhibition_model)
    #Добавление или изменение
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

    #Вывод выставки по ID
    def get(self, exhibition_id):
        """
        Получить выставку по ID
        """
        if exhibition_id not in exhibitions:
            api.abort(404, "Выставка не найдена")
        return exhibitions[exhibition_id]
    
    #Удаление выставки
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
    
    # Получение всех выставок, фильтрация и сортировка по желанию
    @ns.expect(exhibition_list_parser)
    def get(self):
        """
        Получить список выставок с фильтрацией и сортировкой
        """
        args = exhibition_list_parser.parse_args()

        result = [
            {"id": exhibition_id, **exhibition}
            for exhibition_id, exhibition in exhibitions.items()
        ]

        for field in ('name', 'company', 'theme', 'price', 'available'):
            if args[field] is not None:
                result = [
                    b for b in result
                    if b[field] == args[field]
                ]

        if args['sort_by']:
            result.sort(
                key=lambda x: x[args['sort_by']],
                reverse=(args['order'] == 'desc')
            )

        return result, 200

    # avg, min, max цены билетов
    @ns.route('/stats')
    class ExhibitionStats(Resource):

        def get(self):
            """
            Минимальная, максимальная и средняя цена билетов
            """
            if not exhibitions:
                return {
                    "message": "Нет данных для анализа"
                }, 200

            price = [exhibition['price'] for exhibition in exhibitions.values()]

            return {
                "min_price": min(price),
                "max_price": max(price),
                "avg_price": round(statistics.mean(price), 2)
            }, 200

#Старт программы
if __name__ == '__main__':
    app.run(debug=True)