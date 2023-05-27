def float_to_bin(n,c):
    s=str(n)
    if s.count(".")>1:
        #error
        return
    i=s.index(".")
    int_part=s[:i]
    dec_part=s[i+1:]
    int_bin=str(bin(int(int_part))[2:])
    dec_bin=""
    l=dectobin(dec_part,c)
    for i in l:
        dec_bin+=str(i)
    fin_bin=int_bin+"."+dec_bin
    return fin_bin

def make(s,n):
    if len(s)==1 and s=="0":
        return "0"*3
    while s[0]=="0":
        s=s[1:]
    if(len(s)>n):
        return s[:n]
    req=n-len(s)
    s=s+"0"*req
    return s

def makedec(s,n):
    if(len(s)>n):
        return s[:n]
    req=n-len(s)
    s=s+"0"*req
    return s


def dectobin(n,c):
    declist=[]
    s="0."+(n)
    dp=n
    s=float(s)
    i=0

    while(i<c):
        if(int(dp)==0):
            return declist
        s=s*2
        #print("s*2 ",s)
        s=str(s)
        ind=s.index(".")
        ip=int(s[:ind])
        dp=(s[ind+1:])
        #print("ip ",ip)
        declist.append(ip)
        s=float("0."+dp)
        #print("new s ",s)
        i=i+1
        
    return declist

def swap(s,i,j):
    s=list(s)
    temp=s[i]
    s[i]=s[j]
    s[j]=temp
    st=""
    for i in s:
        st+=i
    return st

def convert_to_power_form(n):
    ind=n.index(".")
    ip=n[:ind]
    #print("ip: ",ip)
    dp=n[ind+1:]
    #print("dp: ",dp)
    exp=0
    j=0
    #print("n: ",n)
    if "1" in ip:
        while(True):
            if(int(ip,2)==1 and ip[-1]=="1"):
                break
            else:
                #print("ip:",ip)
                #print("dp:",dp)
                
                n=swap(n,ind,ind-1)
                ind=n.index(".")
                ip=n[:ind]
                dp=n[ind+1:]
                exp+=1
                j+=1
            
    elif "1" not in ip:
        while(True):
            if(int(ip,2)==1 and ip[-1]=="1"):
                break
            else:
                n=swap(n,ind,ind+1)
                ind=n.index(".")
                ip=n[:ind]
                dp=n[ind+1:]
                #print("n: ",n)
                exp-=1
                j+=1
    dp=makedec(dp,5)
    n=make(ip,1)+"."+dp
    l=[make(ip,1),dp,exp]
    return l

def final_conversion(l):
    b=l[1]
    c=l[2]
    exponent=str(bin(c+3)[2:])
    return make(exponent,3)+b



n=float(input())
s=float_to_bin(n,100)
t=convert_to_power_form(s)
m=final_conversion(t)
print(m)









