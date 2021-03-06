from random import  randint
from actions import *
from peon import Peon
from wall import Wall
import numpy as np
import time

class Partida:
    
    def __init__(self, data_game) -> None:
        
        self.id_game = data_game['game_id']
        
        self.str_board = data_game['board']
        self.side = data_game['side']
        
        opciones_side = ['N','S']
        opciones_side.remove(self.side)
        self.opposite = opciones_side[0]
        
        self.np_board = self.to_numpy(self.str_board)
        
        self.historial_movimientos = None
        
        self.side = data_game['side']
        
        self.TIMEOUT = 15
        self.data_actual = data_game
        self.col_points = np.array([ 2**i for i in range(9) ])
    
        self.len_board = 9
        self.board_length = 17
        
        self.h_wall = '-'
        self.v_wall = '|'
        
        self.walls_restantes = 10
        self.movimientos_restantes = 200
    
    def actualizar_tablero(self):
        
        self.np_board = self.to_numpy(self.str_board)
        if self.side == 'S': self.np_board = np.flipud(self.np_board)
        
    
    def actualizar_data(self, data):
        
        self.data_actual = data
        self.str_board = data['board']
        self.np_board = self.to_numpy(self.str_board)
        self.walls_restantes = int(data['walls'])
        self.movimientos_restantes = int(data['remaining_moves'])
        self.side = data['side']
        
        opciones_side = ['N','S']
        opciones_side.remove(self.side)
        self.opposite = opciones_side[0]
        self.print_board()
        
        
        pass
    
    def print_board(self):
        """show the boar normalized
        """
        print('='*17+"    SIDE : "+self.side)
        if self.side == 'S': board = np.flipud(self.np_board)
        else:board = self.np_board 
        for row in board :print( ''.join(list(row)))
        print('='*17)
        print()
        time.sleep(0.5)
    
    def to_numpy(self,board):
        board = np.array(list(board)).reshape(17,17)
        if self.side == 'S': 
            board = np.flipud(board)
            
        
        return board
    
    def to_str(self,np_board:np.array):
        if self.side == 'S': np_board = np.flipud(np_board)
        return ''.join(list(np_board.reshape(289)))
          
    
    def getRealPosition(self, row,col,side):
        zeros = np.zeros(( self.board_length, self.board_length  ))
        zeros[row,col] = 8
        if side == 'S' : 
            zeros = np.flipud( zeros)
        return [[int(i),int(j)] for i,j in zip(*np.where( zeros == 8 ))][0]
 
    def flipBoard(self, board:np.array) -> np.array:
        return np.flipud(board)
        
 
    def getPawns(self):        
        return [ Peon(int(i),int(j),self.np_board,self.side ) for i,j in zip(*np.where( self.np_board == self.side )) ]
       
    def getEnemysPawns(self):
        
        return [ [int(i),int(j)] for i,j in zip(*np.where( self.np_board == self.opposite )) ]
  

    def calculateMoves(self):
        
        self.peones = self.getPawns()        
        self.mejores_opciones = {}
        for i,peon in enumerate(self.peones):
                    
            if peon.hay_movimientos_validos:
                mov,puntos = peon.mejorMovimiento()   
                self.mejores_opciones[i] = [mov,puntos]
           
        return len(self.mejores_opciones)

    
    def elegirMejorMovimiento(self):
            
        
        move_wall, action = self.wallManagement()
        if move_wall: return action
        
        self.calculateMoves()  
        if randint(0, 6) > 0 : id_peon = -1
        
        else:
            if len(self.mejores_opciones ) > 1:
                id_peon = -2
            else:id_peon = -1
        
        peon_index,[best_move,puntaje] = sorted(self.mejores_opciones.items(),  key= lambda x: x[1][1] )[id_peon]
        
        # en caso de que haya un paredes disponibles y peones cerca de la meta
        
        
        return self.movePawn(peon_index, best_move )
        
    
    def putHorizontalWall(self):
        pawns = self.getEnemysPawns()
        pawns = sorted( pawns , key = lambda x: x[0])
        # pawns.reverse()
        self.empty_wall_places = Wall.getEmptyWallPlaces(self.np_board.copy())
        poner_wall = False
        w_row, w_col = None, None
        
        
        for p_row, p_col  in pawns: 
            
            if p_row < 10:
                if not Wall.WallInFront(self.np_board.copy(), p_row, p_col):
                    
                    possible_walls = Wall.wallIndexSide( p_row, p_col, 'front')
                    
                    for w_row, w_col in possible_walls :
                        if [w_row, w_col] in self.empty_wall_places:
                            if Wall(w_row, w_col, 'h', self.np_board.copy(),self.side).movimientoPermitido():
                                poner_wall = True
                                break                            
                    else:
                        continue
                    break
                            
        return   poner_wall, w_row, w_col
      

     
    def wallManagement(self):
        
        move_wall = False
        action = None
        self.enemy_pawns = self.getEnemysPawns()
        
        self.empty_wall_places = Wall.getEmptyWallPlaces(self.np_board.copy())
        
        if self.walls_restantes:
            if randint(0,7)>0:
                move_wall , w_row, w_col = self.putHorizontalWall()
                if move_wall: 
                    w_row, w_col = Wall.getWallCordinates(w_row, w_col,self.side)                
                    return move_wall, WallAction(self.data_actual,w_row, w_col,'h').to_dict()
            
            move_wall , w_row, w_col = self.putVerticalWall() 
            if move_wall: 
                w_row, w_col = Wall.getWallCordinates(w_row, w_col,self.side)                
                return move_wall, WallAction(self.data_actual,w_row, w_col,'v').to_dict()
        return   move_wall, action
    
    
    def movePawn(self,peon_index,movimiento):
        
        peon = self.peones[peon_index]
        
        to_row, to_col = peon.mapa_movimiento[movimiento]
        from_row, from_col = peon.ubicacionPeon()
      
        
        from_row_2, from_col_2 = int(from_row/2), int(from_col/2)
        to_row_2, to_col_2 = int(to_row/2), int(to_col/2)
                     
        return Move(self.data_actual,from_row_2, from_col_2, to_row_2, to_col_2).to_dict() 

    
    def putVerticalWall(self):
        
        
        
        put_wall, wall_row, wall_col =False, None, None
        
        
        
        # verificar pared de delante
        for p_row, p_col  in self.enemy_pawns: 
            if Wall.WallInFront(self.np_board, p_row, p_col):
            
                way = Wall.freeWaySide(self.np_board, p_row, p_col )
                if way:
                    
                    #obtienne walls            
                    walls = Wall.wallIndexSide( p_row, p_col,way )
                    # verifica 
                    for wall_row, wall_col in walls:
                        
                        if [wall_row, wall_col] in self.empty_wall_places:
                        
                            if Wall(wall_row, wall_col, 'v', self.np_board.copy(),self.side).movimientoPermitido():
                                put_wall = True 
                                break 
                    else: continue        
                    break                    
        
        return put_wall, wall_row, wall_col
    
