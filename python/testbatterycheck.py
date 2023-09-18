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
            print("LEDSegDisplay.append LED ", i)
            i -= 1
        
        percentageOfBattery = 0
        batteryVoltage = voltagePerDegree * batteryLowVoltage.read_u16()
        print("Battery Voltage: ", batteryVoltage)
        percentageOfBattery = batteryVoltage/batterySmallVolt * 100
        print("Percentage: ", percentageOfBattery)
        LEDdisplay = int(percentageOfBattery*LEDMeterRange)
        print("LED Display: ", LEDdisplay)

        #Calculate 9v reading when 1.5v pin is not being used
        if LEDdisplay < 1:
            batteryVoltage = voltagePerDegree * batteryHighVoltage.read_u16()
            print("Battery Voltage: ", batteryVoltage)
            percentageOfBattery = batteryVoltage/batteryHighVolt * 100
            print("Percentage: ", percentageOfBattery)
            LEDdisplay = int(percentageOfBattery*LEDMeterRange)
            print("LED Display: ", LEDdisplay)

        i = 0
        while i < len(LEDSegDisplay):
            LEDSegDisplay[i].high()
            print("while LED ", i, " on")
            time.sleep(1)
            i += 1
        for i in LEDSegDisplay:
            i.low()
            print("for LED ", i, " off")
            time.sleep(1)

    except KeyboardInterrupt:
        print("stopping program")
    
    finally:
        print("Graceful exit")
        for i in range(0,len(LEDSegDisplay)):
            LEDSegDisplay[i].low()

if __name__ == '__main__':
    main()