import xlrd
import pymysql
import glob, os

#THIS GOES AT THE BEGINNING OF THE FILE
#These are the arrays that may need their order changed, but I believe they have been fixed
sat = [[52,0],[44,1],[20,2],[38,3]]
psat = [[47,0],[44,1],[17,2],[31,3]]
act= [[40,2],[75,0],[60,1],[40,3]]
test= []
def sqlDate(day):
    order = day.replace("/","-").split("-")
    day = order[2]+"-"+order[0]+"-"+order[1]
    return day
#This function take a file and uploads the student data to the database
def upload(file):
    f = open(file, "r")
    answers = f.readlines()
    info = []
    #Get student information
    for x in range(7):
        info.append(answers[0])
        del answers[0]
    #Check if Student is already in data base, strip off new lines, and format date correctly
    print("Name: \n "+info[0]+" "+info[1])
    cursor.execute("SELECT idStudent FROM Student WHERE FirstName=%s AND LastName=%s AND BirthDate=%s;",(info[0].strip(),info[1].strip(),sqlDate(info[2].strip())))
    response = cursor.fetchall()
    if len(response)==0:
        cursor.execute("INSERT INTO Student (FirstName, LastName, BirthDate) VALUES (%s, %s, %s);",(info[0].strip(), info[1].strip(), sqlDate(info[2].strip())))
        cursor.execute("SELECT idStudent FROM Student WHERE FirstName=%s AND LastName=%s AND BirthDate=%s;",(info[0].strip(),info[1].strip(),sqlDate(info[2].strip())))
        response = cursor.fetchall()
    id = response[0][0]
    #print(id)
    #retrieve survey questions
    survey = ""
    sub = ""
    for x in range(40):
        sub = answers[0].strip().split(" ")[1]+" "
        #print(sub)
        if(sub == "DNE "):
            survey = survey+"0 "
        else:    
            survey = survey+sub
        del answers[0]
    #print(survey)
    #check if test has been inserted
    cursor.execute("SELECT Student_idStudent FROM Student_has_taken_Test WHERE Student_idStudent=%s AND Test_idTest=%s AND DateTaken=%s;", (id, info[6].strip(), sqlDate(info[3].strip())))
    response = cursor.fetchall()
    if len(response)==0:
        ans = []
        #Insert the new test into the database.
        cursor.execute("INSERT INTO Student_has_taken_Test (Student_idStudent, Test_idTest, DateTaken, Survey) VALUES (%s, %s, %s, %s);",(id, info[6].strip(), sqlDate(info[3].strip()), survey))
        option = info[6].strip()[:-2]
        #print(option)
        if(option=="S"):
            test=sat
        if(option=="P"):
            test=psat
        if(option=="A"):
            test=act
        #insert student answers into the database.
        for x in range(len(test)):
            del answers[0]
            #print(test[x])
            for y in range(test[x][0]):
                #print(str(y)+" "+answers[0].strip().split(" ")[1])
                ans.append((id, answers[0].strip().split(" ")[1], y, test[x][1], info[6].strip()))
                del answers[0]
        cursor.executemany("INSERT INTO Student_Answer (Student_idStudent, AnswerChoice, Question_idQuestion, Question_Section_idSection, Question_Section_Test_idTest) VALUES (%s, %s, %s, %s, %s);",ans)        
    else:
        print("Test already in database.")

#THIS GOES AFTER THE TEST HAS BEEN WRITTEN TO A TXT FILE
#make the connection to the database
db = pymysql.connect("45.13.252.1","u636238502_root","Schol01","u636238502_Blueprint")
db.autocommit(True)
#CHANGE THIS LINE TO YOUR USED DIRECTORY, OR YOU CAN REMOVE IT IF ATTACHING TO FILE
os.chdir("./tests")
cursor = db.cursor()

#CHANGE THIS FOR LOOP TO A SINGLE CALL TO upload(file)
#SET file TO THE FILE NAME OF THE RECENTLY WRITTEN FILE
# read through every txt file in the directory and if it is a new test upload it to the database.
for file in glob.glob("*.txt"):
    upload(file)


#THIS GOES AT THE END OF THE FILE
#commit changes to database close connection
cursor.close()
db.commit()
db.close()

