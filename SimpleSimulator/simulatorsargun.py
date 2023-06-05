# check for 
# 0001000010000101
# 0010100010000011
# 1101000000000000

opcodes_dict = {"00000": ["add", "A"], "00001": ["sub", "A"], "00010": ["mov", "B"], "00011": ["mov", "C"], "00100": ["ld", "D"],
           "00101": ["st", "D"], "00110": ["mul", "A"], "00111": ["div", "C"], "01000": ["rs", "B"], "01001": ["ls", "B"],
           "01010": ["xor", "A"], "01011": ["or", "A"], "01100": ["and", "A"], "01101": ["not", "C"], "01110": ["cmp", "C"],
           "01111": ["jmp", "E"], "11100": ["jlt", "E"], "11101": ["jgt", "E"], "11111": ["je", "E"], "11010": ["hlt", "F"]}

reg_dict = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}

flags = [0] * 4
reg_list = [0, 0, 0, 0, 0, 0, 0, flags]
halted = False


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

# type A
def typeA(instrn, op1, op2):  # add,sub,mul,xor,or,and(arithmetic)
    if instrn == "add":
        res = op1+op2
        res = check_overflow(res)
        return res
    elif instrn == "sub":
        res = op1-op2
        res = check_overflow(res)
        return res
    elif instrn == "mul":
        res = op1 * op2
        res = check_overflow(res)
        return res
    elif instrn == "and":
        res = op1 & op2
        return res
    elif instrn == "xor":
        res = op1 ^ op2
        return res
    elif instrn == "or":
        res = op1 | op2
        return res
    

# type B
def typeB(instrn, imm, reg):  # use imm values
    if instrn == "mov":
        return imm
    
    elif instrn == "ls":
        return reg << imm
    elif instrn == "rs":
        return reg >> imm

# type C
def typeC(instrn, updated_val, op):  # mov,div,notcmp
    if instrn == "mov":
        if op == flags:
            op = int(convert_flagstobin(), 2)
        reset_flags()
        return op
    elif instrn == "cmp":
        if updated_val == op:  # Equal - E flag set
            flags[3] = 1
        elif updated_val < op:  # Less than - L
            flags[1] = 1
        else:  # Greater than - G
            flags[2] = 1
        return updated_val
    elif instrn == "div":
        reg_list[0] = updated_val//op
        reg_list[1] = updated_val % op
        return updated_val
    elif instrn == "not":
        return op ^ 65535
    

# type D
def typeD(instrn, mem, reg):  # ld,st(memory instrns)
    if instrn == "ld":
        return int(memory[mem], 2)
    elif instrn == "st":
        memory[mem] = convert_to_16bit_bin(reg)
        return reg

# type E
def typeE(instrn, mem):  # jmp,jlt,jgt,je -jums
    global pc
    if instrn == "jmp":
        pc = mem-1
    elif instrn == "jlt":
        if flags[1] == 1:
            pc = mem-1
    elif instrn == "jgt":
        if flags[2] == 1:
            pc = mem-1
    elif instrn == "je":
        if flags[3] == 1:
            pc = mem-1
    reset_flags()

# type F
def typeF():
    global halted
    halted = True


def reset_flags():
    for i in range(4):
        flags[i] = 0


def check_and_reset_flags(instrn, type):
    if (instrn == "jlt" or instrn == "jgt" or instrn == "je"):
        return
    if (instrn == "mov" and type == "C"):
        return
    else:
        reset_flags()

def execute_instruction(type, line, instrn):
    check_and_reset_flags(instrn, type)

    if type == "A":
        op1 = reg_list[reg_dict[line[10:13]]]
        op2 = reg_list[reg_dict[line[13:]]]
        reg_list[reg_dict[line[7:10]]] = typeA(instrn, op1, op2)
    
    elif type == "B":
        imm = int(line[9:], 2)
        reg = reg_list[reg_dict[line[6:9]]]
        reg_list[reg_dict[line[6:9]]] = typeB(instrn, imm, reg)
    
    elif type == "C":
        updated_val = reg_list[reg_dict[line[10:13]]]
        op = reg_list[reg_dict[line[13:]]]
        reg_list[reg_dict[line[10:13]]] = typeC(instrn, updated_val, op)
    
    elif type == "D":
        mem = int(line[9:], 2)
        reg = reg_list[reg_dict[line[6:9]]]
        reg_list[reg_dict[line[6:9]]] = typeD(instrn, mem, reg)
    
    elif type == "E":
        mem = int(line[9:], 2)
        typeE(instrn, mem)
    
    else:
        typeF()


def convert_to_16bit_bin(num):
    a = bin(int(num))[2:]
    b = (16-len(a))*"0" + a
    return b

def convert_to_7_bit_bin(num):
    a = bin(int(num))[2:]
    b = (7-len(a))*"0" + a
    return b

def convert_flagstobin():
    f = 12*"0"
    for i in flags:
        f = f+str(i)
    return f

def printregs(pc):
    print(convert_to_7_bit_bin(pc)+" "+convert_to_16bit_bin(reg_list[0])+" "+convert_to_16bit_bin(reg_list[1])
          + " "+convert_to_16bit_bin(reg_list[2]) + " "+convert_to_16bit_bin(reg_list[3])+" " +
          convert_to_16bit_bin(reg_list[4])+" "+convert_to_16bit_bin(reg_list[5])+" " +
          convert_to_16bit_bin(reg_list[6])+" "+convert_flagstobin())

# def store_regs(pc):
#     register_values = {
#         "PC": convert_to_7_bit_bin(pc),
#         "R0": convert_to_16bit_bin(reg_list[0]),
#         "R1": convert_to_16bit_bin(reg_list[1]),
#         "R2": convert_to_16bit_bin(reg_list[2]),
#         "R3": convert_to_16bit_bin(reg_list[3]),
#         "R4": convert_to_16bit_bin(reg_list[4]),
#         "R5": convert_to_16bit_bin(reg_list[5]),
#         "R6": convert_to_16bit_bin(reg_list[6]),
#         "FLAGS": convert_flagstobin()
#     }
#     return register_values

# register_values = store_regs(pc)
# print(register_values)

with open('simulator_test.txt') as f:
    instrunctns = f.read().splitlines()


lst = "0"*16
memory = [lst]*128

i = 0
for line in instrunctns:
    memory[i] = line
    i += 1
pc = 0 


while not halted:
    opcode = instrunctns[pc][:5]
    instrn = opcodes_dict[opcode][0]
    # type = opcodes_dict[1]
    type = opcodes_dict[opcode][1]
    current = pc
    execute_instruction(type, instrunctns[pc], instrn)
    printregs(current)
    pc += 1

ctr = 0
# print \ memory dump
for i in memory:
    print(i)
    ctr += 1


