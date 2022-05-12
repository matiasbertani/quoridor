
from traceback import print_tb
import numpy as np
from datetime import datetime

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
        
        self.point_behind_wall = -30
        
        self.col_izq_vacia = int()
        self.col_der_vacia = self.len_tablero_peones - 1  
        self.movimientosValidos()
        self.columnasProximasVacias()
        self.ponitBoard()
        self.mapa_movimiento = dict()
    
    def ponitBoard(self):
            
            # p_row, p_col = peon
            
                        
            # obtener columna_puntuada para columna de ubicacion actual
            self.tablero_peones[:, self.col_tp] = self.puntuarCol(self.row, self.col, axis='col')
            # obtener columna_puntuada para columna de ubicacion PREVIA
            self.tablero_peones[:, self.col_izq_vacia] = self.puntuarCol( self.row, self.col_izq_vacia , axis='col') # self.col - 2, self.col_tp - 1
            # obtener columna_puntuada para columna de ubicacion POSTERIOR
            self.tablero_peones[:, self.col_der_vacia] = self.puntuarCol( self.row, self.col_der_vacia,  axis='col' )#self.col_tp + 1 , self.col + 2
            # obtener row
            self.tablero_peones[self.row_tp, :] = self.puntuarCol( self.row, self.col ,  axis='row' )
            
        
    def puntuarCol(self,row, col, axis='col') -> np.array:
        
        
        
        # CALCULO DE ROW puntuadao
        if axis == 'row':
            
            # temp_board = np.transpose(self.tablero.copy()) # esta paa cuando haya que rotar, o hacerlo en una funcion afuera antes de devolver los datos
            
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
            
            # temp_board = self.tablero.copy()
            # calula el retorno seg
            # array en tamaña de taberon peones
            array_puntuado  = np.array([-2 if i<=int(row/2) else 1 for i in range( self.len_tablero_peones)]) * self.col_points
            
            if self.hayWall(col): 
                # (considero siempre que es orte, es decir vista de que el avance es hacia abajo)
                # REPETIR para cada pared:
                for wall in self.nextWalls(col):
                        
                    # si la pared esta a la DEBAJO  en en caso de ser NORTE O ARRIBA en caso de ser SUR ( VER DE ROTAR TABLERO SEGUN LO QU TOQUE APRA MANTENER MISMAS REGLAS) 
                    if wall > row:
                        
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
            # print(self.tablero[:,col])
            return self.h_wall in self.tablero[:,col]
        else :
            return self.v_wall in self.tablero[col,:]
    
    def columnasProximasVacias(self):
        if not self.limite_izquierda : 
            for col in list(range(self.col_tp))[::-1]:
                if not self.hayWall(int(col*2)): 
                    self.col_izq_vacia = col
                    print()
                    break
                
        if not self.limite_derecha : 
            for col in list(range(self.col_tp +1, self.len_tablero_peones )):
                if not self.hayWall(int(col*2)): 
                    self.col_der_vacia = col
                    break
                    
            
        
    def limitesTablero(self):
        self.limite_atras   = self.row == 0
        self.limite_adelante = self.row == (self.len_tablero- 1)
        
        self.limite_izquierda =  self.col == 0
        self.limite_derecha   =  self.col == (self.len_tablero- 1)
        
    
    def movimientosValidos(self):
        
        
        # ---  LIMITES EL TABLERO ------
            
        self.limitesTablero()    
        # ---- PAREDES -----------------------------------        
                   
        # frente o atras
        pared_atras = self.tablero[ self.row - 1 , self.col] == self.h_wall if not self.limite_atras else self.limite_atras
        pared_adelante = self.tablero[ self.row + 1 , self.col] == self.h_wall if not self.limite_adelante else self.limite_adelante
                
        # izquierda o derecha
        pared_izquierda = self.tablero[ self.row , self.col - 1 ] == self.v_wall if not self.limite_izquierda else self.limite_izquierda 
        pared_derecha = self.tablero[ self.row , self.col + 1 ] == self.v_wall if not self.limite_derecha else self.limite_derecha
                
        # ---------------------------------------------------- 

        
        # --------- PEONES A LOS LADOS -------------------- 
        
        # PEONES enemigos o amigos a los COSTADOS 
        peon_izquierda = self.tablero[ self.row , self.col + 2 ] in ['N','S'] if not self.limite_izquierda else self.limite_izquierda 
        peon_derecha = self.tablero[ self.row , self.col - 2 ] in ['N','S'] if not self.limite_derecha else self.limite_derecha
        
        # PEONES enemigos o propio a los ATRAS
        peon_atras = self.tablero[ self.row - 2 , self.col ] in ['N','S'] if not self.limite_atras else self.limite_atras
        peon_propio_adelante = self.tablero[ self.row + 2 , self.col ] == self.side if not self.limite_adelante else self.limite_adelante
        
        # ------------------------------------
        
        #esti en realidad es una ventaja plus que hay que ver como usar. seguro enla parte de puntuar movimiento
        peon_enemigo_adelante = self.tablero[ self.row + 2 , self.col ] == self.side if not self.limite_adelante else self.limite_adelante
        
        # considerar tambien si hay un peon enemigo al costado, o un peon amigo par prohibir ese movimientos
        
        
        # CONTEMPLAR CASOS ESPECIALISIMOS
        # contemplar en caso de que haya un peon delante, ya atras una rpared con la que no pueda avanzar. 
        # o que tenga un pon y no pueda moverme de costado         
        
        self.atras = not self.limite_atras and not pared_atras and not peon_atras
        self.adelante = not self.limite_adelante and not pared_adelante and not peon_propio_adelante
        self.izquierda = not self.limite_izquierda and not pared_izquierda and not peon_izquierda # peon enemigo o prop a la izquierda se podra?  en algun caso mover igua
        self.derecha = not self.limite_derecha and not pared_derecha and not peon_derecha
        
        # despues agregar mas complejidad pensando posibilidad de enjaularse

    def puntaje_movimiento(self, movimiento:str) -> int:
        
        # devuelve la suma de los valores de todas las columnas desde donde 
        if movimiento =='atras':            
            gx = self.tablero_peones[self.row_tp - 1,self.col_tp]
            camino_h = np.array([])
            camino_v = self.tablero_peones[self.row_tp - 1:self.row_tp ,self.col_tp]
            self.mapa_movimiento[ movimiento ] = [self.row-2, self.col]
            
        elif movimiento =='adelante':    
            gx = self.tablero_peones[self.row_tp + 1,self.col_tp]        
            camino_h = np.array([])
            camino_v = self.tablero_peones[self.row_tp:self.len_tablero_peones,self.col_tp]
            self.mapa_movimiento[ movimiento ] = [self.row+2, self.col]
            
        elif movimiento =='izquierda':
            gx = self.tablero_peones[self.row_tp,self.col_tp - 1]
            camino_h = self.tablero_peones[self.row_tp, self.col_izq_vacia :self.col_tp + 1 ]
            camino_v = self.tablero_peones[self.row_tp:self.len_tablero_peones,self.col_izq_vacia]
            self.mapa_movimiento[ movimiento ] = [self.row, self.col-2]
            
        elif movimiento =='derecha':
            gx = self.tablero_peones[self.row_tp,self.col_tp + 1]
            camino_h = self.tablero_peones[self.row_tp, self.col_tp :self.col_der_vacia + 1 ]
            camino_v = self.tablero_peones[self.row_tp:self.len_tablero_peones,self.col_der_vacia]
            self.mapa_movimiento[ movimiento ] = [self.row, self.col+2]
        
        # print(movimiento)    
        # print(self.tablero_peones)
        # print(self.tablero_peones[p_row_desde:p_row_hasta,p_col_desde:p_col_hasta])
        
        return  2*gx+int((camino_h.sum() + camino_v.sum())/(len(camino_v) +len(camino_h)))
    
    def armarDicMovimientos(self):
        
        self.dic_movimientos = dict() 
        
        if self.atras:     self.dic_movimientos['atras']      = self.puntaje_movimiento('atras')
        if self.adelante:  self.dic_movimientos['adelante']   = self.puntaje_movimiento('adelante')
        if self.izquierda: self.dic_movimientos['izquierda']  = self.puntaje_movimiento('izquierda')
        if self.derecha:   self.dic_movimientos['derecha']    = self.puntaje_movimiento('derecha')
        self.dic_movimientos = dict(sorted(self.dic_movimientos.items(), key =  lambda x: x[1])[::-1]) 
        return self.dic_movimientos
        
    
        


    def detrasWall(self):
        
        # ubicacoin de todas las PAREDES HORIZONTALES Y VERTICALES en tablero --- esto deberia hacerse enla clase de PARTIDA Y PASARSE COMO UN ARGUMENTO
        # REPETIR  para cada PARED_H:
        # setear todos los caminos
    
    
        pass
    def print_movimientos(self):
        print()
        print('atras: ',self.atras)
        print('adelante: ',self.adelante)
        print('izquierda: ',self.izquierda)
        print('derecha: ',self.derecha)
        print()
    
    
    
def test_puntaje_tablero(table):
    p_row = 4
    p_col = 8
    
  
    table[p_row, p_col] = 'N'
    print(table)
    
    p = Peon(p_row,p_col, table)
    p.ponitBoard()
    print(p.tablero_peones)


def test_movimientos_validos(table):
    t1 = datetime.now()
    p_row = 4
    p_col = 8    
    
    
  
    table[p_row, p_col] = 'N'
    print(np.array(list(range(17))).astype('str'))
    print(table)
    p = Peon(p_row,p_col, table)
    
    p.print_movimientos()
    
    print(p.tablero_peones)
    print()
    p.armarDicMovimientos()
    print(p.dic_movimientos)

    print(datetime.now()-t1)

    pass


if __name__ == '__main__':
    table = np.array([
        
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']]
            
            )
    
    #disrae mucho al boto las paredes solapadas en escalon
    test_movimientos_validos(table)
    # test_puntaje_tablero(table)
