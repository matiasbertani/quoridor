
import numpy as np

class Scanner:
    
    
    def __init__(self, p_row:int ,p_col:int , board:np.array ,side:str) -> None:
        '''Class to scan if exist a way out in the boar for the selected position'''
        self.row = p_row
        self.col = p_col
        self.start_row = int()
        self.start_col = int()
        
        opciones_side = ['N','S']
        
        self.board = board        
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
                
           
        col_points = np.array([ 2**i for i in range(9) ])
        self.points = np.array([-2 if i<=int(self.row/2) else 1 for i in range( 9)]) * col_points
        self.h_wall = '-'
        self.v_wall = '|'
        
        self.point_behind_wall = -5
        self.hay_movimientos_validos = bool()
         
        self.indiceDirecciones = self.armarDictDirecciones() # direcciones contando 17x17
        
        
        
        self.setMovimientosValidos()
        
        self.border_position = str() # al principio esta a la izquierda y
        self.possibles_moves_at_start = list()
        self.historico = dict()   
        self.from_move = None
        
          
    def armarDictDirecciones(self):
        return {
            #movimientos normales
            'atras':       [self.row -2, self.col],
            'adelante':    [self.row +2, self.col],
            'izquierda':   [self.row   , self.col -2],
            'derecha':     [self.row   , self.col +2],
        }       
        

    def setMovimientosValidos(self) -> dict :
                        
        self.borders = self.limitesTablero()                                
        self.paredes = self.paredesCerca()                
        self.peones_propios = self.peonesCerca(self.side)
        self.peones_enemigos = self.peonesCerca(self.opposite)

        self.movimientos_validos = self.dicMovimientosValidos()
        self.hay_movimientos_validos =  any(self.movimientos_validos.values())
        self.valid_moves = [ move for move, valid in self.movimientos_validos.items()  if valid ]
        return self.movimientos_validos          
    
    
    def limitesTablero(self)-> dict:
        """Arma diccionario de cuantos casilleros faltan para llegar al limite indica
            Nos dice que tan lejos estan los limites del tablero segun la posicion del peon        
        Returns:
            dict: diccionario de limites en 4 direcciones
        """
        self.row_tp = int(self.row/2)
        self.col_tp = int(self.col/2)
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
        
    def peonesCerca(self,tipo) -> dict:
        
        peon_atras     = 100
        peon_adelante  = 100
        peon_izquierda = 100
        peon_derecha   = 100
        
        # --------- PEONES A LOS LADOS -------------------- 
        peones_col = self.findPeones(self.col, tipo ,'col') 
        peones_row = self.findPeones(self.row, tipo ,'row') 
        
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
    
    def findPeones(self,col ,tipo, axis ='col'):
        
        if axis== 'col':            
            return [int(i) for i in   np.where(self.board[:,col] == tipo)[0] if i != self.row ]
        else:
            return [int(i) for i in   np.where(self.board[col,:] == tipo)[0] if i != self.col]

    def dicMovimientosValidos(self) -> dict:
        
        movimientos_validos = dict()                        
                
        for direc in ['atras','adelante','izquierda','derecha']:
            # moovimiento normal en la direccion
            movimientos_validos[direc] = self.borders[direc] > 0  and self.paredes[direc]  > 1 and self.peones_propios[direc]     > 1  and self.peones_enemigos[direc] > 1     
            # # salto normal en la direccion
            # if not movimientos_validos[direc] and  self.borders[direc] > 1 and self.paredes[direc]  > 3  and self.peones_propios[direc] > 2 and self.peones_enemigos[direc] == 1:
            #     movimientos_validos[f'{direc}-salto'] = self.saltoFrontalPermitido(direc)
                
            # # salto oblicuo
            # if not movimientos_validos[direc] and self.borders[direc] > 1 and self.paredes[direc]  == 3  and self.peones_propios[direc] > 2 and self.peones_enemigos[direc] == 1:
            #     movimientos_validos[f'{direc}-obl-1'],movimientos_validos[f'{direc}-obl-2'] =  self.saltosOblicuosPermitidos(direc)                 
                    
        return movimientos_validos
   
    def move(self,to_row, to_col) -> None:
        self.board[self.row, self.col] = ' '
        self.board[to_row, to_col] = 'N'        
        self.row, self.col = to_row, to_col
            
    def seeTheGoal(self) -> bool:
        return '-' not in self.board[ self.row:, self.col]
    
    def findWalls(self,col, axis ='H'):
        
        if axis== 'H':            
            return [int(i) for i in   np.where(self.board[:,col] == self.h_wall)[0] ]
        else:
            # a = np.where(self.tablero[col,:] == self.v_wall)
            # for i in  a[0]:
            #     print(i)
            return [int(i) for i in   np.where(self.board[col,:] == self.v_wall)[0] ]
       
    def getLimits(self, row_index:int,col_index:int, tipo:str ='H') ->list:
        
        if tipo == 'H': index, thresh=col_index, row_index
        else: index, thresh =row_index, col_index
        
        walls = self.findWalls(index,tipo)
        limit_1 = int()
        limit_2 = 16
        
        for wall in walls:            
            if wall < thresh:  
                if  limit_1 < wall  : limit_1 = wall  +1                
            else: 
                if wall <  limit_2: limit_2 =  wall  -1
            
        return limit_1, limit_2    
       
    def eraseOtherPawns(self):
        pawns = self.getPawnsPositions()
        for p_row, p_col in pawns:
            if not (self.row == p_row  and self.col == p_col):
                self.board[p_row, p_col] = ' ' 
                 
    def getPawnsPositions(self) -> list:
        
                
        my_pawns =    [ [int(i),int(j)] for i,j in zip(*np.where( self.board == self.side )) ]
        enemy_pawns = [ [int(i),int(j)] for i,j in zip(*np.where( self.board == self.opposite )) ]
        return my_pawns + enemy_pawns
         
                        
    def guardarNodoAdnMoves(self):
        if (self.row,self.col) not in self.historico: # , self.border_position
            # prohibidos ={
            #     'izquierda':'derecha',
            #     'derecha':'izquierda',
            #     'atras':'adelante',
            #     'adelante':'atras'}
            moves = self.valid_moves.copy()
            # if prohibidos[self.border_position] in moves:  moves.remove(prohibidos[self.border_position])
            self.historico[ (self.row,self.col) ] = moves # , self.border_position

    def remove_movement(self, move):
        if self.existInHistoric():
            if move in self.historico[ (self.row,self.col) ]: # , self.border_position
                self.historico[ (self.row,self.col) ].remove(move) #, self.border_position
                
    def existInHistoric(self) -> bool:
        return  (self.row,self.col) in self.historico # , self.border_position
        
    def isCorner(self):
        corn1 = sorted(self.valid_moves) == ['atras','derecha']
        corn2 = sorted(self.valid_moves) == ['adelante','derecha']
        corn3 = sorted(self.valid_moves) == ['atras','izquierda']
        corn4 = sorted(self.valid_moves) == ['adelante','izquierda']
        return corn1 or corn2 or corn3 or corn4
    
    def chooseNextMove(self):
        contrario ={
            'izquierda':'derecha',
            'derecha':'izquierda',
            'atras':'adelante',
            'adelante':'atras'}
        valid_moves = self.getValidMoves()
        if contrario[self.border_position] in valid_moves and not self.isCorner():  valid_moves.remove(contrario[self.border_position])
        
        if self.border_position == 'izquierda':
            # no elible derecha
            if 'izquierda' in valid_moves:
                self.border_position = 'atras'
                self.from_move = contrario['izquierda']
                return   'izquierda'        
                
            elif 'adelante' in valid_moves: 
                self.border_position = 'izquierda'
                self.from_move = contrario['adelante']
                return   'adelante'   
                
            elif 'derecha' in valid_moves:
                self.border_position = 'adelante'
                self.from_move = contrario['derecha']
                return   'derecha'   
                
                            
            elif 'atras' in valid_moves:
                self.border_position = 'derecha'
                self.from_move = contrario['atras']
                return   'atras'   

        
        elif self.border_position == 'adelante':
            # no elegible atras
            if 'adelante' in valid_moves:             
                self.border_position = 'izquierda'
                self.from_move = contrario['adelante']
                return   'adelante' 
                
            elif 'derecha' in valid_moves:    
                self.border_position = 'adelante'
                self.from_move = contrario['derecha']
                return   'derecha' 
            
            elif 'atras' in valid_moves: 
                self.border_position = 'derecha'
                self.from_move = contrario['atras']
                return   'atras' 
                
            elif 'izquierda' in valid_moves:            
                self.border_position = 'atras'
                self.from_move = contrario['izquierda']
                return   'izquierda' 
                
            
        
        elif self.border_position == 'derecha': 
            # no elegible atras

                            
            if 'derecha' in valid_moves:    
                self.border_position = 'adelante'
                self.from_move = contrario['derecha']
                return   'derecha' 
            
            elif 'atras' in valid_moves: 
                self.border_position = 'derecha' 
                self.from_move = contrario['atras'] 
                return   'atras'           

                                            
            elif 'izquierda' in valid_moves:            
                self.border_position = 'atras'
                self.from_move = contrario['izquierda']
                return   'izquierda' 
                            
            elif 'adelante' in valid_moves:             
                self.border_position = 'izquierda'
                self.from_move = contrario['adelante']
                return   'adelante' 

            
        elif self.border_position == 'atras': 
            
            
            if 'atras' in valid_moves: 
                self.border_position = 'derecha'
                self.from_move = contrario['atras']      
                return   'atras'       
                                                        
            elif 'izquierda' in valid_moves:            
                self.border_position = 'atras'
                self.from_move = contrario['izquierda']
                return   'izquierda' 
                                                                                    
            elif 'adelante' in valid_moves:             
                self.border_position = 'izquierda'
                self.from_move = contrario['adelante']
                return   'adelante' 
                                                            
            elif 'derecha' in valid_moves:    
                self.border_position = 'adelante'
                self.from_move = contrario['derecha']
                return   'derecha' 
            
    
    def getValidMoves(self) ->list:
        if not self.existInHistoric():
            self.guardarNodoAdnMoves()
        # self.remove_movement(self.from_move)
        return self.historico[ (self.row,self.col) ] #, self.border_position

         
    def thereIsValidMoves(self) -> bool:
        if (self.row,self.col) in self.historico:#, self.border_position
            return len(self.historico[ (self.row,self.col) ])>0 #, self.border_position
        return True
        
    def thereIsWayOut(self):
        
        valid_moves = True
        self.eraseOtherPawns()
    
        left_limit ,_ =  self.getLimits(self.row, self.col, 'V')
    
        self.move(self.row, left_limit)        
        self.border_position ='izquierda'                
        movimientos = self.armarDictDirecciones()       
        see_goal = self.seeTheGoal()
        
        while not see_goal and valid_moves:
            
           
            see_goal = self.seeTheGoal()
                        
            movimientos = self.armarDictDirecciones()
            self.setMovimientosValidos()  
           
            self.actual_move = self.chooseNextMove()
            valid_moves = self.thereIsValidMoves()
            
            if self.actual_move  and valid_moves:
                
                self.remove_movement(self.actual_move)
                to_row , to_col =  movimientos[ self.actual_move ]                
                self.move(to_row , to_col)

            valid_moves = self.thereIsValidMoves()
            
        
        
        return see_goal and valid_moves   
    