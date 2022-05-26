import sys
from pathlib import Path

from matplotlib.pyplot import get
from pyrsistent import v

file = Path(__file__).resolve()
parent = file.parent.parent
sys.path.append(str(parent))
from peon import Peon



import unittest
import numpy as np

# from ..peon import *



def get_np_tablero() ->np.array:
    tablero_str = ' '*289
    return np.array(  list(tablero_str) ).reshape(17,17)
      
def getPeon(p_row,p_col,side, board = None) -> Peon:        
        if board is None: board = get_np_tablero()    
        board[p_row,p_col] = side
        return Peon( p_row, p_col, board, side)


def getPeonWithWalls(p_row,p_col,side, h_wall=None, v_wall=None) -> Peon:
    if h_wall is None: h_wall=list()
    if v_wall is None: v_wall=list()
    board = get_np_tablero()
    
    for row,col in h_wall:
        board[row,col-1], board[row,col],board[row,col+1]  ='-','*','-'
    for row,col in v_wall:
        board[ row-1,col]  = '|'
        board[ row,col]    = '*'
        board[ row+1,col]  = '|'
        
    return getPeon(p_row,p_col,side, board)

def getPeonWithPeones(p_row,p_col,side,peones_mios=None, peones_enemigos=None):
    
    all_sides = ['N','S']
    all_sides.remove(side)
    enemy_side = all_sides[0]

    board = get_np_tablero()
    
    if peones_mios is None: peones_mios=list()
    if peones_enemigos is None: peones_enemigos=list()
    
    for row,col in peones_mios: board[row,col] = side
    
    for row,col in peones_enemigos: board[row,col] = enemy_side

    return getPeon(p_row,p_col,side, board)

class  TestPeones( unittest.TestCase):
    
    # region TEST detecion de bordes tablero
    
    def test_border_cases_1(self):

        result = getPeon( 10, 10,  'N').getBoarBorders()
        self.assertEqual({'atras': 5, 'adelante': 3, 'izquierda': 5, 'derecha': 3},result)
            
    def test_border_cases_2(self):
        """esquina superior izquierda"""        
        result = getPeon( 0, 0,  'N').getBoarBorders()
        self.assertEqual({'atras': 0, 'adelante': 8, 'izquierda': 0, 'derecha': 8},result)
        
    def test_border_cases_3(self):        
        """esquina superior derecha"""
        result = getPeon(0, 16, 'N' ).getBoarBorders()
        self.assertEqual({'atras': 0, 'adelante': 8, 'izquierda': 8, 'derecha': 0},result)        
        
    def test_border_cases_4(self):        
        """esquina inerior derecha"""
        result = getPeon(16, 16, 'N' ).getBoarBorders()
        self.assertEqual({'atras': 8, 'adelante': 0, 'izquierda': 8, 'derecha': 0},result)        

    def test_border_cases_5(self):        
        """esquina inerior izquierda"""
        result = getPeon(16, 0, 'N' ).getBoarBorders()
        self.assertEqual({'atras': 8, 'adelante': 0, 'izquierda': 0, 'derecha': 8},result)        
        
    def test_border_cases_6(self):        
        """esquina inferior medio"""
        result = getPeon(16, 8, 'N' ).getBoarBorders()
        self.assertEqual({'atras': 8, 'adelante': 0, 'izquierda': 4, 'derecha': 4},result)        

    # endregion TEST detecion de bordes tablero
    
    # region TEST DISTANCIA PAREDES
    

    def test_pared_distantia_0(self):
        result = getPeonWithWalls(0,8,'N' ).paredesCerca()
        self.assertEqual( {'atras':100,'adelante':100,'izquierda':100,'derecha':100},result  )
    
    def test_pared_distantia_1(self):
        result = getPeonWithWalls(0,8,'N',h_wall=[[1,9]], ).paredesCerca()
        self.assertEqual( {'atras':100,'adelante':1,'izquierda':100,'derecha':100},result  )
    
    def test_pared_distantia_2(self):
        result = getPeonWithWalls(0,8,'N',h_wall=[[3,9]], ).paredesCerca()
        self.assertEqual( {'atras':100,'adelante':3,'izquierda':100,'derecha':100},result  )
    
    def test_pared_distantia_3(self):
        result = getPeonWithWalls(0,8,'N',h_wall=[[1,9],[3,9]], ).paredesCerca()
        self.assertEqual( {'atras':100,'adelante':1,'izquierda':100,'derecha':100},result  )
    
    def test_pared_distantia_4(self):
        result = getPeonWithWalls(0,8,'N',h_wall=[[1,9],[3,9]],v_wall=[[1,5]] ).paredesCerca()
        self.assertEqual( {'atras':100,'adelante':1,'izquierda':3,'derecha':100},result  )
        
    def test_pared_distantia_5(self):
        result = getPeonWithWalls(0,8,'N',h_wall=[[1,9],[3,9]],v_wall=[[1,5],[1,7]] ).paredesCerca()
        self.assertEqual( {'atras':100,'adelante':1,'izquierda':1,'derecha':100},result  )
    
    def test_pared_distantia_6(self):
        result = getPeonWithWalls(8,8,'N',  h_wall=[[1,9],[3,9]], v_wall=[[1,5],[1,7]] ).paredesCerca()
        self.assertEqual( {'atras':5,'adelante':100,'izquierda':100,'derecha':100},result  )
    
    def test_pared_distantia_7(self):
        result = getPeonWithWalls(8,8,'N',  h_wall=[[9,9],[7,7]], v_wall=[[1,5],[7,1]] ).paredesCerca()
        self.assertEqual( {'atras':1,'adelante':1,'izquierda':7,'derecha':100},result  )
    
    
    # endregion 
     
    # region ------ TEST DISTNACIA PEON ----------
    
    def test_distancia_peon_0(self):
        """sin peones cerca"""
        result =getPeonWithPeones(0,8,'N').getNearbyPawns('N')
        self.assertEqual({'atras':100,'adelante':100,'izquierda':100,'derecha':100} ,  result)
    
    def test_distancia_peon_1(self):
        """sin peones cerca"""
        result = getPeonWithPeones(0,8,'N',peones_enemigos=[[2,8]]).getNearbyPawns('N')
        self.assertEqual({'atras':100,'adelante':100,'izquierda':100,'derecha':100} ,  result)
        
    def test_distancia_peon_2(self):
        """sin peones cerca"""
        result = getPeonWithPeones(0,8,'N',peones_enemigos=[[2,8]]).getNearbyPawns('S')
        self.assertEqual({'atras':100,'adelante':1,'izquierda':100,'derecha':100} ,  result)
    
    def test_distancia_peon_3(self):
        """sin peones cerca"""
        result = getPeonWithPeones(0,8,'N',peones_enemigos=[[2,8],[4,8]]).getNearbyPawns('S')
        self.assertEqual({'atras':100,'adelante':1,'izquierda':100,'derecha':100} ,  result)
    
    def test_distancia_peon_4(self):
        """sin peones cerca"""
        result = getPeonWithPeones(0,8,'N',peones_enemigos=[[2,8],[4,8]]).getNearbyPawns('S')
        self.assertEqual({'atras':100,'adelante':1,'izquierda':100,'derecha':100} ,  result)
    
    def test_distancia_peon_5(self):
        """sin peones cerca"""
        result = getPeonWithPeones(0,8,'N',peones_enemigos=[[4,8]]).getNearbyPawns('S')
        self.assertEqual({'atras':100,'adelante':2,'izquierda':100,'derecha':100} ,  result)
    
    def test_distancia_peon_6(self):
        """sin peones cerca"""
        result = getPeonWithPeones(0,8,'N',peones_enemigos=[[4,8]], peones_mios=[[2,8]]).getNearbyPawns('S')
        self.assertEqual({'atras':100,'adelante':2,'izquierda':100,'derecha':100} ,  result)
        
    def test_distancia_peon_7(self):
        """sin peones cerca"""
        result = getPeonWithPeones(2,8,'N',peones_enemigos=[[2,6],[8,8],[6,8]]).getNearbyPawns('S')
        self.assertEqual({'atras':100,'adelante':2,'izquierda':1,'derecha':100} ,  result)
        
    def test_distancia_peon_8(self):
        """sin peones cerca"""
        result = getPeonWithPeones(4,8,'N',
                                   peones_enemigos=[[2,6],[8,8],[6,8]],
                                   peones_mios=[[0,8],[4,0],[4,10]]).getNearbyPawns('N')
        self.assertEqual({'atras':2,'adelante':100,'izquierda':4,'derecha':1} ,  result)
   
    def test_distancia_peon_9(self):
        """sin peones cerca"""
        result = getPeonWithPeones(10,8,'N',peones_mios=[[14,8],[8,8],[10,14]]).getNearbyPawns('N')
        self.assertEqual({'atras':1,'adelante':2,'izquierda':100,'derecha':3} ,  result)
    
    # endregion  
        

    
    def test_movimientos_validos_00(self):
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'N', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':True,'izquierda':True,'derecha':True},result)
        
        
        pass
    
    def test_movimientos_validos_01(self):
        
        p_row ,p_col ,side = 8, 0, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        ['N', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':True,'izquierda':False,'derecha':True},result)
         
    def test_movimientos_validos_02(self):
        
        p_row ,p_col ,side = 8, 0, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        ['N', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':True,'izquierda':False,'derecha':False},result)
        
    def test_movimientos_validos_03(self):
        
        p_row ,p_col ,side = 2, 10, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'N', '|', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ',' ', ' ', ' ', ' '], # 3
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
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':False,'izquierda':True,'derecha':False},result)
        
    def test_movimientos_validos_04(self):
        
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', '*', '-', '*', '-', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', '|', 'S', ' ', 'N', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':False,'adelante':True,'izquierda':False,'derecha':True,'izquierda-obl-1':False,'izquierda-obl-2':True},result)
        
    def test_movimientos_validos_05(self):
                
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', '-', '*', '-', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', '|', 'S', ' ', 'N', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':False,'adelante':True,'izquierda':False,'derecha':True,'izquierda-obl-1':True,'izquierda-obl-2':True},result)
        
        pass
    
    def test_movimientos_validos_06(self):
        
                
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', 'N', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':True,'izquierda':False,'derecha':True,'izquierda-salto':True},result)
        
    def test_movimientos_validos_07(self):
        
                        
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', 'N', ' ', 'N', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':True,'izquierda':False,'derecha':False,'izquierda-salto':True},result)
        
    def test_movimientos_validos_08(self):
                                
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', 'N', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result = Peon( p_row, p_col, board, side).setValidMoves()
        self.assertEqual({'atras':True,'adelante':False,'izquierda':False,'derecha':False,'adelante-salto':True},result)
    
    def test_movimientos_validos_09(self):
                                        
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', 'N', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'N', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        result =Peon( p_row, p_col, board, side).getValidMoves()
        result = [  i[0] for i  in  result.items() if i[1]]        
        self.assertEqual(['atras'],result)
    
    def test_movimientos_validos_10(self):
        p_row ,p_col ,side = 8, 16, 'N'
        board =np.array([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', '-', '*', '-'],
            ['N', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', 'S'],
            ['-', '*', '-', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', '-','*', '-', ' ', ' '],
            [' ', ' ', ' ', ' ', 'N', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', 'N'],
            [' ', ' ', '-', '*', '-', ' ', '-', '*', '-', ' ', ' ', ' ', ' ',' ', '-', '*', '-'],
            [' ', '|', 'S', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
            [' ', ' ', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']])
        result =Peon( p_row, p_col, board, side).getValidMoves()
        result = [  i[0] for i  in  result.items() if i[1]]        
        self.assertEqual(['atras-obl-1', 'izquierda'], result)
  

    # endregion
    
if __name__ == '__main__':
    # print(os.getcwd())



    unittest.main()