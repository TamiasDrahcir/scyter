import math
from datetime import datetime
import pytz

# Get constellation for a date
def get_constellation(date_obj):
    # Constellation date ranges (month, day)
    constellations = [
        ("aries", (3, 21), (4, 19)),
        ("taurus", (4, 20), (5, 20)),
        ("gemini", (5, 21), (6, 20)),
        ("cancer", (6, 21), (7, 22)),
        ("leo", (7, 23), (8, 22)),
        ("virgo", (8, 23), (9, 22)),
        ("libra", (9, 23), (10, 22)),
        ("scorpio", (10, 23), (11, 21)),
        ("sagittarius", (11, 22), (12, 21)),
        ("capricorn", (12, 22), (1, 19)),
        ("aquarius", (1, 20), (2, 18)),
        ("pisces", (2, 19), (3, 20))
    ]
    
    month, day = date_obj.month, date_obj.day
    
    for name, (start_month, start_day), (end_month, end_day) in constellations:
        if start_month == end_month:
            if month == start_month and start_day <= day <= end_day:
                return name
        else:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return name
    return "capricorn"

# Get constellation for today in Beijing timezone
def get_today_constellation():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today_beijing = datetime.now(beijing_tz).date()
    return get_constellation(datetime(today_beijing.year, today_beijing.month, today_beijing.day))

# Vigenère cipher
def vigenere_encode(text, key):
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def vigenere_decode(text, key):
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].upper()) - ord('A')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

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
  
  # Apply Vigenère cipher with constellation passcode
  passcode = get_today_constellation()[::-1].lower()  # Reverse and lowercase
  Final = vigenere_encode(Final, passcode)
  
  print("Here\'s the cipher:\n" + Final.replace(" ","/"))
if ende == "decode":
  print("Cool! Can you show me your cipher?\n NOTE: your cipher shouldn't contain spaces, so make sure there is no spacing when copying and pasting.")
  code = input()
  
  # Prompt for passcode
  print("Please enter the passcode (constellation name spelled backwards, all lowercase):")
  passcode = input().lower()
  
  # Apply Vigenère decoding with provided passcode (no error checking)
  code = vigenere_decode(code, passcode)
  
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
  FINALSPLIT.reverse()
  end = "".join(FINALSPLIT)
  print(end)
