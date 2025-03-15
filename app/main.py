from flask import Flask
from controllers.imoveis import imoveis_bp

app = Flask(__name__)
app.register_blueprint(imoveis_bp)

if __name__ == '__main__':
    app.run(debug=True)
