import gevent
from gevent import monkey
monkey.patch_all()
#gevent让我们可以按同步的方式来写异步程序
# monkey.patch_all()会在Python程序执行时动态的将网络库（socket, select, thread)，替换掉,变成异步的库，让我们的程序可以异步的方式处理网络相关的任务
from locust import HttpUser, task,TaskSet,run_single_user,between,SequentialTaskSet,events,LoadTestShape
from locust.contrib.fasthttp import FastHttpUser
from auth import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_admin_formdata,headers_cxgj
import datetime
import requests
import psutil
import os
import math

#创建任务类
class Test1(SequentialTaskSet):


    def on_start(self):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        global headersadmin
        headersadmin = headers_admin()

        # global headers_admin_formdata
        # headers_admin_formdata = headers_admin_formdata()

        global headersgzh
        headersgzh = cookies_headers_gzh(13538878368, 123456)

        global headerscxgj
        headerscxgj = headers_cxgj()

    # @task
    # def view_api(self):
    #     self.client.get("/hello")  # 这里的地址需要排除 host 部分
    #     self.client.get("/world")

    # @task
    def view_item1(self):
        # self.client.get(f"/item?id={item_id}", name="/item")
        url_flowAccountList = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/flowAccountList"
        for i in range(1,4):
            json = {"data":{"current":1,"size":10,"params":{"type":i},"total":1,"pages":0},"sign":"nosign","timestamp":1634798420205}
            flowAccountList = self.client.post(url_flowAccountList,json=json,headers=headersvcd,name="flowAccountList:%i"%(i))

    @task
    def view_item2(self):
        u'''订单—可查看到店单列表'''
        #查看到点单列表
        url_ycxReceivelist = "http://test.chebufan.cn/vcd/api/cz/receive/ycxReceive/page"
        json = {"data":{"current":1,"params":{"shopId":"1361"}},"sign":"nosign","timestamp":1636008301835}
        with self.client.post(url_ycxReceivelist,json=json,headers=headersvcz,catch_response=True) as response:
            # if response.status_code == 200:
            #     response.failure("Got wrong response")
            pass


    # @events.init.add_listener
    # def on_locust_init(web_ui, **kw):
    #     @web_ui.app.route("/added_page")
    #     def my_added_page():
    #         return "Another page"

    def on_stop(self):
        self.interrupt()


# 创建用户类
class QuickstartUser(FastHttpUser):
    wait_time = between(2, 5)  #设置运行过程中的间隔时间，需要在locust中引入between
    tasks = [Test1]
    min_wait = 1000
    max_wait = 2000
    host = 'http://test.chebufan.cn'

#逐步加载
class StepLoadShaper(LoadTestShape):
    '''
    逐步加载实例
    参数解析：
        step_time -- 逐步加载时间
        step_load -- 用户每一步增加的量
        spawn_rate -- 每秒增加用户数
        time_limit -- 时间限制

    '''
    # setp_time = 30
    # setp_load = 10
    spawn_rate = 5
    user_count = 10
    time_limit = 20
    def tick(self):
        '''
        设置 tick()函数
        并在tick()里面调用内置get_run_time()方法获取执行时间
        '''
        # 调用get_run_time()方法
        run_time = self.get_run_time()
        print(run_time)
        # 运行时间在30秒之内，则继续执行
        if run_time < self.time_limit:
            # 将执行时间四舍五入，作为用户数
            user_count = 10
            # 返回user_count,spawn_rate这两个参数
            return self.user_count, self.spawn_rate


if __name__ == '__main__':
    '''
    -u 指定需要的并发用户数，-r指定每秒产生的用户数。
    如果你想指定的测试运行时间，可以使用 --run-time 或 -t
    '''

    os.system("locust -f locustfile.py --headless  --html ../reportfile/report.html")
    # os.system("locust -f locustfile.py")
    # run_single_user(QuickstartUser)