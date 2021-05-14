from config.ext import db


class userModel(db.Model):
    __tablename__ = "zzjg_user"
    username = db.Column(db.String(600)) # 用户名
    pwd = db.Column(db.String(600)) # 密码
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}




