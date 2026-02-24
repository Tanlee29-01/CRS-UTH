# Course Registration System Specification

## 1) Overview
Build a web-based Course Registration System (CRS) for a university. The system allows students to search and register for course offerings, instructors to manage rosters, and administrators to manage catalog, terms, and policies.

## 2) Scope
- In scope
  - Student registration and schedule management
  - Course catalog and term offerings
  - Enrollment rules and validations
  - Waitlists and enrollment caps
  - Basic reporting and audit log
- Out of scope (for v1)
  - Billing/tuition payment
  - LMS integration
  - Degree audit
  - Financial aid and scholarships

## 3) Assumptions
- Single institution with multiple departments and terms.
- Authentication is handled by the hosting environment (SSO or local auth).
- Time zones use the institution’s local time.

## 4) User Roles
- Student: search courses, register/drop, view schedule.
- Instructor: view roster, export list, manage waitlist (optional).
- Administrator: manage catalog, terms, sections, rules, overrides.
- Registrar (admin subtype): finalize schedules, open/close registration.

## 5) Functional Requirements
### 5.1 Student
- Search courses by term, subject, level, instructor, time, credits, delivery mode.
- View course details: description, prerequisites, corequisites, capacity, schedule.
- Add/drop courses during allowed windows.
- Join waitlist if section full and waitlist enabled.
- View schedule and conflicts.
- View registration status and errors.

### 5.2 Instructor
- View section roster (enrolled + waitlisted).
- Export roster to CSV.
- Submit capacity override requests (optional).

### 5.3 Administrator
- Manage terms and registration windows.
- Manage course catalog (course definitions).
- Manage sections (offerings) per term.
- Configure rules: prerequisites, corequisites, time conflicts, max credits.
- Apply overrides for individual students.
- Open/close registration, add drop deadlines.
- Generate reports: enrollment by section, waitlist counts, capacity utilization.

## 6) Non-Functional Requirements
- Availability: 99.5% during registration windows.
- Performance: search results < 2s for typical queries.
- Security: role-based access control, audit logs for admin changes.
- Data integrity: prevent over-enrollment and invalid registrations.
- Accessibility: WCAG 2.1 AA for UI.

## 7) Domain Model (Core Concepts)
- Course: abstract catalog definition (e.g., CS101).
- Term: a semester or quarter.
- Section: a course offering in a term with capacity and schedule.
- Enrollment: student registration in a section.
- WaitlistEntry: student queue when full.
- Rule: prerequisite, corequisite, credit limits, time conflict.
- Override: admin exception to a rule.

## 8) Data Model (Entities and Fields)
### 8.1 Entities
- Student
  - id (UUID)
  - student_number (string, unique)
  - name_first, name_last
  - email
  - status (active, inactive)
  - level (undergrad, grad)
  - created_at, updated_at
- Instructor
  - id (UUID)
  - employee_number (string, unique)
  - name_first, name_last
  - email
  - department_id
  - created_at, updated_at
- Department
  - id (UUID)
  - code (string, unique)
  - name
- Course
  - id (UUID)
  - code (string, unique, e.g., CS101)
  - title
  - description
  - credits_min, credits_max
  - department_id
  - level (100, 200, 300, 400, 500)
  - active (bool)
- Term
  - id (UUID)
  - code (string, unique, e.g., 2026SP)
  - name (string, e.g., Spring 2026)
  - start_date, end_date
  - registration_open, registration_close
  - add_drop_deadline
- Section
  - id (UUID)
  - term_id
  - course_id
  - section_number (string)
  - instructor_id
  - capacity
  - waitlist_capacity
  - delivery_mode (in_person, online, hybrid)
  - location
  - status (open, closed, cancelled)
  - created_at, updated_at
- MeetingTime
  - id (UUID)
  - section_id
  - day_of_week (Mon..Sun)
  - start_time, end_time
- Enrollment
  - id (UUID)
  - student_id
  - section_id
  - status (enrolled, dropped)
  - enrolled_at, dropped_at
  - source (self, admin)
- WaitlistEntry
  - id (UUID)
  - student_id
  - section_id
  - position
  - created_at
- Rule
  - id (UUID)
  - course_id (nullable if global)
  - rule_type (prereq, coreq, max_credits, time_conflict)
  - rule_data (JSON)
  - active (bool)
- Override
  - id (UUID)
  - student_id
  - rule_id
  - term_id
  - granted_by
  - reason
  - created_at
- AuditLog
  - id (UUID)
  - actor_id
  - actor_role
  - action
  - entity_type
  - entity_id
  - created_at

### 8.2 Relationships
- Department 1..* Course
- Course 1..* Section
- Term 1..* Section
- Section 1..* MeetingTime
- Student *..* Section via Enrollment
- Student *..* Section via WaitlistEntry
- Course 1..* Rule
- Student 1..* Override

## 9) Business Rules
- A student cannot enroll in two sections with overlapping MeetingTime.
- A student cannot exceed max credits per term (configurable).
- Prerequisite and corequisite rules are enforced at registration time.
- Enrollment cannot exceed capacity.
- Waitlist can be enabled per section up to waitlist_capacity.
- When a seat opens, the first waitlisted student can be auto-promoted.

## 10) Core Workflows
- Search and view section details.
- Add course -> validate rules -> enroll or waitlist.
- Drop course -> update enrollment -> promote waitlist.
- Admin creates term, sections, and sets registration windows.

## 11) API Outline (v1)
- Auth: `POST /login`, `POST /logout`
- Courses: `GET /courses`, `GET /courses/{id}`
- Sections: `GET /terms/{termId}/sections`, `GET /sections/{id}`
- Enrollment: `POST /sections/{id}/enroll`, `POST /sections/{id}/drop`
- Waitlist: `POST /sections/{id}/waitlist`, `GET /sections/{id}/waitlist`
- Admin: `POST /admin/terms`, `POST /admin/sections`, `POST /admin/overrides`
- Reports: `GET /admin/reports/enrollment`

## 12) UI Outline (v1)
- Student dashboard: search, filters, results, schedule view.
- Section detail modal/page: capacity, instructor, meeting times.
- Registration cart: pending actions and validation feedback.
- Admin console: terms, courses, sections, rules, overrides.

## 13) Testing Strategy
- Unit tests for rule engine and enrollment checks.
- Integration tests for enroll/drop and waitlist promotion.
- Load test for search and enrollment endpoints.

## 14) Deployment
- Single environment for v1 (staging/production later).
- Database migrations versioned.
- Daily backups during registration window.

## 15) Milestones (Suggested)
- M1: Data model + API for courses/sections.
- M2: Enrollment + waitlist.
- M3: Admin console + reports.
- M4: Hardening + performance testing.
