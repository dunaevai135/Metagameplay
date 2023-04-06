from __future__ import print_function

import logging

import grpc
import metagameplay_pb2
import metagameplay_pb2_grpc


def run():
    logged = False
    session_id = ''

    print("Connecting ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = metagameplay_pb2_grpc.MetagameplayerStub(channel)

        while True:
            if not logged:
                name = input('Login\nNickname: ').strip()
                response = stub.Login(metagameplay_pb2.User(nickname=name))
                if not response.status.ok:
                    print('Login error. '+response.status.error)
                    continue
                print('Login success')
                logged = True
                session_id = response.user.session
            else:
                print("Enter a command: logout, buy, sell, getallitems, getuser (to get items on and credits), or exit")
                command = input('command: ').strip()

                if command == "logout":
                    logged = False
                    stub.Logout(metagameplay_pb2.User(session=session_id))

                elif command == "buy":
                    name = input('item name: ').strip()
                    response = stub.BuyItem(metagameplay_pb2.BuyRequest(session=session_id, item_name=name))
                    print('Success' if response.ok else 'Error: '+response.error)

                elif command == "sell":
                    name = input('item name: ').strip()
                    response = stub.SellItem(metagameplay_pb2.BuyRequest(session=session_id, item_name=name))
                    print('Success' if response.ok else 'Error: '+response.error)
                
                elif command == "getallitems":
                    response = stub.GetAllItems(metagameplay_pb2.User(session=session_id))
                    print(response)
                
                elif command == "getuser":
                    response = stub.GetUser(metagameplay_pb2.User(session=session_id))
                    print(response)

                elif command == "exit":
                    break
                else:
                    print("Invalid command. Please try again.")

        print('Goodbye')
        stub.Logout(metagameplay_pb2.User(session=session_id))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
