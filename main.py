from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    title="Todo API",
    description="GET и PUT",
)

todos = {}

todo_model = api.model('Todo', {
    'data': fields.String(required=True, description='Текст задачи')
})


@api.route('/todo/<string:todo_id>')
class Todo(Resource):

    @api.response(200, 'Задача найдена')
    @api.response(404, 'Задача не найдена')
    def get(self, todo_id):
        if todo_id not in todos:
            api.abort(404, f"Задача {todo_id} не найдена")

        return {
            "todo_id": todo_id,
            "data": todos[todo_id]
        }


    @api.expect(todo_model)
    @api.response(200, 'Задача сохранена')
    def put(self, todo_id):
        todos[todo_id] = api.payload['data']

        return {
            "todo_id": todo_id,
            "data": todos[todo_id]
        }


if __name__ == '__main__':
    app.run(debug=True)