import json
from concurrent.futures import ThreadPoolExecutor
import datacompy
from flask import Flask
from config import dbConfig
from config.ext import db
import pandas as pd
from flask import render_template, request
from flask_cors import CORS
from models.xsxx import xsxxModel, xsxxCwModel, xsxxUploadModel
import config.feishuiconfig as fs_config
import requests as rs

app = Flask(__name__, template_folder='templates/feishui/dist', static_folder="templates/feishui/dist/static")
app.config.from_object(dbConfig.Config)
CORS(app, cors_allowed_origins="*")
db.init_app(app)

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
        result = rs.post("http://127.0.0.1:8081/upload_stuinfo_2_feishui",
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
def upload_data_2_feishui():
    arrinfo = xsxxUploadModel.query.all()
    future_to_url = {executor.submit(upload, arr)  for arr in arrinfo}
    # for arr in arrinfo:
    #     executor.submit(upload, arr)
    return "开始上传，请等待几分钟后刷新页面"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
