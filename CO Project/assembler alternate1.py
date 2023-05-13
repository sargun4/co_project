
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
    

def opcode(l,ind,biglist,actu):
    global progl

    try:
        counthlt=0
        for i in biglist:
            if "hlt " in i:
                counthlt+=1
                break
        if counthlt==0:
            raise Error
    except:
        return "Error: No Hlt instruction present"
            

    if len(l)==1:
        s=l[0]
        try:
            if s=="hlt":
                return "11010_00000000000"
                
            else:
                raise Error
        except:
            return ("Error: Wrong")
            
           
           
        

    if len(l)==2:                                                                # group e
        s=l[0]
        r=l[1]
        if s[-2::-1][::-1] in labeldict:
            lllll=[r]
            return opcode(lllll,ind,biglist,actu)
        else:

            try:
                if s in groupedict:
                    if s!='var':
                        t=groupedict[s]
                else:
                    raise Error
            except:
                return ("Error: Incorrect Instruction name")
            if s=='var':
                xd=str(bin(progl+1)[2:])   
                fs=make7(xd)
                vardict[r]=fs;                              
                progl+=1    
                return None
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
                

                return t

                                            



    elif len(l)==4:                                                              # group a
        s=l[0]
        if s[-2::-1][::-1] in labeldict:
            lllll=[l[1],l[2],l[3]]
            return opcode(lllll,ind,biglist,actu)
        else:

            try:

                t=groupadict[s]

                try:
                    for i in l[1:]:
                        t+='_'+regdict[i]
                    

                except:
                    return ("Error: Wrong register accessed")
            
            except:
                return "Error: Incorrect instruction name"
            
            return t
            
        
        
    elif len(l)==3:
            s=l[0]
            p=l[1]
            r=l[2]
            n=127

            if s[-2::-1][::-1] in labeldict:
                lllll=[l[1],l[2]]
                return opcode(lllll,ind,biglist,actu)
                
            else:
            

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
                    
                    return t     
                
                else:
                    try:
                        if s in groupcdict or s in groupddict:
                            try:
                                if p in regdict:
                                    try:
                                        if r in regdict:
                                            t=groupcdict[s]+"_"+regdict[p]+"_"+regdict[r]
                                            return t
                                        elif r in vardict:
                                            t=groupddict[s]+"_"+regdict[p]+"_"+vardict[r]
                                            return t
                                        elif r in vardict.values():
                                            t=groupddict[s]+"_"+regdict[p]+"_"+r
                                            return t
                                        elif r[0]=="R" or r[0]=="r":
                                            raise Error
                                        else:
                                            raise Error2
                                    except Error:
                                        return f"Error: Incorrect Register {r}"
                                    except Error2:
                                        return "Error: Incorrect Memory Address or variable"              # refine
                                else:
                                    raise Error
                            except:
                                return "Error: Incorrect register accessed"
                        else:
                            raise Error
                    except:
                        return "Error: Incorrect instruction type"

                
f=open("assembly code.txt")
listoflines=f.readlines()
progl=len(listoflines)
xy=0
f.close()
erc=1
g=open("errors.txt","w")
for i in range(len(listoflines)):
    fina=make7(str(bin(xy)[2:]))
    x=listoflines[i]
    x=x.strip()
    l=x.split(" ")
    if opcode(l,i,listoflines,xy)!=None:
       final=fina+":"+opcode(l,i,listoflines,xy)
       print(final)
       xy+=1



#print(vardict)
#print(labeldict)
'''x="hlt_label: hlt"
l=x.split(" ")
ll=['hlt']
print(opcode(ll,0,0,3))'''




    

