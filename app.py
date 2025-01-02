from flask import Flask

app = Flask(__name__)
app.debug = True

#import blueprints
from api.views.users import user_blueprint


app.register_blueprint(user_blueprint)


if __name__ == '__main__':
    app.run(port=5000)

