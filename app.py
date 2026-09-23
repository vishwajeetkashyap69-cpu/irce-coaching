from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os, secrets
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "irce-change-this-secret")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "irce.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "irce123")

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.execute("""CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_no TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL, father TEXT, mother TEXT, mobile TEXT NOT NULL,
        whatsapp TEXT, dob TEXT, gender TEXT, class_name TEXT, school TEXT,
        village TEXT, district TEXT, address TEXT, course TEXT,
        photo TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'New'
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS updates(
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
        description TEXT, date TEXT, link TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit(); con.close()

@app.route("/")
def home():
    con=db()
    updates=con.execute("SELECT * FROM updates ORDER BY id DESC LIMIT 6").fetchall()
    con.close()
    return render_template("index.html", updates=updates)

@app.route("/admission", methods=["GET","POST"])
def admission():
    if request.method=="POST":
        name=request.form.get("name","").strip()
        mobile=request.form.get("mobile","").strip()
        if not name or not mobile:
            flash("नाम और मोबाइल नंबर जरूरी है।","error")
            return redirect(url_for("admission"))
        appno="IRCE-"+secrets.token_hex(4).upper()
        photo=request.files.get("photo")
        photo_name=""
        if photo and photo.filename:
            ext=os.path.splitext(photo.filename)[1].lower()
            if ext in [".jpg",".jpeg",".png",".webp"]:
                photo_name=appno+ext
                photo.save(os.path.join(UPLOAD_DIR, secure_filename(photo_name)))
        con=db()
        con.execute("""INSERT INTO applications
        (application_no,name,father,mother,mobile,whatsapp,dob,gender,class_name,school,village,district,address,course,photo)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            appno,name,request.form.get("father"),request.form.get("mother"),mobile,
            request.form.get("whatsapp"),request.form.get("dob"),request.form.get("gender"),
            request.form.get("class_name"),request.form.get("school"),request.form.get("village"),
            request.form.get("district"),request.form.get("address"),request.form.get("course"),photo_name))
        con.commit(); con.close()
        return render_template("success.html", application_no=appno, name=name)
    return render_template("admission.html")

@app.route("/admin/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")==ADMIN_USER and request.form.get("password")==ADMIN_PASSWORD:
            session["admin"]=True
            return redirect(url_for("admin"))
        flash("गलत username या password","error")
    return render_template("login.html")

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    if not session.get("admin"): return redirect(url_for("login"))
    con=db()
    apps=con.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
    updates=con.execute("SELECT * FROM updates ORDER BY id DESC").fetchall()
    con.close()
    return render_template("admin.html", applications=apps, updates=updates)

@app.post("/admin/application/<int:app_id>/status")
def status(app_id):
    if not session.get("admin"): return redirect(url_for("login"))
    con=db(); con.execute("UPDATE applications SET status=? WHERE id=?",(request.form.get("status"),app_id))
    con.commit(); con.close()
    return redirect(url_for("admin"))

@app.post("/admin/update/add")
def add_update():
    if not session.get("admin"): return redirect(url_for("login"))
    con=db(); con.execute("INSERT INTO updates(title,description,date,link) VALUES(?,?,?,?)",
        (request.form.get("title"),request.form.get("description"),request.form.get("date"),request.form.get("link")))
    con.commit(); con.close(); return redirect(url_for("admin"))

@app.post("/admin/update/<int:update_id>/delete")
def delete_update(update_id):
    if not session.get("admin"): return redirect(url_for("login"))
    con=db(); con.execute("DELETE FROM updates WHERE id=?",(update_id,)); con.commit(); con.close()
    return redirect(url_for("admin"))

@app.get("/application/<application_no>")
def application_status(application_no):
    con=db(); row=con.execute("SELECT * FROM applications WHERE application_no=?",(application_no,)).fetchone()
    con.close()
    return render_template("status.html", row=row)

if __name__=="__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
