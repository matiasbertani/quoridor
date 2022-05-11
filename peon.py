from re import S
import numpy as np

class Peon:
    
    def __init__(self, x:int ,y:int , board:np.array) -> None:
        
        self.row = x
        self.col = y
        
        
        self.tablero = board
        self.tablero_peones = np.zeros((9,9))
        self.row_tp = int(self.row/2)
        self.col_tp = int(self.col/2)
        # self.tablero_puntuado = np.zeros((17,17))
        self.side = str()
        
        # DIMENSIONES DE TABLEROS
        self.len_tablero = 17
        self.len_tablero_peones = 9
        
        
        #movimientos validos como vbooleaonos
        self.adelante = bool()
        self.atras = bool()        
        self.izquierda = bool()
        self.derecha = bool()
        pass
        self.col_points = np.array([ 2**i for i in range(9) ])
        
        self.h_wall = '-'
        self.v_wall = '|'
        
        self.point_behind_wall = -100
    
    def ponitBoard(self):
            
            # p_row, p_col = peon
            
                        
            # obtener columna_puntuada para columna de ubicacion actual
            self.tablero_peones[:, self.col_tp] = self.puntuarCol(self.row, self.col, axis='col')
            # obtener columna_puntuada para columna de ubicacion PREVIA
            self.tablero_peones[:, self.col_tp - 1] = self.puntuarCol( self.row, self.col - 2 , axis='col')
            # obtener columna_puntuada para columna de ubicacion POSTERIOR
            self.tablero_peones[:, self.col_tp + 1] = self.puntuarCol( self.row, self.col + 2,  axis='col' )
            # obtener row
            self.tablero_peones[self.row_tp, :] = self.puntuarCol( self.row, self.col ,  axis='row' )
            
        
    def puntuarCol(self,row, col, axis='col') -> np.array:
        
        
        
        # CALCULO DE ROW puntuadao
        if axis == 'row':
            
            temp_board = np.transpose(self.tablero.copy()) # esta paa cuando haya que rotar, o hacerlo en una funcion afuera antes de devolver los datos
            
            array_puntuado =  np.zeros(self.len_tablero_peones)
            if self.hayWall( col, axis= axis):
                print('acciones por si hay ared')
                
                #obtiene los indices de las paredes en la misma row
                
                # REPETIR para CADA PARED
                for wall in self.nextWalls(col, axis):
                    # SEGUN la posicion de la PARED respecto al peon:
                    
                    
                    
                    # si la pared esta a la IZQUEIRDA 
                    if wall < col:
                        # todos los lugares a la izquierda del peon se vuelve -100
                        thresh = int( (wall-1)/2)
                        array_puntuado [ thresh: ] = self.point_behind_wall
                        pass
                            
                    # si la pared esta a la DERECHA:
                    elif wall > col:
                        # todas los lugares a la derecha de la pared se vuelven -100 
                        thresh = int( (wall-1)/2)
                        array_puntuado [ thresh: ] = self.point_behind_wall
                    
        else: 
            
            temp_board = self.tablero.copy()
            # calula el retorno seg
            # array en tamaña de taberon peones
            array_puntuado  = np.array([-2 if i<=row else 1 for i in range( self.len_tablero_peones)]) * self.col_points
            
            if self.hayWall(col): 
                # (considero siempre que es orte, es decir vista de que el avance es hacia abajo)
                # REPETIR para cada pared:
                for wall in self.nextWalls(col):
                        
                    # si la pared esta a la DEBAJO  en en caso de ser NORTE O ARRIBA en caso de ser SUR ( VER DE ROTAR TABLERO SEGUN LO QU TOQUE APRA MANTENER MISMAS REGLAS) 
                    if wall > row:
                        print(' puntuar debajo')
                        #limite para cambio puntaje tras pared
                        thresh = int( (wall+1)/2)
                                        
                        #cambiando puntos tras pared
                        array_puntuado [ thresh: ] = self.point_behind_wall
                        # no pun
                        
                            # todos los lugares a la izquierda del peon se vuelve -100
                        # si  la PARED ESTA DETRAS  por ahora no ahcer nada posteriormente agregar
                
                # prev , siguie = self.nextToWall(col)
                # thresh = siguie if self.side == 'N' else prev
                
                # # cambia puntajes para delante  de la pared para imposibilitar avance
                # array_puntuado [thresh:] = self.point_behind_wall
            
        return array_puntuado
    
    def nextWalls(self,col, axis ='col'):
        
        if axis== 'col':
            return [i[0] for i in   np.where(self.tablero[:,col] == self.h_wall)]
        else:
            return [i[0] for i in   np.where(self.tablero[col,:] == self.v_wall)]
        
    def hayWall(self, col, axis='col'):
        if axis == 'col':
            return self.h_wall in self.tablero[:,col]
        else :
            return self.v_wall in self.tablero[col,:]
    
    
    def movimientosValidos(self):
        
        # verifica  las 4 direcciones o accioens posibles del peon si son validos
         
         # invalido es cuando : 
        # - hay una pared en frente o atras
        if self.board[ self.row + 1 , self.col] == '-' : print(' PARED EN FRENTE')
        if self.board[ self.row - 1 , self.col] == '-' : print(' PARED EN ATRAS')
        
        # - hay una pared en frente o atras
        if self.board[ self.row , self.col + 1 ] == '-' : print(' PARED DERECHA')
        if self.board[ self.row , self.col - 1 ] == '-' : print(' PARED IZQUIERDA')
        
        # - hay un limite del tablero (bordes)
        if self.row == 0: print('LIMITE SUPERIOR')
        if self.row == (self.len_tablero- 1): print('LIMITE INFERIOR')
        
        if self.col == 0: print('LIMITE IZQUEIRDO')
        if self.col == (self.len_tablero- 1): print('LIMITE INFERIOR')
        
        
        # CONTEMPLAR CASOS ESPECIALISIMOS
        # contemplar en caso de que haya un peon delante, ya atras una rpared con la que no pueda avanzar. 
        # o que tenga un pon y no pueda moverme de costado 
        
                
            

        
        # atras
        # adelante
        # izuierda
        # derecha
        pass

def test_puntaje_tablero():
    p_row = 0
    p_col = 8
    
    table = np.array([
        
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']]
            
            )
    
    table[p_row, p_col] = 'N'
    
    p = Peon(p_row,p_col, table)
    p.ponitBoard()
    print(p.tablero_peones)

if __name__ == '__main__':
    test_puntaje_tablero()
