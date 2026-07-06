"""
singleton_demo.py

Task 2.3(c)
Thread-safe Singleton Design Pattern

"""

import threading


class DatabaseConnection:
    """
    Singleton class representing a shared database connection.
    """

    # Holds the single instance of the class
    _instance = None

    # Lock used to synchronize instance creation between threads
    _lock = threading.Lock()

    def __init__(self):
        """
        Constructor.

        It should never be called directly by users.
        """

        # Prevent creating another instance directly.
        if DatabaseConnection._instance is not None:
            raise Exception(
                "This class is a Singleton. "
                "Use DatabaseConnection.get_connection()."
            )

        # Simulated database connection object
        self.connection = "Shared Database Connection Established"

    @classmethod
    def get_connection(cls):
        """
        Returns the shared DatabaseConnection instance.

        Uses double-checked locking to ensure that only
        one instance is created, even when multiple
        threads call this method simultaneously.
        """

        # First check (avoids unnecessary locking once created)
        if cls._instance is None:

            # Only one thread may enter this block at a time
            with cls._lock:

                # Second check prevents another thread
                # from creating a second instance while
                # waiting for the lock.
                if cls._instance is None:
                    cls._instance = cls()

        return cls._instance


# --------------------------------------------------------
# Demonstration
# --------------------------------------------------------

def worker():
    """
    Function executed by each thread.

    Every thread requests the shared connection.
    """
    db = DatabaseConnection.get_connection()

    print(
        f"Thread: {threading.current_thread().name}"
    )
    print(
        f"Object ID: {id(db)}"
    )
    print(
        f"Connection: {db.connection}"
    )
    print("-" * 40)


def main():
    """
    Starts multiple threads simultaneously to verify
    that only one DatabaseConnection object is created.
    """

    threads = []

    for i in range(5):
        thread = threading.Thread(
            target=worker,
            name=f"Thread-{i + 1}"
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()


"""
------------------------------------------------------------

Why naive lazy initialization is unsafe

Example (NOT thread-safe):

if DatabaseConnection._instance is None:
    DatabaseConnection._instance = DatabaseConnection()

Suppose two threads execute this code at exactly the same time.

Thread A checks:
_instance is None → True

Before creating the object,
Thread B also checks:
_instance is None → True

Both threads create a new DatabaseConnection object,
resulting in TWO Singleton instances.

Using threading.Lock ensures that only one thread
can create the object, preventing this race condition.

The second check inside the lock (double-checked locking)
prevents another instance from being created if one thread
has already initialized it while others were waiting.

------------------------------------------------------------
"""
```
