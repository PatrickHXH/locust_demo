import pymysql
import requests

def headers_vcz(phone:int):
    '''
    登录车主小程序
    '''
    # 连接数据库
    conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727", db="cbf")
    # 创建游标
    cur = conn.cursor()
    sql = "SELECT id FROM tb_cz_user WHERE phone = %d and agency_type = 2"%(phone)
    # 执行游标
    cur.execute(sql)
    id = cur.fetchall()

    url_login = "http://test.chebufan.cn/vcd/api/cz/czuser/maUser/testlogin"
    headers = {"Content-Type": 'application/json;charset=UTF-8'}
    json = {
        "timeStamp": 1612265639,
        "nosign": 1111,
        "data": {
            "code": id[0][0],
            "appId": "wx467d93d7f179a217",
            "encryptedData": "",
            "iv": ""
        }
    }
    login = requests.post(url_login, headers=headers, json=json)
    print(login)
    token_vcz = login.json()['data']['token']
    headers_vcz = {"Content-Type": 'application/json;charset=UTF-8', "cz-token": token_vcz, "qd": "VCHEDIAN"}
    return headers_vcz

def headers_vcd(phone:int):
    '''
    登录车店小程序
    '''
    # 连接数据库
    conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727", db="cbf")
    # 创建游标
    cur = conn.cursor()
    sql = "SELECT id FROM tb_bz_user WHERE phone = %d and agency_type = 2"%(phone)
    # 执行游标
    cur.execute(sql)
    id = cur.fetchall()
    url_login = "http://test.chebufan.cn/vcd/api/open/bzuser/maUser/testlogin"
    headers = {"Content-Type": 'application/json;charset=UTF-8'}
    json = {
        "timeStamp": 1612265639,
        "nosign": 1111,
        "data": {
            "code": id[0][0],
            "appId": "wxde0940347260a768",
            "encryptedData": "",
            "iv": ""
        }
    }
    login = requests.post(url_login, headers=headers, json=json)
    token_vcd = login.json()['data']['token']
    headers_vcd = {"Content-Type": 'application/json;charset=UTF-8', "bz-token": token_vcd, "qd": "VCHEDIAN"}
    return headers_vcd

def cookies_headers_gzh(account:str,password:str):
    '''
    登录公众号
    '''
    import requests
    url_login = "http://test.chebufan.cn/chebftest/wx/xlc/account/loginByPassword"
    data = {"account": account, "password": password}
    login = requests.post(url_login, data=data)
    token = login.json()["returnParm"]["token"]
    #         global wz_headers
    #         wz_headers = {"Content-Type":"application/json","SYS-TOKEN":token,"qd":"CHEBUFANSHB"}
    cookies_gzh = {"SESSION": login.cookies['SESSION'],"VCHEDIAN-TOKEN":token}
    old_cookies_gzh = {"OLD-SESSION": login.cookies['SESSION']}
    headers_gzh = {"Content-Type": "application/json;charset=UTF-8",
                             "Referer":"http://test.chebufan.cn/chebftest/vue/view/xlc/directRelationship?keepAlive=true&qd=VCHEDIAN",
                            "Origin":"http://test.chebufan.cn",
                            "Connection":"keep-alive",
                            "Host":"test.chebufan.cn",
                            "Accept":"application/json, text/plain, */*"}
    headers_gzh_check = {"Content-Type": "application/json;charset=UTF-8",
                             "Referer":"http://test.chebufan.cn/chebftest/vue/view/xlc/autoOffer?qd=VCHEDIAN",
                            "Origin":"http://test.chebufan.cn",
                            "Connection":"keep-alive",
                            "Host":"test.chebufan.cn",
                            "Accept":"application/json, text/plain, */*"}
    return cookies_gzh,old_cookies_gzh,headers_gzh,headers_gzh_check

def headers_cxgj():
    '''
    登录报价员端

    '''
    import pymysql
    import requests
    null = None
    url = "http://zdbjtest.jximec.com/zdbj/cxyqzx/api/quoter/account/login"
    json = {"data":{"agentId":"15800190442","agentAuth":"e99a18c428cb38d5f260853678922e03","imgValidCodeId":null,"imgValidCodeText":""},"timestamp":1650266483204,"sign":"nosign"}
    login = requests.post(url,json=json)
    token = login.json()["data"]["token"]
    headers = {"Content-Type": 'application/json;charset=UTF-8',"Q-Token": token}
    # cookie_token = {"Bjy-Token": token}
    return headers

def headers_admin():
    '''
    登录车店管家管理后台
    '''
    url_login = "http://test.chebufan.cn/vcd/api/admin/token/login"
    headers = {"Content-Type": 'application/json;charset=UTF-8'}
    json = {"timestamp": 1629771682597, "sign": "nosign",
            "data": {"agentId": "admin", "agentAuth": "8943e202da22b47012a91c74a0c4fccd", "imgValidCodeText": ""}}
    login = requests.post(url_login, headers=headers, json=json)
    token_admin = login.json()['data']['token']
    headers_admin = {"Content-Type": 'application/json;charset=UTF-8', "x-token": token_admin, "qd": "VCHEDIAN"}
    return headers_admin

def headers_admin_formdata():
    '''
    登录车店管家管理后台
    '''
    url_login = "http://test.chebufan.cn/vcd/api/admin/token/login"
    headers = {"Content-Type": 'application/json;charset=UTF-8'}
    json = {"timestamp": 1629771682597, "sign": "nosign",
            "data": {"agentId": "admin", "agentAuth": "8943e202da22b47012a91c74a0c4fccd", "imgValidCodeText": ""}}
    login = requests.post(url_login, headers=headers, json=json)
    token_admin = login.json()['data']['token']
    headers_admin = {"x-token": token_admin, "qd": "VCHEDIAN"}
    return headers_admin
    # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryH9F7XgrUhHZmnnw9'

def CzAccountId(phone:int):
    '''
    车主accountid
    '''
    # 连接数据库
    conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727", db="cbf")
    # 创建游标
    cur = conn.cursor()
    sql = "SELECT id FROM tb_cz_account WHERE account = %d"%(phone)
    # 执行游标
    cur.execute(sql)
    id = cur.fetchall()
    return id[0][0]


