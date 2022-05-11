from random import choice, shuffle
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
        
    def puntuarBoard(self):
        """Genera la matriz total de puntaje
        Le da puntaje a cla columna donde se encuentra el peon
        a las columnas 2 laterales ( en cas de haberse movido a derecha)
        y la horizontal o row donde se encuentra el poeon que esta llena de ceros, salvo 
        
        con esta matriz obtenida en esta dfuncion, voy a calcular fuera de 
        """
        for p_row, p_col in self.peones:
            
            
            
            pass    
    
    def ponitBoard(self,peon):
        p_row, p_col = peon
        
        # obtener columna_puntuada para columna de ubicacion actual
        # obtener columna_puntuada para columna de ubicacion PREVIA
        # obtener columna_puntuada para columna de ubicacion POSTERIOR
        # obtener row
        pass
    
      
    def getOnlyCasilleros(self):
        pass
        
      
    def puntuarCol(self,row, col, axis='col',side='N') -> np.array:
        
        
        if axis == 'row':
            temp_board = np.transpose(self.np_board)
            ret =  np.array([0 for i in range(9)])
            if self.hayWall(col, axis= axis):
                print('acciones por si hay ared')
                self.nextToWall(col)
                #obtiene los indices de las paredes en la misma row
                
                # REPETIR para cada pared
                    # segun la posicion de la pred respecto al peon:
                        # si la pared esta a la IZQUEIRDA 
                            # todos los lugares a la izquierda del peon se vuelve -100
                        # si la pared esta a la DERECHA:
                            # todas los lugares a la derecha de la pared se vuelven -100 
            
            # retornan el fila ROW  puntuada
            
        else: 
            
            temp_board = self.np_board.copy()
        
            ret  = np.array([-2 if i<=row else row for i in range(9)])*self.col_points
            
            if self.hayWall(col): 
                # REPETIR para cada pared:
                    # segun la posicion de la pred respecto al peon:
                        # si la pared esta a la DEBAJO  en en caso de ser NORTE O ARRIBA en caso de ser SUR ( VER DEROTAR TABLERO SEGUN LO QU TOQUE APRA MANTENER MISMAS REGLAS) 
                            # todos los lugares a la izquierda del peon se vuelve -100
                        # si  la
                
                prev ,siguie = self.nextToWall(col)
                thresh = siguie if self.side == 'N' else prev
                ret[thresh:] = -100            
            
            return ret
        
    
        
        
    def columas_casillerps(self,col):
    
        return self.board[0::2,col] 





        # pyedo hace un sol hay pared con 

    def nextToWall(self,col):
        
        #Elegir la  pared que esete inmediatemente despues POR AHORA CONEMPLO QUE ME PONEN UNA SOLA PARED
        l = [i[0] for i in   np.where(self.board[:,col] == self.wall)]
        y = l[0]
        return int( (y-1)/2 ), int( (y+1)/2 )
    
    def hayWall(self, col, axis='col'):
        return self.wall in self.board[:,col]

    def hayParedRow(self, row):        
        return '-' in self.board[row,:]
            
    
  
  
  
  
    
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
    pass