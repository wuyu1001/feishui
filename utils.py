import records


class DbConnect:
    """
    不同数据库的连接方式
    """
    def __init__(self, db_type, username, password, host, port, db_name):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db_type = db_type

    def db_connect(self):
        if self.db_type == "mysql":
            database_url = "mysql://{}:{}@{}:{}/{}".format(
                self.username, self.password, self.host, self.port, self.db_name
            )
            db = records.Database(database_url, connect_args={"charset": "utf8"})
        if self.db_type == "oracle":
            try:
                database_url = "oracle+cx_oracle://{}:{}@{}:{}/?service_name={}".format(
                    self.username, self.password, self.host, self.port, self.db_name
                )
                db = records.Database(database_url)
            except:
                database_url = "oracle+cx_oracle://{}:{}@{}:{}/?sid={}".format(
                    self.username, self.password, self.host, self.port, self.db_name
                )
                db = records.Database(database_url)
        if self.db_type == "mssql":
            database_url = "mssql+pymssql://{}:{}@{}:{}/{}".format(
                self.username, self.password, self.host, self.port, self.db_name
            )
            db = records.Database(database_url, connect_args={"charset": "utf8"})
        return db
