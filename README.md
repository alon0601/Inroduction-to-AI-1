# Inroduction-to-AI-1
הוראות הפעלה:
The input test should be in the following format:
#X 5                ; Maximum x coordinate
#Y 4                ; Maximum y coordinate
#P 4 0 0  D 0 3 50  ; Package at (4,0) from time 0, deliver to (0,3) on or before time 50
#P 0 3 5  D 4 0 50  ; Package at (0,3) from time 5, deliver to (4,0) on or before time 50
#B 3 0 4 0          ; Edge from (3,0) to (4,0) is always blocked
#B 2 2 2 3          ; Edge from (2,2) to (2,3) is always blocked
#F 0 0 0 1          ; Edge from (0,0) to (0,1) is fragile (can only be traversed once)
#S 0 0              ; Gridi a_i agent with start point of (0, 0)
#R 4 3              ; A_star regular agent with start point of (4,3)
#D 0 0				; RTA agent with start point of (0,0)

important notes: 
	* R = A_STAR Regular agent
	* S = Gridi a_i agent
	* D = RTA agent

Before running the code you should install networkx package to your computer using : pip install networkx command in your cmd.

To run the project please run python main.py
You need to add test file to the code folder and then enter the file name (the program will ask you to dont worry)