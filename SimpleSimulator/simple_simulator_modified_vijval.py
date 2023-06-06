# check for 
# 0001000010000101
# 0010100010000011
# 1101000000000000

import EE
import RF
import MEM
from Helper import *
import PC

global halted
halted=False

pc=PC.initialize()
instrunctns=MEM.initialize()[1]
memory=MEM.initialize()[0]

while not halted:
    opcode = instrunctns[pc][:5]
    instrn = opcodes_dict[opcode][0]
    type = opcodes_dict[opcode][1]
    current = pc

    halted,reg_list=EE.execute_instruction(type, instrunctns[pc], instrn,memory,halted,reg_list)[0],EE.execute_instruction(type, instrunctns[pc], instrn,memory,halted,reg_list)[1]
    RF.dump(current,reg_list,flags)
    pc=PC.update(pc)
    
MEM.dump(memory)


