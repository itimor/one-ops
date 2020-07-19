# -*- coding: utf-8 -*-
# author: itimor

import asyncio
import websockets


async def send_msg(ws):
    while True:
        response_str = await ws.recv()
        room_group_name = eval(response_str)['group_name']
        print(room_group_name)

        _text = input("please enter your context: ")
        if _text == "exit" or _text == 'quit':
            print(f'you have enter "exit", goodbye')
            await ws.disconnect(close_code=552)
            return False
        await ws.send(
            {
                'type': 'chat_message',
                'message': _text
            }
        )
        recv_text = await ws.recv()
        print(f"{recv_text}")


# 客户端主逻辑
async def main():
    async with websockets.connect('ws://127.0.0.1:8000/chat/qq-123/') as ws:
        await send_msg(ws)


asyncio.get_event_loop().run_until_complete(main())
