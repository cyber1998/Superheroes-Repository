from api import create_app


if __name__ == '__main__':
    app = create_app('api.config')
    app.run(debug=True, port=5000, host='localhost')
