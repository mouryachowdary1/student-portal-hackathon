import sqlite3
def init_db():
    with sqlite3.connect('example2.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                registration_number VARCHAR PRIMARY KEY,
                student_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL,
                course_description TEXT NOT NULL
            )
        ''')

        # Insert predefined courses
        courses = [
            ("Computer Science", "This subject explores the theory and practice of computing, covering algorithms, data structures, programming languages, and software development. It emphasizes problem-solving skills and the application of computational techniques."),
            ("Mathematics", "Mathematics for engineers focuses on advanced topics such as calculus, linear algebra, and differential equations. These mathematical tools are essential for modeling and solving engineering problems."),
            ("Physics", "Physics for engineers delves into fundamental principles such as mechanics, electromagnetism, and thermodynamics. The course applies these concepts to practical engineering scenarios."),
            ("Chemistry", "Engineering Chemistry introduces chemical principles relevant to material properties and reactions. It covers topics like thermodynamics, kinetics, and materials science, essential for various engineering applications."),
            ("Electrical Engineering", "This subject covers the basics of electrical circuits, components, and systems. Key areas include circuit analysis, electromagnetism, and the functioning of electrical devices and machines."),
            ("Engineering Drawing", "Engineering Drawing teaches the principles of technical drawing and graphical representation. It includes orthographic projection, isometric views, and the use of CAD software for creating detailed engineering designs.")
        ]

        cursor.executemany('''
            INSERT INTO courses (course_name, course_description) VALUES (?, ?)
        ''', courses)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                semester INTEGER,
                sgpa REAL,
                cgpa REAL, 
                registration_number VARCHAR,
                FOREIGN KEY (registration_number) REFERENCES users (registration_number)
            )
        ''')
        
        # Insert predefined grades
        grades = [
            (1, 8.6, 8.6, "BU21CSEN0300373"),
            (2, 8.8, 8.7, "BU21CSEN0300373"),
            # Add other grades data here
        ]

        cursor.executemany('''
            INSERT INTO grades (semester, sgpa, cgpa, registration_number) VALUES (?, ?, ?, ?)
        ''', grades)

        conn.commit()

if __name__ == '__main__':
    init_db()
