from proxysocksgen import Proxies


proxies = Proxies()
proxies.initialize()


while True:
        proxy = proxies.get_proxy('socks5')
        print(proxy)


