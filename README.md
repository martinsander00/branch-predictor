# branch-predictor
This is a branch predictor project which uses 4 types of algorithms: Bimodal, G-Shared, P-shared and Tournament.

To run each specific algorithm, you will need to input this cmds in your terminal:

-s stands for the amount of PC bits used for indexing
-bp stands for and int number between 0 and 3 denoting the predictor you want to utilize
-gh stands for the global history size
-lh stands for the local history size

### **Bimodal**: 
python branch_predictor.py --bp 0 -s 8

### **P-Shared**: 
python branch_predictor.py --bp 2 -s 8 --lh 12

### **G-Shared**: 
python branch_predictor.py --bp 1 -s 12 --gh 6

### **Torneo**: 
python branch_predictor.py --bp 3 -s 


Note: The file that you want to process has to have the following syntax (T stands for "taken" and N for "not taken"). 
The first number stands for the PC direction of the instruction that will take (or not) the branch.

3086629576 T<br/>
3086629604 T<br/>
3086629599 N<br/>
3086629604 T<br/>
