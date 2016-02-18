#@author SRI HARSHA GANJA
#ganjash

import csv
import pdb
import math
import sys
import pydot
import random

def cal_Entropy(a,b):
    a = float(a)
    b = float(b)
    if a==0 and b==0:
        return -1
    pa = a/(a+b)
    pb = b/(a+b)
    if pa == 0:
        E = -pb*math.log(pb,2)
        return E
    elif pb == 0:
        E = -pa*math.log(pa,2)
        return E

    E = -pa*math.log(pa,2) -pb*math.log(pb,2)
    return E

def best_InfoGain(X_list):
    len_X = len(X_list)
    len_Attr = len(X_list[0]) - 1
    parent1_sum = 0
    parent_Eh =  child1_Eh = child0_Eh = 0.0
    child1_sum = child0_sum = 0
    infogain = 0.0
    temp = [[0,0],[0,0]]
    max_info = 0.0
    mark_attr = 0
    brk = 0
    
    for i in range(len_X):
        if X_list[i][len_Attr]:
            parent1_sum +=1
    parent_Eh = cal_Entropy(parent1_sum,len_X - parent1_sum)
    #print 'PARENT   ENTROPY ',parent_Eh
    #print '****',len_Attr,'******'
    for j in range(len_Attr):
        brk=0
        temp = [[0,0],[0,0]]
        for i in range(len_X):
            if X_list[i][j]:
                if X_list[i][len_Attr]:
                    temp[1][1] +=1
                else:
                    temp[1][0] +=1
            else:
                if X_list[i][len_Attr]:
                    temp[0][1] +=1
                else:
                    temp[0][0] +=1
        child1_Eh = cal_Entropy(temp[1][1],temp[1][0])
        child0_Eh = cal_Entropy(temp[0][1],temp[0][0])
        if child0_Eh == -1 or child1_Eh == - 1 :
    #        print 'BAD ATTRIBUTE'
            continue
    #    print 'child1 ENTROPY : ',child1_Eh
    #    print 'child2 ENTROPY : ',child0_Eh
        child1_sum = temp[1][0] + temp[1][1]
        child0_sum = temp[0][0] + temp[0][1]
    #    print 'child1_sum : ',child1_sum,
    #    print 'child0_sum : ',child0_sum
        infogain  = parent_Eh - (  (float(child1_sum)/len_X)*child1_Eh  + (float(child0_sum)/len_X)*child0_Eh  )
    #    print 'INFORMATION GAIN ',infogain,'\n'
        if max_info < infogain:
            max_info = infogain
            mark_attr = j
    #print 'best split attribute index : ',mark_attr,' info gain : ',max_info

    return mark_attr

def traverse(tt, graph=None, z=None):
        if(tt == None): return
        if tt.L is not None:
            pass#print tt.L
            if z is not None:
                if len(z)==2:
                    if tt.L:
                        z[1] += 1
                    else:
                        z[0] += 1
        else:    
            pass#print tt.Attr
            if z is not None :
                if len(z)==2:
                    pass               
                elif z[0] >=0:                            # z >=0  => label each node with number 
                     z[0]+= 1
                     tt.X = z[0]
                elif z[0]<0 and len(z)==1:  
                    if  -z[0] == tt.X :             # z < 0  => find prune node
                         z.append(tt)
                         z.append(0)
        if tt.left0 is not None and graph != None:
                if tt.left0.Attr is not None:
                    edge = pydot.Edge(tt.Attr+'('+tt.inc+')',tt.left0.Attr+'('+tt.left0.inc+')')
                    graph.add_edge(edge)
                else:
                    edge = pydot.Edge(tt.Attr+'('+tt.inc+')',str(tt.left0.L)+'('+tt.left0.inc+')')
                    graph.add_edge(edge)
        
        traverse(tt.left0,graph,z)
        if tt.right1 is not None and graph != None:
                if tt.right1.Attr is not None:
                    edge = pydot.Edge(tt.Attr+'('+tt.inc+')',tt.right1.Attr+'('+tt.right1.inc+')')
                    graph.add_edge(edge)
                else:
                    edge = pydot.Edge(tt.Attr+'('+tt.inc+')',str(tt.right1.L)+'('+tt.right1.inc+')')
                    graph.add_edge(edge)    
        traverse(tt.right1,graph,z)         

class Node:
    
    def __init__(self, X , Attr_list ,inc,L = None ):
        #pdb.set_trace()
     #   print '#######'
     #   print len(X)
     #   print len(Attr_list)
     #   print '#######'
        self.inc = inc
        self.X = X
        self.Attr_list = Attr_list
        self.L = L
        if L != None or X == []:
            ##pdb.set_trace()
            self.Attr_list = None
            self.Attr=None
            self.left0 = None
            self.right1=None
            self.X=None
            return
        self.left0 = None
        self.right1 = None
        len_Attr = len(self.Attr_list) - 1
        c0 , c1 = self.count01(X)
        if len_Attr == 0:        # Attribute list empty
            if c0 > c1: self.L = 0        # max vote of Target attribute
            else:   self.L = 1
            self.Attr=None
            self.Attr_list = []
            ##pdb.set_trace()
            return     
        len_X = len(self.X)    
        if c1 == len_X :
            ##pdb.set_trace()
            self.L = 1        # Label 1 reutrned (pure 1 set)
            self.Attr=None
            self.Attr_list=[]
            ##pdb.set_trace()
            return
        elif c0 == len_X :
            ##pdb.set_trace()
            self.L = 0        # Label 0 returned (pure 0 set)
            self.Attr=None
            self.Attr_list=[]
            ###pdb.set_trace()
            return
        Attr_indx = best_InfoGain( self.X )
        len_Attr = len(X[0])  - 1
        ##pdb.set_trace()
     #   print '********'
     #   print Attr_list
     #   print Attr_indx
     #   print '********'
        self.Attr = self.Attr_list[Attr_indx]
        #self.Attr_indx = Attr_indx
        c0 = c1 = 0
        j = Attr_indx
        #X0 = list(self.X)
        #X1 = list(self.X)
        X0=[]
        X1=[]
        y = self.X.__iter__()
        for i in range(len(self.X)):
            X0.append(list(y.next()))
        y = self.X.__iter__()
        for i in range(len(self.X)):
            X1.append(list(y.next()))
         
        dec_X = self.X[0][len_Attr]   # only 1 example is present , Target val
        dec_X0 = None
        dec_X1 = None
        for i in range(len_X):   
            if X[i][j]:
                del(X0[c0])           # removing covered examples
                c1 += 1
            else:
                del(X1[c1])
                c0 += 1
        #pdb.set_trace()
        if X0 == []: X0=[]
        elif len(X0[0])-1 == 1:         # only 1 Attribute is present 
            c0,c1 = self.count01(X0)
            if c0 > c1:dec_X0=0
            else :   dec_X0=1
              # max target attribute value
        if  X1 == []: X1 = []
        elif   len(X1[0])-1 == 1:       # only 1 Attribute is present 
               c0,c1 = self.count01(X1)       # max target attribute value
               if c0 > c1: dec_X1=0
               else:   dec_X1=1
            
        Attr_list = self.Attr_list
        Attr_list.remove(self.Attr)
        len_X0 = len(X0)                  
        len_X1 = len(X1)
        for i in range(len_X0):       # Removing covered Attribute
            del X0[i][j]
        for i in range(len_X1):
            del X1[i][j]
        #pdb.set_trace()
        
        if X0 == []: X0=[]
        elif    len(X0[0]) == 1: X0=[]
        
        if X1 == []: X1=[]
        elif    len(X1[0]) == 1: X1=[]
        
        if len(X0)==0 or len(X1)==0:  # case when no more examples are present or no more Attributes
            if dec_X0 is not None or dec_X1 is not None:
                if dec_X1 == None:
                    dec_X1 = 1
                if dec_X0 == None:
                    dec_X0 = 0
                self.left0 = Node([],[],self.inc+'-',dec_X0)
                self.right1 = Node([],[],self.inc+'+',dec_X1)
                return
                ##pdb.set_trace()
            else:
                if len(X0)==0:           # only 1 example before,now 0 example # no data for attribute
                    self.left0 = Node([],[],self.inc+'-',0)                 # random val -> 0
                    self.right1 = Node([],[],self.inc+'+',dec_X)
                    ###pdb.set_trace()
                    return
                if len(X1)==0:
                    self.left0 = Node([],[],self.inc+'-',dec_X) # no data for attribute, random val -> 1
                    self.right1 = Node([],[],self.inc+'+',1)
                    ###pdb.set_trace()
                    return

        
     #   print '$$$$$$$$$$$$$$$$$$$$$ DIVIDING LEFT $$$$$$$$$$$$$$$$'
        self.left0 = Node(X0,list(Attr_list),self.inc+'-')
     #   print '$$$$$$$$$$$$$$$$$$$$$ DIVIDING RIGHT $$$$$$$$$$$$$$$$'
        self.right1 = Node(X1,list(Attr_list),self.inc+'+')

        

    def count01(self, X ):
        if len(X[0]) == 1:
            len_Attr = 1           # not Attr length, it is the Target attribute
        else:
            len_Attr = len(X[0]) - 1 # this is Attr length
        len_X = len(X)
        c0 = 0
        c1 = 0
        for i in range(len_X):
            if X[i][len_Attr]: c1 += 1
            else:   c0 += 1
        return c0,c1

    #validation
def accuracy(Root,set):
    ######
    f1 = open(set,'rt')           #on test set       75.85% accurate
    has_header = csv.Sniffer().has_header(f1.read(1024))      #on validation set 75.9% accurate
    f1.seek(0)
    in_csv = csv.reader(f1)
    ##pdb.set_trace()
    if has_header:
        Attr_names = next(in_csv)
    #Attr_names.pop()
    X = [map(int , i) for i in in_csv]
    X.insert(0,Attr_names)
    f1.close()

    mov= Root
    corr = 0
    res=0
    dec = 0
    len_Attr = len(X[0])
    for i in range(1,len(X)):
        mov = Root
        res = 0
        dec=0
        while(mov.Attr is not None):
            res=X[i][X[0].index(mov.Attr)]
            #print res
            #pdb.set_trace()
            if res == 0:
                mov = mov.left0
            else:
                mov = mov.right1
        if  mov.L ==  X[i][len_Attr-1]:     #comparison with decision
            corr += 1
    prec = float(corr)/(len(X)-1)
    #print 'Precision of decision tree : ',prec
    return prec

class copyNode(Node):
    def __init__(self,tt):
        if(tt == None): return None
        if tt.L is not None:
            self.Attr=tt.Attr
            self.X = None
            #self.Attr_list =  list(tt.Attr_list)
            self.L = tt.L
            self.inc = tt.inc

        else:    #adf
            self.Attr=tt.Attr
            self.X = None
            self.Attr_list =  list(tt.Attr_list)
            self.L = tt.L
            self.inc = tt.inc

            
        if tt.left0 is not None:
            self.left0 = copyNode(tt.left0)
        else:
            self.left0 = None
            
        if tt.right1 is not None:
            self.right1 = copyNode(tt.right1)
        else:
            self.right1 = None
def prune_node(Rbest_temp,choose):
    n = [-choose]                           # -choose , minus signifies to find the specified node
    traverse(Rbest_temp, None, n)
    pnode = n[1]
    #pdb.set_trace()
    count =[0,0]                                 # count  index 0 => count of 0 , index 1 => count of 1
    traverse(pnode,None,count)       
    pnode.Attr = None
    ll = pnode.left0
    pnode.left0 = None
    del(ll)
    ll = pnode.right1
    pnode.right1=None
    del(ll)
    if count[0]>count[1]:
        pnode.L = 0
    elif count[1]>count[0]:
        pnode.L = 1
    else :
        if pnode.inc.count('+') > pnode.inc.count('-'):
            pnode.L = 1
        else :pnode.L = 0
    return pnode.inc


def postPrune(Root , L , K , ref_set):
    path=[]
    ii = 0
    Rbest = Root
    R_accr = 0.0
    Rtemp_accr = 0.0
    for i in xrange(1,L+1):
        Rbest_temp = copyNode(Rbest)
        M = random.randint(1,K)
        for j in xrange(1,M+1):
            Rcount = [0]
            traverse(Rbest_temp,None,Rcount)        # New Rcount is  produced at this stage
            #print "no. of nodes",Rcount[0]
            if Rcount[0]== 0: break;
            if Rcount[0] == 0: pdb.set_trace()
            choose = random.randint(1,Rcount[0])
            #print "choose", choose
            path.append(prune_node(Rbest_temp,choose))           # Node pruned after this stage
        R_accr = accuracy(Rbest,ref_set)
        Rtemp_accr = accuracy(Rbest_temp,ref_set)
        #print "#####  Accuracy Rbest  Rbest_temp    ",R_accr,Rtemp_accr
        #pdb.set_trace()
        if Rtemp_accr > R_accr:
            temp = Rbest
            Rbest = Rbest_temp
            R_accr = Rtemp_accr
            ii = len(path)
        else:
            temp = Rbest_temp
        path = path[0:ii]
        if temp != None:
            del(temp)
    #pdb.set_trace()
    Rcount=[0]
    traverse(Rbest,None, Rcount)
    print "No.of nodes in Rbest :",Rcount[0]
    return Rbest,path,R_accr

            
L ,K,train_set,valid_set,test_set,to_print = sys.argv[1:]    
L = int(L)
K = int(K)
f1 = open(train_set,'rt')
has_header = csv.Sniffer().has_header(f1.read(1024))
f1.seek(0)
in_csv = csv.reader(f1)
##pdb.set_trace()
if has_header:
    Attr_names = next(in_csv)
#Attr_names.pop()
X = [map(int , i) for i in in_csv]
inc= '0'
Root = Node( X , Attr_names , inc)

#pdb.set_trace()
f1.close()
# validation
Rcount = [0]
traverse(Root, None, Rcount)
Rfinal,path,Rfinal_accr = postPrune(Root, L, K , valid_set)
print "No.of nodes in Root :",Rcount[0]
print "Accuracy of original tree :",accuracy(Root, test_set)
print "Accuracy of pruned tree   :",accuracy(Rfinal, test_set)
print "pruned nodes , path or ID :",path
if to_print=="yes" or to_print=='YES':
    graph1 = pydot.Dot(graph_type = 'graph')
    traverse(Root,graph1)
    graph1.write_jpg('tree.jpg')
    graph2 = pydot.Dot(graph_type = 'graph')
    traverse(Rfinal, graph2)
    graph2.write_jpg('prune_tree.jpg')
    
 

    

