from flask import Flask, render_template, request
import config as cfg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
msg = MIMEMultipart()
to_email = "EcoTourismRus@yandex.ru"
msg["From"] = cfg.LOGIN
ques1_za = 0
ques1_prot = 0
ques2_za = 0
ques2_prot = 0
ques3_za = 0
ques3_prot = 0
ques4_za = 0
ques4_prot = 0


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/opros", methods=['POST', 'GET'])
def opros():
    if request.method == 'GET':
        return render_template("opros.html")
    elif request.method == 'POST':
        param = {}
        param['question1'] = request.form['question1']
        param['question2'] = request.form['question2']
        param['question3'] = request.form['question3']
        param['comment3'] = request.form['comment3']
        param['question4'] = request.form['question4']
        msg["Subject"] = "Опрос"
        msg_body = f'Вопрос № 1: {param["question1"]}\n' \
                   f'Вопрос № 2: {param["question2"]}\n' \
                   f'Вопрос № 3: {param["question3"]}\n' \
                   f'Примеры: {param["comment3"]}\n' \
                   f'Вопрос № 4: {param["question4"]}'
        msg.attach(MIMEText(msg_body, "plain"))
        server = smtplib.SMTP_SSL("smtp.yandex.com: 465")
        server.login(cfg.LOGIN, cfg.PASSWORD)
        server.sendmail(cfg.LOGIN, to_email, msg.as_string())
        f = open("opros.csv", "a+", encoding="utf-8")
        file_writer = csv.writer(f, delimiter=",", lineterminator="\n")
        file_writer.writerow([param["question1"], param["question2"], param["question3"], param["question4"]])
        return render_template('succes.html', title="Успешно")


@app.route("/result")
def result():
    global people, ques1_za, ques1_prot, ques2_za, ques2_prot, ques3_za, ques3_prot, ques4_za, ques4_prot
    with open("opros.csv", "r", encoding="utf-8") as file:
        file_reader = csv.reader(file, delimiter=",")
        for row in file_reader:
            if row[0].lower() == 'да':
                ques1_za += 1
            if row[0].lower() == 'нет':
                ques1_prot += 1
            if row[1].lower() == 'да':
                ques2_za += 1
            if row[1].lower() == 'нет':
                ques2_prot += 1
            if row[2].lower() == 'да':
                ques3_za += 1
            if row[2].lower() == 'нет':
                ques3_prot += 1
            if row[3].lower() == 'да':
                ques4_za += 1
            if row[3].lower() == 'нет':
                ques4_prot += 1
        return render_template("result.html", people=people, value1=((ques1_za * 100) // people), value2=((ques1_prot * 100) // people),
                               value3=((ques2_za * 100) // people), value4=((ques2_prot * 100) // people),
                               value5=((ques3_za * 100) // people), value6=((ques3_prot * 100) // people),
                               value7=((ques4_za * 100) // people), value8=((ques4_prot * 100) // people))


if __name__ == '__main__':
    file1 = open("opros.csv", "r", encoding="utf-8")
    people = sum(1 for i in file1)
    app.run()