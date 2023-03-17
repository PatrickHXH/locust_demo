import time
import gevent
from gevent import monkey
monkey.patch_all()
import os
import datetime
from locust import HttpUser, task,TaskSet,run_single_user,between,SequentialTaskSet,events,LoadTestShape
from gevent._semaphore import Semaphore
from locust.contrib.fasthttp import FastHttpUser
from auth import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_admin_formdata,headers_cxgj
import  requests

# # 创建集合点，当locust实例产生完成时触发（即10用户启动完毕）
all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()

def getProfitId():
    print("获取活动id")
    headersvcd = headers_vcd(13538878368)
    # 创建免费活动
    startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    endTime = datetime.datetime.now() + datetime.timedelta(days=+30)
    time.sleep(5)
    url_saveProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
    json = {
        "data": {
            "name": "免费自动化" + startTime,
            "salePrice": 0,
            "stock": "2",
            "shouldPay": 0,
            "startTime": str(startTime),
            "endTime": str(endTime),
            "limitTimes": "50",
            "validMonths": 6,
            "profitTicketSkuQueryList": [
                {
                    "name": "免费自动化",
                    "num": 1,
                    "originalPrice": 6600
                }
            ],
            "profitSkuImageList": [
                {
                    "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/153d1952c1e948529f7324756b4e3b14.webp",
                    "sortNo": 1,
                    "imageType": 1
                },
                {
                    "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/21123dba375845b5bbd0b0c70455cebd.webp",
                    "sortNo": 2,
                    "imageType": 2
                }
            ],
            "type": 1,
            "onePurchaser": 1,
            "onlyNewPurchaser": 0,
            "groupPrice": "",
            "groupCapacity": 2,
            "supplyPrice": 6600,
            "description": "特惠活动购买不退换不折现,优惠券以及金额等权益过期作废不予退还"
        },
        "sign": "nosign",
        "timestamp": 1632989480908
    }
    saveProfitSku = requests.post(url_saveProfitSku, json=json, headers=headersvcd)
    global free_id
    free_id = saveProfitSku.json()["data"]["id"]
    print("免费活动id：", free_id)
    return free_id

def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()

events.spawning_complete.add_listener(on_hatch_complete)

#任务
class Sequential(SequentialTaskSet):
    # @task(3)	# 设置执行次数
    @task
    def takeTicket(self):
        u'''领取活动，活动库存2，并发数为5，预期结果为：2次领取成功，其余领取失败'''
        #循环次数
        all_locusts_spawned.wait()  # 集合点等待并发
        #领取优惠券
        url_takeTicket = "http://test.chebufan.cn/vcd/api/cz/profit/profitSkuRel/takeTicket"
        json = {"data":{"profitId":self.parent.free_id},"sign":"nosign","timestamp":1636014898422}
        with self.client.post(url_takeTicket,json=json,headers=self.parent.headersvcz,catch_response=True) as resp:
            print(resp.text)
            if resp.json()["msg"] == "成功":
                resp.success()
            # elif resp.json()["msg"] == "当前活动每个用户只能参与2次":
            #     resp.success()
            else:
                resp.failure("领取失败")
        time.sleep(3)

#创建用户类
class QuickstartUser(FastHttpUser):
    host = 'http://test.chebufan.cn'
    tasks = [Sequential]
    headersvcz = headers_vcz(13538878368)
    free_id = getProfitId()
    # min_wait = 1000  #设置最小思考时间
    # max_wait = 2000  #设置最大思考时间
    # wait_time = between(2, 5)  # 设置运行过程中的间隔时间，需要在locust中引入between

#逐步加载
class StepLoadShaper(LoadTestShape):
    spawn_rate = 2
    user_count = 5
    time_limit = 25
    def tick(self):
        run_time = self.get_run_time()
        print(run_time)
        if run_time < self.time_limit:
            return self.user_count, self.spawn_rate


if __name__ == '__main__':
    # os.system("locust -f test2.py --headless  --html ../reportfile/report.html")
    os.system("locust -f test2.py")
