from concurrent import futures
import logging

import grpc
import metagameplay_pb2
import metagameplay_pb2_grpc

import config

import gamecontroller as gamec
from logincontroller import LoginController

login_controller = LoginController()

class Metagameplayer(metagameplay_pb2_grpc.Metagameplayer):

    def SayHello(self, request, context):
        return metagameplay_pb2.HelloReply(message=config.HELLO_STR_S % request.name)
    
    def Login(self, user, context):
        if user.nickname == '':
            return metagameplay_pb2.SessionResponse(
                status=metagameplay_pb2.Status(ok=False, error='nickname empty')
            )

        session_id, ok = login_controller.new_session(user.nickname)

        if not ok:
            return metagameplay_pb2.SessionResponse(
                status=metagameplay_pb2.Status(ok=False, error='new_session error')
            )

        gamec.on_user_login(user.nickname)
        dbuser = gamec.db.get_user(user.nickname)

        dbitems = gamec.db.get_items(dbuser['id'])

        user.session = session_id
        user.credits = dbuser['credits']
        for i in dbitems:
            newitem = user.items.add()
            newitem.name = i['name']
            # its buy price, not sell price
            # newitem.price = i['price']

        return metagameplay_pb2.SessionResponse(
            user=user,
            status=metagameplay_pb2.Status(ok=True)
            )
    
    def Logout(self, user, context):
        if user.session == '':
            return metagameplay_pb2.SessionResponse(
                status=metagameplay_pb2.Status(ok=False, error='session empty')
            )
        
        login_controller.logout(user.session)

        return metagameplay_pb2.SessionResponse(status=metagameplay_pb2.Status(ok=True))
    
    def BuyItem(self, buy_request, context):
        if buy_request.session == '':
            return metagameplay_pb2.Status(ok=False, error='session empty')

        username = login_controller.get_username_session(buy_request.session)

        if username is None:
            return metagameplay_pb2.Status(ok=False, error='session invalid')
        
        ok = gamec.buy(username, buy_request.item_name)
        if not ok:
            return metagameplay_pb2.Status(ok=False, error='buying fail')

        return metagameplay_pb2.Status(ok=True)

    def SellItem(self, buy_request, context):
        if buy_request.session == '':
            return metagameplay_pb2.Status(ok=False, error='session empty')

        username = login_controller.get_username_session(buy_request.session)

        if username is None:
            return metagameplay_pb2.Status(ok=False, error='session invalid')
        
        ok = gamec.sell(username, buy_request.item_name)
        if not ok:
            return metagameplay_pb2.Status(ok=False, error='sell fail')

        return metagameplay_pb2.Status(ok=True)
    
    def GetAllItems(self, user, context):
        username = login_controller.get_username_session(user.session)

        if username is None:
            return metagameplay_pb2.ItemsResponse(
                status=metagameplay_pb2.Status(ok=False, error='new_session error')
            )

        items = gamec.get_items()

        resp = metagameplay_pb2.ItemsResponse(status=metagameplay_pb2.Status(ok=True))

        for name, price in items.items():
            newitem = resp.items.add()
            newitem.name = name
            newitem.price = price

        return resp

    
    def GetUser(self, user, context):
        username = login_controller.get_username_session(user.session)

        if username is None:
            return metagameplay_pb2.SessionResponse(
                status=metagameplay_pb2.Status(ok=False, error='new_session error')
            )

        dbuser = gamec.db.get_user(username)

        dbitems = gamec.db.get_items(dbuser['id'])

        user.nickname = dbuser['username']
        user.session = user.session
        user.credits = dbuser['credits']
        for i in dbitems:
            newitem = user.items.add()
            newitem.name = i['name']
            # its buy price, not sell price
            # newitem.price = i['price']

        return metagameplay_pb2.SessionResponse(
            user=user,
            status=metagameplay_pb2.Status(ok=True)
            )


 
def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metagameplay_pb2_grpc.add_MetagameplayerServicer_to_server(Metagameplayer(), server)
    server.add_insecure_port('[::]:' + port)
    server.add_insecure_port('0.0.0.0:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
