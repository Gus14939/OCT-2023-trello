# decimal to binary
# input num
# binary is base = 2
# return a num as binary

# function(num)
def convert_base(num):
    # var base
    base = 2
    # int(num)
    # var binary_set = ""
    remainders = ""
    # loop that takes var num and divides by base until num is  = 1
    # num to in
    if num == 0:
        print("0")
        return 0
    while num > 0:
        remainder = num % base
        num = num // base
        remainders += str(remainder)
        print(num, remainder)
    binary_string = "".join(reversed(remainders))
    print(binary_string)
        
    # return
    # return binary set
    
    
# result = convert_base(10)
# print(result)
convert_base(0)

def convert_base2(num):
    # var base
    base = 2
    # int(num)
    # var binary_set = ""
    binary_list = []
    # loop that takes var num and divides by base until num is  = 1
    # num to in
    while num > 0:
        remainder = num % base
        num = num // base
        binary_list.insert(0, str(remainder))
        print(num, remainder)
    binary_set = "".join(binary_list)
    print(binary_set)

convert_base2(15)