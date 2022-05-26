import sys
from pathlib import Path

from pandas import array

file = Path(__file__).resolve()
parent = file.parent.parent
sys.path.append(str(parent))
from wall import Wall
import numpy as np


                
def get_board()->np.array:
    return np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )

def get_board_with_walls(h_wall=None, v_wall=None) -> np.array:
    if h_wall is None: h_wall=list()
    if v_wall is None: v_wall=list()
    board = get_board()
    
    for row,col in h_wall:
        board[row,col-1], board[row,col],board[row,col+1]  ='-','*','-'
    for row,col in v_wall:
        board[ row-1,col]  = '|'
        board[ row,col]    = '*'
        board[ row+1,col]  = '|'
    return board     
    
        


import unittest
import numpy as np


class TestWall(unittest.TestCase):
    #region --- TESTS CALCULO DE POSICION DE WALL CON COORDENADAS ---
    
    def test_posicion_wall_0(self):
        board =get_board()
        w = Wall(9,9,'h',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([9,8],[9,9],[9,10]),(muro1,centro,muro2))
        
    def test_posicion_wall_1(self):
        board =get_board()
        w = Wall(9,9,'v',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([8,9],[9,9],[10,9]),(muro1,centro,muro2))

    def test_posicion_wall_2(self):
        board = get_board()
        w = Wall(7,3,'h',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([7,2],[7,3],[7,4]),(muro1,centro,muro2))

    def test_posicion_wall_3(self):
        board =get_board()
        w = Wall(7,3,'v',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([6,3],[7,3],[8,3]),(muro1,centro,muro2))
    
    # endregion --------------------------------------------



    #region --- TESTS ESPACIO VACIO ---
    
    def test_espacio_vacio_0(self):
        board =get_board_with_walls()
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( True, result)
        
    def test_espacio_vacio_1(self):
        board =get_board_with_walls()
        result = Wall(9,9,'v',board,'N').emptySpace()
        self.assertEqual( True, result)
            
    def test_espacio_vacio_2(self):
        board =get_board_with_walls(h_wall=[[9,9]])
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( False, result)
          
    def test_espacio_vacio_3(self):
        board =get_board_with_walls(h_wall=[[9,7]])
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( False, result)
          
    def test_espacio_vacio_4(self):
        board =get_board_with_walls(h_wall=[[9,11]])
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( False, result)
              
    def test_espacio_vacio_5(self):
        board =get_board_with_walls(v_wall=[[11,9]])
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( True, result)
    
    def test_espacio_vacio_6(self):
        board =get_board_with_walls(v_wall=[[7,9]])
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( True, result)
        
    def test_espacio_vacio_7(self):
        board =get_board_with_walls(v_wall=[[7,7]])
        result = Wall(9,9,'h',board,'N').emptySpace()
        self.assertEqual( True, result)
        
    def test_espacio_vacio_8(self):
        board =get_board_with_walls(v_wall=[[7,9]])
        result = Wall(9,9,'v',board,'N').emptySpace()
        self.assertEqual( False, result)
        
    def test_espacio_vacio_7(self):
        board =get_board_with_walls(v_wall=[[11,9]])
        result = Wall(9,9,'v',board,'N').emptySpace()
        self.assertEqual( False, result)
    # endregion ----------------------
    
    # region ---- TEST WALL COLOCATION ----
    
    def test_colocate_wall_0(self):
        empty_board = get_board()
        
        w = Wall(1,1,'h',empty_board,'N')
        w.putWall()        
        
        muro_1 = w.board[1,0]  == '-'
        centro = w.board[1,1]  == '*'
        muro_2 = w.board[1,2]  == '-'
        
        self.assertEqual(muro_1 and centro and muro_2, True)
        
        
    
    
    def test_colocate_wall_1(self):
        empty_board = get_board()
        
        w = Wall(1,1,'v',empty_board,'N')
        w.putWall()        
        
        muro_1 = w.board[0,1]  == '|'
        centro = w.board[1,1]  == '*'
        muro_2 = w.board[2,1]  == '|'        

        
        self.assertEqual(muro_1 and centro and muro_2, True)
        
        
 
        
        
    # endregion  --------------------------------


    def test_allowed_collocation_00(self):
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', 'N', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        ['-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )

        result = Wall(7, 3, 'v', board,'S').movimientoPermitido()
        self.assertEqual(False, result)
        
    def test_allowed_collocation_01(self):
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', 'N', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        ['-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )

        result = Wall(9, 3, 'v', board,'S').movimientoPermitido()
        self.assertEqual(False, result)
        
    def test_allowed_collocation_02(self):
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', 'N', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        ['-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )

        result = Wall(7, 1, 'h', board,'S').movimientoPermitido()
        self.assertEqual(False, result)
        
    def test_allowed_collocation_02(self):
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', 'N', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        ['-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )

        result = Wall(3, 1, 'h', board,'S').movimientoPermitido()
        self.assertEqual(True, result)
        
        
    def test_allowed_collocation_03(self):
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', 'N', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        ['-', '*', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )

        result = Wall(9, 3, 'h', board,'S').movimientoPermitido()
        self.assertEqual(False, result)


    # region ----- TEST si hay ENCERRAMIENTO 

        # caso de cerrar un peon con una barra horizontal
    
        # caso de encerrar un pon en un casillero chiqiuito
        
        # caso de encerrar un peon en un esquin
        
        # caso de encerrar con una barra vertical en una esquina
        
        # caso de encerrar con un aforma no cuadrada
        
        # caso de generar un pasilllo no cerrado 
    
    
    # endregion   ------------------------------  

    
    # region ----- TEST WALL COLOCATION INTO BOARD
    
    
    

    
    
    # endregion   ------------------------------  
    
    
    
    
    
  

if __name__ == '__main__':
    unittest.main()