import json
import pdb
import csv
import random
import math
import sys
#def func_dist(x1,x2):
def ssd(X,k_pt):
    dist = 0
    temp = 0
    for j in k_pt:
        for i in X:
            if( X[j][1] != j): continue
            temp =   1 - float(len((X[i][0]).intersection(X[j][0])))/len((X[i][0]).union(X[j][0]))
            dist += math.pow(temp, 2)
    print 'ssd: ',dist,' k = ',len(k_pt)
            

def ssd_cluster(X):
    temp = 0
    for i in X:
        temp += math.pow(i, 2)
    return temp
    
    
#pdb.set_trace()
#f1 = open('Tweets.json','rt')
#X = json.load(f1)
k,initial,inp,out = sys.argv[1:]
#pdb.set_trace()
#k = 4
#initial = 'InitialSeeds.txt'
#inp = 'Tweets.json'
#out = 'hello.txt'
k = int(k)
f1 = open(out,'w')
temporary = sys.stdout
sys.stdout = f1
#pdb.set_trace()
f2 = open(inp)    
#f2 = open('Tweets.json')
X = {}
stopwords = ["a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
stopwords = set(stopwords)
x = f2.readline()
i = 0
while(x!=''):
    #X.append(json.loads(x))
    XX = json.loads(x)
    #X[i]['text']=set((X[i]['text']).split(' ')).difference(stopwords)
    XX['text']=set((XX['text']).split(' ')).difference(stopwords)
    X.update({XX['id']:[XX['text'],-1]})
    x = f2.readline()
    #i += 1
#spdb.set_trace()

f1 = open(initial,'rt')
has_header = csv.Sniffer().has_header(f1.read(1024))
f1.seek(0)
in_csv = csv.reader(f1)
if has_header:
    Attr_names = next(in_csv)
K = [int(i[0]) for i in in_csv]
# selecting random k centroids
temp = random.sample(K,k)
k_pt = {}
len_k_pt = len(temp)
for i in temp:
    k_pt.update({i:X[i]})
#print 'Debug point 1'
#pdb.set_trace()



len_X = len(X)
f2.close()
f1.close()
################################## STABLE ####################################
dist = {}
centre = []
iter = 0
diff = []
old = []

for i in xrange(k):
    diff.append([-1])
#pdb.set_trace()
print 'Iterations : ',
while(iter < 25 and any( h != 0 for h in diff)):
    print iter,
    #print diff
    old = []
    temp = X.iterkeys()
    for j in xrange(len_X):
        old.append(temp.next())
    #pdb.set_trace()
    # selecting elements into cluster
    #for i in xrange(len_X):
    for i in X:
        #put each element into nearest centroid cluster.
        dist = 1
        min_dist = 2
        assign_id = 0
        for k_iter in k_pt:
            #dist.append(math.sqrt(math.pow(k_pt[k_iter][1]-X[i][1],2) + math.pow(k_pt[k_iter][2]-X[i][2],2)))
            #dist.update({k_iter: 1 - float(len((X[i]).intersection(k_pt[k_iter])))/len((X[i]).union(k_pt[k_iter]))})
            dist = 1 - float(len((X[i][0]).intersection(k_pt[k_iter][0])))/len((X[i][0]).union(k_pt[k_iter][0]))
            if(dist < min_dist):
                min_dist = dist
                assign_id = k_iter
        X[i][1]=assign_id
    #pdb.set_trace()
    ##################################################### STABLE #############################    
    #selecting centroid of cluster
    #temp = range(len_X)
    k_pt_temp = {}
    for k_iter in k_pt:
        dist = 1
        min_ssd = 999999999
        assign_id = 0
        
        for i in X:
            if(X[i][1] != k_iter): continue
            temp_set = []
            for j in X:
                if( X[j][1] != k_iter): continue
                if( i == j): continue
                temp_set.append(  1 - float(len((X[i][0]).intersection(X[j][0])))/len((X[i][0]).union(X[j][0])))
            dist = ssd_cluster(temp_set)
            if(dist < min_ssd):
                #pdb.set_trace()
                min_ssd = dist
                assign_id = i
        #pdb.set_trace()
        #print assign_id,':',min_ssd
        k_pt_temp.update({assign_id : X[assign_id]})
        
    k_pt_len = len(k_pt)
    k_pt_temp_ptr = k_pt_temp.__iter__() 
    diff = []
    for j in k_pt:
        diff.append(j - k_pt_temp_ptr.next())
    k_pt = k_pt_temp
    iter += 1
    

print "\n"
#print ssd(X,k_pt)
for i in k_pt:
    print 'Cluster ID: ',i
    print 'text :',k_pt[i][0]
    print 'Points : ',
    for j in X:
        if(i==X[j][1]):
            print j,',',
    print '\n\n'
ssd(X, k_pt)
sys.stdout = temporary
f1.close()
print 'out printed in file:', out                
            
        

