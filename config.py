import pygame as pg
from numpy import array

class Config:
    def __init__(self):
        # Key maps to convert the key option in blocks to pygame constants
        KEY=array(['up arrow', 'down arrow', 'left arrow', 'right arrow', 'space', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'enter', '<', '>', '+', '-', '=', '.', ',', '%', '$', '#', '@', '!', '^', '&', '*', '(', ')', '[', ']', '?', '\\', '/', "'", '"', '`', 'backspace', 'escape', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'])
        BIND=array([pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT,pg.K_SPACE,pg.K_a,pg.K_b,pg.K_c,pg.K_d,pg.K_e,pg.K_f,pg.K_g,pg.K_h,pg.K_i,pg.K_j,pg.K_k,pg.K_l,pg.K_m,pg.K_n,pg.K_o,pg.K_p,pg.K_q,pg.K_r,pg.K_s,pg.K_t,pg.K_u,pg.K_v,pg.K_w,pg.K_x,pg.K_y,pg.K_z,pg.K_0,pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9,])
        KEY_MAPPING = {
           
            # Scratch supports these keys internally
            "enter": pg.K_RETURN,
            "<": pg.K_LESS,
            ">": pg.K_GREATER,
            "+": pg.K_PLUS,
            "-": pg.K_MINUS,
            "=": pg.K_EQUALS,
            ".": pg.K_PERIOD,
            ",": pg.K_COMMA,
            "%": pg.K_PERCENT,
            "$": pg.K_DOLLAR,
            "#": pg.K_HASH,
            "@": pg.K_AT,
            "!": pg.K_EXCLAIM,
            "^": pg.K_CARET,
            "&": pg.K_AMPERSAND,
            "*": pg.K_ASTERISK,
            "(": pg.K_LEFTPAREN,
            ")": pg.K_RIGHTPAREN,
            "[": pg.K_LEFTBRACKET,
            "]": pg.K_RIGHTBRACKET,
            "?": pg.K_QUESTION,
            "\\": pg.K_BACKSLASH,
            "/": pg.K_SLASH,
            "'": pg.K_QUOTE,
            "\"": pg.K_QUOTEDBL,
            "`": pg.K_BACKQUOTE,

            "backspace": pg.K_BACKSPACE,
            "escape": pg.K_ESCAPE,
            "f1": pg.K_F1,
            "f2": pg.K_F2,
            "f3": pg.K_F3,
            "f4": pg.K_F4,
            "f5": pg.K_F5,
            "f6": pg.K_F6,
            "f7": pg.K_F7,
            "f8": pg.K_F8,
            "f9": pg.K_F9,
            "f10": pg.K_F10,
            "f11": pg.K_F11,
            "f12": pg.K_F12,
        }
        print(KEY_MAPPING.keys(),'\n',KEY_MAPPING.values())
    def get_mapping(self,key):
        return self.KEY_MAPPING.get(key,None)
    
Config()