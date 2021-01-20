from mitmproxy import ctx



def request(flow):
    #print(flow.request.headers)
    ctx.log.warn(str(flow.request.headers))     #获取请求头
    print(flow.request.path)                    #获取请求路径
    print(flow.request.method)                  #获取请求方法
    print(flow.request.url)                     #获取请求url
    print(flow.request.host)                    #获取请求主机
    print(flow.response.status_code)            #获取请求状态
    print(flow.response.text)                   #获取请求内容
