#for loop

for y in range(1,20,3):
  if y == 13:
   continue
  else:
   print(y, end=" ")

   print()  

credit_no = input("Enter Credit number: ")

for x in reversed(credit_no):
 print(x, end = " ")

 print()         #For a new line

 #While loop

food = input("Enter Food Name: ")

while not food == "q":
 print(f"I love {food}")
 food = input("Enter another Food Name: ")

 print("Bye")

#Nested Loops

row = int(input("Enter number of rows: "))
Col = int(input("Enter number of Coloumns: "))
sym = input("Enter sign: ")

for x in range(row):
    for y in range(Col):
        {
        print(sym,end=" ")
        }
        
    print()

        

