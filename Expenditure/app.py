from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'Expenditure'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        status = request.form['status']
        amount = request.form['amount']
        con = mysql.connection.cursor()
        
        if status == 'Credited':
            credited = amount
            debited = 0
        else:
            credited = 0
            debited = amount
        
        sql = "INSERT INTO money_history (date, category, credited, debited) VALUES (%s, %s, %s, %s)"
        con.execute(sql, [date, category, credited, debited])
        mysql.connection.commit()
        con.close()
        return redirect('/')
    
    # Fetching history from the database
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM money_history")
    history = con.fetchall()
    con.close()
    
    # Calculate totals
    total_credited = sum(item['credited'] for item in history)
    total_debited = sum(item['debited'] for item in history)
    
    return render_template("home.html", history=history, total_credited=total_credited, total_debited=total_debited)

@app.route("/delete/<int:id>")
def delete(id):
    con = mysql.connection.cursor()
    con.execute("DELETE FROM money_history WHERE id = %s", [id])
    mysql.connection.commit()
    con.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
