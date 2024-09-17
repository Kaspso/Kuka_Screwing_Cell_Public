## Set Static IP
1. Set static IP (IPv4) for ethernet adapter on personal PC as shown
<img src="Images\Change_IP_Configs.jpg" width="640">

## How To Run the Cell
1. Insert ethernet cable into personal PC

2. Connect air and power to the cell
<img src="Images\Air_Connection.jpg" width="320">
<img src="Images\Power_Plugged_In.jpg" width="320">

3. Power on the PLC and motor driver
<img src="Images\PLC_Power_ON.jpg" width="320">

4. Power on KUKA controller
<img src="Images\KUKA_ON.jpg" width="320">

5. Open "Software PLC" on cell PC and click "Run"
<img src="Images\Software_PLC_Program.jpg" width="320">
<img src="Images\Run_Soft_PLC.jpg" width="320">

6. Deactivate all emergency buttons and close the door

7. Push blue button to activate the cell
<img src="Images\Activate_Cell.jpg" width="320">

8. Under "Applications" on KUKA interface, click on the program "RobotApplication"
<img src="Images\KUKA_Applications_Overview.jpg" width="320">

9. Click the play icon
<img src="Images\Start_KUKA_Program.jpg" width="320">

10. Open this repository on personal PC, run "main_program.py" and wait for GUI to open.

11. If "Robot Data Status" is red see the section "Fix Robot Communication" before continuing

12. Enter "Screwing Program" to ID of srewing process (1=normal, 2=...)

13. Enter process type (A=Normal, B=...) and tree number

14. Enter number of screwing processes to run i.e. number of screws before pausing

15. If the wood is not new, change "Absolute Screwing Number" to number of screws already screwed in the wood

16. Click "fixture on"

17. Click "Get Ready"

18. Click "Start Screwing"

19. Repeat step 12-18 until desired number of tests has been performed


## How To Close the Cell (order is important!)
1. Close python GUI

2. In "Software PLC" program click "Stop" and "Terminate" (click "OK" to warning)

3. Close all programs and shutdown the cell PC

4. Turn off power to KUKA controller
<img src="Images\KUKA_OFF.jpg" width="320">

5. Turn off power to PLC and motor driver
<img src="Images\PLC_Power_Off.jpg" width="320">

6. When KUKA interface has turned black the power to the cell can be disconnected
<img src="Images\Power_Not_Plugged_In.jpg" width="320">


## Fix Robot Communication
1. Close python GUI

2. Restart "BackgroundTaskUDP" under "Applications" on KUKA interface
<img src="Images\Stop_KUKA_BG_Application.jpg" width="320">
<img src="Images\Start_KUKA_BG_Program.jpg" width="320">

3. Run "main_program.py" again

4. Check that "Robot Data Status" is now green





