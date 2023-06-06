

flags = [0] * 4
reg_list = [0, 0, 0, 0, 0, 0, 0, flags]



def check_overflow(reg):
    if (reg < 0):
        reg = 0
        flags[0] = 1
    if (reg > 65535):
        flags[0] = 1
        reg = takelower_16(reg)
    return reg


def takelower_16(n):
    b = bin(n)[2:]
    l = len(b)-16
    n = int(b[l:], 2)
    return n

def convert_to_16bit_bin(num):
    a = bin(int(num))[2:]
    b = (16-len(a))*"0" + a
    return b

def convert_to_7_bit_bin(num):
    a = bin(int(num))[2:]
    b = (7-len(a))*"0" + a
    return b

def convert_flagstobin(flags):
    f = 12*"0"
    for i in flags:
        f = f+str(i)
    return f

opcodes_dict = {"00000": ["add", "A"], "00001": ["sub", "A"], "00010": ["mov", "B"], "00011": ["mov", "C"], "00100": ["ld", "D"],
           "00101": ["st", "D"], "00110": ["mul", "A"], "00111": ["div", "C"], "01000": ["rs", "B"], "01001": ["ls", "B"],
           "01010": ["xor", "A"], "01011": ["or", "A"], "01100": ["and", "A"], "01101": ["not", "C"], "01110": ["cmp", "C"],
           "01111": ["jmp", "E"], "11100": ["jlt", "E"], "11101": ["jgt", "E"], "11111": ["je", "E"], "11010": ["hlt", "F"]}

reg_dict = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}

flags = [0] * 4
reg_list = [0, 0, 0, 0, 0, 0, 0, flags]