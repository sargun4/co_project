Bonus part of the Project

Instructions Added:

->Comp R1 R2
Updates the value of R1 to the 1's complement of R2.

->Floor R1 R2
Updates the value of R1 to the floor of half the value of R2.

->Ceil R1 R2
Updates the value of R1 to the ceil of half the value of R2.

->Min R1 R2 R3
Updates the value of R1 to the minimum of R2 and R3.

->Max R1 R2 R3
Updaes the value of R1 to the maximum of R2 and R3.



Semantics for the added Instructions:

comp: 10100
opcode(5 bits) + filler(5 bits) + reg1(3 bits) +reg2(3 bits)

ceil: 10101
opcode(5 bits) + filler(5 bits) + reg1(3 bits) +reg2(3 bits)

floor: 10110
opcode(5 bits) + filler(5 bits) + reg1(3 bits) +reg2(3 bits)

max: 10111
opcode(5 bits) + filler(2 bit) +reg1(3 bits) + reg2(3 bits) + reg3(3 bits)

min: 11000
opcode(5 bits) + filler(2 bit) +reg1(3 bits) + reg2(3 bits) + reg3(3 bits)
