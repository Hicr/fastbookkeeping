#!/usr/bin/python3
import pymysql
import flask
import json
import datetime
import uuid
from functools import wraps
from flask import make_response


server = flask.Flask(__name__)

MYSQL_PARAMS = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "******",
    "database": "bookkeeping",
    "charset": "utf8"
}
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

@server.route('/ylbk/login',methods=['post'])
@allow_cross_domain
def login():
    today = datetime.datetime.today()
    today_time = today.strftime("%Y-%m-%d")
    print(today_time)
    username = flask.request.values.get('username')
    pwd = flask.request.values.get('pwd')
    if(username and pwd):
        user = queryUser(username,pwd)
        if(user):
            return result_handler('success', user)
        else:
            return result_handler('error', '登录失败')

@server.route('/ylbk/bookkeeping',methods=['post'])
@allow_cross_domain
def bookkeeping():
    userid = flask.request.values.get('userid')
    money_type = flask.request.values.get('type')
    money_desc = flask.request.values.get('desc')
    money = flask.request.values.get('money')
    if(flask.request.values.get('day')):
        if (money and money_desc and money_type):
            money_result = insert_bk(money_type, money_desc, money, userid,flask.request.values.get('day'))
            if (money_result):
                return result_handler('success', None)
            else:
                return result_handler('error', '插入数据遇到异常')
    else:
        if(money and money_desc and money_type):
            money_result = insert_bk(money_type,money_desc,money,userid,None)
            if(money_result):
                return result_handler('success', None)
            else:
                return result_handler('error', '插入数据遇到异常')

@server.route('/ylbk/querybkToday',methods=['post'])
@allow_cross_domain
def querybookkeepingToday():
    userid = flask.request.values.get('userid')
    today_monays = querybkTody(userid)
    if(today_monays):
        return result_handler('success', today_monays)
    else:
        return result_handler('success', [])

@server.route('/ylbk/statistics',methods=['post'])
@allow_cross_domain
def queryStatistics():
    userid = flask.request.values.get('userid')
    today = datetime.datetime.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    today_time = today.strftime("%Y-%m-%d")
    yesterday_time = yesterday.strftime("%Y-%m-%d")
    mounth = today.strftime("%Y-%m")
    # 1.查询今日总数
    t_sum = queryStody(userid,today_time)
    # 2.查询与昨日对比
    y_sum = queryStody(userid, yesterday_time)
    # 3.查询本月总数
    tm_sum = queryStody(userid, mounth)
    d_sum = 0
    stats = 0
    if(t_sum > y_sum):
        print('正 今日花销大')
        stats = 1
        d_sum = t_sum - y_sum
    elif(t_sum < y_sum):
        print('负 ')
        stats = 0
        d_sum = y_sum - t_sum
    else:
        print('平')
        stats = 2
        d_sum = 0
    data = {
        'todaySum' : t_sum,
        'yesSum' : y_sum,
        'tmSum':tm_sum,
        'stats':stats,
        'dSum':d_sum
    }
    return result_handler('success', data)

@server.route('/ylsc/d1',methods=['get'])
@allow_cross_domain
def querySCd1():
    userid = flask.request.values.get('userid')
    day = flask.request.values.get('day')
    d1result = []
    if (userid and day):
        d1list = querySCd1dao(userid,day)
        if(len(d1list) > 0):
            for d1item in d1list:
                d1item_temp = []
                d1item_temp.append(d1item[0])
                d1item_temp.append(float(d1item[1]))
                d1result.append(d1item_temp)
        return result_handler('success',d1result)
    else:
        return result_handler('success', [])


@server.route('/ylsc/m1',methods=['get'])
@allow_cross_domain
def querySCm1():
    userid = flask.request.values.get('userid')
    month = flask.request.values.get('month')
    m1result = []
    if(userid and month):
        m1list = querySCm1dao(userid, month)
        if (len(m1list) > 0):
            for m1item in m1list:
                m1item_temp = []
                m1item_temp.append(m1item[0])
                m1item_temp.append(float(m1item[1]))
                m1result.append(m1item_temp)
        return result_handler('success', m1result)
    else:
        return result_handler('success', [])


@server.route('/ylsc/m2',methods=['get'])
@allow_cross_domain
def querySCm2():
    userid = flask.request.values.get('userid')
    month = flask.request.values.get('month')
    m2result = []
    m2sum = 0
    m2big = 0
    if (userid and month):
        m2list = querySCm2dao(userid,month)
        m2map = {}
        if(len(m2list) > 0):
            for m2item in m2list:
                if(m2item[2] in m2map):
                    num = m2map.get(m2item[2])
                    m2map[m2item[2]] = num + float(m2item[3])
                    m2sum = m2sum + float(m2item[3])
                    if float(m2item[3]) > m2big:
                        m2big = float(m2item[3])
                else:
                    m2map[m2item[2]] = float(m2item[3])
                    m2sum = m2sum + float(m2item[3])
                    if float(m2item[3]) > m2big:
                        m2big = float(m2item[3])

            for key in m2map:
                m2temp = {}
                name = key
                money = m2map[key]
                point = format_percentage(money,m2sum)
                if money == m2big:
                    print()
                    m2temp['name'] = name
                    m2temp['y'] = float(point)
                    m2temp['sliced'] = True
                    m2temp['selected'] = True
                    m2result.append(m2temp)
                else:
                    m2temp['name'] = name
                    m2temp['y'] = float(point)
                    m2result.append(m2temp)
        return result_handler('success', m2result)
    else:
        return result_handler('error', '缺少参数')


@server.route('/ylsc/m3',methods=['get'])
@allow_cross_domain
def querySCm3():
    userid = flask.request.values.get('userid')
    month = flask.request.values.get('month')
    if (userid and month):
        # 同一个查询逻辑
        m3list = querySCm2dao(userid,month)
        m3result = {}
        m3cata = []
        m3charts = []
        m3map = {}
        if (len(m3list) > 0):
            for m3item in m3list:
                today = m3item[5][5:10]
                if (today in m3map):
                    num = m3map.get(today)
                    m3map[today] = num + float(m3item[3])

                else:
                    m3map[today] = float(m3item[3])
            for key in m3map:
                m3cata.append(key)
                m3charts.append(m3map[key])
            m3result['cata'] = m3cata
            m3result['charts'] = m3charts
            return result_handler('success', m3result)
        else:
            return result_handler('error', '未查询出结果')
    else:
        return result_handler('error', '缺少参数')



@server.route('/ylsc/y1', methods=['get'])
@allow_cross_domain
def querySCy1():
    userid = flask.request.values.get('userid')
    year = flask.request.values.get('year')
    if (userid and year):
        # 同一个查询逻辑
        y1list = querySCy1dao(userid,year)
        y1result = {}
        y1cata = []
        y1charts = []
        y1map = {}
        if (len(y1list) > 0):
            for y1item in y1list:
                today = y1item[5][5:7]
                if (today in y1map):
                    num = y1map.get(today)
                    y1map[today] = num + float(y1item[3])
                else:
                    y1map[today] = float(y1item[3])
            for key in y1map:
                y1cata.append(key)
                y1charts.append(y1map[key])
            y1result['cata'] = y1cata
            y1result['charts'] = y1charts
            return result_handler('success', y1result)
        else:
            return result_handler('error', '未查询出结果')
    else:
        return result_handler('error', '缺少参数')

@server.route('/ylsc/y2',methods=['get'])
@allow_cross_domain
def querySCy2():
    userid = flask.request.values.get('userid')
    year = flask.request.values.get('year')
    if (userid and year):
        y2list = querySCy2dao(userid,year)
        y2result = []
        if(len(y2list) > 0):
            for y2item in y2list:
                y2temp = {}
                y2temp['name'] = y2item[0]
                y2temp['weight'] = y2item[1]
                y2result.append(y2temp)
            return  result_handler('success', y2result)
        else:
            return result_handler('error', '未查询出结果')
    else:
        return result_handler('error', '缺少参数')




# 后续考虑分页问题
@server.route('/ylmanager/list',methods=['get'])
@allow_cross_domain
def queryManagerList():
    userid = flask.request.values.get('userid')
    type = flask.request.values.get('type')
    desc = flask.request.values.get('descs')
    date = flask.request.values.get('date')
    money = flask.request.values.get('money')
    if(userid):
        sql = getQueryListSql(userid,date,money,type,desc)
        result_list = queryManagerList(sql)
        moneylist = []
        if(len(result_list) > 0):
            for item in result_list:
                money_object = {}
                money_object['date'] = item[5][0:10]
                money_object['type'] = item[1]
                money_object['money'] = item[3]
                money_object['desc'] = item[2]
                money_object['id'] = item[0]
                moneylist.append(money_object)
            return result_handler('success', moneylist)
        else:
            return result_handler('error', [])
    return []

@server.route('/ylmanager/edit',methods=['get'])
@allow_cross_domain
def editManagerItem():
    userid = flask.request.values.get('userid')
    id = flask.request.values.get('id')
    money = flask.request.values.get('money')
    if(userid and id and money):
        editManagerItemDao(id,money,userid)
        return result_handler('success',[])
    else:
        return result_handler('error',[])

@server.route('/ylmanager/delete',methods=['get'])
@allow_cross_domain
def deleteManagerItem():
    userid = flask.request.values.get('userid')
    id = flask.request.values.get('id')
    if(userid and id):
        deleteManagerDao(id,userid)
        return result_handler('success',[])
    else:
        return result_handler('error',[])



def queryStody(userid,day):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " SELECT money " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + day + "%'"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        monays = cursor.fetchall()
        print(len(monays))
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    sum = 0
    if(monays and len(monays) >0):

        for monays_i in monays:
            print(float(monays_i[0]))
            sum = sum + float(monays_i[0])
    return sum



def querybkTody(userid):
    today = datetime.datetime.today()
    today_time = today.strftime("%Y-%m-%d")
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " SELECT * " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + today_time + "%' order by today desc"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        today_monays = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    if(len(today_monays) >0):
        todays = []
        for item in today_monays:
            toitem = {}
            toitem['id'] = item[0]
            toitem['type'] = item[1]
            toitem['desc'] = item[2]
            toitem['money'] = item[3]
            toitem['userid'] = item[4]
            toitem['today'] = item[5][11:16]
            todays.append(toitem)
        return todays
    else:
        return []



# 用户权限查询
def queryUser(userid,pwd):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " SELECT id,userid,pwd " \
          " FROM yl_user where userid = '" + userid + "' and pwd = '" + pwd + "'"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        users = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    print(users)
    if(len(users) > 0):
        return userid;
    else:
        return None

def querySCd1dao(userid,today):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " SELECT type,SUM(money) " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + today + "%' GROUP BY type"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        q1list = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    return q1list

def querySCm1dao(userid,tomonth):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " SELECT type,SUM(money) " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + tomonth + "%' GROUP BY type"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        m1list = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    return m1list

def querySCm2dao(userid,tomonth):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " select * " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + tomonth + "%' order by today desc"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        m2list = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    print(m2list)
    return m2list

def querySCy1dao(userid,year):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " select * " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + year + "%' order by today desc"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        y1list = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    print(y1list)
    return y1list

def querySCy2dao(userid,year):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = " select `desc`,count(`desc`) as num " \
          " FROM bookkeeping where userid = '" + userid + "' and today like '" + year + "%' GROUP BY `desc`"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        y2list = cursor.fetchall()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    print(y2list)
    return y2list
# 插入
def insert_bk(type,desc,money,userid,day):
    today = datetime.datetime.today()
    uuid_id = uuid.uuid4()
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO `"+MYSQL_PARAMS['database']+"`.`bookkeeping` (`id`, `type`, `desc`, `money`, `userid`, `today`) VALUES (%s,%s,%s,%s,%s,%s);"
    datas = []
    datas.append(uuid_id)
    datas.append(type)
    datas.append(desc)
    datas.append(money)
    datas.append(userid)
    if(day):
        datas.append(day)
    else:
        datas.append(today)
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql,datas)
        # cursor.executemany(sql, datas)
        conn.commit()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()
    return True

def getQueryListSql(userid,date,money,type,desc):
    sql = "select * From bookkeeping "
    if(userid):
        sql = sql + "where userid = '" + userid + "' "
        if(type):
            sql = sql + " and type = '" + type + "' "
        if(desc):
            sql = sql + " and `desc` like '%" + desc + "%' "
        if(money):
            sql = sql + " and money = '" + money + "' "
        if(date):
            sql = sql + " and today like '" + date + "%' "
        sql = sql + " order by today desc"
        return sql
    else:
        return None


def queryManagerList(sql):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    if(sql):
        print(sql)
        try:
            # 执行sql语句
            # mysql查询得这样
            cursor.execute(sql)
            monayslist = cursor.fetchall()
        except Exception as e:
            print('query data error', e)
            # 关闭数据库连接
        cursor.close()
        conn.close()
        if(len(monayslist) >0):
            return monayslist
        else:
            return []
    else:
        return []

def editManagerItemDao(id,money,userid):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = "Update bookkeeping set money = '" + money + "' where id = '" + id + "' and userid = '" + userid + "'"
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()


def deleteManagerDao(id,userid):
    conn = pymysql.connect(
        user=MYSQL_PARAMS["user"],
        password=MYSQL_PARAMS["password"],
        host=MYSQL_PARAMS["host"],
        port=MYSQL_PARAMS["port"],
        database=MYSQL_PARAMS["database"],
        charset='utf8'
    )
    sql = "delete from bookkeeping where id = '" + id + "' and userid = '" + userid + "'";
    cursor = conn.cursor()
    print(sql)
    try:
        # 执行sql语句
        # mysql查询得这样
        cursor.execute(sql)
        # monayslist = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print('query data error', e)
        # 关闭数据库连接
    cursor.close()
    conn.close()


def format_percentage(a, b):
	p = 100 * a / b
	if p == 0.0:
		q = '0'
	else:
		q = f'%.2f' % p
	return q

def result_handler(type,data):
    if(type == 'success'):
        if(data):
            # res = {'message': 'success!', 'code': 200, 'data': json.dumps(data,ensure_ascii=False)}
            res = {'message': 'success!', 'code': 200, 'data': data}
            return json.dumps(res,ensure_ascii=False)
        else:
            res = {'message': 'success!', 'code': 200}
            return json.dumps(res, ensure_ascii=False)
    else:
        if(data):
            res = {'message': 'error!', 'code': 500, 'data': json.dumps(data, ensure_ascii=False)}
            return json.dumps(res, ensure_ascii=False)
        else:
            res = {'message': 'error!', 'code': 500}
            return json.dumps(res, ensure_ascii=False)



server.run(port=9988, debug=True,host='0.0.0.0')