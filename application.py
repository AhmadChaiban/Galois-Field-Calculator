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

##########################################################################################
                                    ## GUI using tkinter
##########################################################################################
                                  
from tkinter import *
from PIL import Image

##########################################################################################
master = Tk() ##initialize the GUI
##########################################################################################
## Rename the title of the software
master.title('Galois Field Calculator')
## setting geometry for GUI
master.geometry('800x480')
##Using Pillow library to import image
backImg = Image.open('UI_back.png')
backImg = backImg.resize((800,480),Image.ANTIALIAS)
backImg.save('UI.ppm','ppm')
gridImg = Image.open('grid.jpg')
gridImg = gridImg.resize((400,100),Image.ANTIALIAS)
gridImg.putalpha(128)
gridImg.save('grid.ppm','ppm')
## selecting background image
backImg = PhotoImage(file = 'UI.ppm')
label_for_image = Label(master,image=backImg,border=0)
label_for_image.grid(row = 0)
## selecting the grid 
gridImg = PhotoImage(file = 'grid.ppm')
label_for_grid = Label(master,image=gridImg,border=2,bg='#56E29B')
label_for_grid.place(x=270,y=140)
## Set the background of the GUI as black
master.configure(background = 'black')
## Define the labels for each input box
## This is the first input box for the field power 
Label(master, text='Field GF(2^m), type in the power m',font=('monospace',8),bg='black',fg='#56E29B').place(x=300,y=250) 
fieldVal = Entry(master,bg='#6E7B7C')
fieldVal.place(x=500,y=250)
##Defining hte second input box for the field generator value
Label(master, text='Type in the Generator value',font=('monospace',8),bg='black',fg='#56E29B').place(x=300,y=280)
genVal = Entry(master,bg='#6E7B7C')
genVal.place(x=500,y=280)
## Input box to enter the binary numbers required for operation
Label(master, text='Values for operation (split with spaces)',font = ('monospace',8),bg='black',fg='#56E29B').place(x=300,y=310)
polyStr = Entry(master,bg='#6E7B7C')
polyStr.place(x=500,y=310)
## Define the checkbutton variable as a boolean variable
showPoly = BooleanVar()
## Define the actual checkbutton here, style it and assign it to the GUI grid
Checkbutton(master, text='Polynomial Form', variable=showPoly,font=('monospace',8),bg='black',fg='#029FC6').place(x=330,y = 410)
## Define the checkbutton variable as a boolean variable
showHex = BooleanVar()
## Define the actual checkbutton here, style it and assign it to the GUI grid
Checkbutton(master, text='Hexadecimal form', variable=showHex,font=('monospace',8),bg='black',fg='#029FC6').place(x=330,y=430)
## Define the label for results of the calculations globally 
global label
## The label here is being defined and set as empty for updating per iteration purposes
label = Label(master, textvariable= "", font = ('monospace',10),bg='black',fg='#029FC6')
## The following function prints the result of the button press
def printResult(oper):
    ## Splitting the binary number input string
    polys = polyStr.get().split(" ")
    ## Calculating the values
    ## If there are no values in the list of binary numbers, return an error
    if len(polys) == 0 or fieldVal.get() == '' or genVal.get() == '' :
        label['text'] = "Error: Please enter field/values to compute"
        label.place(x=290,y=180)
        return 0
    ## if values entered for mod are only 1, throw an error
    if oper == 'mod' and len(polys) == 1:
        label['text'] = "Error: Please enter exactly two elements"
        label.place(x=290,y=180)
        return 0
    ## make the calculations in the selected field
    x = ffield_calculator(polys,oper,int(fieldVal.get()),int(genVal.get()),showPoly.get(),showHex.get())
    ## Changing the label value to the result
    label['text'] = str(x)
    ## Assigning the label to the GUI grid
    label.place(x=290,y=180)
    
## Defining each operation button an assigning it in the GUI grid. Each button runs the printResult function with the corresponding operation
## The function implementation was done using lambda notation
## Some styling was also applied to each button.
Button1 = Button(master, text='Multiply',font=('monospace',10), width=0, command= lambda: printResult('multiply'),fg='#56E29B',bg='black',border=0)
Button1.place(x = 80,y = 27)
Button2 = Button(master, text='Divide', font=('monospace',10),width=0, command= lambda: printResult('divide'),fg='#56E29B',bg='black',border=0)
Button2.place(x = 80,y = 75)
Button3 = Button(master, text='Add',font=('monospace',10), width=0, command= lambda: printResult('add'),fg='#56E29B',bg='black',border=0)
Button3.place(x = 80,y = 120)
Button4 = Button(master, text='Subtract',font=('monospace',10), width=0, command= lambda: printResult('subtract'),fg='#56E29B',bg='black',border=0)
Button4.place(x = 80,y = 165)
Button5 = Button(master, text='Inverse',font=('monospace',10), width=0, command= lambda: printResult('inverse'),fg='#56E29B',bg='black',border=0)
Button5.place(x = 80,y = 211)
Button6 = Button(master, text='Modulo', font=('monospace',10), width=0, command= lambda: printResult('mod'),fg='#56E29B',bg='black',border=0)
Button6.place(x = 80,y = 258)
Button62 = Button(master, text='Multiply w/ reducing',font=('monospace',10), width=0, command= lambda: printResult('mod'),fg='#56E29B',bg='black',border=0)
Button62.place(x = 80,y = 306)
Button7 = Button(master, text='Exit',font=('monospace',10), width=0, command= master.destroy,fg='#56E29B',bg='black',border=0)
Button7.place(x = 80,y = 352)

############################################################################################
mainloop() ## loop the GUI
############################################################################################