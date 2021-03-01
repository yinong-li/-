import execjs
import requests
import json
import hashlib
import random
import time


# 需要安装pyexecjs,requests

# 不确定client_key是否发生变化
client_key = "472770f9e581cffb09349f422af57c5d"

# 加载js文件
f = open("decode.js", 'r', encoding='utf-8')
htmlstr = f.read()
f.close()
ctx = execjs.compile(htmlstr)
session = requests.session()
ts = int(time.time())

# 对t，v格式的数据进行解码，获得原始格式
def decodemsg(t, v):
    return ctx.call('decode', t, v)

# 对原始数据进行编码获得t，v的格式
def encodemsg(t, v):
    return ctx.call('encode', t, v)

# 获取md5
def getmd5(a):
    m = hashlib.md5()
    m.update(a.encode("utf-8"))
    return m.hexdigest()

# 发送post指令，url为网址后面的指令部分，如/game/exchange，msg为map格式，只需要传parm内的数据
def commandpost(url, msg):
    global ts
    global uid
    headers = {
        "referer": "https://appservice.qq.com/1110797565/1.1.5/page-frame.html",
        "user-agent": "Mozilla/5.0 (Linux) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36 QQ/8.5.5.5105 V1_AND_SQ_8.5.5_1630_YYB_D QQ/MiniApp",
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip"}

    parm = json.dumps(msg).replace(" ", "")
    sign = getmd5(uid+str(ts)+parm+client_key) #计算sign
    
    datas = {"uid": uid, "ts": ts, "params": parm, "sign": sign} #拼凑数据包
    t = random.randint(10000000, 99999999)
    v = encodemsg(t, json.dumps(datas).replace(" ", "")) #将数据包转化为t，v格式

    res = session.post("https://rane.jwetech.com:9080/"+url,
                           't={}&v={}'.format(t, v), headers=headers, timeout=0.2)
    text = res.text
    js = json.loads(text)
    js = json.loads(decodemsg(js["t"], js["v"])) #解密返回数据
    print(ts, url, js)
    ts = ts+1
    return(js)

# post发送登录命令，datas可以留空
def loginpost(datas):
    global ts
    global uid
    headers = {
        "referer": "https://appservice.qq.com/1110797565/1.1.5/page-frame.html",
        "user-agent": "Mozilla/5.0 (Linux;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36 QQ/8.5.5.5105 V1_AND_SQ_8.5.5_1630_YYB_D QQ/MiniApp",
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip"
    }
    # sign=getmd5(uid+str(ts)+parm+client_key)
    res = session.post(
    'https://rane.jwetech.com:9080//login/login', datas, headers=headers)
    text = res.text
    js = json.loads(text)
    js = json.loads(decodemsg(js["t"], js["v"]))
    print(js)

# 编解码测试
print(decodemsg(16421077, "b262ac856f59a182dfc9f4ab6ca18710420ea551"))
print(encodemsg(51907146, '{"errCode":0,"errMsg":"物品已被兑换完了"}'))

datas = "t=38057816&v=ae57d3c975599d78046cf9308d9de7fcf12f203eb7b2a757eabb084ec4fd963ab1f22039299dd8f06c493db94a9a77439fbd23c904f5a90719b03343c5e14f61b5f71264595f64f8089582073fb585bafbf98cd2f0e005acf65a830e72a5cbaa6f0eda134e6e90c95f32ead9a148722443d39a9c"#此处可以填login抓包的全部参数，用于登录，实测不登录，只要ts足够大就能响应请求
uid = "B8D8E72C33407333485083AA468FBB0C" #个人的uid，右上角头像出可查看
loginpost(datas) #发送登陆数据

# gift id
# 超会月201 超会三月、六月、年 202 203 204
# 大会员月214 大会员年 215

# dat={"id":214}
# commandpost("/game/exchange",dat)
# 兑换测试

a=1
while a<10:
    dat={}
    commandpost("/game/fbStart",dat)
    dat={"score":250,"step":15}
    time.sleep(10)
    commandpost("/game/fbSingle",dat)
    a+=1
#单人模式刷分测试
