from config.ext import db


# from config.ext import ma


class xsxxModel(db.Model):
    __tablename__ = "zzjg_xsxx"
    flsh = db.Column(db.String(600), primary_key=True)
    xh = db.Column(db.String(600))
    xm = db.Column(db.String(600))
    xb = db.Column(db.String(600))
    csrq = db.Column(db.String(600))
    csd = db.Column(db.String(600))
    jg = db.Column(db.String(600))
    mzm = db.Column(db.String(600))
    gjdq = db.Column(db.String(600))
    sfzjlxm = db.Column(db.String(600))
    sfzjlxmc = db.Column(db.String(600))
    sfzjh = db.Column(db.String(600))
    xjzt = db.Column(db.String(600))
    xslbm = db.Column(db.String(600))
    xslbmc = db.Column(db.String(600))
    szbh = db.Column(db.String(600))
    sznj = db.Column(db.String(600))
    yxsh = db.Column(db.String(600))
    zyh = db.Column(db.String(600))
    xz = db.Column(db.String(600))
    frxnd = db.Column(db.String(600))
    flxnd = db.Column(db.String(600))
    xkml = db.Column(db.String(600))
    xsdqzt = db.Column(db.String(600))
    xqdm = db.Column(db.String(600))
    qyzt = db.Column(db.String(600))
    fzsbs = db.Column(db.String(600))
    bdtime = db.Column(db.String(600))
    bz = db.Column(db.String(600))
    is_changed = db.Column(db.String(600))
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class xsxxCwModel(db.Model):
    __tablename__ = "zzjg_xsxx_cw"
    flsh = db.Column(db.String(600), primary_key=True)
    xh = db.Column(db.String(600))
    xm = db.Column(db.String(600))
    xb = db.Column(db.String(600))
    csrq = db.Column(db.String(600))
    csd = db.Column(db.String(600))
    jg = db.Column(db.String(600))
    mzm = db.Column(db.String(600))
    gjdq = db.Column(db.String(600))
    sfzjlxm = db.Column(db.String(600))
    sfzjlxmc = db.Column(db.String(600))
    sfzjh = db.Column(db.String(600))
    xjzt = db.Column(db.String(600))
    xslbm = db.Column(db.String(600))
    xslbmc = db.Column(db.String(600))
    szbh = db.Column(db.String(600))
    sznj = db.Column(db.String(600))
    yxsh = db.Column(db.String(600))
    zyh = db.Column(db.String(600))
    xz = db.Column(db.String(600))
    frxnd = db.Column(db.String(600))
    flxnd = db.Column(db.String(600))
    xkml = db.Column(db.String(600))
    xsdqzt = db.Column(db.String(600))
    xqdm = db.Column(db.String(600))
    qyzt = db.Column(db.String(600))
    fzsbs = db.Column(db.String(600))
    bdtime = db.Column(db.String(600))
    bz = db.Column(db.String(600))
    sjcz = db.Column(db.String(600))
    flag = db.Column(db.String(600))

    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class xsxxUploadModel(db.Model):
    __tablename__ = "zzjg_xsxx_upload"
    flsh = db.Column(db.String(600), primary_key=True)
    xh = db.Column(db.String(600))
    xm = db.Column(db.String(600))
    xb = db.Column(db.String(600))
    csrq = db.Column(db.String(600))
    csd = db.Column(db.String(600))
    jg = db.Column(db.String(600))
    mzm = db.Column(db.String(600))
    gjdq = db.Column(db.String(600))
    sfzjlxm = db.Column(db.String(600))
    sfzjlxmc = db.Column(db.String(600))
    sfzjh = db.Column(db.String(600))
    xjzt = db.Column(db.String(600))
    xslbm = db.Column(db.String(600))
    xslbmc = db.Column(db.String(600))
    szbh = db.Column(db.String(600))
    sznj = db.Column(db.String(600))
    yxsh = db.Column(db.String(600))
    zyh = db.Column(db.String(600))
    xz = db.Column(db.String(600))
    frxnd = db.Column(db.String(600))
    flxnd = db.Column(db.String(600))
    xkml = db.Column(db.String(600))
    xsdqzt = db.Column(db.String(600))
    xqdm = db.Column(db.String(600))
    qyzt = db.Column(db.String(600))
    fzsbs = db.Column(db.String(600))
    bdtime = db.Column(db.String(600))
    bz = db.Column(db.String(600))
    sjcz = db.Column(db.String(600))
    def __init__(self, **kwargs):
        for v, m in kwargs.items():
            self.__setattr__(v, m)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
