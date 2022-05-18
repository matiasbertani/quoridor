import sys
from pathlib import Path

file = Path(__file__).resolve()
parent = file.parent.parent
sys.path.append(str(parent))
from peon import Peon


import unittest
import numpy as np

class TestPuntuacionBoard(unittest.TestCase):
    
    def test_board_peones_puntuado_0(self):
        
        
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
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', '*', '-', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        p = Peon( p_row, p_col, board, side)
        p.puntuarDetrasWall(8)  # detras primer muro
        p.puntuarDetrasWall(10) # detras segundo muro
        result_0 = list(p.tablero_peones[:,8])
        result_1 = list(p.tablero_peones[:,4])
        result_2 = list(p.tablero_peones[:,5])
        result_3 = list(p.tablero_peones[4,:])
        print(p.tablero_peones)

        self.assertEqual([-2,-4,-8,-16, 0 ,32, 64, 128, 256],result_0  )
        self.assertEqual([-2,-4,-8,-16,0,-40,-30,-20,-10],result_1  )
        self.assertEqual([-2,-4,-8,-16,0,-40,-30,-20,-10],result_2  )
        self.assertEqual([0]*9,result_3  )
        
        
        
    
    def test_board_peones_puntuado_1(self):
        
        p_row ,p_col ,side = 8, 8, 'N'
        board = np.array([
        
        # 0    1    2    3    4    5    6    7    8    9   10   11   12  13   14   15   16    
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 6
        [' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', '*', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 7
        [' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', 'N', '|', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 8
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 9
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 10
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 11
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 12
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 13
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 14
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' '], # 15
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']] # 16
            
            )
        p = Peon( p_row, p_col, board, side)
        p.puntuarDetrasWall(8)  # detras primer muro
        p.puntuarDetrasWall(10) # detras segundo muro
        col_peon = list(p.tablero_peones[:,4])
        row_peon = list(p.tablero_peones[4,:])
        row_detras_peon = list(p.tablero_peones[3,:])
        
        # print(p.tablero_peones)
        self.assertEqual([-2,-4,-8,-16, 0 ,32, 64, 128, 256],col_peon  )
        self.assertEqual([-5,-5,-5,0,0,-5,-5,-5,-5],row_peon  )
        self.assertEqual([-16]*9,row_detras_peon  )
        
        
        
        
    
    
    
    
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    # def test_board_peones_puntuado_0():
    #     pass
    
if __name__ == '__main__':
    unittest.main()