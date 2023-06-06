from use import check_overflow, convert_to_16bit_bin, convert_flagstobin


reg_dict = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}

flags = [0] * 4
reg_list = [0, 0, 0, 0, 0, 0, 0, flags]

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
def typeD(instrn, mem, reg,memory):  # ld,st(memory instrns)
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
def typeF(halted):
    return not halted


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

def execute_instruction(type, line, instrn,memory,halted,reg_list):
    check_and_reset_flags(instrn, type)

    if type == "A":
        op1 = reg_list[reg_dict[line[10:13]]]
        op2 = reg_list[reg_dict[line[13:]]]
        reg_list[reg_dict[line[7:10]]] = typeA(instrn, op1, op2)
        return [False,reg_list]
    
    elif type == "B":
        imm = int(line[9:], 2)
        reg = reg_list[reg_dict[line[6:9]]]
        reg_list[reg_dict[line[6:9]]] = typeB(instrn, imm, reg)
        return [False,reg_list]
    
    elif type == "C":
        updated_val = reg_list[reg_dict[line[10:13]]]
        op = reg_list[reg_dict[line[13:]]]
        reg_list[reg_dict[line[10:13]]] = typeC(instrn, updated_val, op)
        return [False,reg_list]
    
    elif type == "D":
        mem = int(line[9:], 2)
        reg = reg_list[reg_dict[line[6:9]]]
        reg_list[reg_dict[line[6:9]]] = typeD(instrn, mem, reg,memory)
        return [False,reg_list]
    
    elif type == "E":
        mem = int(line[9:], 2)
        typeE(instrn, mem)
        return [False,reg_list]
    
    else:
        return [typeF(halted),reg_list]