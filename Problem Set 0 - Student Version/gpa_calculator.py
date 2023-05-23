from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    hours=0
    gradesum=0
    for i in range(len(courses)):
        if (Course.convert_grade_to_points(courses[i].grades.get(student.id,"N")))==0:
           continue


        else:
          hours+=courses[i].hours
          gradesum+=courses[i].hours*courses[i].convert_grade_to_points(courses[i].grades.get(student.id))


    if hours==0:
        return 0
    
    return gradesum/hours

