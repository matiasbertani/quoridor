from random import choice, shuffle
from peon import Peon
import numpy as np
import time

class Partida:
    def __init__(self, data_game) -> None:
        
        self.id_game = data_game['game_id']
        
        self.str_board = data_game['board']
        self.np_board = self.to_numpy(self.str_board)
        
        self.historial_movimientos = None
        
        self.side = data_game['side']
        
        self.TIMEOUT = 15
        self.data_actual = data_game
        self.col_points = np.array([ 2**i for i in range(9) ])
    
        self.len_board = 9
        
        self.h_wall = '-'
        self.v_wall = '|'
        
    def actualizar_tablero():
        pass
    
    def print_board(self):
        """show the boar normalized
        """
        print('='*17)
        for row in self.np_board :print( ''.join(list(row)))
        print('='*17)
        print()
        time.sleep(0.5)
    
    def to_numpy(self,board):
        return np.array(list(board)).reshape(17,17)
    
    def to_str(self,np_board:np.array):
        return ''.join(list(np_board.reshape(289)))
    
    
    def jugarMovimiento(self, movimiento):
        pass
    
    
    def mover_adelante(self, peon) -> list:        
        return peon[0] +2 if self.side=='N'else peon[0] -2, peon[1]
        
        
    
    def decidirMovimiento(self,data):
        'Decide el siguiente movimiento y retorna el dict de respuesta apra enviar al servidor'
        
        self.print_board()
        #SOLO MOVER PARA ADELANTE LOS PEONES
        peones = [ [i,j] for i,j in zip(*np.where( self.np_board == self.side ))]
        n =len(peones.copy())
        to_row,to_col = None, None
        for _ in range(n):
            shuffle(peones)
            peon =  peones.pop()
            
            if ( peon[0] != 8*2 and self.side=='N') or (peon[0] != 0 and self.side=='S'):
                to_row,to_col = self.mover_adelante(peon)
                break
        self.np_board[to_row][to_col] = self.side
        self.np_board[peon[0]][peon[1]] = ' '
        self.str_board = self.to_str(self.np_board)
        return Move(data,peon[0],peon[1],to_row,to_col).to_dict() if (to_row is not None and to_col is not None )else False , self.str_board
 
 
    def detectarPeones(self):
        
        return [ [i,j] for i,j in zip(*np.where( self.np_board == self.side )) ]
 
    def testmoverPeon(self,data):
        self.print_board()
        time.sleep(0.1)
        peones = self.detectarPeones()
        to_row, to_col =  None, None
        prow, pcol = peones[0]
        if prow != 16:
            peon = Peon(prow, pcol, self.np_board.copy())
            mov = list(peon.armarDicMovimientos().keys())[0]
            print(peon.dic_movimientos)
            to_row, to_col = peon.mapa_movimiento[mov]
            # self.print_board()
            self.np_board[ to_row , to_col ] = self.side
            # self.print_board()
            self.np_board[ peon.row, peon.col ] = ' '
            # self.print_board()
            self.str_board = self.to_str(self.np_board)
        
        return Move(data,peon.row, peon.col, to_row, to_col).to_dict() if (to_row is not None and to_col is not None )else False , self.str_board
        
    def calcularOpciones(self,data):
        
        # DETECTAR TODOS LOS PEONES
        peones = self.detectarPeones()
        # PARA CADA PEON
            # calcular sus movimientos
            # guardar el mejor en un dic con el indice del peon
            # 
        pass
    
    def moverPeon(self):
        pass
 
def armar_tablero_str() ->str:
    # tablero_str = ' '*289
    # tablero_np = np.array(  list(tablero_str) ).reshape(17,17)
    
    
    # for posiciones, peon_side in zip(peones, ['N','S']):
    #     for i,j in posiciones:
    #             tablero_np[i][j] = peon_side
                
    table = np.array([
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'N', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )        
                
                
        
    return ''.join(list(table.reshape(289)))
            
    
def test_avance_inteligente_peon(side='N'):
    """Priebas de bot off-line miviendo hacia delante
    """
    
    
    tablero_str = armar_tablero_str()
    
    
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
        print()
        testeando, board = partidita.moverPeon(data['data'])
        data['data']['board'] = board
        

  
  
  
    
class Action:
            
    def __init__(self, data) -> None:
        
        self.action = None
        self.game_id = data['game_id']
        self.turn_token = data['turn_token']
        
    def to_dict(self):
        return {
            'action': self.action,
            'data': {
                'game_id': self.game_id,
                'turn_token': self.turn_token,
            },
        }
 
    
class Move(Action):
    
    def __init__(self, data, from_row, from_col,to_row, to_col) -> None:
        super().__init__(data)
        self.action = 'move'
        self.from_row = from_row
        self.to_row = to_row
        self.from_col = from_col
        self.to_col = to_col
        
    def to_dict(self):
        
        ret = super().to_dict()
        ret['data'].update({
            'from_row': self.from_row,
            'to_row': self.to_row,
            'from_col': self.from_col,
            'to_col': self.to_col,
        })
        return ret
    
    
class Wall(Action):
    def __init__(self, data, row, col, orientation) -> None:
        super().__init__(data)
        self.action = 'wall'
        self.row = row
        self.col = col
        self.orientation = orientation

    def to_dict(self):
        ret = super().to_dict()
        ret['data'].update({
            'row': self.row,
            'col': self.col,
            'orientation': self.orientation,
        })
        return ret





if __name__ == '__main__':
    
    test_avance_inteligente_peon()
    pass