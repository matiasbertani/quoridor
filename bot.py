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
    
    
def test_partida_1(side='S'):
    """Priebas de bot off-line miviendo hacia delante
    """
    posiciones_iniciales = [ [ [i*2,j*2] for j in range(0,9,4) ] for i in range(0,9,8)]
    
    tablero_str = ' '*289
    tablero_np = np.array(  list(tablero_str) ).reshape(17,17)
    
    for posiciones, peon_side in zip(posiciones_iniciales, ['N','S']):
        for i,j in posiciones:
            tablero_np[i][j] = peon_side
    
    # for i in tablero_np:
    #     print(i)
    
    tablero_str = ''.join(list(tablero_np.reshape(289)))
    del(tablero_np)
    
    data = {
                "event": "your_turn",
                "data": {
                    "player_2": "uno",
                    "player_1": "dos",
                    "score_2": 0.0,
                    "walls": 10.0,
                    "score_1": 0.0,
                    "side": side,
                    "remaining_moves": 200,
                    "board": tablero_str,
                    "turn_token": "tokencito",
                    "game_id": "ab16e71c-caeb-11eb-975e-0242c0a80004"
                }
            }
    
    
    partidita = Partida(data['data'])
    testeando = True        
    while testeando:
        
        testeando, board = partidita.decidirMovimiento(data['data'])
        data['data']['board'] = board
        
        
        
    
    
    
if __name__ == '__main__':

    test_partida_1()