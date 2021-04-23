import json
from concurrent.futures import ThreadPoolExecutor
import datacompy
from flask import Flask
from config import dbConfig
from config.ext import db
import pandas as pd
from flask import render_template, request
from flask_cors import CORS
from models.bjxx import bjxxModel, bjxxCwModel, bjxxUploadModel
from models.xsxx import xsxxModel, xsxxCwModel, xsxxUploadModel
from models.yxxx import yxxxModel, yxxxCwModel, yxxxUploadModel
from models.zyxx import zyxxModel, zyxxCwModel, zyxxUploadModel
import config.feishuiconfig as fs_config
import requests as rs
from flask_migrate import Migrate


app = Flask(__name__, template_folder='templates/feishui/dist', static_folder="templates/feishui/dist/static")
app.config.from_object(dbConfig.Config)


app.config["SQLALCHEMY_ECHO"] = True

CORS(app, cors_allowed_origins="*")
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)


fs_set = fs_config.config

executor = ThreadPoolExecutor(max_workers=12)


@app.route('/compare/<dataType>/<pagesize>/<page>')
def compareData(dataType, pagesize, page):
    total_new = 0
    total_change = 0
    df1 = pd.read_sql(
        "select xh, xm, xb, csrq, csd, jg, mzm, gjdq, sfzjlxm, sfzjlxmc, sfzjh, xjzt, xslbm, xslbmc, szbh, sznj, yxsh, zyh, xz, frxnd, flxnd, xkml, xsdqzt, xqdm, fzsbs, flsh, bdtime, bz, qyzt from zzjg_xsxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select xh, xm, xb, csrq, csd, jg, mzm, gjdq, sfzjlxm, sfzjlxmc, sfzjh, xjzt, xslbm, xslbmc, szbh, sznj, yxsh, zyh, xz, frxnd, flxnd, xkml, xsdqzt, xqdm, fzsbs, flsh, bdtime, bz, qyzt from zzjg_xsxx_CW where flsh in (select flsh from zzjg_xsxx where is_changed = '1')",
        db.engine)
    compare = datacompy.Compare(df1, df2, join_columns=['flsh'])
    # print(compare.report())

    page = int(page)
    pagesize = int(pagesize)
    # 只存在于第一个dataframe的数据 不存在第二个dataframe的数据 用df1_unq_rows拿到
    df_new = pd.read_sql(
        "select xh, xm, xb, csrq, csd, jg, mzm, gjdq, sfzjlxm, sfzjlxmc, sfzjh, xjzt, xslbm, xslbmc, szbh, sznj, yxsh, zyh, xz, frxnd, flxnd, xkml, xsdqzt, xqdm, fzsbs, flsh, bdtime, bz, qyzt from zzjg_xsxx where flsh not in (select flsh from zzjg_xsxx_cw)",
        db.engine)
    total_new = len(df_new)
    # 2个dataframe 标识列一样 任意一个字段不一样的数据 用all_mismatch拿到
    df_change = compare.all_mismatch()
    total_change = len(df_change)
    df_new = df_new[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    df_change = df_change[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    if (dataType == 'new'):
        return_data = {'total': total_new, "data": df_new.to_dict(orient='records')}
        return return_data
    if (dataType == 'change'):
        return_data = {'total': total_change, "data": df_change.to_dict(orient='records')}
        return return_data


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/table/<tablename>/<pagesize>/<page>', methods=["POST"])
def table(tablename, pagesize, page):
    search_value = request.json.get("search_value") if request.json.get("search_value") else ''
    total = 0
    for aa in db.session.execute('select  count(1) sl from ' + tablename + ' ' + search_value):
        total = aa.sl
    pagesize = int(pagesize)
    page = int(page)
    start_row = pagesize * (page - 1) + 1
    end_row = (pagesize * page) + 1
    sql = ''' SELECT *
         FROM (SELECT tt.*, ROWNUM AS rowno
          FROM (  SELECT t.*
                    FROM {} t {}
                ORDER BY rowid ) tt
         WHERE ROWNUM < {}) a
         WHERE a.rowno >= {}
    '''.format(tablename, search_value, end_row, start_row)
    df = pd.read_sql(sql, db.engine)
    return_data = {'total': total, "data": df.to_dict(orient='records')}
    return return_data


@app.route('/modifyTable/<tablename>', methods=["POST"])
def modifyTable(tablename):
    par = request.json
    # 这2个字段 一个分页的临时属性 一个前端用来编辑行的临时属性 不是表的字段 干掉
    try:
        par.pop('rowno')
        par.pop('is_edit')
        if (tablename == 'zzjg_xsxx'):
            xsxxModel.query.filter_by(flsh=par.get('flsh')).update(par)
        if (tablename == 'zzjg_xsxx_cw'):
            xsxxCwModel.query.filter_by(flsh=par.get('flsh')).update(par)
        db.session.commit()
        return "修改成功"
    except Exception as e:
        return "修改失败"


@app.route('/create_upload_data', methods=["POST"])
def create_upload_data():
    db.session.execute('truncate  table zzjg_xsxx_upload')
    db.session.commit()
    df1 = pd.read_sql(
        "select xh, xm, xb, csrq, csd, jg, mzm, gjdq, sfzjlxm, sfzjlxmc, sfzjh, xjzt, xslbm, xslbmc, szbh, sznj, yxsh, zyh, xz, frxnd, flxnd, xkml, xsdqzt, xqdm, fzsbs, flsh, bdtime, bz, qyzt from zzjg_xsxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select xh, xm, xb, csrq, csd, jg, mzm, gjdq, sfzjlxm, sfzjlxmc, sfzjh, xjzt, xslbm, xslbmc, szbh, sznj, yxsh, zyh, xz, frxnd, flxnd, xkml, xsdqzt, xqdm, fzsbs, flsh, bdtime, bz, qyzt from zzjg_xsxx_CW where flsh in (select flsh from zzjg_xsxx where is_changed = '1')",
        db.engine)

    compare = datacompy.Compare(df1, df2, join_columns=['flsh'])
    df_new = pd.read_sql(
        "select xh, xm, xb, csrq, csd, jg, mzm, gjdq, sfzjlxm, sfzjlxmc, sfzjh, xjzt, xslbm, xslbmc, szbh, sznj, yxsh, zyh, xz, frxnd, flxnd, xkml, xsdqzt, xqdm, fzsbs, flsh, bdtime, bz, qyzt from zzjg_xsxx where flsh not in (select flsh from zzjg_xsxx_cw)",
        db.engine)
    # 新数据实际操作状态为 1
    df_new['sjcz'] = '1'
    all_new = [xsxxUploadModel(**stu) for stu in df_new.to_dict(orient='records')]
    db.session.add_all(all_new)
    db.session.commit()
    # df_new.to_sql('zzjg_xsxx_upload', db.engine, index=False, if_exists='append')
    df_change = compare.all_mismatch()
    list = df_change['flsh'].tolist()
    data_change = xsxxModel.query.filter(xsxxModel.flsh.in_(list)).all()
    all_change = [xsxxUploadModel(**stu.to_dict()) for stu in data_change]
    # 老数据数据实际操作状态为 2
    for a in all_change:
        a.sjcz = '2'
    db.session.add_all(all_change)
    db.session.commit()
    return "生成成功"


# @socketio.on('beginupload')
# def beginupload():
#     socketio.emit('beginupload', '已开始上传')
#     upload_data_2_feishui()


def upload(stu_data):
    with app.app_context():
        aa = "[" + json.dumps(stu_data.to_dict()) + "]"
        result = rs.post("http://127.0.0.1:8081/upload_stuinfo_feishui",
                         json.dumps({"arrinfo": aa}),
                         headers={"Content-Type": "application/json"}).text
        result = json.loads(result)
        xsxxModel.query.filter(xsxxModel.flsh == stu_data.flsh).update({'is_changed':'0'})
        xsxxCwModel.query.filter(xsxxCwModel.flsh == stu_data.flsh).delete()
        xsxxUploadModel.query.filter(xsxxUploadModel.flsh == stu_data.flsh).delete()
        db.session.commit()
        bb = xsxxCwModel(**stu_data.to_dict())
        bb.flag = "9"
        db.session.add(bb)
        db.session.commit()
        print(result)

@app.route('/beginupload', methods=["POST"])
def upload_data_feishui():
    arrinfo = xsxxUploadModel.query.all()
    future_to_url = {executor.submit(upload, arr)  for arr in arrinfo}
    # for arr in arrinfo:
    #     executor.submit(upload, arr)
    return "开始上传，请等待几分钟后刷新页面"



# 对比班级信息表
@app.route('/compare3/<dataType>/<pagesize>/<page>')
def compareData3(dataType, pagesize, page):
    total_new = 0
    total_change = 0
    df1 = pd.read_sql(
        "select nj, bh, bjmc, zyh, xqdm, bjrs, fdydh, fdysfzjh, xz, frxnd, flxnd, yxsh from zzjg_bjxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select nj, bh, bjmc, zyh, xqdm, bjrs, fdydh, fdysfzjh, xz, frxnd, flxnd, yxsh from zzjg_bjxx_CW where bh in (select bh from zzjg_bjxx where is_changed = '1')",
        db.engine)
    compare = datacompy.Compare(df1, df2, join_columns=['bh'])
    # print(compare.report())

    page = int(page)
    pagesize = int(pagesize)
    # 只存在于第一个dataframe的数据 不存在第二个dataframe的数据 用df1_unq_rows拿到
    df_new = pd.read_sql(
        "select nj, bh, bjmc, zyh, xqdm, bjrs, fdydh, fdysfzjh, xz, frxnd, flxnd, yxsh from zzjg_bjxx where bh not in (select bh from zzjg_bjxx_cw)",
        db.engine)
    total_new = len(df_new)
    # 2个dataframe 标识列一样 任意一个字段不一样的数据 用all_mismatch拿到
    df_change = compare.all_mismatch()
    total_change = len(df_change)
    df_new = df_new[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    df_change = df_change[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    if (dataType == 'new'):
        return_data = {'total': total_new, "data": df_new.to_dict(orient='records')}
        return return_data
    if (dataType == 'change'):
        return_data = {'total': total_change, "data": df_change.to_dict(orient='records')}
        return return_data


@app.route('/modifyTable3/<tablename>', methods=["POST"])
def modifyTable3(tablename):
    par = request.json
    # 这2个字段 一个分页的临时属性 一个前端用来编辑行的临时属性 不是表的字段 干掉
    try:
        par.pop('rowno')
        par.pop('is_edit')
        if (tablename == 'zzjg_bjxx'):
            bjxxModel.query.filter_by(flsh=par.get('bh')).update(par)
        if (tablename == 'zzjg_bjxx_cw'):
            bjxxCwModel.query.filter_by(flsh=par.get('bh')).update(par)
        db.session.commit()
        return "修改成功"
    except Exception as e:
        return "修改失败"


@app.route('/create_upload_data3', methods=["POST"])
def create_upload_data3():
    db.session.execute('truncate  table zzjg_bjxx_upload')
    db.session.commit()
    df1 = pd.read_sql(
        "select nj, bh, bjmc, zyh, xqdm, bjrs, fdydh, fdysfzjh, xz, frxnd, flxnd, yxsh from zzjg_bjxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select nj, bh, bjmc, zyh, xqdm, bjrs, fdydh, fdysfzjh, xz, frxnd, flxnd, yxsh from zzjg_bjxx_CW where bh in (select bh from zzjg_bjxx where is_changed = '1')",
        db.engine)

    compare = datacompy.Compare(df1, df2, join_columns=['bh'])
    df_new = pd.read_sql(
        "select nj, bh, bjmc, zyh, xqdm, bjrs, fdydh, fdysfzjh, xz, frxnd, flxnd, yxsh from zzjg_bjxx where bh not in (select bh from zzjg_bjxx_cw)",
        db.engine)
    # 新数据实际操作状态为 1
    df_new['sjcz'] = '1'
    all_new = [bjxxUploadModel(**stu) for stu in df_new.to_dict(orient='records')]
    db.session.add_all(all_new)
    db.session.commit()
    # df_new.to_sql('zzjg_xsxx_upload', db.engine, index=False, if_exists='append')
    df_change = compare.all_mismatch()
    list = df_change['flsh'].tolist()
    data_change = bjxxModel.query.filter(bjxxModel.flsh.in_(list)).all()
    all_change = [bjxxUploadModel(**stu.to_dict()) for stu in data_change]
    # 老数据数据实际操作状态为 2
    for a in all_change:
        a.sjcz = '2'
    db.session.add_all(all_change)
    db.session.commit()
    return "生成成功"



def upload3(stu_data):
    with app.app_context():
        aa = "[" + json.dumps(stu_data.to_dict()) + "]"
        result = rs.post("http://127.0.0.1:8081/upload_stuinfo_3_feishui",
                         json.dumps({"arrinfo": aa}),
                         headers={"Content-Type": "application/json"}).text
        result = json.loads(result)
        bjxxModel.query.filter(bjxxModel.bh == stu_data.bh).update({'is_changed':'0'})
        bjxxCwModel.query.filter(bjxxCwModel.bh == stu_data.bh).delete()
        bjxxUploadModel.query.filter(bjxxUploadModel.bh == stu_data.bh).delete()
        db.session.commit()
        bb = bjxxCwModel(**stu_data.to_dict())
        bb.flag = "9"
        db.session.add(bb)
        db.session.commit()
        print(result)

@app.route('/beginupload3', methods=["POST"])
def upload_data_3_feishui():
    arrinfo = bjxxUploadModel.query.all()
    future_to_url = {executor.submit(upload3, arr)  for arr in arrinfo}
    return "开始上传，请等待几分钟后刷新页面"


# 对比院系信息表
@app.route('/compare1/<dataType>/<pagesize>/<page>')
def compareData1(dataType, pagesize, page):
    total_new = 0
    total_change = 0
    df1 = pd.read_sql(
        "select yxsdm, yxsmc from zzjg_yxxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select yxsdm, yxsmc from zzjg_yxxx_CW where yxsdm in (select yxsdm from zzjg_yxxx where is_changed = '1')",
        db.engine)
    compare = datacompy.Compare(df1, df2, join_columns=['yxsdm'])
    # print(compare.report())

    page = int(page)
    pagesize = int(pagesize)
    # 只存在于第一个dataframe的数据 不存在第二个dataframe的数据 用df1_unq_rows拿到
    df_new = pd.read_sql(
        "select yxsdm, yxsmc from zzjg_yxxx where yxsdm not in (select yxsdm from zzjg_yxxx_cw)",
        db.engine)
    total_new = len(df_new)
    # 2个dataframe 标识列一样 任意一个字段不一样的数据 用all_mismatch拿到
    df_change = compare.all_mismatch()
    total_change = len(df_change)
    df_new = df_new[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    df_change = df_change[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    if (dataType == 'new'):
        return_data = {'total': total_new, "data": df_new.to_dict(orient='records')}
        return return_data
    if (dataType == 'change'):
        return_data = {'total': total_change, "data": df_change.to_dict(orient='records')}
        return return_data


@app.route('/modifyTable1/<tablename>', methods=["POST"])
def modifyTable1(tablename):
    par = request.json
    # 这2个字段 一个分页的临时属性 一个前端用来编辑行的临时属性 不是表的字段 干掉
    try:
        par.pop('rowno')
        par.pop('is_edit')
        if (tablename == 'zzjg_yxxx'):
            yxxxModel.query.filter_by(yxsdm=par.get('yxsdm')).update(par)
        if (tablename == 'zzjg_yxxx_cw'):
            yxxxCwModel.query.filter_by(yxsdm=par.get('yxsdm')).update(par)
        db.session.commit()
        return "修改成功"
    except Exception as e:
        return "修改失败"


@app.route('/create_upload_data1', methods=["POST"])
def create_upload_data1():
    db.session.execute('truncate  table zzjg_yxxx_upload')
    db.session.commit()
    df1 = pd.read_sql(
        "select yxsdm, yxsmc from zzjg_yxxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select yxsdm, yxsmc from zzjg_yxxx_CW where yxsdm in (select yxsdm from zzjg_yxxx where is_changed = '1')",
        db.engine)

    compare = datacompy.Compare(df1, df2, join_columns=['yxsdm'])
    df_new = pd.read_sql(
        "select yxsdm, yxsmc from zzjg_yxxx where yxsdm not in (select yxsdm from zzjg_yxxx_cw)",
        db.engine)
    # 新数据实际操作状态为 1
    df_new['sjcz'] = '1'
    all_new = [yxxxUploadModel(**stu) for stu in df_new.to_dict(orient='records')]
    db.session.add_all(all_new)
    db.session.commit()
    df_change = compare.all_mismatch()
    list = df_change['yxsdm'].tolist()
    data_change = yxxxModel.query.filter(yxxxModel.yxsdm.in_(list)).all()
    all_change = [yxxxUploadModel(**stu.to_dict()) for stu in data_change]
    # 老数据数据实际操作状态为 2
    for a in all_change:
        a.sjcz = '2'
    db.session.add_all(all_change)
    db.session.commit()
    return "生成成功"

def upload1(stu_data):
    with app.app_context():
        aa = "[" + json.dumps(stu_data.to_dict()) + "]"
        result = rs.post("http://127.0.0.1:8081/upload_stuinfo_1_feishui",
                         json.dumps({"arrinfo": aa}),
                         headers={"Content-Type": "application/json"}).text
        result = json.loads(result)
        yxxxModel.query.filter(yxxxModel.yxsdm == stu_data.yxsdm).update({'is_changed':'0'})
        yxxxCwModel.query.filter(yxxxCwModel.yxsdm == stu_data.yxsdm).delete()
        yxxxUploadModel.query.filter(yxxxUploadModel.yxsdm == stu_data.yxsdm).delete()
        db.session.commit()
        bb = yxxxCwModel(**stu_data.to_dict())
        bb.flag = "9"
        db.session.add(bb)
        db.session.commit()
        print(result)

@app.route('/beginupload1', methods=["POST"])
def upload_data_1_feishui():
    arrinfo = yxxxUploadModel.query.all()
    future_to_url = {executor.submit(upload1, arr)  for arr in arrinfo}
    return "开始上传，请等待几分钟后刷新页面"

# 对比专业信息表
@app.route('/compare2/<dataType>/<pagesize>/<page>')
def compareData2(dataType, pagesize, page):
    total_new = 0
    total_change = 0
    df1 = pd.read_sql(
        "select zyh, zwmc, ywmc, zyfxh, bzkzym, yjszym, ssxkdl, ssxk, xz, pycc, zylxdm, yxsh, xqdm from zzjg_zyxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select zyh, zwmc, ywmc, zyfxh, bzkzym, yjszym, ssxkdl, ssxk, xz, pycc, zylxdm, yxsh, xqdm from zzjg_zyxx_CW where zyh in (select zyh from zzjg_zyxx where is_changed = '1')",
        db.engine)
    compare = datacompy.Compare(df1, df2, join_columns=['zyh'])
    # print(compare.report())

    page = int(page)
    pagesize = int(pagesize)
    # 只存在于第一个dataframe的数据 不存在第二个dataframe的数据 用df1_unq_rows拿到
    df_new = pd.read_sql(
        "select zyh, zwmc, ywmc, zyfxh, bzkzym, yjszym, ssxkdl, ssxk, xz, pycc, zylxdm, yxsh, xqdm from zzjg_zyxx where zyh not in (select zyh from zzjg_zyxx_cw)",
        db.engine)
    total_new = len(df_new)
    # 2个dataframe 标识列一样 任意一个字段不一样的数据 用all_mismatch拿到
    df_change = compare.all_mismatch()
    total_change = len(df_change)
    df_new = df_new[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    df_change = df_change[(int(page) - 1) * int(pagesize): (int(page) * int(pagesize))]
    if (dataType == 'new'):
        return_data = {'total': total_new, "data": df_new.to_dict(orient='records')}
        return return_data
    if (dataType == 'change'):
        return_data = {'total': total_change, "data": df_change.to_dict(orient='records')}
        return return_data


@app.route('/modifyTable2/<tablename>', methods=["POST"])
def modifyTable2(tablename):
    par = request.json
    # 这2个字段 一个分页的临时属性 一个前端用来编辑行的临时属性 不是表的字段 干掉
    try:
        par.pop('rowno')
        par.pop('is_edit')
        if (tablename == 'zzjg_yxxx'):
            zyxxModel.query.filter_by(zyh=par.get('zyh')).update(par)
        if (tablename == 'zzjg_yxxx_cw'):
            zyxxCwModel.query.filter_by(zyh=par.get('zyh')).update(par)
        db.session.commit()
        return "修改成功"
    except Exception as e:
        return "修改失败"


@app.route('/create_upload_data2', methods=["POST"])
def create_upload_data2():
    db.session.execute('truncate  table zzjg_zyxx_upload')
    db.session.commit()
    df1 = pd.read_sql(
        "select zyh, zwmc, ywmc, zyfxh, bzkzym, yjszym, ssxkdl, ssxk, xz, pycc, zylxdm, yxsh, xqdm from zzjg_zyxx where is_changed ='1'",
        db.engine)
    df2 = pd.read_sql(
        "select zyh, zwmc, ywmc, zyfxh, bzkzym, yjszym, ssxkdl, ssxk, xz, pycc, zylxdm, yxsh, xqdm from zzjg_zyxx_CW where zyh in (select zyh from zzjg_zyxx where is_changed = '1')",
        db.engine)

    compare = datacompy.Compare(df1, df2, join_columns=['zyh'])
    df_new = pd.read_sql(
        "select zyh, zwmc, ywmc, zyfxh, bzkzym, yjszym, ssxkdl, ssxk, xz, pycc, zylxdm, yxsh, xqdm from zzjg_zyxx where zyh not in (select zyh from zzjg_zyxx_cw)",
        db.engine)
    # 新数据实际操作状态为 1
    df_new['sjcz'] = '1'
    all_new = [zyxxUploadModel(**stu) for stu in df_new.to_dict(orient='records')]
    db.session.add_all(all_new)
    db.session.commit()
    # df_new.to_sql('zzjg_xsxx_upload', db.engine, index=False, if_exists='append')
    df_change = compare.all_mismatch()
    list = df_change['zyh'].tolist()
    data_change = zyxxModel.query.filter(zyxxModel.zyh.in_(list)).all()
    all_change = [zyxxUploadModel(**stu.to_dict()) for stu in data_change]
    # 老数据数据实际操作状态为 2
    for a in all_change:
        a.sjcz = '2'
    db.session.add_all(all_change)
    db.session.commit()
    return "生成成功"



def upload2(stu_data):
    with app.app_context():
        aa = "[" + json.dumps(stu_data.to_dict()) + "]"
        result = rs.post("http://127.0.0.1:8081/upload_stuinfo_2_feishui",
                         json.dumps({"arrinfo": aa}),
                         headers={"Content-Type": "application/json"}).text
        result = json.loads(result)
        zyxxModel.query.filter(zyxxModel.zyh == stu_data.zyh).update({'is_changed':'0'})
        zyxxCwModel.query.filter(zyxxCwModel.zyh == stu_data.zyh).delete()
        zyxxUploadModel.query.filter(zyxxUploadModel.zyh == stu_data.zyh).delete()
        db.session.commit()
        bb = zyxxCwModel(**stu_data.to_dict())
        bb.flag = "9"
        db.session.add(bb)
        db.session.commit()
        print(result)

@app.route('/beginupload2', methods=["POST"])
def upload_data_2_feishui():
    arrinfo = zyxxUploadModel.query.all()
    future_to_url = {executor.submit(upload2, arr)  for arr in arrinfo}
    return "开始上传，请等待几分钟后刷新页面"

@app.route('/upload_to_bajun', methods=["POST"])
def upload_data_to_bajun():
    return "开始上传八骏，请等待几分钟后刷新页面"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
