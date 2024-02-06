# Inroduction-to-AI-1
הוראות הפעלה:
The input test should be in the following format:

#X 5                
#Y 4                
#P 4 0 0  D 0 3 50  
#P 0 3 5  D 4 0 50  
#B 3 0 4 0          
#B 2 2 2 3          
#F 0 0 0 1          
#S 0 0              
#R 4 3              
#D 0 0				

important notes: 
	* R = A_STAR Regular agent
	* S = Gridi a_i agent
	* D = RTA agent

if you want to modify the limit for the RTA and the regular A_star agents please write the new limition after is location for example

#R 4 3 20000


Before running the code you should install networkx package to your computer using : pip install networkx command in your cmd.

To run the project please run python main.py
You need to add test file to the code folder and then enter the file name (the program will ask you to dont worry)