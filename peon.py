

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
        
        self.owner = 'myself' # enemy
        
        
        # DIMENSIONES DE TABLEROS
        self.len_tablero = 17
        self.len_tablero_peones = 9
                
           
        col_points = np.array([ 2**i for i in range(9) ])
        self.points = np.array([-2 if i<=int(self.row/2) else 1 for i in range( 9)]) * col_points
        self.h_wall = '-'
        self.v_wall = '|'
        
        self.point_behind_wall = -5
        self.hay_movimientos_validos = bool()
         
        self.indiceDirecciones = self.getDictDirections() # direcciones contando 17x17
        self.pointPawnsBoard()
        self.setValidMoves()
        self.findPassage()
                
        self.mapa_movimiento = dict()
    
    def pointPawnsBoard(self):
                        
        self.tablero_peones = (np.zeros( self.tablero_peones.shape) + (self.points)).T
        self.tablero_peones[self.row_tp,:] = 0
        self.puntuarDetrasWallVertical()
        self.puntuarWallHorizonales()
       
    def puntuarWallHorizonales(self):
        for col in range(0,self.len_tablero,2):
            self.puntuarDetrasWall( col)
            
              
    def puntuarDetrasWall(self, col) -> None:
        
        
        h_walls = self.findWalls(col,'H')    
        for wall_row in  h_walls:
            
            if wall_row > self.row:
                n_casilleros = int((self.len_tablero - wall_row)/2)    
                puntos_detras= np.arange(-20*n_casilleros,0,20)
                self.tablero_peones[ int( (wall_row+1) /2 ):self.len_tablero_peones, int(col/2)] = puntos_detras
    
    def puntuarDetrasWallVertical(self) -> None:
        v_walls = self.findWalls(self.row, 'V')
        for col_wall in v_walls:
            if col_wall < self.col:
                self.tablero_peones[self.row_tp,:int((col_wall+1)/2)] = self.point_behind_wall                            
            else: 
                self.tablero_peones[self.row_tp,int((col_wall+1)/2):] = self.point_behind_wall
                    
    def findWalls(self,col, axis ='H'):
        
        if axis== 'H':            
            return [int(i) for i in   np.where(self.tablero[:,col] == self.h_wall)[0] ]
        else:
            # a = np.where(self.tablero[col,:] == self.v_wall)
            # for i in  a[0]:
            #     print(i)
            return [int(i) for i in   np.where(self.tablero[col,:] == self.v_wall)[0] ]
            
    def findPawns(self,col ,tipo, axis ='col'):
        
        if axis== 'col':            
            return [int(i) for i in   np.where(self.tablero[:,col] == tipo)[0] if i != self.row ]
        else:
            return [int(i) for i in   np.where(self.tablero[col,:] == tipo)[0] if i != self.col]
              
    def ubicarPosicion(self,row,col):
        zeros = np.zeros(( self.len_tablero,self.len_tablero  ))
        zeros[row,col] = 8
        if self.side == 'S' : 
            zeros = np.flipud( zeros)
            
        return [[int(i),int(j)] for i,j in zip(*np.where( zeros == 8 ))][0]
                  
    def getBoarBorders(self)-> dict:
        """Arma diccionario de cuantos casilleros faltan para llegar al limite indica
            Nos dice que tan lejos estan los limites del tablero segun la posicion del peon        
        Returns:
            dict: diccionario de limites en 4 direcciones
        """
        
        atras   = self.row_tp
        adelante = (self.len_tablero_peones-1) - self.row_tp
        
        izquierda =  self.col_tp
        derecha   =  (self.len_tablero_peones-1) -self.col_tp
        
        return {'atras':atras,'adelante':adelante,'izquierda':izquierda,'derecha':derecha}
        
    def paredesCerca(self) -> dict :
        """Crea diccionario con la cantidad de posiciones a las que se encuentra una pared respecto al peon en los 4 sentido
        a que distancia esta la pared del peon
        """
        # ❗❗ incluir oblicuos ttambien 
        pared_atras = 100
        pared_adelante = 100
        pared_izquierda = 100
        pared_derecha = 100
        h_walls = self.findWalls(self.col,'H')
        v_walls  = self.findWalls(self.row,'V')
        
        
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
    
    def getNearbyPawns(self,tipo) -> dict:
        
        peon_atras     = 100
        peon_adelante  = 100
        peon_izquierda = 100
        peon_derecha   = 100
        
        # --------- PEONES A LOS LADOS -------------------- 
        peones_col = self.findPawns(self.col, tipo ,'col') 
        peones_row = self.findPawns(self.row, tipo ,'row') 
        
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
    
    def setValidMoves(self) -> dict :
                        
        self.borders = self.getBoarBorders()                                
        self.paredes = self.paredesCerca()                
        self.peones_propios = self.getNearbyPawns(self.side)
        self.peones_enemigos = self.getNearbyPawns(self.opposite)

        self.movimientos_validos = self.getValidMoves()
        self.hay_movimientos_validos =  any(self.movimientos_validos.values())
        return self.movimientos_validos
        
        # despues agregar mas complejidad pensando posibilidad de enjaularse
    
    def getValidMoves(self):
        
        movimientos_validos = dict()                        
                
        for direc in ['atras','adelante','izquierda','derecha']:
            # moovimiento normal en la direccion
            movimientos_validos[direc] = self.borders[direc] > 0  and self.paredes[direc]  > 1 and self.peones_propios[direc]     > 1  and self.peones_enemigos[direc] > 1     
            # salto normal en la direccion
            if not movimientos_validos[direc] and  self.borders[direc] > 1 and self.paredes[direc]  > 3  and self.peones_propios[direc] > 2 and self.peones_enemigos[direc] == 1:
                movimientos_validos[f'{direc}-salto'] = self.allowedJumpFronted(direc)
                
            # salto oblicuo
            if not movimientos_validos[direc] and self.borders[direc] > 1 and self.paredes[direc]  == 3  and self.peones_propios[direc] > 2 and self.peones_enemigos[direc] == 1:
                movimientos_validos[f'{direc}-obl-1'],movimientos_validos[f'{direc}-obl-2'] =  self.allowedObliqueJumps(direc)                 
                    
        return movimientos_validos
       
    def allowedJumpFronted(self,direccion):
        row ,col = self.indiceDirecciones[f'{direccion}-salto']        
        return self.tablero[row,col] == ' '
   
    def getDictDirections(self):
        return {
            #movimientos normales
            'atras':       [self.row -2, self.col],
            'adelante':    [self.row +2, self.col],
            'izquierda':   [self.row   , self.col -2],
            'derecha':     [self.row   , self.col +2],
            #saltos frontales
            'atras-salto':     [ self.row -4 , self.col   ],
            'adelante-salto':  [ self.row +4 , self.col   ],
            'izquierda-salto': [ self.row    , self.col -4],
            'derecha-salto':   [ self.row    , self.col +4],
            #saltos oblicuos
            'atras-obl-1':    [ self.row -2 , self.col -2],
            'atras-obl-2':    [ self.row -2 , self.col +2],
            'adelante-obl-1': [ self.row +2 , self.col -2],
            'adelante-obl-2': [ self.row +2 , self.col +2],
            'izquierda-obl-1':[ self.row -2 , self.col -2],
            'izquierda-obl-2':[ self.row +2 , self.col -2],
            'derecha-obl-1':  [ self.row -2 , self.col +2],
            'derecha-obl-2':  [ self.row +2 , self.col +2]
        }
                        
    def allowedObliqueJumps(self,direccion):
        
        [row_1,col_1],  [row_2 ,col_2] = self.indiceDirecciones[f'{direccion}-obl-1'], self.indiceDirecciones[f'{direccion}-obl-2']
        
        if   direccion == 'atras' or direccion == 'adelante':             
            row_wall_1, row_wall_2, col_wall_1,col_wall_2 = row_1, row_2,  col_1 +1, col_2 -1
                        
        elif direccion == 'izquierda' or direccion == 'derecha' : 
            row_wall_1, row_wall_2, col_wall_1,col_wall_2 = row_1 +1, row_2 -1,  col_1, col_2
        
        if 0 <= col_1 and 0 <= col_wall_1:
            mov_1 = self.tablero[row_1,col_1] == ' ' and self.tablero[row_wall_1,col_wall_1] == ' ' 
        else: mov_1= False
        if col_2 <17 and col_wall_2 < 17:
            mov_2 = self.tablero[row_2,col_2] == ' ' and self.tablero[row_wall_2,col_wall_2] == ' ' 
        else:
            mov_2 = False
        return  mov_1, mov_2

    def pointMove(self, movimiento:str) -> int:
        
        row,col = self.indiceDirecciones[movimiento]
        row_tp,col_tp = int(row/2), int(col/2)
        gx = int(self.tablero_peones[row_tp,col_tp])
        camino_v = self.tablero_peones[row_tp:self.len_tablero_peones ,col_tp]
        distancia = 3*(len(camino_v))
        
        
        # AJUSTE  de puntos 
        if 'salto' in movimiento:
            
            if 'atras' in movimiento:
                gx +=  int(self.points[ row_tp + 1  ])
            elif 'adelente' in movimiento:
                gx += int(self.points[ row_tp-1])
                        
            distancia -= 1

        
        self.mapa_movimiento[ movimiento ] = self.ubicarPosicion(row,col)
        
        return  2.5 *gx + int(( camino_v.sum())/(distancia))
    
    def armarDicMovimientos(self):
        
        self.dic_movimientos = dict() 
        
        for movimiento , valido in self.movimientos_validos.items():
            if valido: self.dic_movimientos[movimiento]   = self.pointMove(movimiento)                

        self.dic_movimientos = dict(sorted(self.dic_movimientos.items(), key =  lambda x: x[1])[::-1]) 
        
        return self.dic_movimientos
        
    def mejorMovimiento(self) -> str:
        l = list(self.armarDicMovimientos().items())
        return l[0] if len(l) else ['invalido',-1000000]
                
    def ubicacionPeon(self):
        return self.ubicarPosicion(self.row,self.col)
 
    def findPassage(self):
        # SI HAY no se puede ir hacia delante movimiento delane invalido
        
        if not self.movimientos_validos['adelante'] and self.borders["adelante"] != 0:

            # buscar en la siguiente columna espacio vacio
            row_buscar = self.tablero[self.row +1, : ]
            
            
            col_index = np.where(row_buscar == ' ')[0]            

            derecha_index    = np.where((col_index%2== 0) & (col_index>self.col))[0]
            izqueirda_index  = np.where((col_index%2== 0) & (col_index<self.col))[0]
            
            
            if len(derecha_index): paso_der = col_index[derecha_index[0]]
            else: paso_der = None            
            
            if len(izqueirda_index): paso_izq = col_index[izqueirda_index[-1]]
            else:paso_izq = None            

            
            # calcular la mas cercana y premiar esa direccion para este peon
            distancia = { 'izquierda':abs(paso_izq - self.col) if paso_izq else 1000,
                          'derecha': abs(paso_der - self.col) if paso_der else 1000}

            self.paso_mas_cercano, self.distnaca_mas_cercana = sorted(distancia.items(), key =  lambda x: x[1])[0]
            l = ['izquierda','derecha']
            l.remove(self.paso_mas_cercano)
            anular = l[0]
            self.movimientos_validos[anular] = False
            if self.distnaca_mas_cercana==1000: 
                self.no_elegir_peon =True
           
