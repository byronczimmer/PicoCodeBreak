import picounicorn as puni  # https://shop.pimoroni.com/products/pico-unicorn-pack?variant=32369501306963
import utime
import random
import neotimer             # https://github.com/jrullan/micropython_neotimer
from machine import Pin
puni.init()

FREQ      = 500
# Change the number of colors ( from colordict ) to alter the dificulty.
# Choose the ones you feel work best.  Magenta, Orange and Purple are the least likely to look 'good'
# The order of the colors in ROYGBIV determines the cycle they will go through while playing.
# 5 is very easy
# 6 is 'standard'
# 7 is a challenge
ROYGBIV   = [ "RED", "MAGENTA", "ORANGE", "YELLOW", "GREEN", "TEAL", "BLUE" ]
ROYGBIVX  = [ "RED", "ORANGE", "YELLOW", "GREEN", "TEAL", "BLUE", "PURPLE" ]
ROYGBIVBW = [ "BLACK", "RED", "ORANGE", "YELLOW", "GREEN", "TEAL", "BLUE", "PURPLE", "WHITE" ]
colordict = { "RED":     (187,0,0),
              "MAGENTA": (194, 68, 102),
              "ORANGE":  (187, 68, 0),
              "YELLOW":  (170, 102, 0),
              "GREEN":   (0, 153, 0),
              "TEAL":    (0, 119, 119),
              "BLUE":    (0, 0, 153),
              "PURPLE":  (153, 0, 153),
              "WHITE":   (119, 119, 119),
              "BLACK":   (0, 0, 0) }
ntimer = neotimer.Neotimer(FREQ)

class PicoCodeBreak:
    def __init__(self):
        self.init()
        
    def init(self):
        puni.clear()
        self.guess_num = 0  # Start at zero
        self.answer = [ random.choice(ROYGBIV), random.choice(ROYGBIV), random.choice(ROYGBIV), random.choice(ROYGBIV) ]
        self.guess = [ROYGBIV[0]]*4
        self.pos_state = True
        self.pos = (0, 0)
        self.do_eval = False
        self.playing = True
        self.failed = False
        self.won = False
        self.adv_turn = False
        self.show_guess()
        
    def show_guess(self):
        for idx in range(4):
            self.pos = (self.guess_num*2, idx)
            self.blink_pos_to( self.guess[idx] )
        self.pos = (self.guess_num*2, 0)
        
    def guess_pick(self, pin):
        print("in guess_pick")
        x, y = self.pos
        idx = ROYGBIV.index(self.guess[ y ])
        idx += 1
        if idx >= len(ROYGBIV):
            idx = 0
        self.guess[y] = ROYGBIV[idx]
        
    def prep_eval(self, pin):
        self.do_eval = True
        
    def pos_pick(self, pin):
        print("in pos_pick")
        x, y = self.pos
        self.blink_pos_to( self.guess[ y ] )
        y += 1
        if y >= 4:
            y = 0
        self.pos = (x, y)
        
    def eval_guess(self):
        print("in eval_guess")
        # Make sure guess is solid
        self.show_guess()        
        matched = 0
        near = 0
        temp_guess = self.guess.copy()
        temp_answer = self.answer.copy()
        for idx in range(4):
            if self.guess[idx] == self.answer[idx]:
                matched += 1
                temp_guess[idx] = "USED"
                temp_answer[idx] = "FOUND"
        for idx in range(4):
            peg = temp_guess[idx]
            if peg in temp_answer:
                near += 1
                temp_answer.remove(peg)
        
        self.display_resp(matched, near, 4-matched-near)
        self.adv_turn = True
        
    def advance_turn(self):
        print("in advance_turn", self.guess_num)
        self.guess_num += 1
        if self.guess_num +1 > puni.get_width()/2:
            self.failed = True
            utime.sleep_ms(1500)
            return
        self.pos = (self.guess_num*2, 0)
        x, y = self.pos
        if x >= puni.get_width():
            self.failed = True
            utime.sleep_ms(1500)
            return
        self.show_guess()
        self.do_eval = False
        self.adv_turn = False
        utime.sleep_ms(500)
        
    def blink_pos_to(self, color):
        self.pos_state = not self.pos_state
        x, y = self.pos
        r, g, b = colordict[ color ]
        puni.set_pixel( x, y, r, g, b )

    def blink_pos(self):
        x, y = self.pos
        if self.pos_state:
            self.blink_pos_to( "BLACK" )
        else:
            self.blink_pos_to( self.guess[y] )

    def color_array(self, grn, ylw, red ):
        return ( (colordict["GREEN"]*grn + colordict["YELLOW"]*ylw + colordict["RED"]*red) )

    def display_resp(self, grn, ylw, red ):
        # Make sure guess is solid
        self.show_guess()  
        x,y = self.ulc()
        wr, wg, wb = colordict["WHITE"]
        rgb = self.color_array(grn, ylw, red)
        puni.set_pixel( x+1, y-1, wr, wg, wb)
        puni.set_pixel( x+1, y  , rgb[0], rgb[ 1], rgb[ 2]  )
        puni.set_pixel( x+1, y+1, rgb[3], rgb[ 4], rgb[ 5]  )
        puni.set_pixel( x  , y  , rgb[6], rgb[ 7], rgb[ 8]  )
        puni.set_pixel( x  , y+1, rgb[9], rgb[10], rgb[11]  )
        if self.guess_num >= puni.get_width()/2 - 1:
            self.failed = True
        if grn == 4:
            self.failed = False
            self.won = True

            
    def winner(self):
        utime.sleep_ms(1000)
        for color in ROYGBIV:
            self.flood(color)
            utime.sleep_ms(333)
        self.playing = False
    
    def loser(self):
        utime.sleep_ms(500)
        for fail_rep in range (3):
            self.flood( "RED" )
            utime.sleep_ms( 500 )
            self.flood( "BLACK" )
            utime.sleep_ms( 500 )
        self.playing = False        
        
    def flood(self, color):
        r,g,b = colordict[color]
        for x in range(16):
            for y in range (7):
                puni.set_pixel( x, y, r, g, b )
                
    def init_irq(self):
        print ("in init_irq")
        pinA = Pin(puni.BUTTON_A + 12, Pin.IN, Pin.PULL_UP)
        pinA.irq(lambda pin: self.guess_pick(pin), Pin.IRQ_FALLING)
        
        pinB = Pin(puni.BUTTON_B + 12, Pin.IN, Pin.PULL_UP)
        pinB.irq(lambda pin: self.pos_pick(pin), Pin.IRQ_FALLING)
        
        pinY = Pin(puni.BUTTON_Y + 12, Pin.IN, Pin.PULL_UP)
        pinY.irq(lambda pin: self.prep_eval(pin), Pin.IRQ_FALLING)

    def ulc(self):
        return ((self.guess_num*2), 5)
    
    def play(self):
        self.init()
        self.init_irq()
        while self.playing:
            if (ntimer.repeat_execution()):
                self.blink_pos()
            if self.adv_turn:
                self.show_guess()
                self.advance_turn()
            if self.do_eval:
                self.eval_guess()
            if self.failed:
                self.loser()
            if self.won:
                self.winner()
        print("END")
        puni.clear()

if __name__ == "__main__":
    game = PicoCodeBreak()
    while True:
        game.play()
