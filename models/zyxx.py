from config.ext import db


class zyxxModel(db.Model):
    __tablename__ = "zzjg_zyxx"
    zyh = db.Column(db.String(600), primary_key=True) # 专业号
    zwmc = db.Column(db.String(600)) # 专业中文名称
    ywmc = db.Column(db.String(600)) # 专业英文名称
    zyfxh = db.Column(db.String(600)) # 专业方向
    bzkzym = db.Column(db.String(600)) # 本专科专业码
    yjszym = db.Column(db.String(600)) # 研究生专业码
    ssxkdl = db.Column(db.String(600)) # 所属学科大类
    ssxk = db.Column(db.String(600)) # 所属学科
    xz = db.Column(db.String(600)) # 学制
    pycc = db.Column(db.String(600)) # 培养层次
    zylxdm = db.Column(db.String(600)) # 专业类型
    yxsh = db.Column(db.String(600)) # 院系所号
    xqdm = db.Column(db.String(600)) # 校区代码 默认值 01
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    qyzt = db.Column(db.String(600)) # T:启动 F:停用
    is_changed = db.Column(db.String(600)) # 是否改变 0，1
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class zyxxCwModel(db.Model):
    __tablename__ = "zzjg_zyxx_cw"
    zyh = db.Column(db.String(600), primary_key=True) # 专业号
    zwmc = db.Column(db.String(600)) # 专业中文名称
    ywmc = db.Column(db.String(600))
    zyfxh = db.Column(db.String(600))
    bzkzym = db.Column(db.String(600))
    yjszym = db.Column(db.String(600))
    ssxkdl = db.Column(db.String(600))
    ssxk = db.Column(db.String(600))
    xz = db.Column(db.String(600))
    pycc = db.Column(db.String(600))
    zylxdm = db.Column(db.String(600))
    yxsh = db.Column(db.String(600))
    xqdm = db.Column(db.String(600))
    sjzc = db.Column(db.String(600))
    qyzt = db.Column(db.String(600))
    flag = db.Column(db.String(600))
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class zyxxUploadModel(db.Model):
    __tablename__ = "zzjg_zyxx_upload"
    zyh = db.Column(db.String(600), primary_key=True) # 专业号
    zwmc = db.Column(db.String(600)) # 专业中文名称
    ywmc = db.Column(db.String(600))
    zyfxh = db.Column(db.String(600))
    bzkzym = db.Column(db.String(600))
    yjszym = db.Column(db.String(600))
    ssxkdl = db.Column(db.String(600))
    ssxk = db.Column(db.String(600))
    xz = db.Column(db.String(600))
    pycc = db.Column(db.String(600))
    zylxdm = db.Column(db.String(600))
    yxsh = db.Column(db.String(600))
    xqdm = db.Column(db.String(600))
    sjzc = db.Column(db.String(600))
    qyzt = db.Column(db.String(600))
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


