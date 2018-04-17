from enum import IntEnum

class PlayerID(IntEnum):
    P1 = 1
    P2 = 2

def get_player_color(inPId):
    return "cyan" if inPId == PlayerID.P1 else "gold"

def get_player_name(inPId):
    return "player1" if inPId == PlayerID.P1 else "player2"

def get_other_player(inPId):
    return PlayerID.P1 if inPId == PlayerID.P2 else PlayerID.P2