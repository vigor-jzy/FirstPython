import socket

__all__ = ["getIpv6"]

# 获取本机IPv6地址
def getIpv6():
    host_ipv6=[]
    ips=socket.getaddrinfo(socket.gethostname(), 80)
    for ip in ips:
        if ip[4][0].startswith('24'):
    #2408 中国联通
    #2409 中国移动
    #240e 中国电信
    #        print(ip[4][0])
            host_ipv6.append(ip[4][0])
    return host_ipv6