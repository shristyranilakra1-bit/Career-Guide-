from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        interest TEXT,
        career TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route('/')
def home():
    return redirect('/login')

# SIGNUP
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        # ADMIN LOGIN
        if u == "admin" and p == "admin123":
            session['admin'] = True
            return redirect('/admin')

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = u
            return redirect('/dashboard')

        return "Invalid Login"

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', user=session['user'])

# CAREER LOGIC
@app.route('/result', methods=['POST'])
def result():

    if 'user' not in session:
        return redirect('/login')

    interest = request.form['interest']

    # CODING
    if interest == "coding":
        career = "Frontend, Backend, Full Stack, Data Science, AI"
        roadmap = "Learn HTML, CSS, JS → Python → Projects → Internship"
        videos = [
            {"title":"Frontend Course","link":"https://www.youtube.com/watch?v=UB1O30fR-EE","thumb":"https://img.youtube.com/vi/UB1O30fR-EE/0.jpg"},
            {"title":"Python Full","link":"https://www.youtube.com/watch?v=rfscVS0vtbw","thumb":"https://img.youtube.com/vi/rfscVS0vtbw/0.jpg"}
        ]
        courses="Udemy, Coursera"
        internship="Internshala, LinkedIn"

    elif interest == "editing":
        career="Video Editor, YouTuber"
        roadmap="Learn CapCut → Premiere Pro → Practice"
        videos=[
            {"title":"Editing Course","link":"https://www.youtube.com/watch?v=1-sBvBB9n7A","thumb":"https://img.youtube.com/vi/1-sBvBB9n7A/0.jpg"}
        ]
        courses="Skillshare"
        internship="Freelancing"

    elif interest == "design":
        career="Graphic Designer, UI/UX"
        roadmap="Learn Canva, Figma → Portfolio"
        videos=[
            {"title":"Figma Course","link":"https://www.youtube.com/watch?v=FTFaQWZBqQ8","thumb":"https://img.youtube.com/vi/FTFaQWZBqQ8/0.jpg"}
        ]
        courses="Udemy"
        internship="Freelancing, startups"

    elif interest == "ai":
        career="AI Engineer, Data Scientist"
        roadmap="Python → ML → Projects"
        videos=[
            {"title":"AI Course","link":"https://www.youtube.com/watch?v=aircAruvnKk","thumb":"https://img.youtube.com/vi/aircAruvnKk/0.jpg"}
        ]
        courses="Coursera"
        internship="AI startups"

    elif interest == "government":
        career="NDA, SSC, Banking, Railways"
        roadmap="Maths + Reasoning + GK + Mock Tests"
        videos=[
            {"title":"NDA Prep","link":"https://www.youtube.com/watch?v=K4k0T6kQyE8","thumb":"https://img.youtube.com/vi/K4k0T6kQyE8/0.jpg"}
        ]
        courses="Unacademy, Testbook"
        internship="Not required"

    else:
        career="Explore more"
        roadmap="Try different skills"
        videos=[]
        courses="Online platforms"
        internship="General"

    # SAVE
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO history(username,interest,career) VALUES(?,?,?)",
                 (session['user'],interest,career))
    conn.commit()
    conn.close()

    return render_template('result.html',career=career,roadmap=roadmap,
                           videos=videos,courses=courses,internship=internship)

# ADMIN PANEL
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    users = conn.execute("SELECT * FROM users").fetchall()
    history = conn.execute("SELECT * FROM history").fetchall()
    conn.close()

    return render_template('admin.html',users=users,history=history)

# logout

app=Flask(__name__)
app.secret_key = "secret123"
@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/login')
if __name__=='_main_':
    app.run(debug=True)

# DATABASE
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        interest TEXT,
        career TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route('/')
def home():
    return redirect('/login')

# SIGNUP
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        # ADMIN LOGIN
        if u == "admin" and p == "admin123":
            session['admin'] = True
            return redirect('/admin')

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = u
            return redirect('/dashboard')

        return "Invalid Login"

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', user=session['user'])

# CAREER LOGIC
@app.route('/result', methods=['POST'])
def result():

    if 'user' not in session:
        return redirect('/login')

    interest = request.form['interest']

    # CODING
    if interest == "coding":
        career = "Frontend, Backend, Full Stack, Data Science, AI"
        roadmap = "Learn HTML, CSS, JS → Python → Projects → Internship"
        videos = [
            {"title":"Frontend Course","link":"https://www.youtube.com/watch?v=UB1O30fR-EE","thumb":"https://img.youtube.com/vi/UB1O30fR-EE/0.jpg"},
            {"title":"Python Full","link":"https://www.youtube.com/watch?v=rfscVS0vtbw","thumb":"https://img.youtube.com/vi/rfscVS0vtbw/0.jpg"}
        ]
        courses="Udemy, Coursera"
        internship="Internshala, LinkedIn"

    elif interest == "editing":
        career="Video Editor, YouTuber"
        roadmap="Learn CapCut → Premiere Pro → Practice"
        videos=[
            {"title":"Editing Course","link":"https://www.youtube.com/watch?v=1-sBvBB9n7A","thumb":"https://img.youtube.com/vi/1-sBvBB9n7A/0.jpg"}
        ]
        courses="Skillshare"
        internship="Freelancing"

    elif interest == "design":
        career="Graphic Designer, UI/UX"
        roadmap="Learn Canva, Figma → Portfolio"
        videos=[
            {"title":"Figma Course","link":"https://www.youtube.com/watch?v=FTFaQWZBqQ8","thumb":"https://img.youtube.com/vi/FTFaQWZBqQ8/0.jpg"}
        ]
        courses="Udemy"
        internship="Freelancing, startups"

    elif interest == "ai":
        career="AI Engineer, Data Scientist"
        roadmap="Python → ML → Projects"
        videos=[
            {"title":"AI Course","link":"https://www.youtube.com/watch?v=aircAruvnKk","thumb":"https://img.youtube.com/vi/aircAruvnKk/0.jpg"}
        ]
        courses="Coursera"
        internship="AI startups"

    elif interest == "government":
        career="NDA, SSC, Banking, Railways"
        roadmap="Maths + Reasoning + GK + Mock Tests"
        videos=[
            {"title":"NDA Prep","link":"https://www.youtube.com/watch?v=K4k0T6kQyE8","thumb":"https://img.youtube.com/vi/K4k0T6kQyE8/0.jpg"}
        ]
        courses="Unacademy, Testbook"
        internship="Not required"

    else:
        career="Explore more"
        roadmap="Try different skills"
        videos=[]
        courses="Online platforms"
        internship="General"

    # SAVE
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO history(username,interest,career) VALUES(?,?,?)",
                 (session['user'],interest,career))
    conn.commit()
    conn.close()

    return render_template('result.html',career=career,roadmap=roadmap,
                           videos=videos,courses=courses,internship=internship)

# ADMIN PANEL
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    users = conn.execute("SELECT * FROM users").fetchall()
    history = conn.execute("SELECT * FROM history").fetchall()
    conn.close()

    return render_template('admin.html',users=users,history=history)

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

app.run(debug=True)