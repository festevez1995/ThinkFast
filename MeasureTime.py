## @file MeasureTime.py
#  Brief doc for MeasureTime.py
#
#  Detailed doc for MeasureTime.py
#  Implemented a timer in it's regular time mode. 
#
#  @author Fernando Estevez
#
#  @copyright License Info
#
#  @date January 24, 2021
#
#  @package MeasureTime
#  Brief doc for  Measuring Time program section 3
#
#  Detailed doc for Measuring Time program
#
#  @author Your Fernando Estevez
#
#  @copyright License Info
#
#  @date January 24, 2021
import pyb
import utime
## This is part 3 Measuring Time 
# 10 s in us
sleepTime = 10000000

# Sets a larg number as the period
p = 0x7FFFFFFF

# Nucleo's clock freq divided by 2
NucleoClock = 80000000

# The freq the clock will count at - 1 MHZ
TimerClock = 1000000

#1Mhz clock = (80MHz/2/(prescale + 1))
pscale = int((NucleoClock / TimerClock) - 1)

# Sets up timer 2 object
timer2 = pyb.Timer(2, prescaler=pscale, period=p)
# Set the timer to start at zero
timer2.counter(0)

while true:
	# Read timers value before going to sleep
	print(timer2.counter())
	# Sleep for 10 seconds
	utime.sleep_us(sleepTime)
	# Read timer value after done sleeping 
	print(timer2.counter())
