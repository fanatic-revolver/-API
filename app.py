from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
import config
from flask_swagger_ui import get_swaggerui_blueprint
from blueprints import my_bp
from exts import mail,db

app=Flask(__name__)
app.config.from_object(config)
api = Api(app)



# 初始化db,Mail对象
mail.init_app(app)
db.init_app(app)

SWAGGER_URL="/docs"
API_URL="/static/swagger.json"
SWAGGER_BLUEPRINT=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name":"知识产权集成服务小程序"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)
app.register_blueprint(my_bp)







migrate=Migrate(app,db)


@app.route("/")
def mine():
    return render_template("index.html")

        

    



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")


    

        



