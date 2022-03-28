#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

import sys 
import time
import collections
import copy
ROW = "ABCDEFGHI"
COL = "123456789"
#num=0
boxOne = {"A1","A2","A3","B1","B2","B3","C1","C2","C3"}
boxTwo = {"A4","A5","A6","B4","B5","B6","C4","C5","C6"}
boxThree = {"A7","A8","A9","B7","B8","B9","C7","C8","C9"}
boxFour = {"D1","D2","D3","E1","E2","E3","F1","F2","F3"}
boxFive = {"D4","D5","D6","E4","E5","E6","F4","F5","F6"}
boxSix = {"D7","D8","D9","E7","E8","E9","F7","F8","F9"}
boxSeven = {"G1","G2","G3","H1","H2","H3","I1","I2","I3"}
boxEight = {"G4","G5","G6","H4","H5","H6","I4","I5","I6"}
boxNine = {"G7","G8","G9","H7","H8","H9","I7","I8","I9"}
boxes = [boxOne,boxTwo,boxThree,boxFour,boxFive,boxSix,boxSeven,boxEight,boxNine]
arcs = collections.deque()


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    arcs.clear()
    for r in ROW:
        for c in COL:
            a = r+c
            neighbors = N(a)
            for varias in neighbors:
                   arcs.append((r+c,varias))
    
    for i in ROW: 
        for j in COL:
            if board[i+j] == 0:
                board[i+j] = {1,2,3,4,5,6,7,8,9}
            else: 
                a = set()
                x = board[i+j]
                a.add(x)
                board[i+j] = a         
    solved_board = backtrack(board)
    return solved_board

def backtrack(board): 
    if all(len(value)==1 for value in board.values()):  
        for k, v in board.items():
            num = v.pop()
            board[k]=num 
        return board
    else: 
        var = select(board)
        for items in board[var]: 
            a = set()
            a.add(items)
            if checkConsistency(board,var,a):
                origboard = copy.deepcopy(board)
                board[var] = a
                if makeAC(board,var):
                    result = backtrack(board)
                    if result != None:
                        return result
                board = origboard
        return None
    
def select(board): 
    minin = None
    m = 10
    for k, v in board.items():
        if len(v)!=1 and len(v)<m:
            #print(v)
            minin = k 
            m = len(v)
    return minin
       
    
def makeAC(board,var):
    arc = arcs.copy()
    while arc:
        a = arc.popleft()
        if revise(board, a[0], a[1]):
            if len(board[a[0]])==0:
                return False
            neb = N(a[0])-set(a[1])
            for n in neb:
                arc.append((a[0],n))
    return True
                
def revise(board, var1, var2):
    revised = False
    if len(board[var2])==1:
       #print((var1,var2))
        start = len(board[var1])
        board[var1] = board[var1]-board[var2]
        end = len(board[var1])
        #print("start: " + str(start) +"   " + "End: " + str(end))
        if start != end:
            revised = True
    return revised
        
    
    
            
def N(var):
    neighbors = set()
    row = var[0]
    col = var[1]
    for j in COL:
        neighbors.add(row+j)
    for i in ROW:
        neighbors.add(i+col)
    for its in boxes:
        if var in its:
            for sq in its:
                neighbors.add(sq)
            break
    neighbors.remove(var)
    return neighbors
    
    
    
def checkConsistency(board, var, item):
    if checkBox(board, var, item) and checkRow(board, var, item) and checkcolumn(board, var, item):
        return True
    else:
        return False

def checkBox(board, var, item): 
    for its in boxes:
        if var in its:
            for sq in its:
                if board[sq]==item:
                    return False 
    return True
    
    
def checkRow(board, var, item):
    row = var[0]
    for j in COL:
        if board[row+j] == item:
            return False
    else: 
        return True
    
    
def checkcolumn(board, var, item):
    col = var[1]
    for i in ROW: 
    #    print(i+col + " . " + item)
        if board[i+col] == item:
            return False
    else :
        return True



if __name__ == '__main__':
    #  Read boards from source.
    #src_filename = 'sudokus_start.txt'
    #try:
     #   srcfile = open(src_filename, "r")
    line = sys.argv[1]
    #except:
     #   print("Error reading the sudoku file %s" % src_filename)
     #   exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # Solve each board using backtracking
    
    line = line[:81]

        # Parse boards to dict representation, scanning board L to R, Up to Down
    board = { ROW[r] + COL[c]: int(line[9*r+c])
             for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        #print_board(board)

        # Solve with backtracking
    solved_board = backtracking(board)

        # Print solved board. TODO: Comment this out when timing runs.
        #print_board(solved_board)

        # Write board to file
    outfile.write(board_to_string(solved_board))
    outfile.write('\n')

    #print("Finishing all boards in file.")
    
    
    
    