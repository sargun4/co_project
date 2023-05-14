
class Error(Exception):
    pass
##different errors?

class Error2(Exception):
    pass

class Error3(Exception):
    pass

class Error4(Exception):
    pass

class Error5(Exception):
    pass




def make7(s):
    if(len(s)<7):
        x=7-len(s)
        mm="0"*x
        s=mm+s
    return s

regdict={'R0':'000',
'R1':'001',
'R2':'010',
'R3':'011',
'R4':'100',
'R5':'101',
'R6':'110',
'FLAGS':'111'}

vardict={}
labeldict={}
groupadict={'add':'00000_00','sub':'00001_00','mul':'00010_00','xor':'01010_00','or':'01011_00','and':'01100_00'}
groupbdict={'mov':'00010_0','rs':'01000_0','ls':'01001_0'}
groupcdict={'mov':'00011_00000','div':'00111_00000','not':'01101_00000','cmp':'01110_00000'}
groupddict={'ld':'00100_0','st':'00101_0'}
groupedict={'jmp':'01111_0000','jlt':'11100_0000','jgt':'11101_0000','je':'11111_0000','var':''}
#label not at start
#label only with jump
#label and op on same line?
#halt as last
#len(l)=5
#vars at start
#label variable error



def checklabel(strin,inde,listt):
    co=1
    for j in range(inde+1,len(listt)):
        if strin+":" in listt[j]:
            co=j
            break

    if co==1:
        return -1
    else:
        return co
    
varc=0
def opcode(l,ind,biglist,actu,varindex):
    global progl
    global varc

    '''try:
        counthlt=0
        for i in biglist:
            if "hlt" in i:
                counthlt+=1
                break
        if counthlt==0:
            raise Error
    except:
        return "Error: No Hlt instruction present"'''
            

    if len(l)==1:
        s=l[0]
        try:
            if s=="hlt":
                varc=1
                return "11010_00000000000"
                
            else:
                raise Error
        except:
            return ("Error: General Syntax Error")
            
           
           
        

    if len(l)==2:                                                                # group e
        s=l[0]
        r=l[1]
        if s[-2::-1][::-1] in labeldict:
            lllll=[r]
            varc=1
            return opcode(lllll,ind,biglist,actu,varindex)
        else:

            try:
                if s in groupedict:
                    if s!='var':
                        t=groupedict[s]
                else:
                    raise Error
            except:
                return ("Error: Incorrect Instruction ")
            try:
                if s=="hlt":
                    raise Error
            except:
                return "Error: General Syntax Error: incorrect syntax for hlt"
            if s=='var':
                try:
                    if varc==1:
                        raise Error
                    else:
                        xd=str(bin(progl-varindex)[2:])   
                        fs=make7(xd)
                        vardict[r]=fs;                              
                        progl+=1 
                        return None
                except:
                    return "Error: Variable not declared in beginning"
            else:
                try:
                    if s!="jmp":
                        if r in vardict:
                            t+='_'+vardict[r]
                        elif r in vardict.values():
                            t+='_'+r
                        else:
                            raise Error

                        
                    else:
                            if r in vardict:
                                raise Error3
                            elif r in labeldict:
                                t+='_'+labeldict[r]
                            elif r in labeldict.values():
                                t+="_"+r
                            elif checklabel(r,ind,biglist)==-1:
                                raise Error2
                            elif checklabel(r,ind,biglist)!=-1:
                                xd=str(bin(checklabel(r,ind,biglist)+actu-ind)[2:])   
                                fs=make7(xd)
                                labeldict[r]=fs;                              
                                progl+=1
                                t+="_"+labeldict[r]

                    
                except Error2:
                    return ("Error: Incorrect use of label")       
                except Error3:
                    return ("Variable used instead of label")
                except:
                    return ("Error: Variable accessed without declaration")
                
                varc=1
                return t

                                            



    elif len(l)==4:                                                              # group a
        s=l[0]
        if s[-2::-1][::-1] in labeldict:
            lllll=[l[1],l[2],l[3]]
            varc=1
            return opcode(lllll,ind,biglist,actu,varindex)
        else:
            try:
                if s=="var":
                    raise Error
            except:
                return "Error: Invalid variable name"
            
            try:
                if s in groupedict and s!="var":
                    raise Error
            except:
                return "Error: Invalid Label Name"
            
            try:
                if s=="hlt":
                    raise Error
            except:
                return "Error: General Syntax Error: Incorrect syntax for hlt"

            try:

                t=groupadict[s]

                try:
                    for i in l[1:]:
                        t+='_'+regdict[i]
                    

                except:
                    return ("Error: Wrong register accessed")
            
            except:
                return "Error: Incorrect instruction name"
            varc=1
            return t
            
        
        
    elif len(l)==3:
            s=l[0]
            p=l[1]
            r=l[2]
            n=127

            if s[-2::-1][::-1] in labeldict:
                lllll=[l[1],l[2]]
                varc=1
                return opcode(lllll,ind,biglist,actu,varindex)
                
            else:
                try:
                    if s=="var":
                        raise Error
                except:
                    return "Error: Invalid variable name"
                
                try:
                    if s in groupedict and s!="var":
                        raise Error
                except:
                    return "Error: Invalid Label Name"
                
                try:
                    if s=="hlt":
                        raise Error
                except:
                    return "Error: General syntax error: Incorrect syntax for hlt"
            

                if r[0]=="$":                                           # GROUP B
                    try:
                        if s in groupbdict:
                            t=groupbdict[s]
                        elif s not in groupbdict:
                            raise Error
                        else:
                            pass
                    except:
                        return("Error: Incorrect Instruction name")
                    
                    try:
                        if p in regdict and p!='FLAGS':
                            t+='_'+regdict[p]
                        else:
                            raise Error
                    except:
                        return ("Error: Invalid register name")
                    
                    try:
                        if r[1:] not in [f"{i}" for i in range(0,128)]:
                            raise Error5
                        if int(r[1:])<=n:
                            x=bin(int(r[1:]))[2:]
                            if(len(x)<7):
                                mm=7-len(x)
                                mmstr="0"*mm
                                fs=mmstr+x
                            t+='_'+fs

                        else:
        
                            raise Error
                        
    
                        
                    except Error:
                        return (f"Error: Invalid immediate value (more than 7 bits)")
                    except Error5:
                        return (f"Error: Immediate value not whole number")
                    varc=1
                    return t     
                
                else:
                    try:
                        if s in groupcdict or s in groupddict:
                            try:
                                if p in regdict:
                                    try:
                                        if r in regdict:
                                            t=groupcdict[s]+"_"+regdict[p]+"_"+regdict[r]
                                            varc=1
                                            return t
                                        elif r in vardict:
                                            t=groupddict[s]+"_"+regdict[p]+"_"+vardict[r]
                                            varc=1
                                            return t
                                        elif r in vardict.values():
                                            t=groupddict[s]+"_"+regdict[p]+"_"+r
                                            varc=1
                                            return t
                                        elif r[0]=="R" or r[0]=="r":
                                            raise Error
                                        else:
                                            raise Error2
                                    except Error:
                                        return f"Error: Incorrect Register {r}"
                                    except Error2:
                                        return f"Error: Incorrect/undeclared Memory Address or variable {r}"              # refine
                                else:
                                    raise Error
                            except:
                                return f"Error: Incorrect register accessed {p}"
                        else:
                            raise Error
                    except:
                        return "Error: Incorrect instruction type"
    
    elif len(l)>4:
        return "General Syntax Error"

                
f=open("input.txt")
h=open("output.txt","w")

listoflines=f.readlines()
for i in range(len(listoflines)-1):
    if listoflines[i]=="\n":
        del listoflines[i]


varindex=0
progl=len(listoflines)
xy=0
f.close()
erc=0
yz=0
cc=0

for i in range(len(listoflines)):
    x=listoflines[i]
    x=x.strip()
    x.split(" ")
    if x[:3]=="var":
        varindex+=1
    
for i in range(len(listoflines)):
    fina=make7(str(bin(xy)[2:]))
    x=listoflines[i]
    x=x.strip()
    l=x.split(" ")
    
    if opcode(l,i,listoflines,xy,varindex)!=None:
       if opcode(l,i,listoflines,xy,varindex)[:5]=="Error":
           if erc==0:
                h=open("output.txt","w")
                h.write(f"{opcode(l,i,listoflines,xy,varindex)} in line {i+1}\n")
                xy+=1
                erc+=1
                h.close()
           else:
               h=open("output.txt","a")
               h.write(f"{opcode(l,i,listoflines,xy,varindex)} in line {i+1}\n")
               xy+=1
               h.close()     
       else:
            if erc>0:
                continue
            else:
                if cc==0:
                    h.write(f"{opcode(l,i,listoflines,xy,varindex)}\n")
                    xy+=1
                    h.close()
                    cc+=1
                    
                else:
                    h=open("output.txt","a")
                    if opcode(l,i,listoflines,xy,varindex)=="11010_00000000000" and i!=len(listoflines)-1 and erc==0:
                        erc+=1
                        h.close()
                        h=open("output.txt","w")
                        h.write(f"Error: Halt not used as last instruction in line {i+1}\n")
                        h.close()
                        break
                    final=fina+":"+opcode(l,i,listoflines,xy,varindex)
                    h.write(f"{opcode(l,i,listoflines,xy,varindex)}\n")
                    xy+=1
                    h.close()

h.close()  
h=open("output.txt")
r=h.read()
h.close()
if "11010_00000000000" not in r and erc==0:
    h=open("output.txt","w")
    h.write(f"Error: Halt not present in the program\n")
    erc+=1
h.close()

'''if erc>=1:
        h=open("output.txt","w")
        h.write("No Binary generated due to errors encountered")
        h.close()'''
