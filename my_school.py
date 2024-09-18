# Programming Fundamental Final Coding Challenge
# Student Name: Abhinav
# Student Number: s3977487
# Highest Part attempted: HD LEVEL - 100% complete

import os
import sys
import datetime

class Student:
    """
    Student class to hold student related data and methods. It holds information like student_id, name, student_type, 
    and mode. It also keeps track of student's results, the number of finished and ongoing courses. 
    """
    def __init__(self, student_id, name, student_type, mode=None):
        # Initialization of the Student object with necessary attributes
        self.__student_id = student_id
        self.__name = name
        self.__student_type = student_type
        self.__mode = mode
        self.results = {} # Stores results in a dictionary. Key: course_id, Value: score
        self.finished = 0 # Number of finished courses
        self.ongoing = 0 # Number of ongoing courses

    # Getter methods
    @property   
    def student_id(self):
        return self.__student_id
    
    # Getter methods
    @property   
    def name(self):
        return self.__name
    
    # Getter methods
    @property   
    def student_type(self):
        return self.__student_type
    
    # Getter methods
    @property   
    def mode(self):
        return self.__mode

    def calculate_gpa(self):
        """
        Method to calculate the GPA on a 100 point scale and a 4 point scale. The GPA is the average 
        of all the scores that are not '--' (indicating the course is not yet graded).
        """
        total_score = sum(score for score in self.results.values() if score != '--')
        self.gpa_100 = total_score / len([score for score in self.results.values() if score != '--']) if self.results else 0
        self.gpa_4 = sum(self.get_4_scale(score) for score in self.results.values() if score != '--') / len([score for score in self.results.values() if score != '--']) if self.results else 0

    def calculate_wgpa(self, courses):
        """
        Method to calculate the weighted GPA on a 4 point scale. The weighted GPA is calculated by summing up the 
        product of each course's credit_points and the student's score - gpa_4 in that course, divided by the total credit_points. 
        """
        total_weighted_score = 0
        total_credits = 0
        for course_id, score in self.results.items():
            if score != '--':
                # Find the course from the list using the course_id
                course = next((course for course in courses if course.course_id == course_id), None)
                if course:
                    total_weighted_score += self.get_4_scale(score) * course.credit_points
                    total_credits += course.credit_points
        self.wgpa_4 = total_weighted_score / total_credits if total_credits else 0

    def satisfies_enrollment(self):
        """
        Method to check if the student satisfies the enrollment conditions. Full-time students need to 
        enroll in at least 4 courses while part-time students need to enroll in at least 2 courses.
        """
        # Total enrolled courses are the ones that the student finished plus the ones they're currently taking
        total_courses = self.finished + self.ongoing
        if self.mode == "FT" and total_courses >= 4:
            return True
        elif self.mode == "PT" and total_courses >= 2:
            return True
        else:
            return False

    @staticmethod
    def get_4_scale(score):
        """
        Static method to convert the 100 point scale score to a 4 point scale. This method is marked as a static 
        method because it doesn't depend on any state of the Student object and can be called on the class itself.
        """
        if score >= 79.5:
            return 4
        elif score >= 69.5:
            return 3
        elif score >= 59.5:
            return 2
        elif score >= 49.5:
            return 1
        else:
            return 0

class Course:
    """
    Course class to hold course-related data and methods. It stores details like course_id, course_type,
    name, credit_points, and semester. It also tracks student enrollment in the course and the number
    of finished and ongoing students.
    """
    def __init__(self, course_id, course_type, name, credit_points, semester):
        # Initialization of the Course object with necessary attributes
        self.__course_id = course_id
        self.__course_type = course_type  # 'E' for Elective or 'C' for Core
        self.__name = name
        self.__credit_points = credit_points # Credit points for the course
        self.__semester = semester # Semester in which the course is offered
        self.students = {} # Dictionary to hold students' scores. Key: student_id, Value: score
        self.finished = 0 # Number of students who finished the course
        self.ongoing = 0 # Number of students who are currently taking the course

    # Getter methods
    @property   
    def course_id(self):
        return self.__course_id
    
    # Getter methods
    @property   
    def course_type(self):
        return self.__course_type
    
    # Getter methods
    @property   
    def name(self):
        return self.__name
    
    # Getter methods
    @property   
    def credit_points(self):
        return self.__credit_points
    
    # Getter methods
    @property   
    def semester(self):
        return self.__semester

    def calculate_average_score(self):
        """
        Method to calculate the average score of the course. The average score is the mean of all the 
        scores of the students enrolled in the course who have a score (i.e., score != '--').
        """
        self.average_score = sum(score for score in self.students.values() if score != '--') / len([score for score in self.students.values() if score != '--']) if self.students else 0

class Results:
    """
    Results class to handle the overall course results for students. It stores the list of all students,
    all courses, their corresponding scores, and other related attributes and methods.
    """
    def __init__(self):
        self.students : list(Student) = [] # List of all Student objects
        self.courses: list(Course) = [] # List of all Course objects
        self.scores = {} # Dictionary to store scores. Key: (student_id, course_id), Value: score
        self.total_scores = 0 # Total number of scores recorded
        self.passed_scores = 0 # Total number of scores >= 49.5

    def read_students(self, student_file):
        """
        Method to read student data from a text file and create Student objects. It validates the data,
        checks for any invalid entries, and handles them accordingly.
        """
        with open(student_file, 'r') as file:
            for line in file.readlines():
                data = line.strip().split(',')
                if len(data) == 4:
                    student_id, name, student_type, mode = data
                else:
                    student_id, name, student_type = data
                    mode = 'FT'
                
                try: 
                    if not student_id.strip().startswith('S'):
                        raise InvalidStudentIDError(student_id)
                except (InvalidStudentIDError) as e:
                    print(str(e))
                    sys.exit(1) # Exit with error status

                self.students.append(Student(student_id.strip(), name.strip(), student_type.strip(), mode.strip()))

    def read_courses(self, course_file):
        """
        Method to read course data from a text file and create Course objects. It validates the data,
        checks for any invalid entries, and handles them accordingly.
        """
        with open(course_file, 'r') as file:
            for line in file.readlines():
                data = line.strip().split(',')
                if len(data) == 4:
                    course_id, course_type, name, credit_points = data
                    semester = "All"

                else:
                    course_id, course_type, name, credit_points, semester = data

                try:
                    if not (course_id.strip().startswith('COSC') or course_id.strip().startswith('ISYS') or course_id.strip().startswith('MATH')):
                        raise InvalidCourseIDError(course_id)
                except (InvalidCourseIDError) as e:
                    print(str(e))
                    sys.exit(1) # Exit with error status
                
                self.courses.append(Course(course_id.strip(), course_type.strip(), name.strip(), int(credit_points), semester.strip()))

    def read_results(self, result_file):
        """
        Method to read student results from a text file. It validates the data, checks for any invalid 
        entries, and handles them accordingly. It then updates the score attributes of the corresponding 
        Student and Course objects.
        """
        with open(result_file, 'r') as file:
            lines = file.readlines()

            try:
                # If file is empty
                if not lines:
                    raise EmptyFileError(result_file)
            except (EmptyFileError) as e:
                print(str(e))
                sys.exit(1) # Exit with error status
                
            for line in lines:
                data = line.strip().split(',')

                try:
                    student_id, course_id, score = data

                    if not score:
                        score = '--'
                    else:
                        try:
                            score = float(score)
                            if score < 0.0 or score > 100.0:
                                raise InvalidScoreError(score)
                        except ValueError:
                            raise InvalidScoreError(score)
                            
                    if not student_id.strip().startswith('S'):
                        raise InvalidStudentIDError(student_id)

                    if not (course_id.strip().startswith('COSC') or course_id.strip().startswith('ISYS') or course_id.strip().startswith('MATH')):
                        raise InvalidCourseIDError(course_id)

                except (EmptyFileError, InvalidScoreError, InvalidStudentIDError, InvalidCourseIDError) as e:
                    print(str(e))
                    sys.exit(1) # Exit with error status

                self.scores[(student_id.strip(), course_id.strip())] = score

                if score != '--':
                    self.total_scores += 1
                    if score >= 49.5:
                        self.passed_scores += 1

                for student in self.students:
                    if student.student_id == student_id.strip():
                        student.results[course_id.strip()] = score
                        if score != '--':
                            student.finished += 1
                        else:
                            student.ongoing += 1

                for course in self.courses:
                    if course.course_id == course_id.strip():
                        course.students[student_id.strip()] = score
                        if score != '--':
                            course.finished += 1
                        else:
                            course.ongoing += 1

    def display_results(self):
        """
        Method to display the results. It first calculates the GPA, average scores and WGPA, then it saves 
        the results to there objects attributes accordingly, and finally, it prints the results tables.
        """
        for student in self.students:
            student.calculate_gpa()

        for course in self.courses:
            course.calculate_average_score()
        
        for student in self.students:
            student.calculate_wgpa(self.courses)

        # Get the current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

        # Read the existing content of the file
        old_content = ""
        try:
            with open('reports.txt', 'r') as file:
                old_content = file.read()
        except FileNotFoundError:
            pass

        # Open the file in write mode, which will erase the existing content
        # Save results in a file and print tables
        with open('reports.txt', 'w') as f:
            # Write the date and time at the top of the file
            print(f"Date and time when the report was generated : {timestamp}", file=f)

            # Call the print_and_save functions
            self.print_and_save_results_table(f)
            self.print_and_save_course_table(f)
            self.print_and_save_student_table(f)

            # Append the old content at the end
            print(old_content, file=f)

    def print_and_save_results_table(self, file):
        """
        Method to print and save the results table. It generates a formatted string for the table and 
        writes it to both the console and a file.
        """
        # Calculate the dynamic size of header based on number of courses
        header_size = 15 + len(self.courses) * 16  # 15 for "Student IDs", len(self.courses) * 16 for each course taking 15 chars and a tab

        # Print table header
        header = f'RESULTS\n{"-" * header_size}\n'
        header += f'{"Student IDs":<15}\t' + "".join([f'{course.course_id:>15}\t' for course in self.courses]) + "\n"
        header += f'{"-" * header_size}\n'
        print(header)
        file.write(header)

        # Print each student's results
        for student in self.students:
            row = f'{student.student_id:<15}\t' + ''.join([f'{str(self.scores.get((student.student_id, course.course_id), "")):>15}\t' for course in self.courses])
            print(f'{row}\n')
            file.write(f'{row}\n')

        # Print summary
        pass_rate = self.passed_scores / self.total_scores if self.total_scores > 0 else 0 
        summary = f"\nRESULTS SUMMARY\nThere are {len(self.students)} students and {len(self.courses)} courses.\nThe average pass rate is {pass_rate*100:.2f}%.\n\n"
        print(summary)
        file.write(summary)

    def print_and_save_course_table(self, file):
        """
        Method to print and save the course information table. It generates a formatted string for 
        the table and writes it to both the console and a file.
        """
        # Print table header for core courses
        header = "COURSE INFORMATION\n" + "-" * 95 + "\n"
        header += f"{'CourseID':<15}{'Name':<15}{'Type':>10}{'Credit':>10}{'Semester':>15}{'Average':>10}{'Nfinish':>10}{'Nongoing':>10}\n"
        header += "-" * 95 + "\n"
        print(header)
        file.write(header)

        # Sort courses based on Average from high to low
        self.courses.sort(key=lambda course: course.average_score, reverse=True)

        # Print each core course's information
        for course in self.courses:
            if course.course_type == 'C':
                line = f"{course.course_id:<15}{course.name:<15}{course.course_type:>10}{course.credit_points:>10}{course.semester:>15}{course.average_score:>10.2f}{course.finished:>10}{course.ongoing:>10}\n"
                print(line)
                file.write(line)
        
        # Print table header for elective courses
        header = "-" * 95 + "\n"
        header += f"{'CourseID':<15}{'Name':<15}{'Type':>10}{'Credit':>10}{'Semester':>15}{'Average':>10}{'Nfinish':>10}{'Nongoing':>10}\n"
        header += "-" * 95 + "\n"
        print(header)
        file.write(header)

        # Print each elective course's information
        for course in self.courses:
            if course.course_type == 'E':
                line = f"{course.course_id:<15}{course.name:<15}{course.course_type:>10}{course.credit_points:>10}{course.semester:>15}{course.average_score:>10.2f}{course.finished:>10}{course.ongoing:>10}\n"
                print(line)
                file.write(line)

        # Print summary
        hardest_core = min(self.courses, key=lambda c: c.average_score if c.course_type == 'C' else float('inf'))
        hardest_elective = min(self.courses, key=lambda c: c.average_score if c.course_type == 'E' else float('inf'))
        summary = f"\nCOURSE SUMMARY\nThe most difficult core course is {hardest_core.course_id} with an average score of {hardest_core.average_score:.2f}.\n"
        summary += f"The most difficult elective course is {hardest_elective.course_id} with an average score of {hardest_elective.average_score:.2f}.\n\n"
        print(summary)
        file.write(summary)

    def print_and_save_student_table(self, file):
        """
        Method to print and save the student information table. It generates a formatted string for 
        the table and writes it to both the console and a file.
        """
        # Print table header for PG students
        header = "STUDENT INFORMATION\n" + "-" * 100 + "\n"
        header += f"{'StudentID':<15}{'Name':<15}{'Type':>10}{'Mode':>10}{'GPA(100)':>10}{'GPA(4)':>10}{'WGPA(4)':>10}{'Nfinish':>10}{'Nongoing':>10}\n"
        header += "-" * 100 + "\n"
        print(header)
        file.write(header)

        # Sort students based on WGPA(4) from high to low
        self.students.sort(key=lambda student: student.wgpa_4, reverse=True)

        # Print each PG student's information
        for student in self.students:
            if student.student_type == 'PG':
                name = student.name
                if not student.satisfies_enrollment():
                    name += " (!)"
                line = f"{student.student_id:<15}{name:<15}{student.student_type:>10}{student.mode:>10}{student.gpa_100:>10.2f}{student.gpa_4:>10.2f}{student.wgpa_4:>10.2f}{student.finished:>10}{student.ongoing:>10}\n"
                print(line)
                file.write(line)
        
        # Print table header for UG students
        header = "-" * 100 + "\n"
        header += f"{'StudentID':<15}{'Name':<15}{'Type':>10}{'Mode':>10}{'GPA(100)':>10}{'GPA(4)':>10}{'WGPA(4)':>10}{'Nfinish':>10}{'Nongoing':>10}\n"
        header += "-" * 100 + "\n"
        print(header)
        file.write(header)

        # Print each UG student's information
        for student in self.students:
            if student.student_type == 'UG':
                name = student.name
                if not student.satisfies_enrollment():
                    name += " (!)"
                line = f"{student.student_id:<15}{name:<15}{student.student_type:>10}{student.mode:>10}{student.gpa_100:>10.2f}{student.gpa_4:>10.2f}{student.wgpa_4:>10.2f}{student.finished:>10}{student.ongoing:>10}\n"
                print(line)
                file.write(line)

        # Print summary
        best_PG = max(self.students, key=lambda s: s.gpa_4 if s.student_type == 'PG' else float('-inf'))
        best_UG = max(self.students, key=lambda s: s.gpa_4 if s.student_type == 'UG' else float('-inf'))
        summary = f"\nSTUDENT SUMMARY\nThe best PG student is {best_PG.student_id} with a GPA score of {best_PG.gpa_4:.2f}.\n"
        summary += f"The best UG student is {best_UG.student_id} with a GPA score of {best_UG.gpa_4:.2f}.\n\n"
        print(summary)
        file.write(summary)

# Custom Exceptions
# Exception to handle the case when certain files are not found
class FilesNotFoundError(Exception):
    def __init__(self, filenames):
        self.filenames = filenames
    def __str__(self):
        return f"File(s) not found: {', '.join(self.filenames)}"

# Exception to handle the case when the file is empty
class EmptyFileError(Exception):
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return f"File is empty: {self.filename}"

# Exception to handle the case when an invalid score is found in the result file
class InvalidScoreError(Exception):
    def __init__(self, score):
        self.score = score
    def __str__(self):
        return f"Invalid score: {self.score} in the result file.    "

# Exception to handle the case when an invalid student ID is found
class InvalidStudentIDError(Exception):
    def __init__(self, student_id):
        self.student_id = student_id
    def __str__(self):
        return f"Invalid student ID: {self.student_id}"

# Exception to handle the case when an invalid course ID is found
class InvalidCourseIDError(Exception):
    def __init__(self, course_id):
        self.course_id = course_id
    def __str__(self):
        return f"Invalid course ID: {self.course_id}"

# SchoolResults class that handles reading and displaying school results : Main Class
class SchoolResults:
    def __init__(self):
         # Instantiate a Results object upon initialization
        self.results = Results()

    def read_files(self, result_file, course_file, student_file):
        # Read courses, students, and results from the respective files
        self.results.read_courses(course_file)
        self.results.read_students(student_file)
        self.results.read_results(result_file)

    def display(self):
        # Display the results
        self.results.display_results()

# Main function to run the program
def main():
    try:
        # Check for correct usage of the program
        if len(sys.argv) != 4:
            raise Exception("[Usage:] python my_school.py <result file> <course file> <student file>")
        else:
            # Check if all the required files exist
            result_file, course_file, student_file = sys.argv[1:]
            missing_files = [filename for filename in [result_file, course_file, student_file] if not os.path.exists(filename)]
            if missing_files:
                # If any files are missing, raise an exception
                raise FilesNotFoundError(missing_files)
                
    except (FilesNotFoundError, Exception) as e:
        # Handle any caught exceptions
        print(str(e))
        sys.exit(1)  # Exit with error status

    # Instantiate a SchoolResults object
    school_results = SchoolResults()
    # Read data from files
    school_results.read_files(result_file, course_file, student_file)
    # Display the results
    school_results.display()

# Check if this file is the main program and then execute it
if __name__ == "__main__":
    main()


"""
    Analysis/Reflection:
    --------------------

Design Process:
---------------
The main design philosophy behind this program was to maintain clean, readable, and manageable code by using object-oriented principles. The
problem at hand seemed to have distinct entities - the results, students, and courses - which hinted towards using classes to 
represent them. This led to the creation of the 'SchoolResults' class.

I started the design process by outlining the responsibilities and behaviors of these classes. It was clear that 'SchoolResults' would need 
to read data from files, so methods for reading files were included. Since the program also required to display the results, a display method 
was included as well.

A significant part of the design was handling errors. A lot of things could go wrong - files might not exist, they could be empty, or contain 
invalid data. To handle these situations elegantly and make the code more descriptive, I decided to implement custom exception classes. These 
exceptions would handle specific errors and provide more context about what went wrong, which would be particularly helpful for users and for 
debugging.

Development Process:
--------------------
After designing the basic structure, I moved on to writing the code. I started with building 'Results', 'Courses', 'Students' class in 
initial levels of the assignment with there respective attributes and methods. Then, I started with the 'SchoolResults' class since it forms the 
core functionality of the program. The 'read_files' and 'display' methods were straightforward to implement.

The main function was designed to parse command line arguments, check for the existence of the input files, and create an instance of the 
'SchoolResults' class to read and display the results. 

The creation of custom exceptions came last in HD level. These were designed to handle specific error scenarios that could occur during the execution of 
the program.

Challenges:
-----------
The primary challenge was to ensure the program was robust and could handle various errors gracefully. Implementing custom exceptions helped 
in this regard but required careful consideration of what scenarios to account for.

Determining how to structure the 'SchoolResults' class and deciding what responsibilities it should have was another challenge. However, 
after outlining the behaviors and responsibilities, it was a matter of translating that into code.

The other challenge was handling the different types of files - results, students, and courses - within the same 'SchoolResults' class. 
However, using separate methods for reading each file type provided a clean and understandable solution.

In conclusion, the design and development of this program provided a useful exercise in object-oriented design, exception handling, and 
working with files.
"""
