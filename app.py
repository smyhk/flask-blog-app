from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = "qwertyuiop"

# MySQL configurations

app.config['MYSQL_DATABASE_USER'] = 'flaskapp'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ZzXxVvBb%^565'
app.config['MYSQL_DATABASE_DB'] = 'FlaskBlogApp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# basic route
@app.route("/")
def main():
    return render_template("index.html")


@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/userHome')
def userHome():
    return render_template('userHome.html')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/showAddBlog')
def showAddBlog():
    return render_template('addBlog.html')


@app.route('/addBlog', methods=['POST'])
def addBlog():
    if session.get("user"):
        try:
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addBlog', (_title, _description, _user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html', error='An error occurred!')
        except Exception as e:
            return render_template('error.html', error=str(e))
        finally:
            cursor.close()
            conn.close()


@app.route('/getBlog')
def getBlog():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetBlogByUser', (_user,))
            blogs = cursor.fetchall()

            blogs_dict = []
            for blog in blogs:
                blog_dict = {
                        'Id': blog[0],
                        'Title': blog[1],
                        'Description': blog[2],
                        'Date': blog[4]}
                blogs_dict.append(blog_dict)

            return json.dumps(blogs_dict)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=5000)
