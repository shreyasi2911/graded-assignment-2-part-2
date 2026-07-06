# system_design.md

# Part 2 – Software System Design: Architecture and Scalability

## Task 2.1 – Requirements and Architecture Choice

### a. Functional and Non-Functional Requirements

#### Functional Requirements

1. Students shall be able to securely log in using their university credentials.
2. Students shall be able to view examination results and enroll in available courses.
3. Administrators shall be able to manage student records, courses, faculty, and academic results.

---

#### Non-Functional Requirements

| Non-Functional Requirement | Description                                                                                                                                                 | Primary Design Principle |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| High Performance           | The system should support approximately **50,000 concurrent users** during examination result publication without significant degradation in response time. | **Scalability**          |
| High Availability          | The application should remain operational during peak periods with minimal downtime through redundancy and failover mechanisms.                             | **Availability**         |
| Secure Access              | User authentication, authorization, and encrypted communication must protect sensitive academic information from unauthorized access.                       | **Security**             |

---

### b. Monolithic vs. Microservices Architecture

| Dimension              | Monolithic Architecture                                                              | Microservices Architecture                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Independent Deployment | Entire application must be deployed even for a small change.                         | Each service can be deployed independently without affecting other services.                         |
| Fault Isolation        | Failure in one module may impact the whole application.                              | Failures are isolated to individual services, allowing the remaining services to continue operating. |
| Management Complexity  | Easier to develop, test, and deploy initially because there is only one application. | More complex due to multiple services, service communication, monitoring, and deployment management. |

#### Recommendation

For SARS, a **microservices architecture** is recommended because the application must support approximately **50,000 concurrent users** during examination result publication. Individual services such as Authentication, Student Portal, and Admin Panel can be scaled independently according to demand. Although microservices introduce greater operational complexity, they provide better scalability, fault isolation, and maintainability, making them more suitable for a large public-facing university system.

---

# Task 2.2 – High-Level Design

## a. Main Components of SARS

| Component                  | Single Responsibility                                                | Interface Exposed              |
| -------------------------- | -------------------------------------------------------------------- | ------------------------------ |
| Authentication Service     | Authenticate users and generate user sessions or tokens.             | REST API                       |
| Student Portal Service     | Allow students to view marks and enroll in courses.                  | REST API                       |
| Admin Panel Service        | Manage students, courses, faculty, and examination records.          | REST API                       |
| Email Notification Service | Send email notifications for important events such as marks updates. | REST API                       |
| Audit Log Service          | Record administrative actions for accountability and auditing.       | REST API                       |
| Database Service           | Store and retrieve all application data.                             | Database Query Interface (SQL) |

---

## b. Layered Architecture for the Student Portal

### 1. Presentation Layer

**Responsibilities**

* Displays web pages and user interface.
* Receives requests from users.
* Performs basic input validation.
* Sends requests to the Business Layer.

**Receives**

* User input (login details, course selections, requests to view marks).

**Passes**

* Validated request data to the Business Layer.

---

### 2. Business Layer

**Responsibilities**

* Implements application logic.
* Validates business rules.
* Processes enrollment requests.
* Retrieves examination results.
* Coordinates communication between services.

**Receives**

* Validated user requests from the Presentation Layer.

**Passes**

* Database queries to the Data Access Layer.
* Processed results back to the Presentation Layer.

---

### 3. Data Access Layer

**Responsibilities**

* Executes SQL queries.
* Retrieves and stores application data.
* Maps database records to application objects.

**Receives**

* Database requests from the Business Layer.

**Passes**

* Student, enrollment, and marks data back to the Business Layer.

---

## c. Scaling Strategy

SARS should use **horizontal scaling** for the web servers.

Instead of upgrading a single server with additional CPU or memory (vertical scaling), multiple web server instances are deployed behind a load balancer. Horizontal scaling provides better fault tolerance because requests continue to be served even if one server fails. It also allows additional servers to be added during examination result publication when demand increases.

A **Round Robin** load-balancing algorithm should be used. This algorithm distributes incoming requests evenly across all available web servers in turn, making it simple, efficient, and suitable when the servers have similar hardware capacity.

---

## d. Elasticity

Elasticity allows the system to automatically adjust computing resources according to workload.

During examination result publication, additional web server instances can be created automatically to handle the large number of concurrent users. During off-peak periods such as semester breaks, unnecessary servers are automatically removed to reduce infrastructure costs. This enables SARS to maintain high performance during busy periods while avoiding unnecessary resource expenses when demand is low.

---

## e. Session Routing Problem

### Problem Name

**Session Affinity (Session Persistence) Problem**

Each web server stores authenticated user sessions in its own local memory. If a student's login request is handled by **Server A**, the session is created only on that server. When the next request is distributed by the Round Robin load balancer to **Server B**, Server B has no record of the user's session. As a result, the student may appear to be logged out or receive an authentication error.

---

### Strategy 1 – Sticky Sessions (Routing-Based)

The load balancer maintains **session affinity** by consistently routing all requests from the same user to the same web server.

**Trade-off**

* Poorer load distribution because some servers may receive more requests than others.
* If the assigned server fails, the user's session is lost unless additional recovery mechanisms are implemented.

---

### Strategy 2 – Centralized Session Store (Storage-Based)

Store sessions in a shared session repository such as a distributed cache or database that is accessible by every web server.

Each server retrieves session information from the shared storage instead of local memory.

**Trade-off**

* Requires additional infrastructure and increases operational cost.
* Every request involves a network call to the shared session store, introducing slight additional latency.

However, this approach provides better fault tolerance and supports horizontal scaling because any server can process any authenticated request.
