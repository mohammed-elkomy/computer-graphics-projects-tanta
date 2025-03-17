from enum import Flag, auto


class ColorOfClothing(Flag):
    Yellow = auto()
    Red = auto()
    Blue = auto()
    Green = auto()


class GameScenes(Flag):
    Main_Menu = auto()
    ShowYellowDress = auto()
    ShowRedDress = auto()
    ShowBlueDress = auto()
    ShowGreenDress = auto()
    Game = auto()
    About = auto()
    Game_Over = auto()


class PlayerState(Flag):
    Idel = auto()
    Run1 = auto()
    Run2 = auto()
    Run3 = auto()


class PlayerLooksTowards(Flag):
    Right = auto()
    Left = auto()

