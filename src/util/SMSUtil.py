import serial
import os
import schedule
import time
import requests
from datetime import datetime

# 串口配置
ser = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)

current_call_number = None
in_call = False

# Webhook 配置
WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxxxxxxxxxxxxxxx"  # 企业微信机器人


def send_cmd(cmd, delay=0.3):
    ser.write((cmd + "\r\n").encode())
    time.sleep(delay)
    return ser.read_all().decode(errors="ignore")


def forward_sms(number, content):
    # 方式3：企业微信机器人
    try:
        requests.post(WECHAT_URL, json={
            "msgtype": "text",
            "text": {
                "content": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n📩 新消息\n来自: {number}\n内容: {content}"}
        }, timeout=5)
    except Exception as e:
        log("企业微信转发失败:" + e)


# 上报状态
def daily_report():
    """每天定时上报一次状态"""
    log("******自检******")
    resp_cfun = send_cmd("AT+CFUN?")
    resp_cereg = send_cmd("AT+CEREG?")
    msg = f"[每日状态报告]\n{resp_cfun.strip()}\n{resp_cereg.strip()}"
    forward_sms("system", msg)


# 检查飞行模式
def check_cfun():
    resp = send_cmd("AT+CFUN?")
    # 解析返回值
    if "+CFUN:" in resp:
        try:
            val = int(resp.split(":")[1].strip().split("\n")[0])
            if val != 1:
                log("CFUN 当前不是全功能模式，执行恢复...")
                send_cmd("AT+CFUN=1")
                time.sleep(10)
            else:
                log("CFUN 正常 (1)")
        except Exception as e:
            print("解析 CFUN 出错:", e)
    else:
        log("未获取到 CFUN 状态，原始返回:" + resp)


# 中文转码
def decode_ucs2(hex_str: str) -> str:
    try:
        # 去掉空格并转成字节
        data = bytes.fromhex(hex_str)
        # UCS2 等价于 UTF-16BE
        return data.decode("utf-16-be")
    except Exception as e:
        return f"[解码失败] {e}"


def main():
    # 首先检查飞行模式
    check_cfun()
    log(send_cmd("AT"))  # 测试模块
    resp = send_cmd("AT+CPIN?")
    log("CPIN：" + resp)
    if "SIM PIN" in resp:
        send_cmd('AT+CPIN="xxxxx"')  # 如果需要PIN，输入
        time.sleep(3)

    global current_call_number, in_call

    # 等待网络注册
    while True:
        resp = send_cmd("AT+CEREG?")
        if ",1" in resp or ",5" in resp:
            log("已注册网络1本地，5漫游" + resp)
            resp = send_cmd("AT+COPS?")
            log("当前网络：" + resp)
            resp = send_cmd("AT+CSQ")
            log("信号：" + resp)
            resp = send_cmd("AT+CEREG?")
            log("CEREG：" + resp)

            # 1显示错误编码，2:显示字符串
            resp = send_cmd("AT+CMEE=2")
            log("CMEE" + resp)

            # 初始化短信功能
            res = send_cmd("AT+CMGF=1")  # 短信文本模式
            log("短信文本模式配置：" + res)
            res = send_cmd('AT+CSCS="GSM"')  # 短信格式
            log("短信格式配置：" + res)
            resp = send_cmd("AT+CSCS?")
            log("CSCS" + resp)
            break
        time.sleep(2)

    log("等待接收短信...")

    while True:
        data = ser.read_all().decode(errors="ignore")

        if "+CMTI" in data:
            idx = data.split(",")[-1].strip()
            sms = send_cmd(f"AT+CMGR={idx}")

            # 解析短信
            try:
                lines = sms.split("\n")
                header = lines[1] if len(lines) > 1 else ""
                content = lines[2].strip() if len(lines) > 2 else ""
                # 判断是否为纯16进制
                if all(c in "0123456789ABCDEFabcdef" for c in content):
                    content = decode_ucs2(content)
                number = ""
                if "," in header:
                    parts = header.split(",")
                    if len(parts) > 1:
                        number = parts[1].replace('"', "")

                log("新短信:" + number + content)
                forward_sms(number, content)

            except Exception as e:
                log("短信解析失败:" + e)

        # 来电开始
        if "+CLIP" in data:
            try:
                clip_line = [line for line in data.split("\n") if "+CLIP" in line][0]
                number = clip_line.split(",")[0].split(":")[1].replace('"', "").strip()
                current_call_number = number
                in_call = True
                log("检测到来电:" + number)
            except Exception as e:
                log("来电号码解析失败:" + e)

        # 电话挂断（通话结束）
        if "NO CARRIER" in data or "BUSY" in data or "NO ANSWER" in data:
            if in_call and current_call_number:
                log("通话结束，推送来电提醒:" + current_call_number)
                forward_sms(current_call_number, "[来电提醒] 未接来电")
            in_call = False
            current_call_number = None
        time.sleep(3)

        # 判断执行定时任务（每日上报）
        schedule.run_pending()


cur_path = os.path.abspath(os.path.dirname(__file__))
print(cur_path)


# 输出日志
def log(info):
    # 声明全局变量
    path = cur_path + "/../log/log.txt"
    if os.path.exists(path):
        datetime_object = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_info = "{} {}\n".format(datetime_object, info)
        print(log_info)
        with open(path, "r+", encoding="utf-8") as f:
            if len(f.readlines()) < 300:
                f.write(log_info)
            else:
                with open(path, "w", encoding="utf-8") as fw:
                    fw.write(log_info)
            pass


# 安排每天执行一次状态上报
# schedule.every().day.at("22:22").do(daily_report)
# 每三小时上报一次
schedule.every(3).hours.do(daily_report)

if __name__ == "__main__":
    log("********************正在启动*********************")

    # 执行主线程
    main()
