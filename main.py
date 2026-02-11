import requests
import time
import json
from datetime import datetime
import collections
# 定义请求头
headers = {
    "Cookie": ""
}
okhongbao=collections.deque(maxlen=1000)
def check_and_claim_redpacket():
    dqpage=1
    reset=True
    maxpage=-1
    while True:
        #try:
            reset=not reset
            if dqpage>=maxpage:
                print("重新查询")
                dqpage=1
            elif not reset:
                dqpage+=1
            time.sleep(0.3)  # 每3秒检查一次
            
            if reset:
                tempdqpage=dqpage
                dqpage=1
            print(f"状态正常，查询第{dqpage}页的数据，共{maxpage}页,当前是否查询1页：{reset}")
            # 获取红包列表
            response = requests.get(f"https://simpbbs.gonm2.cn/api/redpackets/hall?page={dqpage}&status=active&sortBy=createdAt",headers=headers)
            if reset:
                dqpage=tempdqpage
            maxpage=response.json()["pagination"]["totalPages"]
            red_packets = response.json().get("redPackets", [])
         
            # 遍历红包列表，查找未领取的红包
            for packet in red_packets:
                #if packet["currencies"]["currencyId"] == "3":
                #    break
                
                packet_id = packet["id"]
                cf=0
                for i in okhongbao:
                    if i==packet_id:
                        
                        cf=1
                        break
                if cf==1:
                    break
                
                okhongbao.append(packet_id)
                
                if packet["type"]=="rain":
                    print("垃圾红包雨")
                    if packet["currencies"][0]["currencyId"]==1:
                        print("快上线，金粒的")
                    continue
                if not packet["userInfo"]["canClaim"]:
                    print("抢不了的红包")
                    continue
                
                dqpacknr=packet["currencies"][0]["currencyId"]
                if dqpacknr==1:
                    dqpacknr="金粒"
                elif dqpacknr==2:
                    dqpacknr="钻石"
                elif dqpacknr==3:
                    dqpacknr="垃圾g币"
                print(f"发现可领取红包，信息：{packet["message"]},剩余：{packet["remaining"]},内容：{dqpacknr}*{packet["currencies"][0]["amount"]}")
                
                # 尝试领取红包
                resp_claim = requests.post(
                    "https://simpbbs.gonm2.cn/api/redpackets/claim",
                    data={"id": packet_id},
                    headers=headers
                )
                result = resp_claim.json()
                    
                # 判断是否已经领取
                if result.get("error"):
                    print(f"错误，{result}")
                    
                    continue  # 跳过当前红包，继续下一个
                dqpacknr=result["currencyId"]
                if dqpacknr==1:
                    dqpacknr="金粒"
                elif dqpacknr==2:
                    dqpacknr="钻石"
                elif dqpacknr==3:
                    dqpacknr="垃圾g币"
                print(f"领取结果: {dqpacknr}*{result["amount"]}")
            
        #except Exception as e:
        #    print(f"发生错误: {e}")
        #    time.sleep(1)
def 获取红包信息():
    红包短id=input("输入红包短id(不带#)")
    返回值存储1=requests.get(f"https://simpbbs.gonm2.cn/api/redpackets/details/{红包短id}")
    返回值存储1=返回值存储1.json()["redPacket"]
    print(f"红包id:{返回值存储1["id"]}\n类型:{返回值存储1["type"]}\n信息:{返回值存储1["message"]}\n状态:{返回值存储1["status"]}\n总额:{返回值存储1["totalAmount"]}\n已抢的人:")
    for i in 返回值存储1["claims"]:
        print(f"uid:{i["user"]["id"]},名称:{i["user"]["name"]},金额:{i["amount"]}")

# 1. 解析JSON数据
data = requests.get("https://simpbbs.gonm2.cn/api/_auth/session",headers=headers).json()

# 2. 提取所需字段
uid = data['user']['id']
uuid = data['id']
name = data['user']['name']
email = data['user']['email']
# 将groups列表转换为逗号分隔的字符串
groups_str = ','.join(data['user']['groups'])

# 3. 时间格式转换
# 解析ISO 8601时间字符串
login_time_iso = data['loggedInAt']
# 转换为datetime对象
login_datetime = datetime.fromisoformat(login_time_iso.replace("Z", "+00:00"))
# 格式化为“xxxx年xx月xx日”格式
formatted_date = login_datetime.strftime("%Y年%m月%d日")

# 4. 打印结果
print(f"用户id:{uid}")
print(f"用户uuid:{uuid}")
print(f"用户名:{name}")
print(f"邮箱:{email}")
print(f"组:{groups_str}")
print(f"登录时间:{formatted_date}")

print(f"你当前有{requests.get("https://simpbbs.gonm2.cn/api/user/balance?currencyId=1",headers=headers).json()["balance"]}金粒")
inputt=input("输入选项:\n1:自动抢红包\n2:红包信息查询\n选择:")
if inputt=="1":
    check_and_claim_redpacket()
elif inputt=="2":
    获取红包信息()
