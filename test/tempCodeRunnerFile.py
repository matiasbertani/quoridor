  def test_posicion_wall_0(self):
        board =get_board()
        w = Wall(4,4,'h',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([9,8],[9,9],[9,10]),(muro1,centro,muro2))
        
    def test_posicion_wall_1(self):
        board =get_board()
        w = Wall(4,4,'v',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([8,9],[9,9],[10,9]),(muro1,centro,muro2))

    def test_posicion_wall_2(self):
        board = get_board()
        w = Wall(3,1,'h',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([7,2],[7,3],[7,4]),(muro1,centro,muro2))

    def test_posicion_wall_3(self):
        board =get_board()
        w = Wall(3,1,'v',board,'N')
        muro1 = [w.row_muro_1, w.col_muro_1]
        centro = [w.row, w.col]
        muro2 = [w.row_muro_2, w.col_muro_2]
        #  -*-
        self.assertEqual(([6,3],[7,3],[8,3]),(muro1,centro,muro2))
    
    # endregion --------------------------------------------
