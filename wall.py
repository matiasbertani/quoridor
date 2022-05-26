import numpy as np
from scanner import Scanner

class Wall:
    
    def __init__(self,row:int,col:int,tipo:str,board:np.array,side) -> None:
        ## ! prhibir creacion con corrdenadas 8,8
        # self.row_cordenada = row # coordanada paso al programa
        # self.col_cordenada = col # cordenada paso al progrrama
        self.row = row
        self.col = col
        
        self.side = side
        self.tipo = tipo
        self.board = board
        
        # # asterisco '*'     - centro de pared
        # self.row,self.col = int(), int()
        # guion '-' o '|'   -  muro de pared
        self.row_muro_1, self.col_muro_1 = int(), int()
        self.row_muro_2, self.col_muro_2 = int(), int()
        self.setWallIndex()
        
    def setWallIndex(self) -> None:
        """obtiene los valores de row y col para la matriz de 17x17"""
                    # posiciones del asterisco centro de pared
        # self.row = int( self.row_cordenada*2 + 1 )
        # self.col = int( self.col_cordenada*2 + 1 )
        
        if self.tipo == 'h':
            # -*-
            #muros o costados de parec. guiones '-'
            self.row_muro_1, self.col_muro_1  = self.row, self.col - 1
            self.row_muro_2, self.col_muro_2  = self.row, self.col + 1
            
        else: 
        
            #muros o costados de parec. guiones '|'
            self.row_muro_1, self.col_muro_1  = self.row -1, self.col 
            self.row_muro_2, self.col_muro_2  = self.row +1, self.col 
                          
    def movimientoPermitido(self) -> bool:
        
        # verifica que donde vaya a 
        # colocarse no haya ninguna otra pared con la que colisione
        return self.emptySpace() and not self.produces_closure() 
    
    def emptySpace(self) -> bool  :
        """        
        verifica que el espacio para colocar este vacio y no haya colision o invalidez
        Returns:
            bool: True o Fase si el lugar esta vacio para colocar una pared
        """
        muro_1 = self.board[self.row_muro_1,self.col_muro_1] == ' '
        centro = self.board[self.row,self.col] == ' '
        muro_2 = self.board[self.row_muro_2,self.col_muro_2] == ' '
        return muro_1 and centro and muro_2
    
    def produces_closure(self) -> bool:
        self.putWall()
        pawn_closed = False
        pawns = self.getPawnsPositions()
        # validate for every pawn in board
        for p_row, p_col  in pawns:
            way_out = Scanner( p_row, p_col, self.board.copy(), 'N').thereIsWayOut()
            if not way_out:
                pawn_closed = True
                break
            
        return pawn_closed
    
    @staticmethod
    def hayWall(board, row,col, tipo = 'h') -> bool:
        if tipo == 'h':            
            muro1 =  board[row, col -1] == '-'
            centro = board[row, col]    == '*'
            muro2 =  board[row, col +1] == '-'
        else:
            muro1 =  board[row -1, col] == '|'
            centro = board[row, col]    == '*'
            muro2 =  board[row +1, col] == '|'
        return muro1 and centro and muro2
        
    def putWall(self) -> None: 
        
        if self.tipo =='h':muro = '-'
        else: muro ='|'

        self.board[self.row_muro_1,self.col_muro_1] = muro
        self.board[self.row,self.col] = '*'
        self.board[self.row_muro_2,self.col_muro_2] = muro
      
        
    def getPawnsPositions(self) -> list:
        
                
        my_pawns =    [ [int(i),int(j)] for i,j in zip(*np.where( self.board == 'N' )) ]
        enemy_pawns = [ [int(i),int(j)] for i,j in zip(*np.where( self.board == 'S' )) ]
        return my_pawns + enemy_pawns 
    
    
    
    
    @staticmethod
    def ubicarPosicion(row,col,side):
        zeros = np.zeros(( 17,17  ))
        zeros[row,col] = 8
        if side == 'S' : 
            zeros = np.flipud( zeros)
        return [[int(i),int(j)] for i,j in zip(*np.where( zeros == 8 ))][0]
    
    @staticmethod
    def getWallCordinates(w_row,w_col,side):
        w_row,w_col = Wall.ubicarPosicion(w_row,w_col, side)
        row = int((w_row -1)/2)
        col = int((w_col -1)/2)
        return row, col
        
    
    # tiene que ser un metodo de clase para acceder sin crear ninguna instancia
    @staticmethod
    def getEmptyWallPlaces( board) -> list:        #self,
        """Entrega una lista de todos los lugares posibles para las walls """
        
        return [[(int(i)*2) +1,(int(j)*2) +1]for  i,j in zip(*np.where(board[1::2,1::2]==' '))]
        
    @staticmethod
    def WallInFront(board,p_row, p_col) -> bool:
        return board[p_row - 1, p_col ]  == '-'
    
    @staticmethod
    def gethorizontalWallCoordinates(board,p_row, p_col) -> list:
        
        wall_row   = p_row -1
        wall_col_1 = p_col -1
        wall_col_2 = p_col +1
        return [wall_row, wall_col_1], [wall_row, wall_col_2]
    
    
    
    @staticmethod
    def canCageUp(board,p_row, p_col) -> bool:
        empty_places = list()
        v_wall_left  = p_row-1, p_col -1 
        v_wall_rigth  = p_row-1, p_col +1 
        left_way  = p_row+1, p_col -2 
        rigth_way = p_row+1, p_col +2
        
        if  board[left_way] == ' ' and not Wall.hayWall(board,*v_wall_left,'v'):
            return 'left'
        if  board[rigth_way] == ' ' and not Wall.hayWall(board,*v_wall_rigth,'v'):
            return 'rigth'
            
            
            # si puede enjaular
            pass
        
        
        Wall.WallInFront(board,p_row, p_col)
        # espacio de wall al lado disponible
        # row, col-1 or  row, col+1 empty
            
    
    @staticmethod
    def freeWaySide(board, p_row, p_col) -> str:
        
        if p_col == 0 or  p_col == 16:
            return ''
            
        
        left_way  = p_row-1 , p_col -2 
        rigth_way = p_row-1 , p_col +2
        if  board[left_way] == ' ' :
            return 'left'
        elif  board[rigth_way] == ' ':
            return 'rigth'
        
    @staticmethod
    def wallIndexSide( p_row, p_col,side):
        
        if side == 'left':
            return [p_row+1, p_col -1],[p_row-1, p_col -1]
        
        elif side == 'rigth':
            return [p_row+1, p_col +1 ], [p_row-1, p_col +1 ]
            
        elif side == 'front':             
            return [p_row -1, p_col -1], [p_row -1, p_col +1]
            