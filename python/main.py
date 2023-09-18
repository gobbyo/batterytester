from machine import Pin, ADC
import time

ADCLowVoltPin = 26 #GP26
ADCMaxVoltPin = 27 #GP27
PicoVoltage = 3.3
ADC16BitRange = 65536
LEDMeterRange = 10
batterySmallVolt = 1.5 #1.5v
batteryHighVolt = 3.0 #9v

def main():

    LEDSegDisplay = []

    try:
        batteryLowVoltage = ADC(ADCLowVoltPin)
        batteryHighVoltage = ADC(ADCMaxVoltPin)
        voltagePerDegree =  PicoVoltage / ADC16BitRange

        i = LEDMeterRange
        while i > 0:
            LEDSegDisplay.append(Pin(i, Pin.OUT))
            i -= 1

        holdvalue = -1

        while True:
            percentageOfBattery = 0
            batteryVoltage = voltagePerDegree * batteryLowVoltage.read_u16()
            percentageOfBattery = batteryVoltage/batterySmallVolt
            LEDdisplay = int(percentageOfBattery*LEDMeterRange)
            #print("percentageOfBattery: ", percentageOfBattery, " LEDdisplay: ", LEDdisplay)
            #Calculate 9v reading when 1.5v pin is not being used
            if LEDdisplay < 1:
                batteryVoltage = voltagePerDegree * batteryHighVoltage.read_u16()
                percentageOfBattery = batteryVoltage/batteryHighVolt
                LEDdisplay = int(percentageOfBattery*LEDMeterRange)

            if LEDdisplay > LEDMeterRange:
                LEDdisplay = LEDMeterRange

            for i in range(0,LEDMeterRange):
                time.sleep(0.07)
                if i < LEDdisplay:
                    LEDSegDisplay[i].high()
                    if holdvalue < i:
                        holdvalue = i
                    #print("LED ", i, " on")
                else:
                    LEDSegDisplay[i].low()
                    #print("for LED ", i, " off")

            if LEDdisplay > 0:
                time.sleep(.5)
                break
    except KeyboardInterrupt:
        print("stopping program")
    
    finally:
        print("Graceful exit")
        i = len(LEDSegDisplay)-1
        while i >= 0:
            if i != holdvalue:
                LEDSegDisplay[i].low()
            i -= 1
            time.sleep(0.07)
        
        time.sleep(1)
        LEDSegDisplay[holdvalue].low()

if __name__ == '__main__':
    main()