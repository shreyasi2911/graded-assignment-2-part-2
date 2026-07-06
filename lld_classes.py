
"""

Task 2.3 (a-b)
Student Academic Record System (SARS)

This file contains:
1. Student class
2. Enrollment class
3. WaitlistedEnrollment subclass
4. EnrollmentRepository interface

SOLID Principles Applied
------------------------
1. Single Responsibility Principle (SRP)
   - Student only stores and manages student information.
   - Email notification functionality is intentionally NOT included.

2. Open/Closed Principle (OCP)
   - Enrollment can be extended through inheritance
     (e.g., WaitlistedEnrollment) without modifying the base class.

3. Dependency Inversion Principle (DIP)
   - Business classes depend on the EnrollmentRepository abstraction,
     not a concrete database implementation.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import List


# ==========================================================
# Student Class
# ==========================================================

class Student:

    def __init__(
        self,
        student_id: int,
        full_name: str,
        email: str,
        program: str
    ):
        self.student_id = student_id
        self.full_name = full_name
        self.email = email
        self.program = program

    # --------------------------
    # Methods
    # --------------------------

    def view_marks(self) -> List[dict]:
        """
        Return the student's marks.

        Returns:
            List[dict]
        """
        pass

    def enroll_course(self, course_id: int) -> bool:
        """
        Request enrollment into a course.

        Parameters:
            course_id (int)

        Returns:
            bool
        """
        pass

    def update_email(self, new_email: str) -> None:
        """
        Update student's email.

        Parameters:
            new_email (str)

        Returns:
            None
        """
        self.email = new_email


# ==========================================================
# Enrollment Class
# ==========================================================

class Enrollment:
    """
    Represents a student's enrollment.

    SOLID:
    ------
    Open/Closed Principle (OCP)

    New enrollment types can extend this class
    without changing existing code.
    """

    def __init__(
        self,
        enrollment_id: int,
        student_id: int,
        course_id: int,
        enrollment_date: date,
        status: str
    ):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.status = status

    def confirm_enrollment(self) -> bool:
        """
        Confirm the enrollment.

        Returns:
            bool
        """
        self.status = "Confirmed"
        return True

    def cancel_enrollment(self) -> bool:
        """
        Cancel the enrollment.

        Returns:
            bool
        """
        self.status = "Cancelled"
        return True


# ==========================================================
# Extension Example
# ==========================================================

class WaitlistedEnrollment(Enrollment):
    """
    Demonstrates the Open/Closed Principle.

    Enrollment is extended without modifying
    the original Enrollment class.
    """

    def __init__(
        self,
        enrollment_id: int,
        student_id: int,
        course_id: int,
        enrollment_date: date,
        waitlist_position: int
    ):
        super().__init__(
            enrollment_id,
            student_id,
            course_id,
            enrollment_date,
            "Waitlisted"
        )

        self.waitlist_position = waitlist_position

    def promote(self) -> bool:
        """
        Promote the student from waitlist.

        Returns:
            bool
        """
        self.status = "Confirmed"
        return True


# ==========================================================
# Repository Interface
# ==========================================================

class EnrollmentRepository(ABC):
    """
    Repository interface.

    SOLID:
    ------
    Dependency Inversion Principle (DIP)

    Business classes depend on this abstraction
    instead of a concrete database implementation.
    """

    @abstractmethod
    def save(self, enrollment: Enrollment) -> None:
        """
        Save an enrollment.
        """
        pass

    @abstractmethod
    def find_by_id(self, enrollment_id: int) -> Enrollment:
        """
        Retrieve an enrollment by ID.
        """
        pass

    @abstractmethod
    def find_by_student(self, student_id: int) -> List[Enrollment]:
        """
        Retrieve all enrollments for a student.
        """
        pass

    @abstractmethod
    def update(self, enrollment: Enrollment) -> None:
        """
        Update an existing enrollment.
        """
        pass

    @abstractmethod
    def delete(self, enrollment_id: int) -> None:
        """
        Delete an enrollment.
        """
        pass


"""
============================================================

Task 2.3(a) Design Decisions

Student Class

Attributes
----------
student_id : int
full_name : str
email : str
program : str

Methods
-------
view_marks() -> List[dict]
enroll_course(course_id: int) -> bool
update_email(new_email: str) -> None

SOLID Principle Applied
-----------------------
Single Responsibility Principle (SRP)

The Student class only represents student information
and student-related operations.

It intentionally DOES NOT contain methods such as:

send_email()
notify_student()

Those responsibilities belong to dedicated notification classes.

============================================================

Enrollment Class

Attributes
----------
enrollment_id : int
student_id : int
course_id : int
enrollment_date : date
status : str

Methods
-------
confirm_enrollment() -> bool
cancel_enrollment() -> bool

SOLID Principle Applied
-----------------------
Open/Closed Principle (OCP)

The WaitlistedEnrollment subclass extends Enrollment
without modifying the original class.

============================================================

Task 2.3(b)

EnrollmentRepository Interface

Methods
-------
save(enrollment: Enrollment) -> None
find_by_id(enrollment_id: int) -> Enrollment
find_by_student(student_id: int) -> List[Enrollment]
update(enrollment: Enrollment) -> None
delete(enrollment_id: int) -> None

Dependency Inversion Principle (DIP)

Enrollment depends on the EnrollmentRepository abstraction
rather than a specific database class.

This allows different implementations
(MySQL, PostgreSQL, SQLite, etc.)
to be substituted without changing business logic,
making the system easier to maintain and test.

============================================================
"""
```
