
def test_register(test_client, init_database):
    res = test_client.post(
        "/api/users/register/", json={
        "firstname": "Kim",
        "lastname": "yatty",
        "email": "yatkim@gmail.com",
        "password": "password@123"
    })
    assert res.status_code == 201


def test_register_forbiden(test_client):
    res = test_client.post(
        "/api/users/register/", json={
        "firstname": "Kim",
        "lastname": "yatty",
        "email": "yatkim@gmail.com",
        "password": "password@123"
    })
    assert res.status_code == 403
   

def test_login(test_client):
    login_res = test_client.post("/api/users/login/", json={
        "email": "yatkim@gmail.com",
        "password": "password@123"
    })
    access_token = login_res.get_json()['access_token']

    update_res = test_client.put("/api/users/update/", json={
        "firstname": "Oly",
        "lastname": "yatty",
        "email": "yatkim01@gmail.com",
        "password": "password@123"
    }, headers={"Authorization": f"Bearer {access_token}"}
    )

    logout_res = test_client.delete("/api/users/logout", headers={"Authorization": f"Bearer {access_token}"})

    assert login_res.status_code == 200
    assert update_res.status_code == 204
    assert logout_res.status_code == 204
