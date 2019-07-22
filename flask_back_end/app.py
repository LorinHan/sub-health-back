from flask import Flask, g, render_template
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request
from flask import jsonify
from sql import Comp_lang, Core, Symptom, Question, User
# from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
app.config['SECRET_KEY'] = 'secret key here'
serializer = Serializer(app.config['SECRET_KEY'], expires_in=1800)
# CORS(app, resources=r'/*')
engine = create_engine("mysql+pymysql://root:123456@localhost/sub-health?charset=utf8")
session = sessionmaker(engine)


@app.route("/")
def render():
	return render_template("index.html")

@app.route("/api/comp_lang")
@auth.login_required
def query():
	mySession = session()
	# index = int(request.args.get("index"))
	core_id = request.args.get("id")
	# 一页返回20条数据
	# limit = 20
	# index *= limit
	arr = []
	# for item in mySession.query(Comp_lang).filter(Comp_lang.core_id == core_id).limit(limit).offset(index):
	try:
		for item in mySession.query(Comp_lang).filter(Comp_lang.core_id == core_id).all():
			arr.append([item.id, item.desc])
	except:
		return "err"
	finally:
		mySession.close()
	
	return json.dumps(arr)

# @app.route('/api/up_photo', methods=['post'])
# def up_photo():
#     img = request.files.get('file')
#     # username = request.form.get("name")
#     path = "./static/photo/"
#     file_path = path+img.filename
#     img.save(file_path)
#     return "ok"
@app.route("/api/core")
@auth.login_required
def query_core():
	mySession = session()
	symptom_id = request.args.get("id")
	arr = []
	try:
		for item in mySession.query(Core).filter(Core.symptom_id == symptom_id).all():
			arr.append([item.id, item.core, item.symptom_id])
	except:
		return "err"
	finally:
		mySession.close()
	
	return json.dumps(arr)

@app.route("/api/symptom")
@auth.login_required
def query_symptom():
	mySession = session()
	kind = request.args.get("kind")
	try:
		if kind == None:
			data = mySession.query(Symptom).filter(Symptom.kind == 1).all()
		else:
			data = mySession.query(Symptom).filter(Symptom.kind == kind).all()
		arr = []
		for item in data:
			arr.append([item.id, item.symptom, item.advice])
	except:
		return "err"
	finally:
		mySession.close()
	
	return json.dumps(arr)

@app.route("/api/question")
@auth.login_required
def query_question():
	mySession = session()
	symptom_id = request.args.get("id")
	arr = []
	try:
		for item in mySession.query(Question).filter(Question.symptom_id == symptom_id).all():
			arr.append([item.id, item.question, item.symptom_id])
	except:
		return "err"
	finally:
		mySession.close()
	
	return json.dumps(arr)


@app.route("/api/add_symptom", methods=['POST'])
@auth.login_required
def add_symptom():
	mySession = session()
	symptom = request.form.get("symptom")
	advice = request.form.get("advice")
	kind = request.form.get("kind")
	try:
		new_symptom = Symptom(symptom=symptom, advice=advice, kind=kind)
		mySession.add(new_symptom)
		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	
	return "ok"

@app.route("/api/add_core", methods=['POST'])
@auth.login_required
def add_core():
	mySession = session()
	core = request.form.get("core")
	symptom_id = request.form.get("symptom_id")
	try:
		new_core = Core(core=core, symptom_id=symptom_id)
		mySession.add(new_core)
		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	
	return "ok"

@app.route("/api/add_comp_lang", methods=['POST'])
@auth.login_required
def add_comp_lang():
	mySession = session()
	desc = request.form.get("desc")
	core_id = request.form.get("core_id")
	try:
		new_comp_lang = Comp_lang(desc=desc, core_id=core_id)
		mySession.add(new_comp_lang)
		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	
	return "ok"

@app.route("/api/add_question", methods=['POST'])
@auth.login_required
def add_question():
	mySession = session()
	question = request.form.get("question")
	symptom_id = request.form.get("symptom_id")
	try:
		new_question = Question(question=question, symptom_id=symptom_id)
		mySession.add(new_question)
		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	
	return "ok"

@app.route("/api/del", methods=['POST'])
@auth.login_required
def del_comp_lang():
	del_id = request.form.get("id")
	del_type = request.form.get("type")
	print(del_type)
	mySession = session()

	try:
		if del_type == "comp_lang":
			comp = mySession.query(Comp_lang).filter(Comp_lang.id == del_id).first()
			mySession.delete(comp)
		elif del_type == "question":
			comp = mySession.query(Question).filter(Question.id == del_id).first()
			mySession.delete(comp)
		elif del_type == "core":
			core = mySession.query(Core).filter(Core.id == del_id).first()
			comp_langs = mySession.query(Comp_lang).filter(Comp_lang.core_id == core.id).all()
			for item in comp_langs:
				mySession.delete(item)
			mySession.delete(core)
		elif del_type == "symptom":
			symptom = mySession.query(Symptom).filter(Symptom.id == del_id).first()
			# 删除二次问诊题目
			for item in mySession.query(Question).filter(Question.symptom_id == symptom.id).all():
				mySession.delete(item)
			# 所有与该症状相关的指标
			cores = mySession.query(Core).filter(Core.symptom_id == symptom.id).all()
			for core in cores:
				comp_langs = mySession.query(Comp_lang).filter(Comp_lang.core_id == core.id).all() # 所有与该指标相关的口语化描述
				for comp_lang in comp_langs:   # 遍历每一个口语化描述
					mySession.delete(comp_lang) # 删除每一个口语化描述
				mySession.delete(core)         # 删除每一个指标
			mySession.delete(symptom)		 # 删除该症状
		
		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	
	return "ok"

@app.route("/api/update", methods=['POST'])
@auth.login_required
def update():
	print("shit")
	update_id = request.form.get("id")
	update_type = request.form.get("type")
	update_value = request.form.get("value")

	mySession = session()
	try:
		if update_type == "comp_lang":
			comp = mySession.query(Comp_lang).filter(Comp_lang.id == update_id).first()
			comp.desc = update_value
			mySession.add(comp)
		elif update_type == "core":
			core = mySession.query(Core).filter(Core.id == update_id).first()
			core.core = update_value
			mySession.add(core)
		elif update_type == "question":
			question = mySession.query(Question).filter(Question.id == update_id).first()
			question.question = update_value
			mySession.add(question)
		elif update_type == "symptom":
			update_value2 = request.form.get("value2")
			symptom = mySession.query(Symptom).filter(Symptom.id == update_id).first()
			symptom.symptom = update_value
			symptom.advice = update_value2
			mySession.add(symptom)

		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	
	return "ok"

@auth.verify_token
def verify_token(token):
	g.user = None
	try:
		data = serializer.loads(token)
		print(data)
	except:
		return False
	if 'username' in data:
		g.user = data['username']
		return True
	return False

@app.route('/api/token', methods=['POST'])
def index():
	username = request.form.get("username")
	password = request.form.get("password")
	mySession = session()
	try:
		user = mySession.query(User).filter(User.username == username).first()
		if user == None:
			return "300" # 用户名或密码错误 300
		if user.password == password:
			token = serializer.dumps({'username': username})
			return token
		else:
			return "300"
	except:
		return "err"
	finally:
		mySession.close()

	return "err"

@app.route('/api/update_password', methods=['POST'])
def update_password():
	username = request.form.get("username")
	password = request.form.get("password")
	old_pwd = request.form.get("old_pwd")
	mySession = session()
	try:
		user = mySession.query(User).filter(User.username == username).first()
		if user.password != old_pwd:
			return "pwd_err"
		user.password = password
		print(password)
		mySession.add(user)
		mySession.commit()
	except:
		return "err"
	finally:
		mySession.close()
	return "ok"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=2001)