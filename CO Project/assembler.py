ops_dict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov_imm': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
            'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
            'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
            'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
            'jlt': ['11100', 'E'], 'jgt': ['11101', 'E'], 'je': ['11111', 'E'], 'hlt': ['11010', 'F']}

reg_addr = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110',
            'FLAGS': '111'}


instruction_list = ['add', 'sub', 'mov_imm', 'mov_reg', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp',
                    'jmp', 'jlt', 'jgt', 'je', 'hlt']

typeA_list = ['add', 'sub', 'mul', 'xor', 'or', 'and']
typeB_list = ['mov_imm', 'ls', 'rs']
typeC_list = ['mov_reg', 'div', 'not', 'cmp']
typeD_list = ['ld', 'st']
typeE_list = ['jmp', 'je', 'jgt', 'jlt']
typeF_list = ['hlt']
var_list = []


# def typeA(instrn, reg1, reg2, reg3):  # add, sub, mul, and, or

#     if instrn not in typeA_list:
#         print("Error: Invalid instruction")
#         return
    
#     if reg1 not in reg_addr.keys() or reg2 not in reg_addr.keys() or reg3 not in reg_addr.keys():
#         print("Error: Invalid register name- error in line", line_no)
#         return
    
#     print(ops_dict[instrn][0] + '00' + reg_addr[reg1] +
#           reg_addr[reg2] + reg_addr[reg3])

reg_data = {'R0': 0,'R1': 0,'R2': 0,'R3': 0,'R4': 0,'R5': 0,'R6':0} 

def get_register_value(register):
    if register not in reg_addr.keys():
        print("Error: Invalid register name -", register)
        return None

    value = reg_data.get(register)
    if value is None:
        print("Error: Register", register, "does not have a value")
        return None
    
    return value

def set_flag(flag):
    pass
def clear_flag(flag):
    pass

FLAGS = "0000000000000000"

def typeA(instrn, reg1, reg2, reg3):
    if instrn not in typeA_list:
        print("Error: Invalid instruction")
        return

    if reg1 not in reg_addr.keys() or reg2 not in reg_addr.keys() or reg3 not in reg_addr.keys():
        print("Error: Invalid register name - error in line", line_no)
        return

    # operation 
    value1 = get_register_value(reg1)
    value2 = get_register_value(reg2)
    result = 0
    overflow = False

    if instrn == 'add':
        result = value1 + value2
        overflow = result > 127
    elif instrn == 'sub':
        result = value1 - value2
        overflow = result < -128
    elif instrn == 'mul':
        result = value1 * value2
        overflow = result > 127 or result < -128
    elif instrn == 'and':
        result = value1 & value2
    elif instrn == 'or':
        result = value1 | value2

    # Set flag
    if overflow:
        FLAGS = FLAGS[:10] + "1" + FLAGS[11:] 
        set_flag('V')
    else:
        clear_flag('V')

    
    print(ops_dict[instrn][0] + '00' + reg_addr[reg1] + reg_addr[reg2] + reg_addr[reg3])


def typeB(instrn, reg1, imm):  # mov,ls,rs
    
    if instrn not in typeB_list:
        print("Error: Invalid instruction")
        return
    
    if reg1 not in reg_addr.keys():
        print("Error: Invalid register name - error in line", line_no)
        return
    
    if not isinstance(imm, int):
        print("Error: Immediate value must be a whole number - error in line", line_no)
        return
    
    if imm < 0 or imm > 127:
        print("Error: Immediate value must be between 0 and 127 - error in line", line_no)
        return
    
    imm_str = format(imm, '08b')
    
    print(ops_dict[instrn][0] + '0' + reg_addr[reg1] + imm_str)

# FLAGS = "0000000000000000"
# reg_data = {'R0': 0,'R1': 0,'R2': 0,'R3': 0,'R4': 0,'R5': 0,'R6':0} 

def typeC(instrn, reg1, reg2):  # mov_reg, div, not, cmp
    
    if instrn not in typeC_list:
        print("Error: Invalid instruction")
        return
    
    if reg1 not in reg_addr.keys() or reg2 not in reg_addr.keys():
        print("Error: Invalid register name- error in line", line_no)
        return
    
    global FLAGS, reg_data
    val1 = reg_data[reg1]
    val2 = reg_data[reg2]
    if val1 < val2:
        FLAGS = FLAGS[:13] + "1" + FLAGS[14:] 
        set_flag('L')
    elif val1 > val2:
        FLAGS = FLAGS[:12] + "1" + FLAGS[13:]
        set_flag('G')
    else: #val1=val2
        FLAGS = FLAGS[:11] + "1" + FLAGS[12:]
        set_flag('E')
    # if result < 0:
    #     set_flag('L')
    # else:
    #     clear_flag('L')
    # if result > 0:
    #     set_flag('G')
    # else:
    #     clear_flag('G')
    # if result == 0:
    #     set_flag('E')
    # else:
    #     clear_flag('E')

    print(ops_dict[instrn][0] + '00000' + reg_addr[reg1] + reg_addr[reg2])



def typeD(instrn, reg1, mem_add_str):  # ld, st

    if instrn not in typeD_list:
        print("Error: Invalid instruction")
        return

    if reg1 not in reg_addr.keys():
        print("Error: Invalid register name")
        return

    try:
        mem_add = int(mem_add_str)

    except ValueError:
        print("Error: Memory address must be an integer")
        return

    if mem_add < 0 or mem_add > 127:
        print("Error: Memory address must be between 0 and 127")
        return

    print(ops_dict[instrn][0] + '0' + reg_addr[reg1] + format(mem_add, '07b'))


def typeE(instrn, mem_add):  # jmp,je,jgt,jlt

    if instrn not in typeE_list:
        print("Error: Invalid instruction")
        return

    try:
        mem_add = int(mem_add)

    except ValueError:
        print("Error: Memory address must be an integer")
        return

    if mem_add < 0 or mem_add > 127:
        print("Error: Memory address must be between 0 and 127")
        return

    print(ops_dict[instrn][0] + '0000' + format(mem_add, '07b'))



def typeF(instrn):  # hlt

    if instrn not in typeF_list:
        print("Error: Invalid instruction")
        return

    print(ops_dict[instrn][0] + '00000000000')


# with open("read2.txt", "r") as f:
# with open("read.txt", "r") as f:
with open("read3.txt", "r") as f:

    s = [line.strip() for line in f]
    lines = len(s)

# print(lines)
# print(s)

line_no = 1
for i in s:
    # print(i)
    if i == '':
        print("empty line")
        continue
    i = i.split()
  
    if i[0] in typeA_list:
        if (len(i) != 4):
            print("Error: wrong syntax used for",
                  i[0], "instruction in line", line_no)
            
        else:
            typeA(i[0], i[1], i[2], i[3])
        line_no += 1
   
    elif i[0] in typeB_list:
        if len(i) != 3:
            print("Error: Wrong syntax used for",
                  i[0], "instruction in line", line_no)
        else:
            if i[2][0] == '$':
                try:
                    imm = int(i[2][1:])
                    typeB(i[0], i[1], imm)
                except ValueError:
                    print( "Error: Immediate value must be a whole number in line", line_no)
            else:
                print("Error: Invalid immediate value in line", line_no)
        line_no += 1
    
    elif i[0] in typeC_list:
        if (len(i) != 3):
            print("Error: wrong syntax used for",
                  i[0], "instruction in line", line_no)
        else:
            typeC(i[0], i[1], i[2])
        line_no += 1
   
    elif i[0] in typeD_list:  # check-incorr
        X = '0001'
        if (len(i) != 3):
            print("Error: wrong syntax used for",
                  i[0], "instruction in line", line_no)
     
        else:
            typeD(i[0], i[1], X)
        line_no += 1
   
    elif i[0] in typeE_list:
        if (len(i) != 2):
            print("Error: wrong syntax used for",
                  i[0], "instruction in line", line_no)
        else:
            typeE(i[0], i[1])

        line_no += 1

    elif i[0] in typeF_list:
        typeF(i[0])
        line_no += 1
        break

    elif i[0] == 'var':
        X = '0001'  # mem addr of var X
        print(X)
        line_no += 1


if 'hlt' not in s:
    print("Error: Missing 'hlt' instruction")

else:
    # Check if 'hlt' instruction is present as the last instruction
    if s[-1] != 'hlt':
        print("Error: 'hlt' instruction must be the last instruction")
    else:
        # print("PAssed- hlt at end")
        pass




labelList = []