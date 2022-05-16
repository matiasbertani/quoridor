
import re
from traceback import print_tb
import numpy as np
from datetime import datetime

class Peon:
    
    def __init__(self, p_row:int ,p_col:int , board:np.array ,side:str) -> None:
        
        # tanto Norte como Sur reciben el teblero de la misma manera. 
        # Cuano uno jeugoa a cualquier juego ve el tablero igual 
        # Las respuesta ser rotan en el caso de sur,
        #   #
        self.row = p_row
        self.col = p_col
        opciones_side = ['N','S']
        
        self.tablero = board        
        self.tablero_peones = np.zeros((9,9))
        self.row_tp = int(self.row/2)
        self.col_tp = int(self.col/2)
        # self.tablero_puntuado = np.zeros((17,17))
        self.side = side
        opciones_side.remove(side)
        self.opposite = opciones_side[0]
        
        # DIMENSIONES DE TABLEROS
        self.len_tablero = 17
        self.len_tablero_peones = 9
        
        
        #movimientos validos como vbooleaonos
        self.adelante = bool()
        self.atras = bool()        
        self.izquierda = bool()
        self.derecha = bool()
        
        self.col_points = np.array([ 2**i for i in range(9) ])
        
        self.h_wall = '-'
        self.v_wall = '|'
        
        self.point_behind_wall = -5
        
        self.hay_paso_izq = True
        self.hay_paso_der = True
        
        self.col_izq_vacia = int()
        self.col_der_vacia = self.len_tablero_peones - 1 
         
        # self.movimientosValidos()
        # self.columnasProximasVacias()
        # self.pointBoard()
        self.mapa_movimiento = dict()
    
    def pointBoard(self):
            
            # p_row, p_col = peon
            
                        
            # obtener columna_puntuada para columna de ubicacion actual
            self.tablero_peones[:, self.col_tp] = self.puntuarCol(self.row, self.col, axis='col')
            # obtener columna_puntuada para columna de ubicacion PREVIA
            self.tablero_peones[:, self.col_izq_vacia] = self.puntuarCol( self.row, int(self.col_izq_vacia *2) , axis='col') # self.col - 2, self.col_tp - 1
            # obtener columna_puntuada para columna de ubicacion POSTERIOR
            self.tablero_peones[:, self.col_der_vacia] = self.puntuarCol( self.row, int(self.col_der_vacia * 2),  axis='col' )#self.col_tp + 1 , self.col + 2
            # obtener row
            self.tablero_peones[self.row_tp, :] = self.puntuarCol( self.row, self.col ,  axis='row' )
            
        
    def puntuarCol(self,row, col, axis='col') -> np.array:
        
        
        
        # CALCULO DE ROW puntuadao
        if axis == 'row':
            
            # temp_board = np.transpose(self.tablero.copy()) # esta paa cuando haya que rotar, o hacerlo en una funcion afuera antes de devolver los datos
            
            array_puntuado =  np.zeros(self.len_tablero_peones)
            if self.hayWall( row, axis= axis):
                # print('acciones por si hay ared')
                
                #obtiene los indices de las paredes en la misma row
                
                # REPETIR para CADA PARED
                for wall in self.nextWalls(row, axis):
                    # SEGUN la posicion de la PARED respecto al peon:
                    
                    
                    
                    # si la pared esta a la IZQUEIRDA 
                    if wall < col:
                        # todos los lugares a la izquierda del peon se vuelve -100
                        thresh = int( (wall-1)/2)
                        array_puntuado [ :thresh+1 ] = self.point_behind_wall
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
    
    def nextWalls(self,col, axis ='H'):
        
        if axis== 'H':            
            return [int(i) for i in   np.where(self.tablero[:,col] == self.h_wall)[0] ]
        else:
            # a = np.where(self.tablero[col,:] == self.v_wall)
            # for i in  a[0]:
            #     print(i)
            return [int(i) for i in   np.where(self.tablero[col,:] == self.v_wall)[0] ]
        
    def hayWall(self, col, axis='col',x_orient='izquierda',y_orient='adelante'):
        
        if axis == 'col':
            # print(self.tablero[:,col])
            if y_orient=='adelante':
                return self.h_wall in self.tablero[self.row:,col]
            else:
                return self.h_wall in self.tablero[:self.row,col]
        else :
            
            return self.v_wall in self.tablero[col,:]
    
    def peonesAlineados(self,col ,tipo, axis ='col'):
        
        if axis== 'col':            
            a = np.where(self.tablero[:,col] == tipo)
            b= a[0]
            return [int(i) for i in   np.where(self.tablero[:,col] == tipo)[0] if i != self.row ]
        else:
            return [int(i) for i in   np.where(self.tablero[col,:] == tipo)[0] if i != self.col]

    
    def columnasProximasVacias(self):
        if not self.limite_izquierda : 
            for col in list(range(self.col_tp))[::-1]:
                if not self.hayWall(int(col*2)): 
                    self.col_izq_vacia = col                    
                    break 
            else: self.hay_paso_izq = False
                
        if not self.limite_derecha : 
            for col in list(range(self.col_tp +1, self.len_tablero_peones )):
                if not self.hayWall(int(col*2)): 
                    self.col_der_vacia = col
                    break 
            else: self.hay_paso_der = False
            
    
    def mapearMovimiento(self,row,col):
        zeros = np.zeros(( self.len_tablero,self.len_tablero  ))
        zeros[row,col] = 8
        if self.side == 'S' : 
            zeros = np.flipud( zeros)
            
        return [[int(i),int(j)] for i,j in zip(*np.where( zeros == 8 ))][0]
            
        
    def limitesTablero(self,):
        """Arma diccionario de cuantos casilleros faltan para llegar al limite indica
            Nos dice que tan lejos estan los limites del tablero segun la posicion del peon
        Args:
            i (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        
        atras   = self.row_tp
        adelante = (self.len_tablero_peones-1) - self.row_tp
        
        izquierda =  self.col_tp
        derecha   =  (self.len_tablero_peones-1) -self.col_tp
        
        return {'atras':atras,'adelante':adelante,'izquierda':izquierda,'derecha':derecha}
        
    def paredesCerca(self):
        """Crea diccionario con la cantidad de posiciones a las que se encuentra una pared respecto al peon en los 4 sentido
        a que distancia esta la pared del peon
        """
        # ❗❗ incluir oblicuos ttambien 
        pared_atras = 100
        pared_adelante = 100
        pared_izquierda = 100
        pared_derecha = 100
        h_walls = self.nextWalls(self.col,'H')
        v_walls  = self.nextWalls(self.row,'V')
        
        
        for wall in h_walls:
            dist = abs(wall - self.row)
            if wall < self.row:  
                if  dist < pared_atras: pared_atras = dist                  
            else: 
                if dist <  pared_adelante: pared_adelante =  dist
                        
        for wall in v_walls:
            dist = abs(wall - self.col)
            if wall < self.col:  
                if  dist < pared_izquierda: pared_izquierda = dist                  
            else: 
                if dist <  pared_derecha: pared_derecha =  dist
        
        
        return {'atras':pared_atras,'adelante':pared_adelante,'izquierda':pared_izquierda,'derecha':pared_derecha}   

    
    def peonesCerca(self,tipo):
        
        peon_atras     = 100
        peon_adelante  = 100
        peon_izquierda = 100
        peon_derecha   = 100
        
        # --------- PEONES A LOS LADOS -------------------- 
        peones_col = self.peonesAlineados(self.col, tipo ,'col') 
        peones_row = self.peonesAlineados(self.row, tipo ,'row') 
        
        # peones sobre columns
        for peon in peones_col:
            dist = int(abs(peon - self.row)/2)
            if peon < self.row:  
                if  dist < peon_atras: peon_atras = dist                  
            else: 
                if dist <  peon_adelante: peon_adelante =  dist
        
        for peon in peones_row:
            dist = int(abs(peon - self.col)/2)
            if peon < self.col:  
                if  dist < peon_izquierda: peon_izquierda = dist                  
            else: 
                if dist <  peon_derecha: peon_derecha =  dist
        
        
        return {'atras':peon_atras,'adelante':peon_adelante,'izquierda':peon_izquierda,'derecha':peon_derecha}   
    
    def movimientosValidos(self):
        
        
        
        self.borders = self.limitesTablero()                                
        self.paredes = self.paredesCerca()                
        self.peones_propios = self.peonesCerca(self.side)
        self.peones_enemigos = self.peonesCerca(self.opposite)

        self.movimientos_validos = self.dicMovimientosValidos()
    
        
        # despues agregar mas complejidad pensando posibilidad de enjaularse
    
    def dicMovimientosValidos(self):
        
        movimientos_validos = dict()                        
                
        for direc in ['atr','ade','izq','der']:
            # moovimiento normal en la direccion
            movimientos_validos[direc] = self.borders[direc] > 0  and self.paredes[direc]  > 1 and self.peones_propios[direc]     > 1  and self.peones_enemigos[direc] > 1     
            # salto normal en la direccion
            if not movimientos_validos[direc] and  self.borders[direc] > 1 and self.paredes[direc]  > 3  and self.peones_propios[direc] > 2 and self.peones_enemigos[direc] == 1:
                movimientos_validos[f'{direc}-salto'] = self.saltoFrontalPermitido(direc)
                
            # salto oblicuo
            if not movimientos_validos[direc] and self.borders[direc] > 1 and self.paredes[direc]  == 3  and self.peones_propios[direc] > 2 and self.peones_enemigos[direc] == 1:
                movimientos_validos[f'{direc}-obl-1'],movimientos_validos[f'{direc}-obl-2'] =  self.saltosOblicuosPermitidos(direc)                 
                    
        return movimientos_validos
       
    def saltoFrontalPermitido(self,direccion):
        if   direccion == 'atr': row ,col = self.row -4, self.col
        elif direccion == 'ade': row ,col = self.row +4, self.col
        elif direccion == 'izq': row ,col = self.row   , self.col -4
        elif direccion == 'der': row ,col = self.row   , self.col +4
        
        return self.tablero[row,col] == ' '
   
    def saltosOblicuosPermitidos(self,direccion):
        
        if   direccion == 'atr': 
            row_1, row_2 , col_1, col_2   = self.row - 2, self.row - 2,  self.col -2, self.col +2
        elif direccion == 'ade': 
            row_1, row_2 , col_1, col_2   = self.row + 2, self.row + 2,  self.col -2, self.col +2
        elif direccion == 'izq': 
            row_1, row_2 , col_1, col_2   = self.row - 2, self.row + 2,  self.col -2, self.col -2
        elif direccion == 'der': 
            row_1, row_2 , col_1, col_2   = self.row - 2, self.row + 2,  self.col +2, self.col +2
        
        return self.tablero[row_1,col_1] == ' ', self.tablero[row_2,col_2] == ' '

    def puntaje_movimiento(self, movimiento:str) -> int:
        
        # devuelve la suma de los valores de todas las columnas desde donde 
        if movimiento =='atras':            
            gx = self.tablero_peones[self.row_tp - 1,self.col_tp]
            camino_h = np.array([])
            camino_v = self.tablero_peones[self.row_tp - 1:self.row_tp ,self.col_tp]
            # self.mapa_movimiento[ movimiento ] = [self.row-2, self.col]
            self.mapa_movimiento[ movimiento ] = self.mapearMovimiento(self.row-2, self.col)
            
        elif movimiento =='adelante':    
            gx = self.tablero_peones[self.row_tp + 1,self.col_tp]        
            camino_h = np.array([])
            camino_v = self.tablero_peones[self.row_tp:self.len_tablero_peones,self.col_tp]
            # self.mapa_movimiento[ movimiento ] = [self.row+2, self.col]
            self.mapa_movimiento[ movimiento ] = self.mapearMovimiento(self.row+2, self.col)
            
        elif movimiento =='izquierda':
            gx = self.tablero_peones[self.row_tp,self.col_tp - 1]
            camino_h = self.tablero_peones[self.row_tp, self.col_izq_vacia :self.col_tp + 1 ]
            camino_v = self.tablero_peones[self.row_tp:self.len_tablero_peones,self.col_izq_vacia]
            # self.mapa_movimiento[ movimiento ] = [self.row, self.col-2]
            self.mapa_movimiento[ movimiento ] = self.mapearMovimiento(self.row, self.col-2)
            
        elif movimiento =='derecha':
            gx = self.tablero_peones[self.row_tp,self.col_tp + 1]
            camino_h = self.tablero_peones[self.row_tp, self.col_tp :self.col_der_vacia + 1 ]
            camino_v = self.tablero_peones[self.row_tp:self.len_tablero_peones,self.col_der_vacia]
            # self.mapa_movimiento[ movimiento ] = [self.row, self.col+2]
            self.mapa_movimiento[ movimiento ] = self.mapearMovimiento(self.row, self.col+2)
        
        # print(movimiento)    
        # print(self.tablero_peones)
        # print(self.tablero_peones[p_row_desde:p_row_hasta,p_col_desde:p_col_hasta])
        distancia = 3*(len(camino_v) +len(camino_h))
        return  2.5*gx+int((camino_h.sum() + camino_v.sum())/(distancia))
    

    def armarDicMovimientos(self):
        
        self.dic_movimientos = dict() 
        
        if self.atras:     self.dic_movimientos['atras']      = self.puntaje_movimiento('atras')
        if self.adelante:  self.dic_movimientos['adelante']   = self.puntaje_movimiento('adelante')
        if self.izquierda: self.dic_movimientos['izquierda']  = self.puntaje_movimiento('izquierda')
        if self.derecha:   self.dic_movimientos['derecha']    = self.puntaje_movimiento('derecha')
        self.dic_movimientos = dict(sorted(self.dic_movimientos.items(), key =  lambda x: x[1])[::-1]) 
        return self.dic_movimientos
        
    def mejorMovimiento(self) -> str:
        
        return list(self.armarDicMovimientos().items())[0]
                
    def ubicacionPeon(self):
        return self.mapearMovimiento(self.row,self.col)

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
    p_row = 16
    p_col = 0
    
  
    table[p_row, p_col] = 'N'
    print(table)
    
    p = Peon(p_row,p_col, table)
    p.pointBoard()
    print(p.tablero_peones)


def test_movimientos_validos(table,side='N'):
    t1 = datetime.now()
    p_row = 12
    p_col = 16   
    
    
  
    table[p_row, p_col] = side
    print(np.array(list(range(17))).astype('str'))
    print(table)
    p = Peon(p_row,p_col, table,side)
    
    p.print_movimientos()
    
    print(p.tablero_peones)
    print()
    p.armarDicMovimientos()
    print(p.dic_movimientos)

    print(datetime.now()-t1)

    pass


if __name__ == '__main__':
    table = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', 'N', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'N', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', '-', '*', '-'], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-','*', '-', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        ['-', '*', '-', ' ', '-', '*', '-', '*', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        ['N', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', 'S',' ', ' ', ' ', ' ']] # 16

            
            )
    
    #disrae mucho al boto las paredes solapadas en escalon
    test_movimientos_validos(table,'S')
    # test_puntaje_tablero(table)
