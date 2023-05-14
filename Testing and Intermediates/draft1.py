instructions = {
    "add": "0000000",
    "sub": "0000100",
    "mov": ["000100", "0001100000"],
    "ld": "001000",
    "st": "001010",
    "mul": "0011000",
    "div": "0011100000",
    "rs": "010000",
    "ls": "010010",
    "xor": "0101000",
    "or": "0101100",
    "and": "0110000",
    "not": "0110100000",
    "cmp": "0111000000",
    "jmp": "011110000",
    "jlt": "111000000",
    "jgt": "111010000",
    "je": "111110000",
    "hlt": "1101000000000000",
    "addf": "1000000",
    "subf": "1000100"
}

variables = {}
labels = {}
mem_start = 0
var_flag = 0
line_num = -1
error_flag = 0

overflow_flag, less_than_flag, greater_than_flag, equal_flag = 0, 0, 0, 0

assembly = []

def send_error(error_msg):
    f = open("output.txt", "w")
    f.write(f"{error_msg}\n")
    f.close()
    exit(0)

def reg_to_bin(reg, line_num):
    if reg == "FLAGS":
        send_error(f"Illegal use of FLAGS registered, line {line_num}")
    try:
        if len(reg) == 2 and reg[0].lower() == "r":
            return (bin(int(reg[1]))[2:]).zfill(3)
        else:
            send_error(f"Typos in register name, line {line_num}")
    except:
        send_error(f"Typos in register name, line {line_num}")

def get_mem_addr(mem):
    return bin(mem)[2:].zfill(7)

def imm_to_bin(num, line_num):
    try:
        num = int(num[1:])
        if num >= 0 and num <= 127:
            return bin(num)[2:].zfill(7)
        else:
            send_error(f"Illegal Immediate Values, line {line_num}")
    except:
        send_error(f"Illegal Immediate Values, line {line_num}")

def var_to_bin(var):
    return variables[var]["mem"]

def get_ins(s):
    global var_flag, mem_start, line_num, error_flag
    line_num += 1
    if s[0] == "var" and not var_flag:
        if s[1] not in variables:
            line_num -= 1
            variables[s[1]] = {"mem": None, "value": None}
            mem_start += 1
        else:
            send_error(f"Variable already declared")
    elif s[0] == "var" and var_flag:
        send_error(f"Variable not declared at the beginning, line {line_num}")
    elif ":" in s[0]:
        if s[0][:-1] not in labels:
            labels[s[0][:-1]] = {"Line": bin(line_num)[2:].zfill(7)}
            line_num -= 1
            get_ins(s[1:])
        else:
            send_error(f"Label already declared, line {line_num}")
    elif s[0] not in instructions:
        send_error(f"Typos in instruction name, line {line_num}")
    elif s[0] == "hlt":
        assembly.append(instructions[s[0]])
        if len(s) != 1:
            send_error(f"General Syntax Error, line {line_num}")
        return
    else:
        ins = instructions[s[0]]
        var_flag = 1
        if s[0] == "mov":
            if len(s) != 3:
                send_error(f"General Syntax Error, line {line_num}")
            if "$" in s[2]:
                ins = ins[0] + reg_to_bin(s[1], line_num) + imm_to_bin(s[2], line_num)
                assembly.append(ins)
            else:
                if s[2] == "FLAGS":
                    ins = ins[1] + reg_to_bin(s[1], line_num) + "111"
                    assembly.append(ins)
                else:
                    ins = ins[1] + reg_to_bin(s[1], line_num) + reg_to_bin(s[2], line_num)
                    assembly.append(ins)
        elif len(ins) == 7:
            if len(s) != 4:
                send_error(f"General Syntax Error, line {line_num}")
            else:
                ins = ins + reg_to_bin(s[1], line_num) + reg_to_bin(s[2], line_num) + reg_to_bin(s[3], line_num)
                assembly.append(ins)
        elif len(ins) == 6:
            if s[0] == "ld":
                if len(s) != 3:
                    send_error(f"General Syntax Error, line {line_num}")
                else:
                    ins = [ins, reg_to_bin(s[1], line_num), s[2]]
                    if s[2] not in variables:
                        send_error(f"Variable not declared at beginning, line {line_num}")
                    assembly.append(ins)
            elif s[0] == "st":
                if len(s) != 3:
                    send_error(f"General Syntax Error, line {line_num}")
                else:
                    ins = [ins, reg_to_bin(s[1], line_num), s[2]]
                    if s[2] not in variables:
                        send_error(f"Variable not declared at beginning, line {line_num}")
                    assembly.append(ins)
            elif s[0] in ["rs", "ls"]:
                if len(s) != 3:
                    send_error(f"General Syntax Error, line {line_num}")
                else:
                    ins = ins + reg_to_bin(s[1], line_num) + imm_to_bin(s[2], line_num)
                    assembly.append(ins)
        elif len(ins) == 10:
            if len(s) != 3:
                send_error(f"General Syntax Error, line {line_num}")
            else:
                ins = ins + reg_to_bin(s[1], line_num) + reg_to_bin(s[2], line_num)
                assembly.append(ins)
        elif len(ins) == 9:
            if len(s) != 2:
                send_error(f"General Syntax Error, line {line_num}")
            else:
                ins = [ins, s[1]]
                assembly.append(ins)

file_name = "input.txt"
with open(file_name, "r") as fin:
    for line in fin:
        if line == "\n":
            continue
        if "\n" in line:
            line = line[:-1]
        line = line.split()
        get_ins(line)

f = open("output.txt", "w")

if assembly[-1] != "1101000000000000":
    f.write("hlt not being used as last function\n")
elif len(assembly) > 128:
    f.write("Assembler instruction limit reached\n")
else:
    for var in variables.keys():
        line_num += 1
        variables[var]["mem"] = get_mem_addr(line_num)
    for i in range(0, len(assembly)):
        if len(assembly[i]) == 2:
            if assembly[i][1] not in labels:
                f.write("Misuse of Label\n")
                f.close()
                exit(0)
            else:
                assembly[i] = assembly[i][0] + labels[assembly[i][1]]["Line"]
        elif len(assembly[i]) == 3:
            assembly[i] = assembly[i][0] + assembly[i][1] + var_to_bin(assembly[i][2])
    for i in assembly:
        f.write(f"{i}\n")
f.close()