# Student Academic Record System (SARS)

## Overview

The **Student Academic Record System (SARS)** is a scalable web-based application designed to manage student academic records for a university. The system allows students to authenticate, view examination results, enroll in courses, and enables administrators to manage students, courses, instructors, and academic records.

This repository contains the software design artifacts and Python implementations required for Part 2 of the assignment.

---

# Repository Structure

```
.
├── system_design.md
├── lld_classes.py
├── singleton_demo.py
├── observer_demo.py
├── README.md
```

---

# Architecture Decisions

## Selected Architecture

A **Microservices Architecture** was selected for SARS instead of a monolithic architecture.

### Reasons

* Supports approximately **50,000 concurrent users** more effectively.
* Each module can be developed, deployed, and scaled independently.
* Individual service failures are isolated and do not necessarily affect the entire system.
* Easier to allocate computing resources only where demand is highest.
* Better suited for future expansion and maintenance.

### Main Services

* Authentication Service
* Student Portal Service
* Admin Panel Service
* Email Notification Service
* Audit Log Service
* Database Service

Communication between services is performed through REST APIs.

---

# Scalability Strategy

To support peak examination-result traffic:

* Horizontal scaling is used for web servers.
* Multiple application server instances run simultaneously.
* A load balancer distributes incoming requests using the **Round Robin** algorithm.
* Additional servers can be added during peak periods and removed during off-peak periods.

This approach provides:

* High availability
* Improved fault tolerance
* Better resource utilization
* Cost efficiency

---

# Session Management

Using multiple web servers introduces a session consistency problem because each server maintains its own memory.

Two common solutions are:

### Sticky Sessions

The load balancer consistently routes a user's requests to the same server.

**Advantage**

* Simple implementation.

**Trade-off**

* Poorer load distribution.
* User sessions are lost if the assigned server fails.

---

### Centralized Session Store

Sessions are stored in a shared session database or distributed cache.

**Advantages**

* Any web server can process any request.
* Better fault tolerance.
* Easier horizontal scaling.

**Trade-off**

* Additional infrastructure cost.
* Slight increase in network latency.

---

# SOLID Principles Applied

## Single Responsibility Principle (SRP)

The `Student` class contains only student-related data and behavior.

Email notification functionality is intentionally separated into dedicated notifier classes instead of placing notification methods inside the `Student` class.

This ensures each class has only one reason to change.

---

## Open/Closed Principle (OCP)

The `Enrollment` class is designed to be extended through inheritance.

For example:

* Regular Enrollment
* WaitlistedEnrollment
* PriorityEnrollment

New enrollment types can be introduced without modifying the original `Enrollment` class.

---

## Dependency Inversion Principle (DIP)

The `Enrollment` class depends on the `EnrollmentRepository` interface rather than a concrete database implementation.

Benefits include:

* Loose coupling
* Easier unit testing
* Ability to replace database implementations without changing business logic

---

# Singleton Pattern

The `DatabaseConnection` class uses the **Singleton** design pattern.

Goals:

* Ensure exactly one shared database connection exists.
* Prevent unnecessary resource consumption.
* Maintain consistency throughout the application.

The implementation is thread-safe using Python's `threading.Lock`.

Without synchronization, two threads could simultaneously detect that no instance exists and each create a separate instance. The lock prevents this race condition by allowing only one thread to initialize the singleton.

---

# Observer Pattern

The Admin Panel must notify multiple services whenever student marks are updated.

The Observer pattern is used to achieve this.

### Subject

* `MarksUpdateNotifier`

### Observers

* `EmailNotifier`
* `AuditLogNotifier`

When marks change:

1. The notifier receives the update.
2. Every registered observer is notified.
3. Each observer performs its own independent action.

Benefits include:

* Loose coupling
* Easy extensibility
* Independent notification services
* No changes required to Admin Panel code when adding new notification services

Observers can also be registered and deregistered dynamically.

---

# Redundancy Strategy

To maximize availability during examination result publication, the database tier uses **primary-replica replication**.

## Normal Operation

* The primary database processes write requests.
* Replicas maintain synchronized copies of the data.
* Read requests may be served by replicas to reduce load.

## Primary Failure

If the primary database fails:

* A replica is promoted to become the new primary.
* Write requests are redirected to the promoted server.
* Read requests continue using the available replicas.

This minimizes downtime while protecting against data loss.

---

# Fault Isolation

Because SARS uses a microservices architecture:

* Failure of the Email Notification Service does not stop the Student Portal.
* Students can still:

  * View marks
  * Enroll in courses
  * Log in successfully

The Student Portal handles notification failures by catching exceptions around notification calls, logging the error, and continuing the primary business operation instead of allowing the exception to propagate.

In a monolithic application, a failure inside the notification component could interrupt the entire request-processing flow and potentially affect unrelated functionality.

---

# Technologies Used

* Python 3
* Object-Oriented Programming
* REST-based architecture
* Singleton Design Pattern
* Observer Design Pattern
* SOLID Principles

---

# Files Included

| File                | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `system_design.md`  | High-level software architecture and scalability design |
| `lld_classes.py`    | Student, Enrollment, and Repository interface           |
| `singleton_demo.py` | Thread-safe Singleton implementation                    |
| `observer_demo.py`  | Observer design pattern implementation                  |
| `README.md`         | Project overview and design rationale                   |

---

# Conclusion

The proposed design emphasizes scalability, maintainability, fault tolerance, and reliability. By adopting a microservices architecture, applying SOLID principles, implementing appropriate design patterns, and using redundancy and horizontal scaling strategies, SARS can efficiently support approximately **50,000 concurrent users** while remaining resilient to failures and easy to extend in the future.
