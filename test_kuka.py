from cmd_robot import CmdRobot
from cmd_plc import CmdPlc

robot = CmdRobot()
plc = CmdPlc()
row = 0
pin = 0

robot.homing()
robot.getRobotReady()
for i in range(4):
    for j in range(4):
        robot.moveToPinHole(j,i)
        plc.setStartSignal()
        plc.waitForProcess()
# here wait input from plc
        robot.modeUpFromPinHole()
robot.homing()
robot.closeConnection()