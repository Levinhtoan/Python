def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"

def test_create_and_get_booking_api(client):
    # 1. Tạo mới lịch hẹn
    payload = {
        "customer": "Hoàng Minh Test",
        "service": "Khám tổng quát",
        "time": "2026-09-20 09:30",
        "notes": "Kiểm tra huyết áp"
    }
    create_res = client.post("/api/v1/bookings", json=payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["id"] is not None
    assert created_data["customer"] == "Hoàng Minh Test"

    booking_id = created_data["id"]

    # 2. Lấy danh sách lịch hẹn
    list_res = client.get("/api/v1/bookings")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 3. Lấy chi tiết lịch hẹn theo ID
    get_res = client.get(f"/api/v1/bookings/{booking_id}")
    assert get_res.status_code == 200
    assert get_res.json()["service"] == "Khám tổng quát"

    # 4. Hủy lịch hẹn
    cancel_res = client.put(f"/api/v1/bookings/{booking_id}/cancel")
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "CANCELLED"

    # 5. Xóa lịch hẹn
    delete_res = client.delete(f"/api/v1/bookings/{booking_id}")
    assert delete_res.status_code == 200
