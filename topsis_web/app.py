from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")

if os.path.exists(ROOT_ENV_PATH):
    load_dotenv(ROOT_ENV_PATH)
else:
    load_dotenv()

app = Flask(__name__)

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    try:
        file = request.files['file']
        raw_weights = request.form['weights']
        raw_impacts = request.form['impacts']
        email = request.form.get('email', '').strip()

        if email and not valid_email(email):
            return render_template(
                "index.html",
                message="Invalid email format"
            )

        weights = raw_weights.split(',')
        impacts = raw_impacts.split(',')

        if len(weights) != len(impacts):
            return render_template(
                "index.html",
                message="Weights and impacts count mismatch"
            )

        if not all(i in ['+','-'] for i in impacts):
            return render_template(
                "index.html",
                message="Impacts must be + or -"
            )

        # Read uploaded file
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file)

        elif file.filename.endswith((".xls", ".xlsx")):
            data = pd.read_excel(file)

        else:
            return render_template(
                "index.html",
                message="Only CSV/XLS/XLSX files allowed"
            )

        if data.shape[1] < 3:
            return render_template(
                "index.html",
                message="File must contain at least 3 columns"
            )

        criteria = data.iloc[:,1:].astype(float)

        weights_arr = np.array(weights, dtype=float)

        if len(weights_arr) != criteria.shape[1]:
            return render_template(
                "index.html",
                message="Weights count mismatch"
            )

        norm = criteria / np.sqrt((criteria**2).sum())

        weighted = norm * weights_arr

        ideal_best=[]
        ideal_worst=[]

        for i in range(len(impacts)):

            if impacts[i]=='+':
                ideal_best.append(weighted.iloc[:,i].max())
                ideal_worst.append(weighted.iloc[:,i].min())

            else:
                ideal_best.append(weighted.iloc[:,i].min())
                ideal_worst.append(weighted.iloc[:,i].max())

        ideal_best=np.array(ideal_best)
        ideal_worst=np.array(ideal_worst)

        dist_best=np.sqrt(
            ((weighted-ideal_best)**2).sum(axis=1)
        )

        dist_worst=np.sqrt(
            ((weighted-ideal_worst)**2).sum(axis=1)
        )

        score=dist_worst/(dist_best+dist_worst)

        data["Topsis Score"]=score

        data["Rank"]=(
            data["Topsis Score"]
            .rank(ascending=False)
            .astype(int)
        )

        csv_data=data.to_csv(index=False)

        html_table=data.to_html(
            index=False,
            border=1
        )

        html_table=html_table.replace(
            '<table border="1" class="dataframe">',
            '<table border="1" cellspacing="0" cellpadding="6" '
            'style="border-collapse:collapse;width:100%;text-align:center;">'
        )

        # Send only if email exists
        if email:
            send_email(
                email,
                csv_data,
                raw_weights,
                raw_impacts,
                html_table
            )

        return render_template(
            "index.html",
            table=data.to_html(
                classes="table",
                index=False
            ),
            message="TOPSIS completed successfully"
        )

    except Exception as e:
        print(e)

        return render_template(
            "index.html",
            message=f"Error: {str(e)}"
        )


def send_email(
    to_email,
    csv_data,
    weights,
    impacts,
    html_table
):

    EMAIL_USER=os.getenv("EMAIL_USER")
    EMAIL_PASS=os.getenv("EMAIL_PASS")

    if not EMAIL_USER or not EMAIL_PASS:
        print("Email credentials missing")
        return

    try:

        msg=EmailMessage()

        msg['Subject']="TOPSIS Results"

        msg['From']=EMAIL_USER

        msg['To']=to_email

        msg.set_content(
            f"""
TOPSIS Analysis Complete

Weights: {weights}

Impacts: {impacts}

Results attached.
"""
        )

        msg.add_alternative(f"""
        <html>
        <body>

        <h2>TOPSIS Results</h2>

        <p><b>Weights:</b> {weights}</p>

        <p><b>Impacts:</b> {impacts}</p>

        {html_table}

        </body>
        </html>
        """,subtype='html')

        msg.add_attachment(
            csv_data.encode(),
            maintype='text',
            subtype='csv',
            filename='topsis_result.csv'
        )

        with smtplib.SMTP_SSL(
            'smtp.gmail.com',
            465
        ) as smtp:

            smtp.login(
                EMAIL_USER,
                EMAIL_PASS
            )

            smtp.send_message(msg)

        print("Email sent")

    except Exception as e:

        print("Email Error:",e)


if __name__=="__main__":

    port=int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )