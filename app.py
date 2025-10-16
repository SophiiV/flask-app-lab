from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('resume.html', title="Моє резюме")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Отримано повідомлення від {name} ({email}): {message}")
    return render_template('contacts.html', title="Контакти")

if __name__ == '__main__':
    app.run(debug=True)
