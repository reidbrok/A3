import sqlite3
from flask import Flask, render_template, request, g, session, redirect, url_for, escape
DATABASE = './Assignment3.db'
#the get_db function is copied from lecture vedio https://youtu.be/J-r34WbcdWo
def get_db():
	db=getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db
#the query_db function is copied from lecture vedio https://youtu.be/J-r34WbcdWo
def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

#the make_dicts function is copied from lecture vedio https://youtu.be/J-r34WbcdWo
def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value)
				for idx, value in enumerate(row))

app = Flask(__name__)
app.secret_key=b'a3'

#the close_connection function is copied from lecture vedio https://youtu.be/J-r34WbcdWo
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database',None)
	if db is not None:
		db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	db = get_db()
	db.row_factory = make_dicts
	name=request.form.get('name')
	password=request.form.get('password')
	par = [name, password]
	#res1 = query_db('SELECT * FROM user WHERE name = ?',[name])['name']
	#res2 = query_db('SELECT * FROM user WHERE name = ?',[name])['password']
	user = query_db('SELECT * FROM user WHERE name = ? AND password <> ?',[name,''],True)
	userinfo = isinstance(user, dict)
	# for info in user:
	# 	if info is not None:
	# 		userinfo += info +" "
	# dict_key = user.keys()
	# keyStr = ""
	# for key in dict_key:
	# 	keyStr += keyStr
	if request.method == 'POST': 
		if user is None:
			error = 'Non-existing user'
			db.close()
		elif password != user['password']:
		 	error = 'Invalid Credentials. Please try again.'
		 	db.close()
		else:
			session['username'] = name
			session['position'] = user['position']
			db.close()
			return render_template('index.html', error='login successfully')
	if name is not None and password is not None:
		error = "username: "+name+", pwd: "+password + ", info: "+ str(user['password'])
	db.close()
	return render_template('login.html', error=error)

'''
	if 'username' in session:
		return 'Logged in as %s <a href="/logout.html">Logout</a>' % escape(session['username'])
	else:
		error = None
		if request.method == 'POST':
			if request.form['username'] != 'admin' or request.form['password'] != 'admin':
				error = 'Invalid Credentials. Please try again.'
		else:
			return render_template('index.html')
		return render_template('login.html', error=error)
'''
'''db = get_db()
		db.row_factory = make_dicts
		name = request.args.get("name")
		password = request.args.get("password")
		user = query_db('SELECT * FROM user WHERE name = ?',[name], one=True)
		key = query_db('SELECT * FROM user WHERE name = ? AND password = ?',[name, password], one=True)
		db.close()
		if user is None:
			return render_template('assignments.html', var = "sorry, user does not exists")
		elif key is None:
			return render_template('lab.html', var = "sorry, wrong password")
		else:
			return render_template('index.html')
'''


@app.route('/')
def root():
	if 'username' in session:
		return render_template('index.html', name = session['username'], position = session["position"])
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return render_template('login.html')

@app.route("/index")
def home():
	if 'username' in session:
		return render_template('index.html', name = session['username'], position = session["position"])
	else:
		return render_template('login.html')

@app.route("/assignments")
def assignments():
	if 'username' in session:
		return render_template('assignments.html', name = session['username'],  position = session["position"])
	else:
		return render_template('login.html')

@app.route("/lab")
def lab():
	if 'username' in session:
		return render_template('lab.html', name = session['username'],  position = session["position"])
	else:
		return render_template('login.html')

@app.route("/news")
def news():
	if 'username' in session:
		return render_template('news.html', name = session['username'], position = session["position"])
	else:
		return render_template('login.html')

@app.route("/discussion board")
def discussion():
	if 'username' in session:
		return render_template('board.html', name = session['username'], position = session["position"])
	else:
		return render_template('login.html')
@app.route("/test")
def test():
	if 'username' in session:
		return render_template('test.html', name = session['username'], position = session["position"])
	else:
		return render_template('login.html')

@app.route("/calender")
def calender():
	if 'username' in session:
		return render_template('calender.html', name = session['username'], position = session['position'])
	else:
		return render_template('login.html')

@app.route("/lectures")
def lectures():
	if 'username' in session:
		return render_template('lectures.html', name = session['username'], position = session['position'])
	else:
		return render_template('login.html')

@app.route("/resource")
def resource():
	if 'username' in session:
		return render_template('resource.html', name = session['username'], position = session['position'])
	else:
		return render_template('login.html')
# @app.route("/test_insert")
# def test_insert():
# 	db = get_db()
# 	db.row_factory = make_dicts
# 	pars=['new','new','student',None,None,None,None,None,None,None]
# 	query_db("INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?,?)",pars)
# 	db.commit()
# 	return "finish"

@app.route("/remarkI")
def remarkI():
	db = get_db()
	db.row_factory = make_dicts
	student_remark= request.args.get('student')
	assignment_remark = request.args.get('assignment')
	mark_remark = request.args.get('mark')
	query_db('''UPDATE user 
					SET mark=? 
					WHERE name=? AND assignment=?;''',[mark_remark,student_remark,assignment_remark])
	db.commit()
	db.close()
	return '''finished remark!
			  <a href="http://127.0.0.1:5000/mark">Back to Mark</a>'''

@app.route("/remarkS")
def remarkS():
	db = get_db()
	student_remark= request.args.get('student')
	assignment_remark = request.args.get('assignment')
	reason_remark = request.args.get('reason')
	query_db('''UPDATE user 
					SET mark=?, reason=?
					WHERE name=? AND assignment=?;''',['-1',reason_remark,student_remark,assignment_remark])
	db.commit()
	db.close()
	return '''finished remark!
			  <a href="http://127.0.0.1:5000/mark">Back to Mark</a>'''

@app.route("/newmark")
def newmark():
	db=get_db()
	name=request.args.get('newstudent')
	assignment=request.args.get('newassignment')
	mark=request.args.get('newmark')
	pars=[name,None,'student',assignment,mark,None,None,None,None,None]
	query_db('INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?,?)',pars)
	db.commit()
	db.close()
	return '''finished posting new mark
	<a href="http://127.0.0.1:5000/mark">Back to Mark</a>'''
	
@app.route("/mark")
def mark():
	if 'username' in session:
		db = get_db()
		db.row_factory = make_dicts
		information=[]
		remark=[]
		allstudents=[]
		if session['position']== 'instructor':
			for student in query_db('SELECT * FROM user WHERE position=? AND mark<>?',['student','']):
				information.append(student)
				if(student.get("mark")=='-1'):
					remark.append(student)
			for student in query_db('SELECT * FROM user WHERE position=? AND password<>?',['student','']):
				allstudents.append(student)
			db.close()
			return render_template("mark.html", students=information, remark=remark, position=session['position'], allstudents=allstudents, name = session['username'])
		else:
			for student in query_db('SELECT * FROM user WHERE position=? AND name=? AND mark<>?',['student', session['username'],'']):
				information.append(student)
			db.close()
			return render_template("mark.html", students=information, position=session['position'],  name = session['username'])
	else:
		return render_template('login.html')

@app.route("/feedbacksS")
def getfeedback():
	name=request.args.get('instructor')
	f1= request.args.get('f1')
	f2= request.args.get('f2')
	f3= request.args.get('f3')
	f4= request.args.get('f4')
	pars=[name, None,'instructor',None, None,None,f1,f2,f3,f4]
	db = get_db()
	query_db('INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?,?)',pars)
	db.commit()
	db.close()
	return '''finished submit!
			  <a href="http://127.0.0.1:5000/feedback">Back to Feedback</a>'''

@app.route("/feedback")
def feedback():
	if 'username' in session:
		db = get_db()
		db.row_factory = make_dicts
		feedbacks=[]
		instructors=[]
		if 'position' in session and session['position'] == 'instructor':
			for feedback in query_db('SELECT * FROM user WHERE name=? AND position=? AND f1<>?',[session['username'], 'instructor', '']):
				feedbacks.append(feedback)
			db.close()
			return render_template('feedback.html', feedbacks=feedbacks, position=session['position'], name = session['username'])
		else:
			for instructor in query_db('SELECT * From user WHERE position=? AND password<>?',['instructor','']):
				instructors.append(instructor)
			db.close()
			return render_template('feedback.html', position=session['position'], instructors=instructors, name = session['username'])
	else:
		return render_template('login.html')


@app.route("/register")
def register():
	db = get_db()
	name=request.args.get('name')
	password=request.args.get('password')
	position=request.args.get('position')
	pars=[name, password,position,None,None,None,None,None,None,None]
	user = query_db('SELECT * FROM user WHERE name = ?',[name], True)
	if user == None:
		query_db('INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?,?)',pars)
		db.commit()
		db.close()
		return '''finished register!
			 	<a href="http://127.0.0.1:5000/login">Back to Login</a>'''
	else: 
		return '''user has exists, try another name
		        <a href="http://127.0.0.1:5000/login#register">Back to Register</a>'''

if __name__ == '__main__':
	app.run(debug = True)




