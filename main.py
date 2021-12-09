#!/usr/bin/env python
import csv
import smtplib 
import random
import os 


def readfile(file):
    with open(file, 'r') as f:
        results = {}
        for row in csv.reader(f):
            results[row[0]] = {
                'first_name': row[1],
                'last_name':  row[2],
                'problem1_score': row[3],
                'problem1_comments': row[4],
                'problem2_score': row[5],
                'problem2_comments': row[6],
                'problem3_score': row[7],
                'problem3_comments': row[8],
            }
            print(row)

        return results

def send_email():
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_LOGIN = os.environ.get('EMAIL_LOGIN')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
    server.login(EMAIL_LOGIN, EMAIL_PASS)
    server.sendmail(
        "test@test.co.uk", 
        "test.send@example.com", 
        "this message is from python")
    server.quit()
    
def choose_random_student(results):
    return random.choice(list(results.keys()))

if __name__ == '__main__':
    readfile("./exam.csv")
    send_email()