from azure.functions import HttpRequest
import function_app as app
import json

def test_post_user_missing_fields():
    req = HttpRequest(
        method='POST',
        url='/api/user',
        body=json.dumps({"pseudo": "test"}).encode('utf-8'),
        params={}
    )

    resp = app.postUser(req, existingUser=[], outputDocument=None)
    assert resp.status_code == 400
    assert "Missing required fields" in resp.get_body().decode()