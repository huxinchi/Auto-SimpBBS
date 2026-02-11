import requests
import time
import json
from datetime import datetime
import collections
# 准备请求头
headers = {
    "Cookie": ""
}
#准备红包缓存队列
okhongbao=collections.deque(maxlen=1000)
def check_and_claim_redpacket():
    #初始化
    dqpage=1
    reset=True
    maxpage=-1
    while True:
        
            #翻转标志
            reset=not reset
            #如果完成了页面，那么重置
            if dqpage>=maxpage:
                print("重新查询")
                dqpage=1
            elif not reset:
                #如果没有，那么翻到下一页
                dqpage+=1
                
            time.sleep(0.3)  #延迟时间
            #如果要回看
            if reset:
                #保存目前值
                tempdqpage=dqpage
                #回看第1页
                dqpage=1
            print(f"状态正常，查询第{dqpage}页的数据，共{maxpage}页,当前是否查询1页：{reset}")
            # 获取红包列表
            response = requests.get(f"https://simpbbs.gonm2.cn/api/redpackets/hall?page={dqpage}&status=active&sortBy=createdAt",headers=headers)
            if reset:
                #恢复保存的值
                dqpage=tempdqpage
            #解析出最大页
            maxpage=response.json()["pagination"]["totalPages"]
            #拿到列表
            red_packets = response.json().get("redPackets", [])
         
            # 遍历红包列表，查找可领取的红包
            for packet in red_packets:
                #获取包id
                packet_id = packet["id"]
                #跳出标志，本来可以用调试器实现jmp，但是为了在3.14-使用，使用跳出标志
                cf=0
                #遍历缓存列表
                for i in okhongbao:
                    #如果有
                    if i==packet_id:
                        #跳出
                        cf=1
                        break
                if cf==1:
                    break
                #入队缓存
                okhongbao.append(packet_id)
                #没有解决红包雨的问题
                if packet["type"]=="rain":
                    print("垃圾红包雨")
                    if packet["currencies"][0]["currencyId"]==1:
                        #提示
                        print("快上线，金粒的")
                    continue
                #如果抢不了
                if not packet["userInfo"]["canClaim"]:
                    print("抢不了的红包")
                    #跳出
                    continue
                
                dqpacknr=packet["currencies"][0]["currencyId"]
                if dqpacknr==1:
                    dqpacknr="金粒"
                elif dqpacknr==2:
                    dqpacknr="钻石"
                elif dqpacknr==3:
                    dqpacknr="垃圾g币"#给出提示信息
                print(f"发现可领取红包，信息：{packet["message"]},剩余：{packet["remaining"]},内容：{dqpacknr}*{packet["currencies"][0]["amount"]}")
                
                # 尝试领取红包
                resp_claim = requests.post(
                    "https://simpbbs.gonm2.cn/api/redpackets/claim",
                    data={"id": packet_id},
                    headers=headers
                )
                result = resp_claim.json()
                    
                # 判断是否领取是吧
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
            
        
def 获取红包信息():
    #输入
    红包短id=input("输入红包短id(不带#)")
    返回值存储1=requests.get(f"https://simpbbs.gonm2.cn/api/redpackets/details/{红包短id}")#查询
    返回值存储1=返回值存储1.json()["redPacket"]
    print(f"红包id:{返回值存储1["id"]}\n类型:{返回值存储1["type"]}\n信息:{返回值存储1["message"]}\n状态:{返回值存储1["status"]}\n总额:{返回值存储1["totalAmount"]}\n已抢的人:")#打印信息
    for i in 返回值存储1["claims"]:#遍历
        print(f"uid:{i["user"]["id"]},名称:{i["user"]["name"]},金额:{i["amount"]}")#打印

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

print(f"你当前有{requests.get("https://simpbbs.gonm2.cn/api/user/balance?currencyId=1",headers=headers).json()["balance"]}金粒")#调用api给出当前余额，垃圾g币就不用获取了
inputt=input("输入选项:\n1:自动抢红包\n2:红包信息查询\n选择:")
if inputt=="1":
    check_and_claim_redpacket()
elif inputt=="2":
    获取红包信息()
