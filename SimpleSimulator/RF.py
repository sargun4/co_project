from Helper import convert_to_16bit_bin, convert_flagstobin,convert_to_7_bit_bin











def dump(pc,reg_list,flags):
    print(convert_to_7_bit_bin(pc)+" "+convert_to_16bit_bin(reg_list[0])+" "+convert_to_16bit_bin(reg_list[1])
          + " "+convert_to_16bit_bin(reg_list[2]) + " "+convert_to_16bit_bin(reg_list[3])+" " +
          convert_to_16bit_bin(reg_list[4])+" "+convert_to_16bit_bin(reg_list[5])+" " +
          convert_to_16bit_bin(reg_list[6])+" "+convert_flagstobin(flags))