import requests
import time
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
        try:
            reset=not reset
            if dqpage>=maxpage:
                print("重新查询")
                dqpage=1
            elif not reset:
                dqpage+=1
            time.sleep(1)  # 每3秒检查一次
            
            if reset:
                tempdqpage=dqpage
                dqpage=1
            print(f"状态正常，查询第{dqpage}页的数据，共{maxpage}页,当前是否查询1页：{reset}")
            # 获取红包列表
            response = requests.get(f"https://simpbbs.gonm2.cn/api/redpackets/hall?page={dqpage}&status=active&sortBy=createdAt")
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
                if result.get("error") and result.get("message") == "alreadyClaimed":
                    print(f"红包 ID: {packet_id} 已被领取，跳过...")
                    continue  # 跳过当前红包，继续下一个
                dqpacknr=result["currencyId"]
                if dqpacknr==1:
                    dqpacknr="金粒"
                elif dqpacknr==2:
                    dqpacknr="钻石"
                elif dqpacknr==3:
                    dqpacknr="垃圾g币"
                print(f"领取结果: {dqpacknr}*{result["amount"]}")
            
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(1)
            
print(f"你当前有{requests.get("https://simpbbs.gonm2.cn/api/user/balance?currencyId=1",headers=headers).json()["balance"]}金粒")
# 启动循环检测
check_and_claim_redpacket()
