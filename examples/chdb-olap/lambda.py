import json
from chdb import session as chs

## Create DB, Table, View in temp session, auto cleanup when session is deleted.
sess = chs.Session()
sess.query("CREATE DATABASE IF NOT EXISTS db_xxx ENGINE = Atomic")
sess.query(
    "CREATE TABLE IF NOT EXISTS db_xxx.log_table_xxx (x String, y Int) ENGINE = Log;"
)
sess.query(
    "INSERT INTO db_xxx.log_table_xxx VALUES ('a', 1), ('b', 3), ('c', 2), ('d', 5);"
)
sess.query("CREATE VIEW db_xxx.view_xxx AS SELECT * FROM db_xxx.log_table_xxx LIMIT 4;")


def handler(event, context):

    query = event["query"]
    default_format = event.get("default_format", "JSONCompact")

    try:
        result = sess.query(query, default_format)
        result_json = result.rows_read()
        # result_json = result.data()
        return {"statusCode": 200, "body": json.dumps(result_json)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
