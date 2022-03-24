import requests
import pandas as pd
import numpy as np

# download the BLOSUM62
# url = 'http://yanglab.nankai.edu.cn/teaching/bioinformatics/BLOSUM62.txt'
# res = requests.get(url)
# with open('./BLOSUM62.txt','w') as f:
#     f.writelines(res.text)

df = pd.read_csv("./BLOSUM62.csv",index_col=0)
def show(arr):
    for line in arr:
        print(line)
def format_show(paint):
    for row in paint:
        for item in row:
            if item == '+':
                print(" +  ",end='')
            else:
                print(" ",end='')
        print('\n')

# NW-DP with affine gap penalty
def NW_Affine(seq1,seq2,opening=-11,extension=-1):
    recordmap = [ [[] for j in range(len(seq1)+1)] for i in range((len(seq2)+1)*3)]
    t_m= [ [-100]*(len(seq1)+1) for i in range(len(seq2)+1)]
    t_x= [ [-100]*(len(seq1)+1) for i in range(len(seq2)+1)]
    t_y= [ [-100]*(len(seq1)+1) for i in range(len(seq2)+1)]

    #init
    t_m[0][0]=0
    for i in range(len(seq2)+1):
        t_x[i][0] = opening + extension * i
        recordmap[i*3][0] = [((i-1)*3,0)]
        recordmap[i*3+1][0] = [((i-1)*3+1,0)]
        recordmap[i*3+2][0] = [((i-1)*3+2,0)]

    for j in range(len(seq1)+1):
        t_y[0][j] = opening + extension * j
        recordmap[0][j] = [(0,j-1)]
        recordmap[1][j] = [(1,j-1)]
        recordmap[2][j] = [(2,j-1)]

    for i in range(1,len(seq2)+1):
        for j in range(1,len(seq1)+1):
            # t_m
            s_ij = df.loc[seq2[i-1]][seq1[j-1]]
            mx_m = max(t_m[i-1][j-1],t_x[i-1][j-1],t_y[i-1][j-1])
            t_m[i][j] = mx_m + s_ij
            if t_m[i-1][j-1] == mx_m:
                recordmap[i*3][j] += [((i-1)*3,j-1)]
            if t_x[i-1][j-1] == mx_m:
                recordmap[i*3][j] += [((i-1)*3+1,j-1)]
            if t_y[i-1][j-1] == mx_m:
                recordmap[i*3][j] += [((i-1)*3+2,j-1)]

            # t_x
            mx_x = max(t_m[i-1][j]+opening,t_x[i-1][j]+extension)
            t_x[i][j] = mx_x
            if t_m[i-1][j]+opening == mx_x:
                recordmap[i*3+1][j] += [((i-1)*3,j)]
            if t_x[i-1][j]+extension == mx_x:
                recordmap[i*3+1][j] += [((i-1)*3+1,j)]
            # t_y
            mx_y = max(t_m[i][j-1]+opening,t_y[i][j-1]+extension)
            t_y[i][j] = mx_y
            if t_m[i][j-1]+opening == mx_y:
                recordmap[i*3+2][j] += [(i*3,j-1)]
            if t_y[i][j-1]+extension == mx_y:
                recordmap[i*3+2][j] += [(i*3+2,j-1)]
    # # draw backline in recordmap
    # paint = [[[] for j in range(len(seq1)+1)] for i in range((len(seq2)+1)*3)]
    res,rc = [],[]
    mx = max(t_m[len(seq2)][len(seq1)],t_x[len(seq2)][len(seq1)],t_y[len(seq2)][len(seq1)])
    def trace(path,lst):
        # item in a pair (12,6)
        for item in lst:
            if (np.array(item)<0).any():
                path.append(item)
                res.append(list(path))
                path.pop()
                return
            path.append(item)
            # if item
            trace(path,recordmap[item[0]][item[1]])
            path.pop()
    i,j = len(seq2),len(seq1)
    if t_m[i][j] == mx:
        trace([(i*3,j)],recordmap[i*3][j])
    if t_x[i][j] == mx:
        trace([(i*3+1,j)],recordmap[i*3+1][j])
    if t_y[i][j] == mx:
        trace([(i*3+2,j)],recordmap[i*3+2][j])
    show(res)
    def gen(l):
        reseq1,reseq2 = list(seq1),list(seq2)
        r1,r2=[],[]
        index = 0
        while index<len(l):
            if int(l[index][0]/3)>0 or int(l[index][1])>0:
                if int(l[index][0]/3)==int(l[index+1][0]/3) and int(l[index][1])>int(l[index+1][1]):
                    r1.append(reseq1.pop())
                    r2.append('-')
                elif int(l[index][0]/3)>int(l[index+1][0]/3) and int(l[index][1])==int(l[index+1][1]):
                    r1.append('-')
                    r2.append(reseq2.pop())
                elif int(l[index][0]/3)>int(l[index+1][0]/3) and int(l[index][1])>int(l[index+1][1]):
                    r1.append(reseq1.pop())
                    r2.append(reseq2.pop())
                else:
                    print("erro")
            index += 1
        list.reverse(r1)
        list.reverse(r2)
        r1 = "".join(r1)
        r2 = "".join(r2)
        print(r1)
        print(r2)
        print("\t")
    for line in res:
        gen(line)

    
    

s1 = 'MPSRVEDYEVLHSIGTGSYGRCQKIRRKSDGKILVWKELDYGSMTEVEKQMLVSEVNLLRELKHPNIVRYYDRIIDRTNTTLYIVMEYCEGGDLASVITKGTKDRQYLEEEFVLRVMTQLTLALKECHRRSDGGHTVLHRDLKPANVFLDSKHNVKLGDFGLARILNHDTSFAKTFVGTPYYMSPEQISRLSYNEKSDIWSLGCLLYELCALMPPFTAFNQKELAGKIREGRFRRIPYRYSDGLNDLITRMLNLKDYHRPSVEEILESPLIADLVAEEQRRNLERRGRRSGEPSKLQDSSPVLSELKLKERQLQDRERALRAREDSLEQKERELCIRERLAEDKLARAESLLKNYSLLKEHRLLCLAGGSELDLPSSALKKKVHFHGESKENTTRSENSESQLAKSKCRDLKKRLHAAQLRAQALSDIEKNYQLKSRQILGMR'
s2 = 'MPSRVEDYEVLHSIGTGSYGRCRKIRRKSDGKILVWKELDYGSMTEVEKQMLVSEVNLLRELKHPNIVRYYDXIIDRTNTTLYIVMEXCEGGDLASVITKGTKERQYLEEEFVLRVMTQLTLALKECHRRSDGGHTVLHRDLKPANVFLDSKHNVKLGDFGLARILKTMTQEQMSRLSYNEKSDIWSLGCLLYELCALMPPFTAFNQKELAGKIREGRFRRIPYRYSDGLNDIITRMLNLKDYHRPSVEEILESPLIADLVEEEQRRHLERRGQRLGEPSKLQASSPVXSELKLKEKQLQDRERALRAREDSLEQKERELCIRERLAEDKLARAESLVKNYSLLKEQRFLCXASGPELDLPSSVMRKKVHFRGESRENATRSENSEIQLAKSKCKDLKKRLHAAQLRAQALSDIEKTYQLKSKQILGMR'
NW_Affine(s1,s2)

