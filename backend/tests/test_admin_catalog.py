def _admin_token(client):
    payload = {"email": "admin2@example.com", "password": "Passw0rd!", "role": "admin"}
    client.post("/auth/register", json=payload)
    r = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    return r.json()["access_token"]


def test_admin_create_catalog(client):
    token = _admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/admin/departments", json={"code": "CS", "name": "Computer Science"}, headers=headers)
    assert r.status_code == 200
    dep_id = r.json()["id"]

    r = client.post(
        "/admin/courses",
        json={
            "code": "CS101",
            "title": "Intro",
            "description": "Intro course",
            "credits_min": 3,
            "credits_max": 3,
            "level": 100,
            "active": True,
            "department_id": dep_id,
        },
        headers=headers,
    )
    assert r.status_code == 200
    course_id = r.json()["id"]

    r = client.post(
        "/admin/terms",
        json={
            "code": "2026SP",
            "name": "Spring 2026",
            "start_date": "2026-01-12",
            "end_date": "2026-05-15",
            "registration_open": "2026-01-02",
            "registration_close": "2026-02-15",
            "add_drop_deadline": "2026-02-01",
        },
        headers=headers,
    )
    assert r.status_code == 200
    term_id = r.json()["id"]

    r = client.post(
        "/admin/sections",
        json={
            "term_id": term_id,
            "course_id": course_id,
            "section_number": "001",
            "capacity": 30,
            "waitlist_capacity": 5,
            "delivery_mode": "in_person",
            "location": "Bldg A",
            "status": "open",
        },
        headers=headers,
    )
    assert r.status_code == 200
    section_id = r.json()["id"]

    r = client.post(
        "/admin/meeting-times",
        json={
            "section_id": section_id,
            "day_of_week": "Mon",
            "start_time": "09:00:00",
            "end_time": "10:15:00",
        },
        headers=headers,
    )
    assert r.status_code == 200

    r = client.get("/departments")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/courses")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/terms")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/sections")
    assert r.status_code == 200
    assert len(r.json()) == 1
