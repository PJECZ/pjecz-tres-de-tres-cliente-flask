"""
Google Cloud App Engine toma main.py
"""
from tres_de_tres_cliente_flask import app

app = app.create_app()


if __name__ == "__main__":
    app.run()
