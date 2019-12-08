###############################################################################################################################
                                                ##Galois Field Calculator 
###############################################################################################################################

## Importing Finite Fields from pyfinite
from pyfinite import ffield

## The follow field_calculator function takes 5 arguments: 
##     1. List of binary numbers to be worked on
##     2. The operation (as a string)
##     3. The field power m in GF(2^m)
##     4. The field generator
##     5. Whether to show the result as a polynomial or binary (boolean)

def ffield_calculator(polyList,operation,field_power_m,generator,showPoly,showHex): 
    ## If there are no values in the list of binary numbers, return an error
    if len(polyList) <= 0:
        return "Error: Please enter binary values to compute"
    ## if the field generator is 0 and greater than 100, return an error
    if generator == 0 and field_power_m>100:
        return 'generator cannot be 0'
    ## Defining the field below using the function input values
    F = ffield.FField(field_power_m,generator) ## Field generator
    ## Assigning the first value of the list of binary numbers to begin the operations
    if showHex == True:
        c = int(str(polyList[0]),16)
    elif showHex == False:
        c = int(str(polyList[0]),2)
    ## If the operation chosen is mod and there are more than two elements throw an error
    if operation == 'mod' and len(polyList)>2:
        return "Error: Please enter two elements"
    ## If the operation is inverse and there is more than one element, throw an error
    if operation == 'inverse':
        ## if there is more than one element in the inverse operation, throw an error
        if len(polyList) > 1:
            return 'Error, enter only one element for the inverse'
        ## if there is only one element, calculate the inverse
        c = F.Inverse(c)
        ## if show as polynomial is selected, show the inverse as a polynomial
        if showPoly == True:
            return F.ShowPolynomial(c)
        ## Return Hex
        elif showHex == True:
            return hex(c)
        ## format the binary number without '0b'
        return ('{0:b}'.format(c))
    ## Begin the loop for multiplication, this loop starts from the second element to the last element.
    ## This is because the first element was already selected previously as 'c'
    for i in range(1,len(polyList)):
        ## Define the value of the next element (starting with the second and then +1 with every iteration)
        if showHex == True:
            a = int(str(polyList[i]),16)
        elif showHex == False:
            a = int(str(polyList[i]),2)
        ## if the operation selected is multiply, then multiply
        if operation == 'multiply':
            c = F.Multiply(c,a)
        ## if the operation selected is divide, then divide
        elif operation == 'divide':
            c = F.Divide(c,a)
        ## if the operation selected is add, then add
        elif operation == 'add':
            c = F.Add(c,a)
        ## if the operation selected is subtract, then subtract
        elif operation == 'subtract':
            c = F.Subtract(c,a)
        ## if the operation select is multiply without reducing, then proceed with that
        elif operation == 'multiplyNoReduce':
            c = F.MultiplyWithoutReducing(c,a)
        ## if the operation selected is mod, then:
        elif operation == 'mod':
            ## If the operation is mod and there is only one element, throw an error
            if len(polyList) == 1:
                return "Error, enter two values for this operation"
            ## Else if there are exactly two elements, apply the full division
            c = F.FullDivision(c,a,F.FindDegree(c),F.FindDegree(a))
    ## if the operation is mod then:
    if operation == 'mod':
        ## if the show as polynomial option is checked, then return the remainder as a polynomial
        if showPoly == True:
            return F.ShowPolynomial(c[1])
        ## if showPoly is false, return as binary
        if showHex == True:
            return hex(c[1])
        return ('{0:b}'.format(c[1]))
    ## in general if show as polynomial is selected, print as a polynomial
    if showPoly == True:
        return F.ShowPolynomial(c)
    ## if show polynomial is false, print as binary
    elif showHex == True:
        return hex(c)
    return ('{0:b}'.format(c))
from tkinter import *

##########################################################################################
                                    ## GUI using tkinter
##########################################################################################
                                  

##########################################################################################
master = Tk() ##initialize the GUI
##########################################################################################
## Rename the title of the software
master.title('Galois Field Calculator')
## Set the background of the GUI as black
master.configure(background = 'black')
## Define the labels for each input box
## This is the first input box for the field power 
Label(master, text='Field GF(2^m), type in the power m',font=('monospace',8),bg='black',fg='#7D5710').grid(row=0) 
fieldVal = Entry(master,bg='#6E7B7C')
fieldVal.grid(row=0,column=1)
##Defining hte second input box for the field generator value
Label(master, text='Type in the Generator value',font=('monospace',8),bg='black',fg='#7D5710').grid(row=1) 
genVal = Entry(master,bg='#6E7B7C')
genVal.grid(row=1,column=1)
## Input box to enter the binary numbers required for operation
Label(master, text='Values for operation (split with spaces)',font = ('monospace',8),bg='black',fg='#7D5710').grid(row=2) 
polyStr = Entry(master,bg='#6E7B7C')
polyStr.grid(row=2,column=1)
## Define the checkbutton variable as a boolean variable
showPoly = BooleanVar()
## Define the actual checkbutton here, style it and assign it to the GUI grid
Checkbutton(master, text='Polynomial Form (Default is Binary, only for result)', variable=showPoly,font=('monospace',8),bg='black',fg='#029FC6').grid(row=3,columnspan = 2)
## Define the checkbutton variable as a boolean variable
showHex = BooleanVar()
## Define the actual checkbutton here, style it and assign it to the GUI grid
Checkbutton(master, text='Hexadecimal form (Default is Binary, for input and output)', variable=showHex,font=('monospace',8),bg='black',fg='#029FC6').grid(row=4,columnspan = 2)
## Define the label for results of the calculations globally 
global label
## The label here is being defined and set as empty for updating per iteration purposes
label = Label(master, textvariable= "", font = ('monospace',20),bg='black',fg='#029FC6')
## The following function prints the result of the button press
def printResult(oper):
    ## Splitting the binary number input string
    polys = polyStr.get().split(" ")
    ## Calculating the values
    x = ffield_calculator(polys,oper,int(fieldVal.get()),int(genVal.get()),showPoly.get(),showHex.get())
    ## Changing the label value to the result
    label['text'] = str(x)
    ## Assigning the label to the GUI grid
    label.grid(row = 9,column =0,columnspan=2)
    
## Defining each operation button an assigning it in the GUI grid. Each button runs the printResult function with the corresponding operation
## The function implementation was done using lambda notation
## Some styling was also applied to each button.
Button1 = Button(master, text='Multiply',font=('monospace',8), width=30, command= lambda: printResult('multiply'),fg='white',bg='#262626')
Button1.grid(row=5)
Button2 = Button(master, text='Divide', font=('monospace',8),width=30, command= lambda: printResult('divide'),fg='white',bg='#262626')
Button2.grid(row=5,column=1)
Button3 = Button(master, text='Add',font=('monospace',8), width=30, command= lambda: printResult('add'),fg='white',bg='#262626')
Button3.grid(row=6,column=0)
Button4 = Button(master, text='Subtract',font=('monospace',8), width=30, command= lambda: printResult('subtract'),fg='white',bg='#262626')
Button4.grid(row=6,column=1)
Button5 = Button(master, text='Inverse',font=('monospace',8), width=30, command= lambda: printResult('inverse'),fg='white',bg='#262626')
Button5.grid(row=7,column=0)
Button6 = Button(master, text='Modulo', font=('monospace',8), width=30, command= lambda: printResult('mod'),fg='white',bg='#262626')
Button6.grid(row=7,column=1)
Button62 = Button(master, text='Multiply without reducing',font=('monospace',8), width=52, command= lambda: printResult('mod'),fg='white',bg='#262626')
Button62.grid(row=8,column=0,columnspan=2)
Button7 = Button(master, text='Exit',font=('monospace',8), width=52, command= master.destroy,fg='#7D5710',bg='#262626')
Button7.grid(row=11,columnspan=2)

############################################################################################
mainloop() ## loop the GUI
############################################################################################