"""
observer_demo.py

Task 2.3(d)

Observer Design Pattern Implementation

"""

from abc import ABC, abstractmethod


# ==========================================================
# Observer Interface
# ==========================================================

class Observer(ABC):
    """
    Abstract Observer interface.
    Every observer must implement update().
    """

    @abstractmethod
    def update(self, student_id: int, new_marks: float) -> None:
        pass


# ==========================================================
# Concrete Observer 1
# ==========================================================

class EmailNotifier(Observer):
    """
    Sends an email notification when marks are updated.
    """

    def update(self, student_id: int, new_marks: float) -> None:
        print(
            f"[Email Service] Email sent to Student {student_id}: "
            f"Your marks have been updated to {new_marks}."
        )


# ==========================================================
# Concrete Observer 2
# ==========================================================

class AuditLogNotifier(Observer):
    """
    Records the marks update in the audit log.
    """

    def update(self, student_id: int, new_marks: float) -> None:
        print(
            f"[Audit Log] Student {student_id} marks changed to "
            f"{new_marks}. Action recorded."
        )


# ==========================================================
# Subject
# ==========================================================

class MarksUpdateNotifier:
    """
    Subject that maintains a list of observers and
    notifies them whenever marks are updated.
    """

    def __init__(self):
        self._observers = []

    def register(self, observer: Observer) -> None:
        """Register an observer."""
        self._observers.append(observer)

    def deregister(self, observer: Observer) -> None:
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, student_id: int, new_marks: float) -> None:
        """Notify all registered observers."""
        for observer in self._observers:
            observer.update(student_id, new_marks)

    def update_marks(self, student_id: int, new_marks: float) -> None:
        """
        Simulates updating marks in the Admin Panel,
        then notifies all observers.
        """
        print(f"\nAdmin Panel: Updating marks for Student {student_id}...")
        print("Marks updated successfully.\n")

        self.notify(student_id, new_marks)


# ==========================================================
# Demonstration
# ==========================================================

def main():
    notifier = MarksUpdateNotifier()

    email_service = EmailNotifier()
    audit_service = AuditLogNotifier()

    # Register observers
    notifier.register(email_service)
    notifier.register(audit_service)

    print("=== First Marks Update ===")
    notifier.update_marks(101, 92.5)

    # Deregister Email Service
    notifier.deregister(email_service)

    print("\n=== Second Marks Update ===")
    notifier.update_marks(101, 95.0)


if __name__ == "__main__":
    main()


"""
============================================================

README Section – Observer Pattern

The Observer pattern allows the Admin Panel to notify
multiple independent services whenever a student's marks
are updated without tightly coupling the Admin Panel to
those services.

MarksUpdateNotifier acts as the Subject, while
EmailNotifier and AuditLogNotifier act as Observers.

When marks are updated, the subject notifies every
registered observer by calling its
update(student_id, new_marks) method.

This design provides loose coupling because the Admin
Panel only depends on the Observer interface rather than
concrete notification implementations.

Benefits:
- Easy to add new notification services without modifying
  the Admin Panel.
- Independent services can be registered or removed at
  runtime.
- Improves maintainability, extensibility, and adherence
  to the Open/Closed Principle.

============================================================
"""
```
