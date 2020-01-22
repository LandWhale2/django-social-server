from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing



application = ProtocolTypeRouter({
    #만약에 웹소켓 프로토콜 이라면 , AuthMiddlewareStack
    'websocket' : AuthMiddlewareStack(
        #URLRouter 로 연결, 소비자의 라우트 연결 HTTP path를 조사
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})