import smtplib

file = "students.txt"
students = {}

with open(file, "r") as f:
    for line in f:
        data = line.strip().split(",")
        email = data[0]
        name = data[1]
        surname = data[2]
        points = int(data[3])
        if len(data) > 4:
            grade = int(data[4])
            status = data[5]
        else:
            grade = None
            status = None
        students[email] = {"name": name, "surname": surname, "points": points, "grade": grade, "status": status}

for email, student in students.items():
    if student["status"] != "GRADED" and student["status"] != "MAILED":
        if student["points"] >= 90:
            student["grade"] = 5
        elif student["points"] >= 75:
            student["grade"] = 4
        elif student["points"] >= 60:
            student["grade"] = 3
        else:
            student["grade"] = 2
        student["status"] = "GRADED"


def add_student(email, name, surname, points):
    if email in students:
        print("Student with this email already exists")
    else:
        students[email] = {"name": name, "surname": surname, "points": points, "grade": None,
                           "status": None}
        print("Student added successfully")


def remove_student(email):
    if email in students:
        del students[email]
        print("Student removed successfully")
    else:
        print("Student with this email does not exist")


def send_email(email, grade):
    if email in students and students[email]["status"] != "MAILED":
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = "pjatk@gmail.com"
        receiver_email = email
        password = "pjatk123"
        message = f"Subject: Your grade\n\nDear {students[email]['name']},\n\nYour grade for the Python Programming course has been calculated. You received a {grade}.\n\nBest regards,\nYour teacher"
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        students[email]["status"] = "MAILED"
        print("Email sent successfully")
    elif email in students:
        print("Email already sent to this student")
    else:
        print("Student with this email does not exist")


with open(file, "w") as f:
    for email, student in students.items():
        data = [email, student["name"], student["surname"], str(student["points"])]
        if student["grade"] != None:
            data.append(str(student["grade"]))
            data.append(student["status"])
        f.write(",".join(data) + "\n")
