import traceback
from matplotlib import testing
import websockets
import asyncio
import json
import numpy as np

from partida import Partida


class Bot:
    def __init__(self) -> None:
        self.nombre = 'Lord Boteus'
        self.PARTIDAS = dict()  # diccionario almecena por id las paridaas actales que se juegan
        self
    
    
    def iniciar():
        pass
    
    def conectar():
        pass
    
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
                    pass
                
                # CASO: DESAFIO
                if request_data['event'] == 'challenge':
                    # if request_data['data']['opponent'] == 'favoriteopponent':
                    
                    self.aceptarChallenge()
                    
                    await self.sendAction(
                        websocket,
                        'accept_challenge',
                        {
                            'challenge_id': request_data['data']['challenge_id'],
                        },
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
            
  
    async def send(websocket, action, data):
        """Send an action to the server by the websocket

        Args:
            websocket (_type_): _description_
            action (_type_): _description_
            data (_type_): _description_
        """
        message = json.dumps(
            {
                'action': action,
                'data': data,
            }
        )
        print(message)
        await websocket.send(message)
    
    
    def desafiar(self):
        pass
    
    def aceptarChallenge(self):
        pass
    
    def rechazarPartida(self):
        pass
     
    
    def agregarPartida(self, data):
        print('Nueva partida ')
        pass
        
    
    def decidirMovimiento(self):
        pass
    
    
    def procesarTurno(self):
        pass
    
    

    
    
    
if __name__ == '__main__':

    test_partida_1()