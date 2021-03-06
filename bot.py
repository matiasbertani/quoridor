import traceback

import websockets
import asyncio
import json
import sys
from partida import Partida
import time

class Bot:
    
    def __init__(self, auth_token) -> None:
        self.nombre = 'Lord Botius'
        self.PARTIDAS = dict()  # diccionario almecena por id las paridaas actales que se juegan
        self.auth_token = auth_token
    
    
    async def conectar(self):
        uri = "wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={}".format(self.auth_token)
        while True:
            try:
                print('connection to {}'.format(uri))
                async with websockets.connect(uri) as websocket:
                    await self.gestionarEvento(websocket)
            except KeyboardInterrupt:
                print('Exiting...')
                break
            except Exception:
                print('connection error!')
                time.sleep(3)
        
    async def gestionarEvento(self, websocket):
        
        while True:
            try:
                request = await websocket.recv()
                print(f"< {request}")
                request_data = json.loads(request)
                
                # CASO: user list
                if request_data['event'] == 'update_user_list':
                    pass
                
                # CASO: GAMEOVER
                if request_data['event'] == 'gameover':
                    self.process_game_over(request_data)
                    pass
                
                # CASO: DESAFIO
                if request_data['event'] == 'challenge':
                    if request_data['data']['opponent']: #== 'botpractica'
                    
                        # self.aceptarChallenge()
                    
                        await self.send(
                            websocket,
                            {                            
                            'action':'accept_challenge',
                            'data': {'challenge_id': request_data['data']['challenge_id'] }
                            }
                        )
                    
                # CASO: MI TURNO  
                if request_data['event'] == 'your_turn':
                    await self.procesarTurno(websocket, request_data)
                    
                    
            except KeyboardInterrupt:
                print('Exiting...')
                break
            
            except: # Exception as e:
                
                print(traceback.format_exc())
                # print('error {}'.format(str(e)))
                break  # force login again
            
  
    async def send(self, websocket, respuesta:dict):
        """Send an action to the server by the websocket

        Args:
            websocket (_type_): _description_
            action (_type_): _description_
            data (_type_): _description_
        """
        message = json.dumps(respuesta)
        # print(message)
        await websocket.send(message)
    
    
    async def procesarTurno(self,websocket, request_data):
        
        game_id = request_data['data']['game_id']
        if game_id not in self.PARTIDAS:
            
            self.PARTIDAS[ game_id  ] = Partida(request_data['data'])
        
        partida = self.PARTIDAS[ game_id ]
        
        partida.actualizar_data(request_data['data'])
        
        movimiento  = partida.elegirMejorMovimiento()
        print(movimiento)
            # partida.print_board()   
        await self.send( websocket, movimiento)


    def process_game_over(self,request_data):
        print(request_data)
        game_id = request_data['data']['game_id']
        print('intenta eliminar')
        del self.PARTIDAS[ game_id  ]
        print('PARTIDA ELIMINADA')
    

    
    
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        
        auth_token = sys.argv[1]
        
        # print(auth_token)
        
        bot = Bot(auth_token) 
        asyncio.get_event_loop().run_until_complete(bot.conectar())
        
           
    else:
        print('please provide your auth_token')
    
    
