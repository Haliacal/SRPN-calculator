import os
import math
import numpy as np
from string import digits as DIGITS, whitespace as WHITESPACE

stack = []
user_input = 0
OPERATIONS = ['+','*','/','%','^']
op = True
num = False
in_comment = False
up_limit = 2147483647
low_limit = -2147483648
r_list = ["1804289383","521595368","35005211","1303455736","304089172","1540383426","1365180540","1967513926","2044897763","1102520059","783368690","1350490027","1025202362","1189641421","596516649","1649760492","719885386","424238335","1957747793","1714636915","1681692777","846930886","1804289383"]
r_count = len(r_list)-1

def calculations(num_1, num_2, op):

  valid  = True
  combine = 0 

  # Check for dividing by 0 
  if(str(num_2) == "0" and op == "/"):
    print("Divide by 0.")
    valid = False
  
  elif(int(num_2) < 0 and op == "^"):
    print("Negative power.")
    valid = False
  
  else:
    
    # Converts "^" to "**" for eval
    if(op == "^"): op = "**"

    # Evaluates string expressions
    combine = eval("("+str(num_1)+")" + op + "("+ str(num_2)+")")
    combine = math.trunc(combine)

    # Saturation (Limits)
    if(combine>up_limit): combine = up_limit
    if(combine<low_limit): combine = low_limit

  return combine,valid

def stackCheck(stack, op_check):

  if((len(stack) == 23) and not op_check):
    print("Stack overflow.")
    return False
  
  elif((len(stack) < 2) and op_check):
    print("Stack underflow.")
    return False
  
  return True

def process_command(command):

  user_input = command
  skip_count = 0
  global in_comment
  global r_count
  
  for count,i in enumerate(user_input):

    # Skip Function for reading past values
    if(skip_count != 0): skip_count -= 1

    elif(i == "#" or in_comment):
      temp_count = count
      
      if(in_comment):
        if(i == "#"):
          if(len(user_input) == 1):
            in_comment = False

          elif(count != (len(user_input)-1)):
            if((user_input[temp_count+1] in WHITESPACE) and (user_input[temp_count-1] in WHITESPACE)):
              in_comment = False 
          
          elif(count == (len(user_input)-1) and (user_input[temp_count-1] in WHITESPACE)):
            in_comment = False 
      
      elif(count == 0 and (count == (len(user_input)-1))):
        in_comment = True
          
      elif(count == (len(user_input)-1) and (user_input[temp_count-1] in WHITESPACE)):
        in_comment = True
      
      elif(count == 0 and (user_input[temp_count+1] in WHITESPACE)):
        in_comment = True
      
      elif(((count != 0) and count != (len(user_input)-1)) and ((user_input[temp_count+1] in WHITESPACE) and (user_input[temp_count-1] in WHITESPACE))):
        in_comment = True
      
      else:
        if(stackCheck(stack, num)):
          stack.append(0)

    # Pass though whitespaces
    elif(i in WHITESPACE): pass

    # Read '-' for either number or operation
    elif(i == "-"):

      neg_number = ''
      temp_count = count
      neg_number_check = False
      oct_to_dec = 0
      not_octal = False
      octal = ''

      if(len(user_input) > 2):
        if(user_input[temp_count+1] == '0'):
          temp_count += 1
          while(user_input[temp_count] in DIGITS):
            temp_count += 1
            skip_count += 1
          
            if(temp_count == len(user_input)\
            or (user_input[temp_count] not in DIGITS)): 
              break

            if(user_input[temp_count]<'8' and user_input[temp_count]>='0'):
              octal += user_input[temp_count]
          
            else:
              not_octal = True
               
          if(not not_octal):
            if(stackCheck(stack, num)):
              oct_to_dec = int(octal, 8)
              if(oct_to_dec>up_limit): oct_to_dec += (low_limit*2)
              if(oct_to_dec<low_limit): oct_to_dec += up_limit
              stack.append(-oct_to_dec)
        
          continue

      #Check for numbers
      if(count != (len(user_input)-1)):
        while(user_input[temp_count+1] in DIGITS):
          neg_number += user_input[temp_count+1]
          temp_count += 1
          skip_count += 1
          neg_number_check = True
          if(temp_count == len(user_input)-1): break
          
        
        if(neg_number_check):
          if(stackCheck(stack, num)): 
            neg_number = int("-" + neg_number)
            if(neg_number<low_limit): neg_number = low_limit
            stack.append(neg_number)
        
      # Operation function
      elif(not neg_number_check):
        if(stackCheck(stack, op)):
          out, valid = calculations(stack[-2],stack[-1],i)
          if(valid):
            stack.pop()
            stack.pop()
            stack.append(out)
    
    # Read integers
    elif(i in DIGITS):

      combined_number = ''
      temp_count = count
      skip_count -= 1
      octal = ''
      oct_to_dec = 0
      not_octal = False

  
      if(i == '0' and len(user_input) != 1):
        while(user_input[temp_count] in DIGITS):
          temp_count += 1
          skip_count += 1
          
          if(temp_count == len(user_input)\
           or (user_input[temp_count] not in DIGITS)): 
           break

          if(user_input[temp_count]<'8' and user_input[temp_count]>='0'):
            octal += user_input[temp_count]
          
          else:
            not_octal = True
               
        
        if(not not_octal):
          if(stackCheck(stack, num)):
            oct_to_dec = int(octal, 8)
            if(oct_to_dec>up_limit): oct_to_dec = up_limit
            if(oct_to_dec<low_limit): oct_to_dec = low_limit
            if((temp_count - count) >= 20): oct_to_dec = -1
            stack.append(oct_to_dec)
        
        continue

      # Appending numbers
      if(count != (len(user_input)-1)):
        while(user_input[temp_count] in DIGITS):

          combined_number += user_input[temp_count]
          temp_count += 1
          skip_count += 1
          if(temp_count == len(user_input)): break

        if(stackCheck(stack, num)):
          combined_number = int(combined_number)
          # Saturation (Limits)
          if(combined_number>up_limit): combined_number = up_limit
          stack.append(combined_number)
      
      else:
        if(stackCheck(stack, num)):
          stack.append(i)
        
      
    # Print stack
    elif(i=='d'):
      if(len(stack) != 0):
        for j in stack: print(j)

      else: print('-2147483648') 
    
    # Random integer appending
    elif(i=='r'):
      print(r_count)
      if(r_count < 0 ):
        r_count = len(r_list)-2

      if(stackCheck(stack, num)):
        stack.append(r_list[r_count])
        r_count -= 1
    
    # Read Operation
    elif(i in OPERATIONS):
      if(stackCheck(stack, op)):
          out, valid = calculations(stack[-2],stack[-1],i)
          if(valid):
            stack.pop()
            stack.pop()
            stack.append(out)
    
    # Print top of stack
    elif(i == '='):
      if(len(stack) != 0):
        print(stack[-1])
      
      else: print("Stack empty.")
    
    # Anything else entered will be appending to the stack as 0
    else:
      if(stackCheck(stack, num)):
        stack.append(0)


#This is the entry point for the program.
#Do not edit the below
if __name__ == "__main__": 
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except:
            exit()
