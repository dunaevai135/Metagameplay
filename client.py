from __future__ import print_function

import logging

import grpc
import metagameplay_pb2
import metagameplay_pb2_grpc

def login(stub):
    while True:
        name = input('Login\nNickname: ').strip()
        response = stub.Login(metagameplay_pb2.User(nickname=name))
        if response.status.ok:
            print('Login success')
            return response.user.session
        else:
            print('Login error. '+response.status.error)

def logout(stub, session_id):
    stub.Logout(metagameplay_pb2.User(session=session_id))

def buy_item(stub, session_id):
    name = input('item name: ').strip()
    response = stub.BuyItem(metagameplay_pb2.BuyRequest(session=session_id, item_name=name))
    print('Success' if response.ok else 'Error: '+response.error)

def sell_item(stub, session_id):
    name = input('item name: ').strip()
    response = stub.SellItem(metagameplay_pb2.BuyRequest(session=session_id, item_name=name))
    print('Success' if response.ok else 'Error: '+response.error)

def get_all_items(stub, session_id):
    response = stub.GetAllItems(metagameplay_pb2.User(session=session_id))
    print(response)

def get_user(stub, session_id):
    response = stub.GetUser(metagameplay_pb2.User(session=session_id))
    print(response)
    
def run():
    logged = False
    session_id = ''

    print("Connecting ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = metagameplay_pb2_grpc.MetagameplayerStub(channel)

        session_id = login(stub)
        while True:
            print("Enter a command: buy, sell, getallitems, getuser, or exit")
            command = input('command: ').strip()

            if command == "buy":
                buy_item(stub, session_id)

            elif command == "sell":
                sell_item(stub, session_id)

            elif command == "getallitems":
                get_all_items(stub, session_id)

            elif command == "getuser":
                get_user(stub, session_id)

            elif command == "exit":
                logout(stub, session_id)
                break

            else:
                print("Invalid command. Please try again.")
        
        print('Goodbye')
        logout(stub, session_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
