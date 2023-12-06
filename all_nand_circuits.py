from itertools import product
import sys

# 出力は分岐する可能性があるが、入力は一つに定まっている必要がある
# よって入力に入るものの選び方を考える
# 変数：nand入力 2n
# 候補：input 0,1  nand出力 i+2 (0<=i<n)


# 個数と期待する機能
n = 4
target = [0,1,1,0] # XOR


def enumerate_combinations(n):
    # 0からn+1までの値を持つリストを生成
    values = list(range(n + 2))
    
    # 各要素の組み合わせを列挙
    combinations = product(values, repeat=2*n)
    
    for combination in combinations:
        flag = True
        for i in range(n):
            # 自分より番号の大きいNANDから線を持ってこない、NANDの対称性から候補を減らせる
            if combination[2*i] >= i+2 or combination[2*i+1] >= i+2 or combination[2*i] > combination[2*i+1]:
                flag = False
                break
        if flag:
            # print(combination)
            yield combination


def print_circuit(lst,n):
    for i in range(n):
        if lst[2*i] == 0 or lst[2*i] == 1:
            print(f'nand_{i}_input_A: input{lst[2*i]}')
        else:
            print(f'nand_{i}_input_A: nand_{lst[2*i]-2}_output')
        if lst[2*i+1] == 0 or lst[2*i+1] == 1:
            print(f'nand_{i}_input_B: input{lst[2*i+1]}')
        else:
            print(f'nand_{i}_input_B: nand_{lst[2*i+1]-2}_output')
        
    print('****************************************')

def NAND(x,y):
    if x==-100 or y==-100:
        print('error')
        sys.exit()
    # NAND実装
    if x==0 or y==0:
        return 1
    elif x==1 and y==1:
        return 0
        
def circuit(a,b,gen):
    nand_output = [-100]*(n+2)
    nand_input = [-100]*(2*n)
    
    nand_output[0] = a  # 回路全体の入力
    nand_output[1] = b
    
    for i in range(n):
        nand_input[2*i] = nand_output[gen[2*i]]
        nand_input[2*i+1] = nand_output[gen[2*i+1]]
        nand_output[i+2] = NAND(nand_input[2*i], nand_input[2*i+1])
        
    return nand_output[n+1]

for gen in enumerate_combinations(n):
    ans = []
    for a in [0,1]:
        for b in [0,1]:
            tmp = circuit(a,b,gen)
            ans.append(tmp)
    if ans == target:
        print_circuit(gen,n)

    
# OR,3 には別解があることが確認できた
# outputは最後以外考えなくてよい　最後以外を使うとそれ以降のNANDが不要になるため
# 40s -> 10s