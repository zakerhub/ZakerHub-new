# Zaker API v1 Endpoints

Base URL: `http://127.0.0.1:8000`

## Authentication (`/api/v1/auth/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **POST** | `/signup/` | Create a new student/teacher account | No |
| **POST** | `/login/` | Get auth token | No |
| **GET** | `/me/` | Get current logged-in user details | Yes |

### Signup Body
```json
{
  "email": "student@example.com",
  "name": "Student Name",
  "password": "strongpassword",
  "phone": "0123456789"
}
```

### Login Body
```json
{
  "username": "student@example.com",
  "password": "strongpassword"
}
```

---

## Academics (`/api/v1/academics/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **GET** | `/curriculums/` | List all curriculums | Yes/Public |
| **GET** | `/subjects/?curriculum={id}` | List subjects (filter by curriculum optional) | Yes/Public |
| **GET** | `/courses/?subject={id}&teacher={id}` | List courses (filter by subject/teacher) | Yes/Public |
| **GET** | `/levels/` | List all levels (Basic/Advanced) | Yes/Public |
| **GET** | `/items/` | **Secure**. List content for approved enrollments | Yes |

### Create Course Body (Teacher)
```json
{
  "subject": 1,
  "description": "Comprehensive SAT Math Course"
}
```

### Create Content Body (Teacher)
```json
{
  "course": 1,
  "type": "MATERIAL", // MATERIAL, ASSIGNMENT, MEETING, ANNOUNCEMENT
  "title": "Week 1 Notes",
  "content_url": "https://drive.google.com/..."
}
```

---

## Subscriptions (`/api/v1/subscriptions/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| **GET** | `/options/` | List subscription plans | Yes |
| **GET** | `/enrollments/` | List my enrollments (Student) or All (Admin) | Yes |
| **POST** | `/enrollments/` | Apply for subscription | Yes |

*Note: Approval is handled exclusively via Django Admin Panel.*

### Enrollment Body
```json
{
  "subscription_option": 1
}
```
