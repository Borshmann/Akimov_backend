Установка зависимостей:

    pip install -r requirements.txt

Локально создать файл .env, прописать нужные настройки окружения
Удачи!

Чтобы развернуть сервер:

    pip install waitress

В файле app.py прописать, указав host и port:

    if __name__ == "__main__":
     from waitress import serve
     serve(app, host="*.*.*.*", port=****)