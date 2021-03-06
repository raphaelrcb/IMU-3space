# --------------------------------------------------------
# Código em Python p/ controle e protese
# YOST LABS 3-SPACE SENSOR WIRELESS IMU
# raphaelrcbarbosa@gmail.com
# --------------------------------------------------------

#Import imu.py code from LARA - UnB
import imu

# Import utilities
import time
import logging
import logging.config
import yaml
import matplotlib.pyplot as plt
import numpy as np
import math

#Borrow ROS msg Format
# from std_msgs.msg import Float64
# from std_msgs.msg import String
# from std_msgs.msg import UInt8
# from std_srvs.srv import Empty
# from sensor_msgs.msg import Imu


with open('imu.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    # logging.config.dictConfig(config)

def quartenion_to_euler (QX, QY, QZ, QW):
    # print("TRANSFORMA QQQQ")
        # """
        # Convert a quaternion into euler angles (roll, pitch, yaw)
        # roll is rotation around x in radians (counterclockwise)
        # pitch is rotation around y in radians (counterclockwise)
        # yaw is rotation around z in radians (counterclockwise)
        # """
    roll_x = []
    pitch_y = []
    yaw_z = []
    
    t0 = +2.0 * (QW * QX + QY * QZ)
    t1 = +1.0 - 2.0 * (QX * QX + QY * QY)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (QW * QY - QZ * QX)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (QW * QZ + QX * QY)
    t4 = +1.0 - 2.0 * (QY * QY + QZ * QZ)
    yaw_z = math.atan2(t3, t4)
     
    
    return roll_x, pitch_y, yaw_z # in radians
    

def main ():
    
    timestamp0 = time.time()
    frame_id = 'base_link'
    
    print("begin")
    yei_imu = imu.IMU(config)

    print("begin calibration")
    for name in yei_imu.imus:
        #yei_imu.calibrate(name)
        yei_imu.tare(name)

    QuaternionX = []
    QuaternionY = []
    QuaternionZ = []
    QuaternionW = []

    EulerX = []
    EulerY = []
    EulerZ = []

    AngVelocityX = []
    AngVelocityY = []
    AngVelocityZ = []

    LinearAccX = []
    LinearAccY = []
    LinearAccZ = []

    tempo = []



    
    i=0
    print("Input anything to begin")
    input()
    while (i<1000):
        #if i == 300:
        #    print("begin")
            # print("inicio tara")
            # for name in yei_imu.imus:
                # yei_imu.tare(name)
            # print("fim tara")
            # print(i)
            
        try:
            timestamp = time.time()
            frame_id = 'base_link'

            # print("aaaa\n") 
            for name in yei_imu.imus:

                # imuMsg = Imu()
                # imuMsg.header.stamp = timestamp
                # imuMsg.header.frame_id = frame_id
                battery_voltage = []
                battery_percent = []
                buttons = []
                


                if (yei_imu.streaming == True and yei_imu.broadcast == False):
                    # print("streaming mode")
                    streaming_data = yei_imu.getStreamingData(name)
                    # print("streaming_data= ")
                    # print(streaming_data)
                    idx = 0
                    # if streaming_data != 0:
                    for slot in yei_imu.streaming_slots[name]:
                        if slot == 'getTaredOrientationAsQuaternion':
                            # imuMsg.orientation.x = streaming_data[idx]
                            QuaternionX.append(streaming_data[idx])  
                            # imuMsg.orientation.y = streaming_data[idx+1]
                            QuaternionY.append(streaming_data[idx+1])  
                            # imuMsg.orientation.z = streaming_data[idx+2]
                            QuaternionZ.append(streaming_data[idx+2])  
                            # imuMsg.orientation.w = streaming_data[idx+3]
                            QuaternionW.append(streaming_data[idx+3])  
                            roll, pitch, yaw = quartenion_to_euler(QuaternionX[-1], QuaternionY[-1], QuaternionZ[-1], QuaternionW[-1])
                            EulerX.append(roll*180/math.pi)
                            EulerY.append(pitch*180/math.pi)
                            EulerZ.append(yaw*180/math.pi)
                            idx = idx+4

                        elif slot == 'getNormalizedGyroRate':
                                    # imuMsg.angular_velocity.x = streaming_data[idx]
                                    AngVelocityX.append(streaming_data[idx])
                                    # imuMsg.angular_velocity.y = streaming_data[idx+1]
                                    AngVelocityY.append(streaming_data[idx+1])
                                    # imuMsg.angular_velocity.z = streaming_data[idx+2]
                                    AngVelocityZ.append(streaming_data[idx+2])
                                    idx = idx+3

                        elif slot == 'getCorrectedAccelerometerVector':
                                    # imuMsg.linear_acceleration.x = -streaming_data[idx]
                                    LinearAccX.append(-streaming_data[idx])
                                    # imuMsg.linear_acceleration.y = -streaming_data[idx+1]
                                    LinearAccY.append(-streaming_data[idx+1])
                                    # imuMsg.linear_acceleration.z = -streaming_data[idx+2]
                                    LinearAccZ.append(-streaming_data[idx]+2)
                                    idx = idx+3

                        elif slot == 'getBatteryVoltage':
                                    battery_voltage = streaming_data[idx]
                                    idx = idx+1

                        elif slot == 'getBatteryPercentRemaining':
                            battery_percent = streaming_data[idx]
                            idx = idx+1

                        elif slot == 'getButtonState':
                            buttons = streaming_data[idx]
                            idx = idx+1

                        # print("Quaternion X: ")
                        # print(QuaternionX)
                        # print("Quaternion Y: ")
                        # print(imuMsg.orientation.y)
                        # print("Quaternion Z: ")
                        # print(imuMsg.orientation.z)
                        # print("Quaternion W: ")
                        # print(imuMsg.orientation.w)

                        # print("Angular Velocity X: ")
                        # print(imuMsg.angular_velocity.x)
                        # print("Angular Velocity Y: ")
                        # print(imuMsg.angular_velocity.y)
                        # print("Angular Velocity Z: ")
                        # print(imuMsg.angular_velocity.z)

                        # print("Linear Acceleration X: ")
                        # print(imuMsg.linear_acceleration.x)
                        # print("Linear Acceleration Y: ")
                        # print(imuMsg.linear_acceleration.y)
                        # print("Linear Acceleration Z: ")
                        # print(imuMsg.linear_acceleration.z)

                        # print("Bateria")
                        # print(battery_percent)

                    print("tempo")
                    tempo.append(timestamp-timestamp0)
                    print(timestamp-timestamp0)
                    i+=1
                    #print(EulerX[-1])
                    #print(EulerY[-1])
                    #print(EulerZ[-1])
                    print(i)

        except TypeError:
            pass 

                    # print("\n")
                    # print(timestamp)
                    # print("\n")
            # saida = input()     
    
    print ("shutting down imu")
    yei_imu.shutdown()
    print ("beggining plot")

    # quartenion_to_euler(QuaternionX, QuaternionY, QuaternionZ, QuaternionW)

    plt.figure()
    plt.plot(tempo, QuaternionX,label='Quaternion X')
    plt.plot(tempo, QuaternionY, label='Quaternion Y')    
    plt.plot(tempo, QuaternionZ, label='Quaternion Z')
    plt.plot(tempo, QuaternionW, label='Quaternion W')
    plt.legend()
    plt.grid()
    # plt.show()

    plt.figure()
    plt.plot(tempo, AngVelocityX, label='Angular Velocity X')    
    plt.plot(tempo, AngVelocityY, label='Angular Velocity Y')
    plt.plot(tempo, AngVelocityZ, label='Angular Velocity Z')
    plt.legend()
    plt.grid()
    # plt.show()

    plt.figure()
    plt.plot(tempo, LinearAccX, label='Linear Acceleration X')    
    plt.plot(tempo, LinearAccY, label='Linear Acceleration Y')
    plt.plot(tempo, LinearAccZ, label='Linear Acceleration Z')
    plt.legend()
    plt.grid()
    # plt.show()

    plt.figure()
    plt.plot(EulerX, label='Euler - roll X')    
    plt.plot(EulerY, label='Euler - pitch Y')
    plt.plot(EulerZ, label='Euler - yaw Z')
    plt.legend()
    plt.grid()
    plt.show()

    print(len(EulerX))
    print(len(tempo))


    # print(QuaternionX)
    # print(QuaternionY)
    # print(QuaternionZ)
    # print(QuaternionW)


if __name__ == '__main__': # chamada da funcao principal
    main()