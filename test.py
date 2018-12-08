from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

app = Flask(__name__)

app.secret_key = 'key'

con = pymysql.connect(host='localhost',user='root',password='root',db='Project',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	email = request.form["email"]
	password = request.form["password"]

	cursor = con.cursor()

	query = 'SELECT * FROM Person WHERE email = %s AND password = SHA2(%s,256)'
	cursor.execute(query, (email,password))

	data = cursor.fetchone()

	cursor.close()
	if(data):
		session['email'] = email
		return redirect(url_for('home'))
	else:
		error = 'Invalid login or email'
		return render_template('login.html', error=error)

@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	email = request.form["email"]
	password = request.form["password"]
	fname = request.form['fname']
	lname = request.form['lname']

	cursor = con.cursor()
	query = 'SELECT * FROM Person WHERE email = %s'
	cursor.execute(query, (email))

	data = cursor.fetchone()

	if(data):
		error = "email taken"
		cursor.close()
		return render_template('register.html', error = error)
	else:
		ins = "INSERT INTO Person (email, password, fname, lname)  VALUES(%s,SHA2(%s,256),%s,%s)"
		cursor.execute(ins,(email,password, fname, lname))
		con.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/logout')
def logout():
	session.pop('email')
	return redirect('/')

# @app.route('/select_blogger')
# def select_blogger():
#     #check that user is logged in
#     #email = session['email']
#     #should throw exception if email not found
    
#     cursor = con.cursor();
#     query = 'SELECT DISTINCT email FROM blog'
#     cursor.execute(query)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('select_blogger.html', user_list=data)

@app.route('/show_posts', methods=["GET", "POST"])
def show_posts():
    #email = request.args['email']
    post = request.form['post']
    session['item_id'] = post
    email = session['email']


    cursor = con.cursor();
    query = 'SELECT * FROM ContentItem WHERE item_id = %s'
    print "TEST RUN"
    cursor.execute(query,(post))
    data = cursor.fetchall()

    tagged = 'SELECT item_id, fname, lname FROM Tag JOIN Person ON Person.email = Tag.email_tagged WHERE item_id = %s AND status = TRUE'
    cursor.execute(tagged,(post))
    data2 = cursor.fetchall()

    query3 = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem WHERE email_post = %s ORDER BY post_time DESC'
    print "YES HELLO THIS RUNS GOOD"
    cursor.execute(query3,(email))
    priv = cursor.fetchall()
    print "THJIS IS THE DATA: ",priv








    rated = 'SELECT * FROM Rate WHERE item_id = %s'
    cursor.execute(rated,(post))
    rate = cursor.fetchall()
    print "THIS: ",rate



    



    cursor.close()
    return render_template('show_posts.html', post =data, tagged = data2, rates = rate, priv=priv )#, email=poster, posts=data)

# @app.route('/rate', methods=["GET", "POST"])
# def rate():
# 	email = session['email']
# 	post = session['item_id']
# 	rate = request.form['emoji']

# 	cursor= con.connect();
# 	query = 'SELECT * FROM Rate WHERE email = %s and item_id = %s'
# 	cursor.execute(query,(email,post))
# 	print "HELOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
# 	data = cursor.fetchall()
# 	error = None
# 	if(data):
# 		error = "Post already rated"
# 	else:
# 		if(emoji=="1"):
# 			print "WE ARE IN 1 NOW"
# 			add = 'INSERT INTO Rate VALUES(%s,%s,NOW(),":)"'
# 		if(emoji == "2"):
# 			add = 'INSERT INTO Rate VALUES(%s,%s,NOW(),":("'
# 		if(emoji == "3"):
# 			add = 'INSERT INTO Rate VALUES(%s,%s,NOW(),":|"'
# 		if(emoji == "4"):
# 			add = 'INSERT INTO Rate VALUES(%s,%s,NOW(),"<3"'
# 		print "THIS CRASHESSSSSSSSSS"
# 		cursor.execute(add,(email,post))
# 		con.commit()
# 		cursor.close()
# 	return redirect(url_for('show_posts'))





@app.route('/show_shared', methods=["GET", "POST"])
def show_shared():
    #email = request.args['email']
    post = request.form['post']
    session['item_id'] = post
    email = session['email']


    cursor = con.cursor();

    belongs = 'SELECT owner_email, fg_name FROM Belong WHERE email = %s'
    cursor.execute(belongs,(email))
    data3 = cursor.fetchall()

    query = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem WHERE is_pub = 1 ORDER BY post_time DESC'
    cursor.execute(query)
 



    



    cursor.close()
    return render_template('show_posts.html', post =data, tagged = data2)#, email=poster, posts=data)




@app.route('/home', methods=['GET', 'POST'])
def home():
	email = session['email']
	cursor = con.cursor();


	query = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem WHERE is_pub = 1 ORDER BY post_time DESC'
	cursor.execute(query)
	#print query
	data = cursor.fetchall()


	query2 = 'SELECT item_id, email_tagger FROM Tag WHERE email_tagged = %s AND status = FALSE ORDER BY tagtime DESC'
	cursor.execute(query2, (email))
	data2 = cursor.fetchall()


	# belongs = 'SELECT owner_email, fg_name FROM Belong WHERE email = %s'
	# cursor.execute(belongs,(email))
	# data3 = cursor.fetchall()

	test = 'SELECT item_id, email_post, post_time, file_path, item_name FROM Share NATURAL JOIN Belong NATURAL JOIN ContentItem WHERE email =%s AND app = TRUE'
	cursor.execute(test,(email))
	shar = cursor.fetchall()



	query3 = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem WHERE email_post = %s AND is_pub = FALSE ORDER BY post_time DESC'
	cursor.execute(query3,(email))
	priv = cursor.fetchall()

	query4 = 'SELECT owner_email, fg_name FROM Belong WHERE email = %s AND app = 0'
	cursor.execute(query4,(email))
	app = cursor.fetchall()





	# if(data3):
	# 	query3 = 'SELECT item_id FROM Share WHERE owner_email = %s AND fg_name = %s'
	# 	cursor.execute(query3,(owner,fgname))
	# 	data4 = cursor.fetchall()
	# 	query4 = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem WHERE item_id = %s ORDER BY post_time DESC'
	# 	share = cursor.fetchall()

	cursor.close()
	return render_template('home.html', email = email, data=data, tags=data2, share=shar, priv=priv, invs =app)
	
	#return render_template('home.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
	email = session['email']
	cursor = con.cursor()
	post = request.form['ContentItem']
	pub = request.form['is_pub']
	query = 'INSERT INTO ContentItem (email_post, item_name, is_pub ) VALUES(%s,%s,%s)'
	print query
	cursor.execute(query,(email, post,pub))
	con.commit()
	cursor.close()
	return redirect(url_for('home'))



@app.route('/tag', methods=['GET','POST'])
def tag():
	tagger = session['email']
	tagged = request.form['tagged']
	post = session['item_id']

	cursor = con.cursor()

	query = 'SELECT * FROM Tag WHERE email_tagged = %s AND item_id = %s'
	cursor.execute(query,(tagged,post))
	data = cursor.fetchone()

	error= None
	if(data):
		error = "This person is already tagged"
	else:
		if (tagger == tagged):
			ins = 'INSERT INTO Tag VALUES(%s,%s,%s,TRUE,NOW())'
		else:
			ins = 'INSERT INTO Tag VALUES(%s,%s,%s,FALSE,NOW())'
		cursor.execute(ins,(tagged,tagger,post))
		con.commit()
		cursor.close()
	return redirect(url_for('home'))


@app.route('/tag_app', methods=['GET','POST'])
def tag_app():
	email = session['email']
	tag = request.form['tag']
	item = request.form['item']
	cursor = con.cursor();

	if (tag == '1'):
		up = 'UPDATE Tag SET status = TRUE WHERE email_tagged = %s AND item_id = %s'
		cursor.execute(up,(email,item))
	else:
		up = 'DELETE FROM Tag WHERE email_tagged = %s AND item_id = %s AND status = FALSE'
		cursor.execute(up,(email,item))
	con.commit()
	cursor.close()
	return redirect(url_for('home'))


@app.route('/share', methods=['GET','POST'])
def share():
	email = session['email']
	post = session['item_id']
	group = request.form['FGTag']
	owner = request.form['FGOwn']

	cursor = con.cursor()

	# query2 = 'SELECT owner_email FROM Friendgroup WHERE fg_name = %s'
	# cursor.execute(query2,(group))
	# owner = cursor.fetchall()

	query = 'SELECT * FROM Share WHERE owner_email = %s AND fg_name = %s AND item_id =%s'
	cursor.execute(query,(owner,group,post))
	data = cursor.fetchall()

	# query3 = 'SELECT * FROM Belong WHERE owner_email = %s AND fg_name = %s AND email = %s'
	# cursor.execute(query3,(owner,group,email))
	# belongs = cursor.fetchall()


	error = None
	if(data):
		error = "Already shared with this group"
	# elif(belongs == 0):
	# 	error = "You don't belong to this group"

	else:
		print "WE ARE HERE"
		query = 'INSERT INTO Share VALUES (%s,%s,%s)'
		test = cursor.execute(query,(owner,group,post))
		print test
		con.commit()
		cursor.close()
	print "GOING TO EXIT NOW"
	return redirect(url_for('home'))

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/login')
def login():
	#email = session['email']
	cursor = con.cursor();
	query = 'SELECT item_id, email_post, post_time, file_path, item_name FROM ContentItem WHERE is_pub = 1 ORDER BY post_time DESC'
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	return render_template('login.html', data=data)

@app.route('/register')
def register():
	return render_template('register.html')
@app.route('/mem_inv', methods=['GET','POST'])
def mem_inv():
	email = session['email']
	group = request.form['FG']
	fname = request.form['fname']
	lname  = request.form['lname']
	


	cursor = con.cursor();
	query = 'SELECT * FROM Belong NATURAL JOIN Person WHERE owner_email = %s AND fg_name = %s AND fname = %s AND lname = %s'
	cursor.execute(query, (email, group, fname, lname))
	data = cursor.fetchall()


	query2 = 'SELECT * FROM Friendgroup WHERE owner_email = %s AND fg_name = %s'
	cursor.execute(query2, (email, group))
	data2 = cursor.fetchall()
	

	query3 = 'SELECT * FROM Person WHERE fname = %s AND lname = %s'
	cursor.execute(query3, (fname, lname))
	data3 = cursor.fetchall()
	

	lst = []
	print "START----------------------------------------------"
	for invited in data:
		lst.append(invited["email"])
	if not (data2):
		print "YEEEEEEEEEEEEEEEEEEEEEEET"
		print  "This group does not exist"
		#not sure why errors dont work leave for later

	else:
		for x in data3:
			if len(data) == 0:
				print "MIDDLE ---------------------------------------"
				ins = 'INSERT INTO Belong VALUES(%s, %s, %s, FALSE)'
				print x["email"]
				cursor.execute(ins, (x["email"], email, group))
				con.commit()
			else:

				if x['email'] not in lst:
					
					ins = 'INSERT INTO Belong VALUES(%s, %s, %s, FALSE)'
					cursor.execute(ins, (x["email"], email, group))
					con.commit()
				
		cursor.close()
	print "END -------------------------------------------------"	
	return redirect(url_for('home'))




@app.route('/mem_app', methods=['GET','POST'])
def mem_app():
	email = session['email']
	appr = request.form['app']

	cursor = con.cursor();

	if(appr == "1"):
		add = 'UPDATE Belong SET app = TRUE WHERE email = %s'
		cursor.execute(add,(email))
	else:
		add = "DELETE FROM Belong WHERE email = %s AND app = FALSE"
		cursor.execute(add,(email))
	con.commit()
	cursor.close()
	return redirect(url_for("home"))

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
	email = session['email']
	
	desc = request.form['description']
	name = request.form['name']
	cursor = con.cursor();

	check = 'SELECT * FROM Friendgroup WHERE owner_email = %s AND fg_name = %s'
	cursor.execute(check,(email,name))
	data = cursor.fetchall()
	error = None

	if(data):
		error = "Group already created"
		###return render_template('home.html', error=error, email=email)
## FIGURE OUT WHY THE ERRORS DONT SHOW UP
	else:
		query = 'INSERT INTO Friendgroup (owner_email, fg_name, description) VALUES(%s, %s, %s)'
		cursor.execute(query, (email,name,desc))
		query2 = 'INSERT INTO Belong (email,owner_email,fg_name, app) VALUES(%s,%s,%s, TRUE)'
		cursor.execute(query2,(email,email,name))
		con.commit()
		cursor.close()

	
	
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)