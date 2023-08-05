import math

def calculate(num1,num2):
    try:
        addition  = num1 + num2
        print(f"Addition of {num1} and {num2} is: {addition}")

        subtraction  = num1 - num2
        print(f"Subtraction of {num1} and {num2} is: {subtraction}")

        multiplication  = num1 * num2
        print(f"Multiplication of {num1} and {num2} is: {multiplication}")

        if num2:
            division  = num1/ num2
            print(f"division of {num1} and {num2} is: {division}")
            return addition,subtraction,multiplication,division
        else:
            return addition,subtraction,multiplication,division
            
        return addition,subtraction,multiplication
    except:
        if num1>0:
            division = math.inf
            print(f"division of {num1} and {num2} is: {division}")
            return addition,subtraction,multiplication,division
        else:
            division = -math.inf
            print(f"division of {num1} and {num2} is: {division}")
            return addition,subtraction,multiplication,division
        return 0
