
class Action:
            
    def __init__(self, data) -> None:
        
        self.action = None
        self.game_id = data['game_id']
        self.turn_token = data['turn_token']
        
    def to_dict(self):
        return {
            'action': self.action,
            'data': {
                'game_id': self.game_id,
                'turn_token': self.turn_token,
            },
        }
 
    
class Move(Action):
    
    def __init__(self, data, from_row, from_col,to_row, to_col) -> None:
        super().__init__(data)
        self.action = 'move'
        self.from_row = from_row
        self.to_row = to_row
        self.from_col = from_col
        self.to_col = to_col
        
    def to_dict(self):
        
        ret = super().to_dict()
        ret['data'].update({
            'from_row': self.from_row,
            'to_row': self.to_row,
            'from_col': self.from_col,
            'to_col': self.to_col,
        })
        return ret
    
    
class WallAction(Action):
    def __init__(self, data, row, col, orientation) -> None:
        super().__init__(data)
        self.action = 'wall'
        self.row = row
        self.col = col
        self.orientation = orientation

    def to_dict(self):
        ret = super().to_dict()
        ret['data'].update({
            'row': self.row,
            'col': self.col,
            'orientation': self.orientation,
        })
        return ret