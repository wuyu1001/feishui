from config.ext import db


class bjxxModel(db.Model):
    __tablename__ = "zzjg_bjxx"
    nj = db.Column(db.String(600)) # 入学年级
    bh = db.Column(db.String(600), primary_key=True) # 班号
    bjmc = db.Column(db.String(600)) # 班级名称
    zyh = db.Column(db.String(600)) # 专业号
    xqdm = db.Column(db.String(600)) # 校区代码 默认值 01
    bjrs = db.Column(db.String(600)) # 预设人数
    fdygh = db.Column(db.String(600)) # 辅导员工号
    fdysfzjh = db.Column(db.String(600)) # 辅导员身份证件号
    xz = db.Column(db.String(600)) # 学制
    frxnd = db.Column(db.String(600)) # 入学年度
    flxnd = db.Column(db.String(600)) # 离校年度
    yxsh = db.Column(db.String(600)) # 院系所号
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    qyzt = db.Column(db.String(600)) # T:启动 F:停用
    is_changed = db.Column(db.String(600)) # 是否改变 0，1
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class bjxxCwModel(db.Model):
    __tablename__ = "zzjg_bjxx_cw"
    nj = db.Column(db.String(600)) # 入学年级
    bh = db.Column(db.String(600), primary_key=True) # 班号
    bjmc = db.Column(db.String(600)) # 班级名称
    zyh = db.Column(db.String(600)) # 专业号
    xqdm = db.Column(db.String(600)) # 校区代码 默认值 01
    bjrs = db.Column(db.String(600)) # 预设人数
    fdygh = db.Column(db.String(600)) # 辅导员工号
    fdysfzjh = db.Column(db.String(600)) # 辅导员身份证件号
    xz = db.Column(db.String(600)) # 学制
    frxnd = db.Column(db.String(600)) # 入学年度
    flxnd = db.Column(db.String(600)) # 离校年度
    yxsh = db.Column(db.String(600)) # 院系所号
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    qyzt = db.Column(db.String(600)) # T:启动 F:停用
    flag = db.Column(db.String(600))
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class bjxxUploadModel(db.Model):
    __tablename__ = "zzjg_bjxx_upload"
    nj = db.Column(db.String(600)) # 入学年级
    bh = db.Column(db.String(600), primary_key=True) # 班号
    bjmc = db.Column(db.String(600)) # 班级名称
    zyh = db.Column(db.String(600)) # 专业号
    xqdm = db.Column(db.String(600)) # 校区代码 默认值 01
    bjrs = db.Column(db.String(600)) # 预设人数
    fdygh = db.Column(db.String(600)) # 辅导员工号
    fdysfzjh = db.Column(db.String(600)) # 辅导员身份证件号
    xz = db.Column(db.String(600)) # 学制
    frxnd = db.Column(db.String(600)) # 入学年度
    flxnd = db.Column(db.String(600)) # 离校年度
    yxsh = db.Column(db.String(600)) # 院系所号
    sjzc = db.Column(db.String(600)) # 1:新增2:修改
    qyzt = db.Column(db.String(600)) # T:启动 F:停用

    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


