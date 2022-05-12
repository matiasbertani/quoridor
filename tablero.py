class Tablero:
    def __init__(self) -> None:
        # que el tablero sea una mtrz numpy 18x18
        #espacios pares
        pass
    
    
    
    
class Peon:
    
    def __init__(self,i,j, np_board) -> None:
        
        pass
    
    
    def movimientosValidos() -> list:
        pass
    
    

class Pared:
    pass
    

async def process_your_turn(websocket, request_data):
    if randint(0, 4) > 0:
        await process_move(websocket, request_data)
    else:
        await process_wall(websocket, request_data)


async def process_move(websocket, request_data):
        side = request_data['data']['side']
        pawn_board = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                string_row = request_data['data']['board'][17*(row*2): 17*(row*2) + 17]
                pawn_board[row][col] = string_row[col * 2]
        for row in range(9):
            for col in range(9):
                if pawn_board[row][col] == side:
                    from_row = row
                    from_col = col
                    to_col = col
                    break
        to_row = from_row + (1 if side == 'N' else -1)
        if pawn_board[to_row][from_col] != ' ':
            to_row = to_row + (1 if side == 'N' else -1)
        await send(
            websocket,
            'move',
            {
                'game_id': request_data['data']['game_id'],
                'turn_token': request_data['data']['turn_token'],
                'from_row': from_row,
                'from_col': from_col,
                'to_row': to_row,
                'to_col': to_col,
            },
        )


async def process_wall(websocket, request_data):
    await send(
        websocket,
        'wall',
        {
            'game_id': request_data['data']['game_id'],
            'turn_token': request_data['data']['turn_token'],
            'row': randint(0, 8),
            'col': randint(0, 8),
            'orientation': 'h' if randint(0, 1) == 0 else 'v'
        },
    )


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(start(auth_token))
    else:
        print('please provide your auth_token')


