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

def send_email(students):
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_LOGIN = os.environ.get('EMAIL_LOGIN')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    presenting_student = choose_random_student(students)

    for student in students:

        message = f"""\
Dear {students[student]['first_name']}, Your score for the book assignment is broken down below by question number.

{students[student]['problem1_score']}%: {students[student]['problem1_comments']}
{students[student]['problem2_score']}%: {students[student]['problem2_comments']}
{students[student]['problem3_score']}%: {students[student]['problem3_comments']}

"""
        if presenting_student == student:
            message += "You've been randomly chosen to present a summary of the book in the next class. Looking forward to it!"

        server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
        server.login(EMAIL_LOGIN, EMAIL_PASS)
        server.sendmail(
            'lecture@example.com',
            student,
            message
            )
        server.quit()
    
def choose_random_student(results):
    return random.choice(list(results.keys()))

if __name__ == '__main__':
    student_list = readfile("./exam.csv")
    send_email(student_list)