from xboxdrv_parser import Controller
from time import sleep
import serial

# add ZMQ server to control
import zmq


def main ():
    # Get input from the two analog sticks as yaw, throttle, roll, and pitch. Take the (0 - 255) input value and
    # map it to a (-1 - 1) range.
    controller = Controller (["X1", "Y1", "X2", "Y2"], ["yaw", "throttle", "roll", "pitch"], (0, 255), (-1, 1))
    #ser = serial.Serial ('/./dev/ttyACM0', 9600, timeout=1)
    # Set the context of the server
    context = zmq.Context()
    # Set the socket to PUBlish
    socket = context.socket(zmq.PUB)
    # Bind the socket to 5556
    socket.bind("tcp://*:5556")
    while True:
        control_packet = controller.get_values ()

        print (control_packet)
	
	
        inp = 0
        if (control_packet["yaw"] <= 1 and control_packet["yaw"] >= 0.05):
            inp *= 255
            inp += 255
           # ser.write (inp)
            print ("d")
            socket.send("%i"% inp)
        elif (control_packet["yaw"] >= -1 and control_packet["yaw"] <= -0.05):
            inp *= 255
            inp -= 255
            #ser.write (inp)
            print ("a")
            socket.send("%i"% inp)
        elif (control_packet["throttle"] >= -1 and control_packet["throttle"] <= -0.08):
            inp *= 255
	    #make the value intuitive
            inp = math.fabs(inp)
           # ser.write (inp)
            print ("w")
            socket.send("%i"% inp)
        elif (control_packet["throttle"] <= 1 and control_packet["throttle"] >= 0.08):
            inp *= 255
	    #make the value intuitive
            inp = -inp
          #  ser.write (inp)
            print ("s")
            socket.send("%i"% inp)

        # Update at 20 messages a second
        sleep (.05)

if __name__ == '__main__':
    main()
