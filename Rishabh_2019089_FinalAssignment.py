from collections import defaultdict
import math

def f():
    global b
    return [None for i in range(b)]

def printcache(cl,b,cachearr,d):
    print ()
    print("Printing Cache Contents")
    print()
    for i in range(cl):
        print (f"Cache Line {i}", end=" ")
        if cachearr[i]=="":
            print ("is Empty")
        else:
            print (f"has block number {int(cachearr[i],2)}")
            print ("Block Contents - ")
            for j in d[cachearr[i]]:
                if j is None:
                    print ("Main Memory Data", end=", ")
                else:
                    print (j, end=", ")
            print()
    print()

def takequery():
    qtyp=int(input("Enter query code - "))
    while qtyp!=1 and qtyp!=2:
        print ("Invalid Code. Please Chose Valid Code from 1 and 2.")
        qtyp=int(input("Enter query code - "))
    adrs=input("Enter address - ")
    while len(adrs)!=N:
        print ("Invalid address")
        adrs=input("Enter address - ")
    print()
    return qtyp, adrs

def directmapping(csize,cl,b,bb,cb,q,N):
    d=defaultdict(f); cachearr=["" for i in range(cl)]
    for i in range(q):
        q1, adrs=takequery()
        blno=adrs[:N-bb]; wrd=adrs[N-bb:]
        if cachearr[int(blno,2)%cl]==blno:
            print ("Cache Hit")
            print (f"{d[blno]} found at Line {int(blno,2)%cl}")
            if q1==1:
                print (f"Requested word is {d[blno][int(wrd,2)]}")
        else:
            print ("Cache Miss")
            if cachearr[int(blno,2)%cl]!="":
                print (f"Replaced Block No {int(cachearr[int(blno,2)%cl],2)} with current block at line {int(blno,2)%cl}")
            else:
                print (f"Inserted current block at empty line {int(blno,2)%cl}")
            cachearr[int(blno,2)%cl]=blno    
        if q1==2:
            data=int(input("Enter data to be entered at current address in integers - "))
            d[blno][int(wrd,2)]=data
            print ("Data successfully written")
        printcache(cl,b,cachearr,d)
        
       
def fullassociative(csize,cl,b,bb,cb,q,n):
    d=defaultdict(f); cachearr=["" for i in range(cl)]; l=[]
    for i in range(q):
        q1, adrs=takequery()
        blno=adrs[:N-bb]; wrd=adrs[N-bb:]
        if blno in cachearr:
            print ("Cache Hit")
            print (f"{d[blno]} found at Line {cachearr.index(blno)}")
            if q1==1:
                print (f"Requested word is {d[blno][int(wrd,2)]}")
            l.remove(blno) ; l.append(blno)
        else:
            print ("Cache Miss")
            if "" in cachearr:
                ind=cachearr.index("")
                print (f"Inserted current block at empty line {ind}")
                cachearr[ind]=blno; l.append(blno)
            else:
                el=l.pop(0)
                print (f"Replaced Block No {int(el,2)} with current block at line {cachearr.index(el)}")
                cachearr[cachearr.index(el)]=blno; l.append(blno)
        if q1==2:
            data=int(input("Enter data to be entered at current address in integers - "))
            d[blno][int(wrd,2)]=data
            print ("Data successfully written")
        printcache(cl,b,cachearr,d)

def nwaysetassociative(csize,cl,b,bb,cb,q,N,k):
    d=defaultdict(f); sets=cl//k; cachearr=["" for i in range(cl)]; l=[[] for i in range(sets)] #Sets is no of sets, k is set size (no of cache lines)
    for i in range(q):
        q1, adrs=takequery()
        blno=adrs[:N-bb]; wrd=adrs[N-bb:]
        setb=int(blno,2)%sets #Which set the current block belongs to
        if blno in cachearr[k*setb:k*setb+k]:
            print ("Cache Hit")
            print (f"{d[blno]} found at Line {cachearr.index(blno)} in set {setb}")
            if q1==1:
                print (f"Requested word is {d[blno][int(wrd,2)]}")
            l[setb].remove(blno) ; l[setb].append(blno)
        else:
            print ("Cache Miss")
            if "" in cachearr[k*setb:k*setb+k]:
                ind=cachearr[k*setb:k*setb+k].index("")+k*setb
                print (f"Inserted current block at empty line {ind} in set {setb}")
                cachearr[ind]=blno; l[setb].append(blno)
            else:
                el=l[setb].pop(0)
                print (f"Replaced Block No {int(el,2)} with current block at line {cachearr.index(el)} in set {setb}")
                cachearr[cachearr.index(el)]=blno; l[setb].append(blno)
        if q1==2:
            data=int(input("Enter data to be entered at current address in integers - "))
            d[blno][int(wrd,2)]=data
            print ("Data successfully written")
        printcache(cl,b,cachearr,d)


cl=int(input("Enter number of cache lines in integer - "))
b=int(input("Enter block size in integer (power of two) - "))
bb=math.log2(b); cb=math.log2(cl)
while (int(bb)!=bb or int(cb)!=cb):
    print ("Incorrect data. Use only Powers of 2")
    cl=int(input("Enter number of cache lines in integer - "))
    b=int(input("Enter block size in integer (power of two) - "))
    bb=math.log2(b); cb=math.log2(cl)

N=int(input("Enter number of bits in address - "))
assert(N>bb)
bb=int(bb); cb=int(cb)
csize=cl*b
print (f"Cache of size {csize} built")

print ('''The codes for mappings are as follows -
1 - Direct Mapping
2 - Fully Associative Mapping
3 - N-Way Set Associative Mapping''')

typ=-1
while typ not in [1,2,3]:
    typ=int(input("Enter code for the type of mapping - "))
    if typ not in [1,2,3]:
        print ("Invalid Type. Enter valid code.")

q=int(input("Enter the number of queries you want to perform - "))
print ('''The query codes are as follows
1- Read (Give address to read from)
2- Write (Give address and data)''')
if typ==1:
    directmapping(csize,cl,b,bb,cb,q,N)

elif typ==2:
    fullassociative(csize,cl,b,bb,cb,q,N)

elif typ==3:
    k=int(input("Enter the value of N for N-Way Set Associative Mapping - "))
    while k>cl or int(math.log2(k))!=math.log2(k):
        print ("Invalid value. It has to be less than no of cache lines and a power of 2.")
        k=int(input("Enter the value of N for N-Way Set Associative Mapping - "))
    nwaysetassociative(csize,cl,b,bb,cb,q,N,k)
    



