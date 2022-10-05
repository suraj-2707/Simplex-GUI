import sys
from tkinter import *
from tkinter import Entry, Label, Tk, Button, Frame
from tkinter.scrolledtext import ScrolledText
import numpy as np  
from fractions import Fraction



class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class MainGUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        #self.root = Frame(self)
        #self.root.pack()
        self.redirect_button = Button(self, text="Redirect console to widget", command=self.redirect_logging)
        self.redirect_button.grid(row=7, column=5)
        #self.redirect_button = Button(self.root, text="Redirect console reset", command=self.reset_logging)
        #self.redirect_button.pack()
        self.test_button = Button(self, text="Test Print", command=self.test_print)
        self.test_button.grid(row=6, column=5)
        self.log_widget = ScrolledText(self, height=200, width=120, font=("consolas", "8", "normal"))
        self.log_widget.grid(row=8, column=0)
        


    def reset_logging(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_print(self):
        z1=z1value.get()
        z2=6
        x1=x1value.get()
        y1=y1value.get()
        c1=c1value.get()
        x2=x2value.get()
        y2=y2value.get()
        c2=c2value.get()
        print("\n                 ****SiMplex Algorithm ****\n\n") 

  


        # A will contain the coefficients of the constraints 


        A = np.array([[x1, y1, 0, 1], [x2, y2, 1, 0]]) 
        # b will contain the amount of resources  

        b = np.array([c1, c2])            
        # c will contain coefficients of objective function Z       

        c = np.array([z1, z2, 0, 0])              


        # B will contain the basic variables that make identity matrix 

        cb = np.array(c[3]) 

        B = np.array([[3], [2]])           

         # cb contains their corresponding coefficients in Z    

        cb = np.vstack((cb, c[2]))         

        xb = np.transpose([b])                  
        # combine matrices B and cb 

        table = np.hstack((B, cb))              

        table = np.hstack((table, xb))          
        # combine matrices B, cb and xb 
        # finally combine matrix A to form the complete simplex table 

        table = np.hstack((table, A))          
        # change the type of table to float 

        table = np.array(table, dtype ='float')  
        # inputs end 


        # if min problem, make this var 1 

        MIN = 0



        print("Table at itr = 0") 

        print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4") 

        for row in table: 
        
            for el in row: 
            
                        # limit the denominator under 100 

                print(Fraction(str(el)).limit_denominator(100), end ='\t')  

            print() 

        print() 

        print("Simplex Working....") 


        # when optimality reached it will be made 1 

        reached = 0     

        itr = 1

        unbounded = 0

        alternate = 0



        while reached == 0: 
        
        
        
            print("Iteration: ", end =' ') 

            print(itr) 

            print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4") 

            for row in table: 
            
                for el in row: 
                
                    print(Fraction(str(el)).limit_denominator(100), end ='\t') 

                print() 



            # calculate Relative profits-> cj - zj for non-basics 

            i = 0

            rel_prof = [] 

            while i<len(A[0]): 
            
                rel_prof.append(c[i] - np.sum(table[:, 1]*table[:, 3 + i])) 

                i = i + 1



            print("rel profit: ", end =" ") 

            for profit in rel_prof: 
            
                print(Fraction(str(profit)).limit_denominator(100), end =", ") 

            print() 

            i = 0



            b_var = table[:, 0] 

            # checking for alternate solution 

            while i<len(A[0]): 
            
                j = 0

                present = 0

                while j<len(b_var): 
                
                    if int(b_var[j]) == i: 
                    
                        present = 1

                        break; 

                    j+= 1

                if present == 0: 
                
                    if rel_prof[i] == 0: 
                    
                        alternate = 1

                        print("Case of Alternate found") 

                        # print(i, end =" ") 

                i+= 1

            print() 

            flag = 0

            for profit in rel_prof: 
            
                if profit>0: 
                
                    flag = 1

                    break
                
                # if all relative profits <= 0 

            if flag == 0: 
            
                print("All profits are <= 0, optimality reached") 

                reached = 1

                break
            
            
            
            # kth var will enter the basis 

            k = rel_prof.index(max(rel_prof)) 

            min = 99999

            i = 0; 

            r = -1

            # min ratio test (only positive values) 

            while i<len(table): 
            
                if (table[:, 2][i]>0 and table[:, 3 + k][i]>0):  
                
                    val = table[:, 2][i]/table[:, 3 + k][i] 

                    if val<min: 
                    
                        min = val 

                        r = i     # leaving variable 

                i+= 1



                # if no min ratio test was performed 

            if r ==-1: 
            
                unbounded = 1

                print("Case of Unbounded") 

                break
            
            
            
            print("pivot element index:", end =' ') 

            print(np.array([r, 3 + k])) 



            pivot = table[r][3 + k] 

            print("pivot element: ", end =" ") 

            print(Fraction(pivot).limit_denominator(100)) 



                # perform row operations 

            # divide the pivot row with the pivot element 

            table[r, 2:len(table[0])] = table[ 
            
                    r, 2:len(table[0])] / pivot 



            # do row operation on other rows 

            i = 0

            while i<len(table): 
            
                if i != r: 
                
                    table[i, 2:len(table[0])] = table[i, 2:len(table[0])] - table[i][3 + k] * table[r, 2:len(table[0])]





                i += 1





            # assign the new basic variable 

            table[r][0] = k 

            table[r][1] = c[k] 



            print() 

            print() 

            itr+= 1





        print() 



        print("***************************************************************") 

        if unbounded == 1: 
        
            print("UNBOUNDED LPP") 

            exit() 

        if alternate == 1: 
        
            print("ALTERNATE Solution") 



        print("optimal table:") 

        print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4") 

        for row in table: 
        
            for el in row: 
            
                print(Fraction(str(el)).limit_denominator(100), end ='\t') 

            print() 

        print() 

        print("value of Z at optimality: ", end =" ") 



        basis = [] 

        i = 0

        sum = 0

        while i<len(table): 
        
            sum += c[int(table[i][0])]*table[i][2] 

            temp = "x"+str(int(table[i][0])+1) 

            basis.append(temp) 

            i+= 1
        # if MIN problem make z negative 

        if MIN == 1: 
        
            print(-Fraction(str(sum)).limit_denominator(100)) 

        else: 
        
            print(Fraction(str(sum)).limit_denominator(100)) 

        print("Final Basis: ", end =" ") 

        print(basis) 



        print("Simplex Finished...")



        print() 


    def redirect_logging(self):
        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger


if __name__ == "__main__":
    app = MainGUI()
    Label(app, text="Simplex Method").grid(row=0, column=5)
    Label(app, text="Max").grid(row=1,column=0)
    z11 = Label(app, text="x =" )
    z21 = Label(app, text="y =" )
    Label(app, text="Subject to").grid(row=3,column=0)
    x11 = Label(app, text="x1 =" )
    y11 = Label(app, text="+ y1 =" )
    c11 = Label(app, text="<=  c1=" )
    x21 = Label(app, text="x2 =" )
    y21 = Label(app, text="+ y2 =" )
    c21 = Label(app, text="<=  c2 =" )
    
    z11.grid(row=1,column=2)
    z21.grid(row=1,column=4)
    x11.grid(row=3,column=2)
    y11.grid(row=3,column=4)
    c11.grid(row=3,column=6)
    x21.grid(row=4,column=2)
    y21.grid(row=4,column=4)
    c21.grid(row=4,column=6)
    
    z1value = IntVar()
    z2value = IntVar()
    x1value = IntVar()
    y1value = IntVar()
    c1value = IntVar()
    x2value = IntVar()
    y2value = IntVar()
    c2value = IntVar()
    
    z1entry = Entry(app,textvariable=z1value)
    z2entry = Entry(app,textvariable=z2value)
    x1entry = Entry(app,textvariable=x1value)
    y1entry = Entry(app,textvariable=y1value)
    c1entry = Entry(app,textvariable=c1value)
    x2entry = Entry(app,textvariable=x2value)
    y2entry = Entry(app,textvariable=y2value)
    c2entry = Entry(app,textvariable=c2value)
    
    z1entry.grid(row=1, column=3)
    z2entry.grid(row=1, column=5)
    x1entry.grid(row=3, column=3)
    y1entry.grid(row=3, column=5)
    c1entry.grid(row=3, column=7)
    x2entry.grid(row=4, column=3)
    y2entry.grid(row=4, column=5)
    z2entry.grid(row=4, column=7)
    #test_button = Button(app, text="Test Print", command=self.test_print)
    #test_button.grid(row=6, column=5)
    app.mainloop()