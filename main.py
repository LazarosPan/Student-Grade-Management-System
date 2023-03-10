# persistant data with sqlite3
# dependencies : files <db_file>.sqlite.sql with definition of database 
#		actresses.txt and actors.txt downloaded from wikipedia
#               entry : Greek film actors and actresses
import os
import os.path
import sqlite3 as lite
import random
import re

VERBOSE = False # set to True to print SQL command information
#################################################################################################
class Student:
    '''
    Student class of one course with 4 assignments, 2 exams
    '''
    students = []

    @staticmethod
    def order_students_list():
        '''Sort the Student.students list by alphabetical order of student surname'''
        Student.students = sorted(Student.students, key=lambda x: x.name.split()[1])
        # for name in Student.students:
        #     sorted(Student.students, key=lambda x: x.name.split()[1])
        pass

    @staticmethod
    def find_am(am):
        '''search for a student by his/her registration number, returns the object Student or False'''
        for s in Student.students:
            if am == s.am: return s
        return False

    @staticmethod
    def success_rate():
        '''calculates the number of students who passed and those who failed, prints number and percentage'''
        perasan=0
        kophkan=0
        for s in Student.students:
            if s.final_grade() >= 5 : perasan += 1
            else: kophkan+=1
        percentage = 100 * perasan / (perasan+kophkan)
        print('Passed: {}      Failed: {}      Percentage: {}%\n'.format(perasan,kophkan,percentage))
        pass

    def __init__(self, am, name):
        self.am = str(am)
        self.name = name  # student's full name - last name the last word
        self.grades = [-1, -1, -1, -1]  # assignment grades
        self.exam1 = -1  # final examination
        self.exam2 = -1  # re-examination
        Student.students.append(self)

    def add_exam1(self, mark):
        try:
            self.exam1 = float(mark)
        except:
            return False

    def add_exam2(self, mark):
        try:
            self.exam2 = float(mark)
        except:
            return False

    def final_grade(self):
        '''Calculation of the final grade'''
        score = 0
        for g in self.grades:
            if g >= 0: score += g
        if score < 20: return -1
        exam = max(self.exam1, self.exam2)
        if exam >= 5:
            final = round((0.7 * exam + 0.3 * score / 4) * 2) / 2
            return final
        elif exam >= 0:
            return exam
        else:
            return -1

    def final_score(self):
        ''' returns student and final grade '''
        return '{} {:30s}\t{:4.1f}'.format(self.am, self.name, self.final_grade())

    def final_exams_check(self):
        '''  checking whether the student is allowed to participate in the final examination '''
        # only for students who meet the criterion
        # self.grades must have 3 grades >=0 and sum >=20
        score = 0
        ergasies=0
        for g in self.grades:
            if g >= 0:
                score += g
                ergasies += 1
        if ergasies >= 3 and score >= 20 : return True
        else: return False

    def print_scores(self):
        'returns a detailed record of student data'
        return '{} {:30s}[\t{:.1f} \t{:.1f} \t{:.1f} \t{:.1f}]\t\t\t[{:.1f}. \t{:.1f}]'.format(
            self.am, self.name, *self.grades, self.exam1, self.exam2)

    def __str__(self):
        'student details and final grade for final class grade'
        return '{} {} {:.2f}'.format(self.am, self.name, self.final_grade())


class Create():
    '''
    Tool for creating records in the Student class
    '''

    def __init__(self, default_size=0):
        ''' define size and create new cohort of students if <enter> return False'''
        if not default_size:
            self.class_size = self.define_size()
        else:
            self.class_size = default_size
        # Assumption that the distributions of scores for assignments and final exam are normal
        # with mean values as below (used in the _random_score method)
        self.mean_work = 8
        self.mean_final = 6
        self.mean_resit = 5.5

    def define_size(self):
        while True:  # define size of new cohort
            try:
                class_size = input('Class size (1-500 students):')
                if class_size == '': return False
                class_size = int(class_size)
                if class_size >= 1 and class_size <= 500: break
            except:
                print('Please give the number of students')
                return 0
        return class_size

    def _create_names(self):
        class_size = self.class_size
        act_names_files = ('actresses.txt', 'actors.txt')
        names = []
        for f in act_names_files:
            with open(f, 'r', encoding='utf-8') as fin:
                for line in fin:
                    if len(line) > 2:
                        name = re.sub(r'\(.*\)', '', line.strip())
                        if len(name.split()) > 1:
                            names.append(name)
        # Select class_size names from names list
        if class_size < len(names):
            student_names = random.sample(names, class_size)
        else:
            student_names = names
        return student_names

    def _random_score(self, mean=5):
        # returns a number from 0 to 10 with an accuracy of 0.5
        while True:
            score = round(
                random.gauss(mean, 3.0) * 2) / 2  # use normal distribution with mean and standard deviation 3
            if score <= 10.0 and score >= 0.0: return score

    def _remove_students(self):
        for s in Student.students:  # remove instances
            del s
        Student.students = []  # clear class objects list

    def create_new_cohort(self):
        self._remove_students()
        student_names = self._create_names()
        for i in range(self.class_size):  # create student crowd class_size
            grades = []
            # we assume 80% participation in the assignments
            for j in range(4):
                if random.randint(1, 100) > 20:  # 20% do not submit assignments
                    grade = self._random_score(self.mean_work)  # average score value self.mean_work
                    grades.append(grade)
                else:
                    grades.append(-1)
            am = str(i + 100)  # assume that the register numbers are integers starting from 100
            s = Student(am, student_names[i])  # create a new student
            s.grades = grades  # grades of assignments
            if s.final_exams_check():  # check if the student is allowed to take exams
                s.add_exam1(self._random_score(self.mean_final))  # average final exam score self.mean_final
                if s.exam1 < 5:  # if he/she failed the final exam take the re-exam
                    s.add_exam2(self._random_score(self.mean_resit))  # average value of re-exam self.mean_resit
        Student.order_students_list()
        print('...successfully created new class of {} students\n'.format(self.class_size))
        return True

########################################################################################################
class Main():
    def __init__(self):
        self.db_file = 'students'
        self.exam_names = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Final Exam', 'Repeat Exam']
        self.db = self.db_file + '.sqlite' # the name of the database sqlite3
        # If the database file does not exist call self.create_database
        if not os.path.isfile(self.db):
            self.create_database()
        # Read the database that already exists
        if os.path.isfile(self.db):
            self.read_sql_database()
        # main MENU
        while True:
            print('\nAdvanced Python Programming [ Peer Review Assignment 1 ]')
            print('(There are {} students in the database)'.format(len(Student.students)))
            print('\t\t1. Create new class' +
                  '\n\t\t\t2. Detailed student grades' +
                  '\n\t\t\t3. Final student score\n' +
                  '\t\t\t4. Average score & pass rate per exam\n' +
                  '\t\t\t<enter> Exit')
            select = ' '
            while select not in '1 2 3 4'.split():
                select = input('>>> SELECT: ')
                if select == '': break
            else:
                if select == '1': # 1. create a new class
                    self.question_1()
                elif select == '2': # 2. detailed rating
                    self.question_2()
                elif select == '3': # 3. final score
                    self.question_3()
                elif select == '4': # pass rate in the exam
                    self.question_4()
            if select == '': break


    def create_database(self):
        # read from the sql file the commands to create the database
        if os.path.isfile(self.db + '.sql'):  # this is the export of the sqlite3 DB Browser
            with open(self.db + '.sql') as f:
                sql = f.read()
        # add the exam data to the exam table
        try:
            conn = lite.connect(self.db)
            with conn:
                curs = conn.cursor()
                curs.executescript(sql)
                sql3 = 'INSERT INTO exam VALUES (?,?);'
                for id,names in enumerate(self.exam_names):
                    curs.execute(sql3,(id,names))
                return True
        except lite.Error as Error2 : print(Error2)


    def read_sql_database(self):
        try:
            con = lite.connect(self.db)
            with con:
                cur = con.cursor()
                # read student and grade data from the database
                sql = 'SELECT * FROM student, exam_score WHERE student.id = exam_score.student_id'
                # this sql returns (id, name, surname id, exam, score)
                cur.execute(sql)
                for row in cur.fetchall():
                    if VERBOSE: print(row)
                    st = Student.find_am(str(row[0]))  # check if the student already exists
                    if not st:
                        name = row[1] + ' ' + row[2]
                        st = Student(str(row[0]), name) # create a new Student object
                    ind = row[4]
                    if ind == '4':
                        st.exam1 = float(row[5])
                    elif ind == '5':
                        st.exam2 = float(row[5])
                    elif ind in '0 1 2 3'.split():
                        st.grades[int(ind)] = float(row[5])
                    else:
                        print('error')
        except:
            print('error in reading students from database')
            return False

    def save_to_sql_database(self):
        '''save the students of the Student class to the students.sqlite database'''
        sql1 = 'INSERT INTO student(id,name,surname) VALUES (?,?,?);'
        sql2 = 'INSERT INTO exam_score(student_id, exam_id, score) VALUES (?,?,?);'
        try:
            con = lite.connect(self.db)
            with con:
                cur = con.cursor()
                # delete the records of the student and exam_score tables
                for t in ['student', 'exam_score']:
                    sql = 'DELETE from {};'.format(t)
                    cur.execute(sql)
                    cur.execute('COMMIT;')
                # insert new students, objects of the class Student
                for s in Student.students:
                    name = ' '.join(s.name.split()[:1])
                    surname = s.name.split()[-1]
                    if VERBOSE: print(s.am, name, surname)
                    cur.execute(sql1, (s.am, name, surname))
                    cur.execute('COMMIT;')
                    grades = s.grades + [s.exam1, s.exam2]
                    for i,g in enumerate(grades):
                        if g > -1:
                            if VERBOSE: print(s.am, self.exam_names[i], g)
                            cur.execute(sql2, (s.am, i, g))
                            cur.execute('COMMIT;')
            return True
        except:
            print('error importing students into the database ')
            return False

    def question_1(self):
        c = Create()
        if c.class_size:
            c.create_new_cohort()
            self.save_to_sql_database()

    def question_2(self):
        print('\nTotal list of scores')
        Student.order_students_list()
        for s in Student.students:
           print(s.print_scores())
        print(Student.success_rate())

    def question_3(self):
        print('\nFinal score')
        Student.order_students_list()
        for s in Student.students:
            print(s.final_score())
        print(Student.success_rate())

    def question_4(self):
        try:
            conn = lite.connect(self.db)
            with conn:
                curs = conn.cursor()
                sql_tp = "select count (*) from exam_score where exam_id=4;"
                sql_ep = "select count (*) from exam_score where exam_id=5;"
                sql_ta = "select avg(score) from exam_score where exam_id=4;"
                sql_ea = "select avg(score) from exam_score where exam_id=5;"

                curs.execute(sql_tp)
                tp = curs.fetchone()[0]
                curs.execute(sql_ep)
                ep = curs.fetchone()[0]
                curs.execute(sql_ta)
                ta = curs.fetchone()[0]
                curs.execute(sql_ea)
                ea = curs.fetchone()[0]

                sql_tperasan = "select count (*) from exam_score where score>=5 and exam_id=4;"
                sql_eperasan = "select count (*) from exam_score where score>=5 and exam_id=5;"

                curs.execute(sql_tperasan)
                tperasan = curs.fetchone()[0]
                curs.execute(sql_eperasan)
                eperasan = curs.fetchone()[0]

                if tp>0:
                    tperc = 100 * tperasan / tp
                else:
                    print('No participant in the final exam.')

                if ep>0:
                    eperc = 100 * eperasan / ep
                else: print('No participant in the re-examination.')

            print('Exam: Final [Participation : {}] : average score: {}, pass rate = {}%\n'.format(tp,ta,tperc))
            print('Exam: Repeat [Attendance : {}] : average score: {}, pass rate = {}%\n'.format(ep,ea,eperc))

        except lite.Error as Error_q4: print(Error_q4)
        pass

if __name__ == "__main__": Main()