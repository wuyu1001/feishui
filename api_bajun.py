from utils import DbConnect
import time
import hashlib

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    print(m.hexdigest())
    return m.hexdigest()


def get_bajun_params():
    head = get_jf_head()
    data = get_jf_data()
    params = {"head": head, "data": data.as_dict()}

def get_jf_data():
    conn = DbConnect("oracle", "user_ods", "xjcz#123", "192", "1521", "192.169.1.121")
    db = conn.db_connect()
    data = db.query("select studno, studname, idno, periodid, periodname, entryid, entryname, amountys, amountss, amountqf, status, info from t_fs_jsfs where flag = 0")
    db.query("update t_fs_jsfs set flag = 1 where flag = 0")

    return data

def get_jf_head():
    timestamp = time.time()
    nonce = "12123123232"
    accesskey = "1000000000000001"
    secretkey = "QfxTYpSk2FlT5tTP5sWl"
    signature = secretkey + timestamp + nonce + accesskey
    signature = md5(signature)
    head = {"timestamp": timestamp, "nonce": nonce, "accesskey": accesskey, "signature": signature}

    return head

