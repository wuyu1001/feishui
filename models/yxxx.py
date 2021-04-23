from config.ext import db


class yxxxModel(db.Model):
    __tablename__ = "zzjg_yxxx"
    yxsdm = db.Column(db.String(600), primary_key=True) # 院系所代码
    yxsmc = db.Column(db.String(600)) # 院系所名称
    xqdm = db.Column(db.String(600)) # 校区代码 默认值01
    isok = db.Column(db.String(600)) # 启用标志 T:启用 F:为启用
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    is_changed = db.Column(db.String(600)) # 是否改变 0，1
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class yxxxCwModel(db.Model):
    __tablename__ = "zzjg_yxxx_cw"
    yxsdm = db.Column(db.String(600), primary_key=True) # 院系所代码
    yxsmc = db.Column(db.String(600)) # 院系所名称
    xqdm = db.Column(db.String(600)) # 校区代码 默认值01
    isok = db.Column(db.String(600)) # 启用标志 T:启用 F:为启用
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    flag = db.Column(db.String(600))
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class yxxxUploadModel(db.Model):
    __tablename__ = "zzjg_yxxx_upload"
    yxsdm = db.Column(db.String(600), primary_key=True) # 院系所代码
    yxsmc = db.Column(db.String(600)) # 院系所名称
    xqdm = db.Column(db.String(600)) # 校区代码 默认值01
    isok = db.Column(db.String(600)) # 启用标志 T:启用 F:为启用
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
