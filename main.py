import requests
import time

# 定义请求头
headers = {
    "Cookie": "自己替换cookie"
}

def check_and_claim_redpacket():
    while True:
        try:
            # 获取红包列表
            response = requests.get("https://simpbbs.gonm2.cn/api/redpackets/hall?page=1&sortBy=createdAt")
            red_packets = response.json().get("redPackets", [])

            # 遍历红包列表，查找未领取的红包
            for packet in red_packets:
                if packet["currencies"]["currencyId"] == "3":
                    break
                if "脚本" in packet["message"]:
                    print("红包已过期")
                    continue
                if packet["status"] == "active":
                    packet_id = packet["id"]
                    print(f"发现可领取红包，ID: {packet_id}")
                    
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
                    
                    print(f"领取结果: {result}")
                    break  # 领取成功后跳出循环
            else:
                print("当前没有可领取的红包")

            time.sleep(3)  # 每5秒检查一次
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(3)

# 启动循环检测
check_and_claim_redpacket()
# 启动循环检测
check_and_claim_redpacket()
