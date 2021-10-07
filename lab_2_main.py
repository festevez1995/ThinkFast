## @file lab_2_main.py
#  Brief doc for lab_2_main.py
#
#  Detailed doc for lab_2_main.py
#  The main program for Lab 2.Program will test a user's reaction time.
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date January 24, 2021
import pyb
import utime
import random
import micropython
import Constants as con

# Emergency buffer to store errors in ISR.
micropython.alloc_emergency_exception_buf(200)
## Initiates Timer 2 object set to NULL.
timer2 = None
## Variable used to keep track of the time elapsed
#  since the LED was turned on.
LEDTimeOn = 0
## Holds the average reaction time.
averageReactTime = 0
## Holds the number of times the interupt button was pressed.
buttonCnt = 0
## LED pin object. Attached to PA5.
myLEDPin = pyb.Pin(pyb.Pin.cpu.A5, mode=pyb.Pin.OUT_PP)
## Interupt pin object. Attached to C13.
pinC13 = pyb.Pin(pyb.Pin.cpu.C13)
	
## Randomly choose a number between 2 and 3.
#
#  Chooses a number between 2 and 3 with .1 step increment.
#  @return rand_sec Random number in miliseconds
def getRandomSec():
	rand_sec = random.randrange(con.START, con.END)
	return int(rand_sec * con.MILISEC)
	
## Function that sets up timer 2
#
# Sets up timer2 with pscale of 79 and period=0x7FFFFFFF
#
def setTimer():
    global timer2
    # Sets a larg number as the period
    p = con.BIG
	# Nucleo's clock freq
    NucleoClock = con.NUCLEO_FRQ 
	# The freq the clock will count at - 1 MHZ
    TimerClock = con.CLK_FRQ
	#1Mhz clock = (80MHz/2/(prescale + 1))
    pscale = int((NucleoClock / TimerClock) - 1)
	# Sets up timer 2 object
    timer2 = pyb.Timer(con.TIMER2, prescaler=pscale, period=p)

## External Interupt Callback Function
#
#  On button pressed, the function will find the difference from
#  the time the button was pressed - the time the LED was turned on
#  and store it into a varuable called averageReactTime. Lastly,
#  it will keep track the number of times the button was pressed.
#  @param line The line at which the interupt occured
def onButtonPress(line):
    global averageReactTime, buttonCnt
    averageReactTime += (timer2.counter() - LEDTimeOn)
    buttonCnt += 1

## Begin Raction Function
#
#  Function that sets up interupt and starts the timer 2 object.
#
def beginReaction():
    binterupt = pyb.ExtInt(pinC13, mode=pyb.ExtInt.IRQ_FALLING, pull=pyb.Pin.PULL_NONE, callback=onButtonPress)
    setTimer()	
	
if __name__ == "__main__":

    beginReaction()
    while True:
        try:
		    # Get a random delay from 2 - 3 sec 
            delayMs = getRandomSec()
			# Sleep the system based on the random delay 
            utime.sleep_ms(delayMs)
			# Turn on the LED 
            myLEDPin.high()
			# Record the start time of the LED 
            LEDTimeOn = timer2.counter()
			# Leave the LED on for 1 Second
            utime.sleep_ms(con.MILISEC)
			# Turn the LED off and repeat
            myLEDPin.low()
		# Check if CTR+C was triggered to termianted the program 
        except KeyboardInterrupt:
		    # Display the Average Button Press 
            # If no presses were made display message			
            if buttonCnt == 0:
                print("The button was not pressed")
            else:				
                print("Average Button Press: {}\n".format(averageReactTime/buttonCnt))
                break