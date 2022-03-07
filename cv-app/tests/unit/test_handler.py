import os
import re
import json
from unittest import mock

from function import app

with open('../../template.yaml', 'r') as f:
    TABLENAME = re.search(r'TableName: (.*)?', f.read()).group(1)

@mock.patch.dict(os.environ, {"TABLENAME": TABLENAME})
def test_lambda_handler():
    ret = app.lambda_handler("", "")

    # assert return keys
    assert "statusCode" in ret
    assert "headers" in ret
    assert "body" in ret

    # check headers for CORS
    assert "Access-Control-Allow-Origin" in ret["headers"]
    assert "Access-Control-Allow-Methods" in ret["headers"]
    assert "Access-Control-Allow-Headers" in ret["headers"]

    # check status code
    if ret["statusCode"] == 200:
        # check body, count
        assert "Count" in ret["body"]
        assert json.loads(ret["body"])["Count"].isnumeric()
    else:
        assert json.loads(ret["body"])["Count"] == -1

    return