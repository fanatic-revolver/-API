from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify,Blueprint

from flask_restful import Resource, Api, reqparse
import re
from flask_mail import Mail,Message

from exts import db, mail
from models import User

my_bp=Blueprint('email and description',__name__)
api=Api(my_bp)
class submitAPI(Resource):
    def post(self):
        # data = request.get_json()
        # email=data["email"] #这里需要修改表单接收的名称
        # description=data["description"]  #这里需要修改表单接收的名称
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str, help="description错误")
        parser.add_argument('email', type=str, help="email错误")
        args = parser.parse_args()
        email = args.get("email")
        description = args.get("description")
        pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$'  # 正则表达式模式
        match_result = re.match(pattern, email)
        if match_result:
            if not email or not description:
                return jsonify({'code':-1,'msg': 'Missing required fields'})

            user = User(email=email, description=description)
            db.session.add(user)
            db.session.commit()
            msg = Message('邮件主题', sender='m626164783@163.com', recipients=['626164783@qq.com'])
            # 设置邮件内容
            # msg.body = '用户提交时间:'+str(user.submission_time)+'\n用户联系方式：'+user.phone_number+'\n用户需求内容：'+user.description
            msg.body="用户提交时间：{}\n用户联系方式：{}\n用户需求内容：{}\n".format(str(user.submission_time),user.email,user.description)
            mail.send(msg)
            return jsonify({'code':0,'msg': 'Form submitted successfully'})
        else:
            return jsonify({'code':-1,'msg': 'Email format incorrect'})


class pageAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help="id验证错误")
        parser.add_argument('email', type=str, help="email验证错误")
        args = parser.parse_args()
        email = args.get("email")
        id = args.get("id")

        if id:
            users = User.query.filter_by(id=id).all()
        elif email:
            users = User.query.filter_by(email=email).all()
        elif email and id:
            users = User.query.filter_by(email=email, id=id).all()

        if not users:
            return jsonify({'code': 0, 'msg': "没有找到匹配的用户"})

        if len(users) == 1:
            user = users[0]
            response = {
                'code': 0,
                'msg': "分页查询成功",
                'data': {
                    'id': user.id,
                    'email': user.email,
                    "description": user.description,
                    'submission_time': user.submission_time
                }
            }
            return jsonify(response)
        else:
            user_list = []
            for user in users:
                user_data = {
                    'id': user.id,
                    'email': user.email,
                    "description": user.description,
                    'submission_time': user.submission_time
                }
                user_list.append(user_data)

            response = {
                'code': 0,
                'msg': "分页查询成功",
                'data': {
                    'total': len(users),
                    'datas': user_list
                }
            }
            return jsonify(response)

api.add_resource(submitAPI,"/submit")
api.add_resource(pageAPI,"/page")