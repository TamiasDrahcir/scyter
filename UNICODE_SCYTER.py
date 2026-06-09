import math
print("Hello, welcome to SCYTER! Do you want to encode or decode? \nNOTE: please enter your response as \"encode\" or \"decode\", in all lowercase; otherwise, your response may be considered as invalid.")
ende = input()
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","/"]
numbers = ["001","002","010","011","012","020","021","022","100","101","102","110","111","112","120","121","122","200","201","202","210","211","212","220","221","222","000"]
while ende != "encode" and ende != "decode":
  print("I beg your pardon?")
  ende = input()
if ende == "encode":
  print("Great! What's your message?")
  message = input()
  unicodes = []
  m = 0
  while m < len(message):
      unicodes.append(ord(message[m]))
      m += 1
  terunicode = []
  t = 0
  def ternary(num):
      ter = []
      power = 11
      while power >= 0:
          ter.append(str(math.floor(num/pow(3,power))))
          num = num%pow(3,power)
          power -= 1
      ter.reverse()
      return "".join(ter)
  while t < len(unicodes):
      terunicode.append(ternary(unicodes[t]))
      t += 1
  concat = "".join(terunicode)
  s = 0
  mnum = []
  while s < len(concat):
      mnum.append(concat[s:s+3])
      s += 3
  A = []
  B = []
  C = []
  m = 0 
  while m < len(mnum):
    A.append(str(mnum[m])[0])
    B.append(str(mnum[m])[1])
    C.append(str(mnum[m])[2])
    m += 1
  scyedstr = "".join(A)+"".join(B)+"".join(C)
  n = 0
  scyedarr = []
  while n < len(scyedstr)/3:
    scyedarr.append(alphabet[numbers.index(scyedstr[n*3:n*3+3])])
    n += 1
  Final = "".join(scyedarr)
  print("Here\'s the cipher:\n" + Final.replace(" ","/"))
if ende == "decode":
  print("Cool! Can you show me your cipher?\n NOTE: your cipher shouldn't contain spaces, so make sure there is no spacing when copying and pasting.")
  code = input()
  cnum = []
  X = []
  Y = []
  Z = []
  DECODE = []
  c = 0 
  while c < len(code):
    cnum.append(numbers[alphabet.index(code[c])])
    c += 1
  string = "".join(cnum)
  s1 = string[0:int(len(string)/3)]
  s2 = string[int(len(string)/3):int(len(string)/3*2)]
  s3 = string[int(2*len(string)/3):len(string)]
  d = 0
  while d < len(s1):
    DECODE.append(s1[d]+s2[d]+s3[d])
    d += 1
  FINAL = []
  final = "".join(DECODE)
  a = []
  split = 0
  while split < len(final):
    a.append(final[split])
    split += 1
  a.reverse()
  final = "".join(a)
  f = 0
  def terdec(s):
    reverse = []
    p = 11
    while p >= 0:
      reverse.append(int(s[11-p])*pow(3,p))
      p -= 1
    return sum(reverse)
  while f < len(final):
    FINAL.append(chr(terdec(final[f:f+12])))
    f += 12
  end = "".join(FINAL)
  FINALSPLIT = []
  SPLIT = 0
  while SPLIT < len(end):
    FINALSPLIT.append(end[SPLIT])
    SPLIT += 1
  FINALSPLIT.reverse()
  end = "".join(FINALSPLIT)
  print(end)
