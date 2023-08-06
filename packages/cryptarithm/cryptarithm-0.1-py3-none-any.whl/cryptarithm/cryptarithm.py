import random

class Box:
    #空欄を表すオブジェクト
    def __init__(self, v=None, editable=False):
        if v is None:
            self.id = id(self)
            self.type = 0 #被りOK, #または*
        else:
            self.id = v
            self.type = 1 #被りだめ, #または*
        self.editable = editable

    def set_id(self, id):
        self.id = id
        self.type = 2 #被りだめ, #または* (隠し条件あり)

    def __eq__(self, other):
        if not isinstance(other, Box):
            return False
        return self.id == other.id
        
    
    def __hash__(self):
        return hash(self.id)
    
class Column:
    #空欄を含む何桁かの数字を表すオブジェクト
    @classmethod
    def str2column(cls, string):
        column = []
        for c in string:
            if c in "0123456789":
                column.append(int(c))
            elif c == "*":
                column.append(Box(editable=False))
            elif c == "#":
                column.append(Box(editable=True))
            else:
                column.append(Box(c))

        column.reverse()
        return cls(column)
    
    @classmethod
    def int2column(cls, value, n=None):
        if n is None:
            n = len(str(value))

        column = []
        for _ in range(n):
            column.append(value%10)
            value = value // 10
        
        return cls(column)
    
    def __init__(self, digits, boxmap=None, defined=None, boxvalues=None):
        self.digits = digits #各位の値．intとBoxが混在．下の位から格納されている
        self.boxmap = boxmap #各boxの位置
        self.defined = defined
        self.boxvalues = boxvalues
        if boxmap is None:
            self.boxvalues = {}
            self.setup()
            self.update()
            

    def update(self):
        #更新の度に実行
        self.defined = 0
        while self.defined < len(self.digits) and not isinstance(self.digits[self.defined], Box):
            self.defined += 1

    def setup(self):
        #初期化
        self.boxmap = {}
        for i, d in enumerate(self.digits):
            if isinstance(d, Box):
                if d not in self.boxmap:
                    self.boxmap[d] = [i]
                else:
                    self.boxmap[d].append(i)

    def copy(self):
        #コピー
        return Column(self.digits.copy(), boxmap=self.boxmap, defined=self.defined, boxvalues=self.boxvalues.copy())
    
    def assump(self, box, value):
        #boxの値を仮定する
        if box not in self.boxmap:
            return
        for index in self.boxmap[box]:
            self.digits[index] = value

        self.boxvalues[box] = value
        self.update()

    def discard(self, box):
        #boxの値を消す．assumpの逆
        if box not in self.boxmap:
            return
        
        for index in self.boxmap[box]:
            self.digits[index] = box
        
        del self.boxvalues[box]
        self.update()
    
    def part_int(self):
        #末尾の確定部分(数字のみからなる最大の位まで)をintにする
        x = 0
        for i in range(self.defined):
            x += self.digits[i] * 10**i
        
        return x
    
    def part_plus(self, other):
        if isinstance(other, Column):
            return Column.int2column(self.part_int() + other.part_int(), min(self.defined,other.defined))
        else:
            raise ValueError()
        
    def full_plus(self, other):
        return Column.int2column(self.part_int() + other.part_int())

        
    
    def part_minus(self, other):
        if isinstance(other, Column):
            x = self.part_int() - other.part_int()
            if x < 0:
                return None
            return Column.int2column(x)
        else:
            raise ValueError()
        
    def full_minus(self, other):
        x = self.part_int() - other.part_int()
        if x>=0:
            return Column.int2column()
    
    def part_multiply(self, other):
        #otherを掛け算して末尾の確定部分をColumn型で出力
        if isinstance(other, Column):
            return Column.int2column(self.part_int() * other.part_int(), min(self.defined,other.defined))
        else:
            return Column.int2column(self.part_int() * other, min(self.defined, 1))
        
    
    def part_match(self, other):
        #otherとの末尾が一致しうるかどうか
        assumptions = {}
        for a, b in zip(self.digits,other.digits):
            if not (isinstance(a,Box) or isinstance(b,Box) or a == b):
                return False
            if isinstance(a,Box):
                if a in assumptions and assumptions[a] == b:
                    return False
                assumptions[a] = b

            if isinstance(b,Box):
                if b in assumptions and assumptions[b] == a:
                    return False
                assumptions[b] = a

            
        return True
            
    def part_set(self, other, assumption=lambda x: True):
        #self.part_match(other) == Trueのとき自身の値の末尾をotherに決定する．
        if not self.part_match(other) or len(other.digits) > len(self.digits):
            return False
        
        for i, digit in enumerate(other.digits):
            if isinstance(self.digits[i], Box):
                if not assumption(self.digits[i], digit):
                    return False
                self.assump(self.digits[i], digit)
            
            self.digits[i] = digit
            
            
        self.update()

        return True
    
    def int(self):
        #すべての位が確定している場合にintにする
        if self.defined != len(self.digits):
            raise ValueError()
        return self.part_int()
    
    def str(self):
        #strにする
        return ''.join([
            (c.id if c.type == 1 else ("#" if c.editable else "*")) if isinstance(c,Box) else str(c) for c in reversed(self.digits)
        ])

    
    def full_multiply(self, other):
        #すべての位が確定している場合にotherと掛け算してcolumn型で出力
        if isinstance(other, Column):
            x = self.int() * other.int()
            
        else:
            x = self.int() * other
        return Column.int2column(x, len(str(x)))
        
    
    def full_match(self, other):
        #桁数を含めotherと一致しうるかどうか
        if len(self.digits) != len(other.digits):
            return False
        
        assumptions = {}
        for a, b in zip(self.digits, other.digits):
            if not (isinstance(a,Box) or isinstance(b,Box) or a == b):
                return False
            
            if isinstance(a,Box):
                if a in assumptions and assumptions[a] != b:
                    return False
                assumptions[a] = b

            if isinstance(b,Box):
                if b in assumptions and assumptions[b] != a:
                    return False
                assumptions[b] = a

            
        return True
    
    def shift(self, n=1):
        return Column(self.digits.copy()[n:], boxmap=self.boxmap, defined=self.defined-n, boxvalues=self.boxvalues.copy())
    
    def full_set(self, other, assumption=lambda x: True):
        #self.full_match(other)==Trueのとき，自身の値をotherに決定する
        if not self.full_match(other) or len(other.digits) != len(self.digits):
            return False
        
        for i, digit in enumerate(other.digits):
            if isinstance(self.digits[i], Box):
                if not assumption(self.digits[i], digit):
                    return False
                self.assump(self.digits[i], digit)
                

            self.digits[i] = digit
        
        self.update()

        return True

    
    def uncomplete(self):
        #未完成かどうか
        return self.defined != len(self.digits)
    

class Division:
    @classmethod
    def string2division(cls, string):
        first, second = string.replace(" ", "").replace("-", "").replace("|", ")").split(")")
        first = first.split("\n")
        second = second.split("\n")
        while "" in first: first.remove("") 
        while "" in second: second.remove("") 
        top, left = first
        ups = second[-1::-2]
        bottoms = second[-2::-2]
        return cls(Column.str2column(top), Column.str2column(left), [Column.str2column(up) for up in ups], [Column.str2column(btm) for btm in bottoms])


    def __init__(self, top, left, ups, bottoms, assumptions={}):
        self.top = top
        self.left = left
        self.bottoms = bottoms #下から順なので注意
        self.ups = ups
        self.columns = [self.top, self.left, *self.bottoms, *self.ups]
        self.assumptions = assumptions

    def assump(self, box, value):
        #boxの値を仮定
        if box.type != 0 and box in self.assumptions and self.assumptions[box] != value:
            return False
        if box.type != 0 and value in self.assumptions.values():
            return False
        
        for column in self.columns:
            column.assump(box, value)
        
        if box.type != 0:
            self.assumptions[box] = value

        return True
    
    def discard(self, box):
        #boxの値を消す．assumpの逆
        if box.type != 0:
            if box in self.assumptions:
                del self.assumptions[box]

        for column in self.columns:
            column.discard(box)

    
    def part_set(self):
        #各columnの末尾の値を決定できるところまで決定して，矛盾がないか判定 (left未決定時に使用)
        for btm, digit in zip(self.bottoms, self.top.digits):
            if not isinstance(digit, Box):
                result = btm.part_set(self.left.part_multiply(digit), self.assump)
                if result == False:
                    return False
                
        for i in range(len(self.bottoms)-1):
            if i > 0:
                result = self.ups[i+1].part_set(self.bottoms[i].part_plus(self.ups[i].shift()), self.assump)
            else:
                result = self.ups[i+1].part_set(self.bottoms[i].part_plus(self.ups[i]), self.assump)
            if result == False:
                return False
            
            if isinstance(self.ups[i+1].digits[0], int) and isinstance(self.ups[-1].digits[i], int):
                if self.ups[i+1].digits[0] != self.ups[-1].digits[i]:
                    return False
        
        if not self.ups[-1].part_set(self.top.part_multiply(self.left).part_plus(self.ups[0]), self.assump):
            return False

            
        return True


    def full_set(self):
        #各columnの値を決定できるところまで決定して，矛盾がないか判定 (left決定時に使用)
        for btm, digit in zip(self.bottoms, self.top.digits):

            if not isinstance(digit, Box):
                result = btm.full_set(self.left.full_multiply(digit), self.assump)
                if result == False:
                    return False
                
        
        for i in range(len(self.bottoms)-1):
            if i > 0:
                result = self.ups[i+1].part_set(self.bottoms[i].part_plus(self.ups[i].shift()), self.assump)
            else:
                result = self.ups[i+1].part_set(self.bottoms[i].part_plus(self.ups[i]), self.assump)
            if result == False:
                return False
            
            if isinstance(self.ups[i+1].digits[0], int) and isinstance(self.ups[-1].digits[i], int):
                if self.ups[i+1].digits[0] != self.ups[-1].digits[i]:
                    return False
                
        if not self.ups[-1].part_set(self.top.part_multiply(self.left).part_plus(self.ups[0]), self.assump):
            return False
            
        return True

    def complete(self):
        #各columnの値を完全に決定して，矛盾がないか判定
        if not self.ups[-1].full_set(self.top.full_multiply(self.left).full_plus(self.ups[0]), self.assump):
            return False
        
        if not self.full_set():
            return False
        
        for i in range(len(self.bottoms)-1):
            if i > 0:
                result = self.ups[i+1].full_set(self.bottoms[i].full_plus(self.ups[i].shift()), self.assump)
            else:
                result = self.ups[i+1].full_set(self.bottoms[i].full_plus(self.ups[i]), self.assump)
            if result == False:
                return False
        
        
        return True
            

    def copy(self):
        return Division(self.top.copy(), self.left.copy(), [col.copy() for col in self.ups], [col.copy() for col in self.bottoms], self.assumptions.copy())
    
    def str(self):
        string = "\n"
        N = len(self.ups[-1].digits) + len(self.left.digits) + 1
        string += " "*(N-len(self.top.digits)) + self.top.str() + "\n"
        string += " "*len(self.left.digits) + "-"*(len(self.ups[-1].digits)+2) + "\n"
        string += self.left.str() + ")" + self.ups[-1].str() + "\n"
        for i, btm, up in zip(range(len(self.bottoms)-1, -1, -1), self.bottoms[::-1], self.ups[-2::-1]):
            string += " "*(N-len(btm.digits)-i) + btm.str() + "\n"
            string += "-"*(N+1) + "\n"
            if i > 0:
                string += " "*(N-len(up.digits)-i+1) + up.str() + "\n"
            else:
                string += " "*(N-len(up.digits)) + up.str() + "\n"
        
        return string
    
    def get_boxes(self):
        #boxをリストにする
        boxes=set()
        for column in self.columns:
            boxes = boxes.union(set(column.boxmap.keys()))
        
        return list(boxes)
    
    def get_answers(self):
        #boxに仮定された値をすべて出力
        answers={}
        for column in self.columns:
            answers.update(column.boxvalues)
        
        return answers

    
class Multiplication:
    @classmethod
    def string2mulitiplication(cls, string):
        #strからMultiplicationに変換
        cols = string.replace(" ", "").replace("-", "").split("\n")
        while "" in cols:
            cols.remove("")
        return cls(Column.str2column(cols[0]), Column.str2column(cols[1]), [Column.str2column(c) for c in cols[2:-1]], Column.str2column(cols[-1]))

    def __init__(self, top1, top2, middles, bottom, assumptions={}):
        self.top1 = top1 #かけられる数
        self.top2 = top2 #かける数
        self.middles = middles #中間
        self.bottom = bottom #掛け算の結果
        self.columns = [self.top1, self.top2, *self.middles, self.bottom]
        self.assumptions = assumptions

    def assump(self, box, value):
        #boxの値を仮定
        if box.type != 0 and box in self.assumptions and self.assumptions[box] != value:
            return False
        if box.type != 0 and value in self.assumptions.values():
            return False
        
        for column in self.columns:
            column.assump(box, value)
        
        if box.type != 0:
            self.assumptions[box] = value

        return True
    
    def discard(self, box):
        #boxの値を消す．assumpの逆
        if box.type != 0:
            if box in self.assumptions:
                del self.assumptions[box]

        for column in self.columns:
            column.discard(box)
    
    def part_set(self):
        #各columnの末尾の値を決定できるところまで決定して，矛盾がないか判定 (top1未決定時に使用)
        for mid,digit in zip(self.middles, self.top2.digits):
            if not isinstance(digit, Box):
                result = mid.part_set(self.top1.part_multiply(digit), self.assump)
                if result == False:
                    return False
        
        return self.bottom.part_set(self.top1.part_multiply(self.top2), self.assump)
    
    def full_set(self):
        #各columnの値(ただしbottomのみ末尾のみ)を決定できるところまで決定して，矛盾がないか判定 (top1決定時に使用)
        for mid,digit in zip(self.middles, self.top2.digits):
            if not isinstance(digit, Box):
                result = mid.full_set(self.top1.full_multiply(digit), self.assump)
                if result == False:
                    return False
        
        return self.bottom.part_set(self.top1.part_multiply(self.top2), self.assump)
    
    def complete(self):
        #各columnの値を完全に決定して，矛盾がないか判定
        for mid,digit in zip(self.middles, self.top2.digits):
            if not isinstance(digit, Box):
                result = mid.full_set(self.top1.full_multiply(digit), self.assump)
                if result == False:
                    return False

        return self.bottom.full_set(self.top1.full_multiply(self.top2), self.assump)
            

    def copy(self):
        #コピー
        return Multiplication(self.top1.copy(), self.top2.copy(), [mid.copy() for mid in self.middles], self.bottom.copy(), self.assumptions.copy())
    
    def str(self):
        #strにする
        string = "\n"
        N = len(self.bottom.digits)

        string += " "*(N-len(self.top1.digits)) + self.top1.str() + "\n"
        string += " "*(N-len(self.top2.digits)) + self.top2.str() + "\n"
        string += "-"*N + "\n"
        for i, mid in enumerate(self.middles):
            string += " "*(N-len(mid.digits)-i) + mid.str() + "\n"
        if len(self.middles) != 0:
            string += "-"*N + "\n"
        string += self.bottom.str()

        return string
    
    def get_boxes(self):
        #boxをリストにする
        boxes=set()
        for column in self.columns:
            boxes = boxes.union(set(column.boxmap.keys()))
        
        return list(boxes)
    
    def get_answers(self):
        #boxに仮定された値をすべて出力
        answers={}
        for column in self.columns:
            answers.update(column.boxvalues)
        
        return answers

# ----------- メインプログラム -----------

def solve_multiplication(mul, outputs=None):
    if outputs is None:
        outputs = set()
    #掛け算の虫食い算をDPで解く．ジェネレータ
    mul.part_set() #boxを埋める
    
    if mul.top1.uncomplete(): #top1(かけられる数)の決定
        digit1 = mul.top1.digits[mul.top1.defined]
        #最も下の位の空欄を0~9に仮定
        for p in range(10):
            mul2 = mul.copy()
            if not mul2.assump(digit1, p):
                continue
            if not mul2.part_set():
                continue
            else:
                yield from solve_multiplication(mul2, outputs)

    elif mul.top2.uncomplete(): #top2(かける数)の決定
        digit2 = mul.top2.digits[mul.top2.defined]
        #最も下の位の空欄を0~9に仮定
        for p in range(10):
            mul2 = mul.copy()
            if not mul2.assump(digit2, p):
                continue
            if not mul2.full_set():
                continue
            else:
                yield from solve_multiplication(mul2, outputs)

    else:
        if mul.complete():
            a, b = mul.top1.int(), mul.top2.int()
            if (a,b) not in outputs:
                outputs.add((a,b))
                yield mul
    
def solve_division(div, outputs=None):
    if outputs is None:
        outputs = set()
    #割り算の虫食い算をDPで解く．ジェネレータ
    div.part_set() #boxを埋める

    if div.ups[0].uncomplete():
        digit0 = div.ups[0].digits[div.ups[0].defined]
        #最も下の位の空欄を0~9に仮定
        for p in range(10):
            div2 = div.copy()
            if not div2.assump(digit0, p):
                continue
            if not div2.part_set():
                continue
            else:
                yield from solve_division(div2, outputs)

    
    elif div.left.uncomplete(): #left(わる数)の決定
        digit1 = div.left.digits[div.left.defined]
        #最も下の位の空欄を0~9に仮定
        for p in range(10):
            div2 = div.copy()
            if not div2.assump(digit1, p):
                continue
            if not div2.part_set():
                continue
            else:
                yield from solve_division(div2, outputs)

    elif div.top.uncomplete(): #top(商)の決定
        digit2 = div.top.digits[div.top.defined]
        #最も下の位の空欄を0~9に仮定
        for p in range(10):
            div2 = div.copy()
            if not div2.assump(digit2, p):
                continue
            if not div2.full_set():
                continue
            else:
                yield from solve_division(div2, outputs)

    
    else:
        if div.complete():
            a, b, c = div.left.int(), div.top.int(), div.ups[0].int()
            if (a,b,c) not in outputs:
                outputs.add((a,b,c))
                yield div
    


# ------ここから生成プログラム-----

def make_unique_selection(ans, original):
    #与えられたanswers(Multiplication型)から1つの要素を一意に決定できるboxの指定方法があれば，その1つをランダムに出力する
    raw_answers = [mul.get_answers() for mul in ans]
    original_answer = original.get_answers()
    boxes = raw_answers[0].keys()
    answers = {box:[ans[box] for ans in raw_answers] for box in boxes if box.editable and box not in original_answer}
    countables = {box:[ans.count(i) for i in range(10)] for box, ans in answers.items()}
    minimum = min(c for array in countables.values() for c in array if c != 0)
    candicates = []
    for box, countable in countables.items():
        if minimum in countable:
            candicates += [(box, value) for value, count in enumerate(countable) if count == minimum]
    

    box, value = random.choice(candicates)

    results = []

    for mul, raw_answer in zip(ans, raw_answers):
        if raw_answer[box] == value:
            results.append(mul)

    return box, value, results


      

    
def make_selection(muls, original):
    #与えられたanswers(Multiplication型)にそれを満たすものが少なくとも1つあるように，boxの指定方法の1つをランダムに出力する
    original_answer = original.get_answers()
    candicates = [(box, value) for mul in muls for box, value in mul.get_answers().items() if box.editable and box not in original_answer]
    box, value = random.choice(candicates)
    ans = [mul for mul in muls if mul.get_answers()[box] == value]
            
    return box, value, ans


def minimize(source, solver, n):
    candicates = []
    answer = source.get_answers()
    if not answer:
        return source, n

    for box, value in answer.items():
        source2 = source.copy()
        source2.discard(box)
        for i, ans in enumerate(solver(source2.copy())):
            if i > 0:
                break

        else:
            candicates.append(source2)


    if not candicates:
        return source, n
    
    
    else:
        return minimize(random.choice(candicates),solver,n-1)



def _make_problem(source, n, solver, key="random", skip=False, answers=None):
    #掛け算の虫食い算を生成しMultiplication型で出力
    if not skip:
        selectable = True
        if answers is None:
            answers = []
            for i, ans in enumerate(solver(source.copy())):
                answers.append(ans)
                if i+1 >= 300:
                    selectable = False
                    break
            
        i = len(answers)
        
        if selectable:
            #答えが300個以下ならそこから選ぶ
            if i == 0:
                return None
            elif i == 1:
                if key == "random":
                    source, n = minimize(source, solver, n)
                return source, answers[0], n
            else:
                if key == "disorder" or key == "random":
                    box, value, ans = make_selection(answers, source)
                elif key == "short":
                    box, value, ans = make_unique_selection(answers, source)
                source2 = source.copy()
                source2.assump(box,value)
                return _make_problem(source2, n+1,solver, key=key, answers=ans)


    #答えが300個を超えたら#の1つをランダムに決定して再試行．
    boxes = [box for box in source.get_boxes() if box.editable and box not in source.get_answers()]
    if boxes:
        box = random.choice(boxes)
        source2 = source.copy()
        source2.assump(box, random.randrange(10))
        #k = random_letter_choice(string)
        #return _make_mulitiplication(string[:k] + str(random.randrange(10)) + string[k+1:], n+1, key=key)
        return _make_problem(source2, n+1, solver, key=key)
            


def make_problem(string, type="m", key="disorder", M=100000):
    #シェル上で掛け算の虫食い算を生成する
    if type=="m":
        source = Multiplication.string2mulitiplication(string)
        solver = solve_multiplication
    
    elif type=="d":
        source = Division.string2division(string)
        solver = solve_division

    else:
        raise ValueError()
        

    i = -1
    to_skip = False
    answers = []
    for i, ans in enumerate(solver(source.copy())):
        answers.append(ans)
        print(f"\033[31mANSWER No.{i+1}\033[0m" + ans.str() + "\n")
        if i+1 >= M:
            print(f"\033[31mThere are {M} or more answers in the given case\033[0m\n")
            to_skip = True
            answers = None
            break

    else:
        if i == -1:
            print(f"\033[31mThere are no answers in the given case\033[0m\n")
            return
        print(f"\033[31mThere are {i+1} answers in the given case\033[0m\n")
    
    
    while True:
        source2 = source.copy()
        result = _make_problem(source2,0,solver,key,to_skip,answers)
        if result is None:
            #生成失敗したら再試行
            continue
        else:
            problem, answer, n = result
            print("\033[34mPROBLEM\033[0m" + problem.str().replace("#","*") + "\n")
            print("\033[31mANSWER\033[0m" + answer.str() + "\n")
            print(', '.join([f"{a.id}:{b}" for a, b in answer.assumptions.items()]))
            print(f"\033[32mFIXED:{n}\033[0m")
            input('Press enter to create another case:')

# ----------------- sample --------------------

STRING_MULTIPLICATION = '''
   ###
   #4#
-------
  ####
 SAKU
MONN
-------
#2####
'''

STRING_DIVISION = '''
       ####
   ---------
1##)#######
    ####
------------
     ####
      #3#
------------
      ####
      ####
------------
       ####
       ####
------------
          0
'''
if __name__ == "__main__":
    make_problem(STRING_DIVISION, type="d", key="disorder", M=100000)

# 関数: make_problem()に問題の元となる文字列を渡すと，その形の問題が作成されます．

# 文法: 問題の元となる文字列の書き方は上のSTRING_MULTIPLICATION,STRING_DIVISIONを参考にしてください．"-"およびスペースは可読性のためのものなのでなくても動きます．
# 文法: "*"と"#"は空欄を表し，0~9の数字が入ることを表します (但し最高位は0でない)．
# 文法: "#"と"*"には若干の違いがあります．"#"は答えが一意に定まるように適当な数字に置き換わることがありますが，"*"は数字に置き換わることなく空欄のままとなります．
# 文法: "*","#","-"," "および0~9の数字以外の文字はすべて空欄として処理され，同じ文字には同じ数字が，異なる文字には異なる数字が入るようになります．これらは数字に置き換わることはありません．

# 設定: type="m"は掛け算で，type="d"は割り算の問題が作れます．
# 設定: keyはとりあえず"disorder"にしておいて，FIXEDが少なめのもの(=空欄が多いもの)を選ぶのが良いと思います．

# 高度な設定: key="disorder"とするとなるべくランダムに問題が出力されます．空欄の数は不安定になります．
# 高度な設定: key="short"とすると空欄が多い問題が優先的に出力されます．その分問題の多様性が少なくなります．
# 高度な設定: key="random"とするとなるべくランダムで，どの追加情報を消しても答えが一意に定まらないよう空欄の数を極大化したものが出力されます．ただしshort,disorderに比べて生成に時間がかかります．
# 高度な設定: Mについて，解答となりうるものは，最初にM個までの範囲で全列挙します．選択肢が多すぎて全列挙できなくても問題は出力されますが，その場合問題の生成に時間がかかります．

# デベロッパ: Multiplication.string2multiplication(STRING_MULTIPLICATION)で掛け算オブジェクト， Division.string2division(STRING_DIVISION)で割り算オブジェクトを得ることができます
# デベロッパ: 掛け算オブジェクトmulに対し，solve_multiplication(mul)とするとmulを満足する答えを表す掛け算オブジェクトをすべて出力するイテレータを返します．solve_divison()も同様です．
# デベロッパ: 掛け算オブジェクトmulに対し，mul.str()で文字列に変換できます．割り算でも同様です．
