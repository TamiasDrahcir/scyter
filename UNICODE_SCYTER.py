import math
from datetime import datetime
import pytz

# Calculate days since relationship started (June 19)
def get_hk_key():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today_beijing = datetime.now(beijing_tz).date()
    anniversary = datetime(2026, 6, 19).date()
    
    days_since = (today_beijing - anniversary).days
    return f"HK{days_since}"

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
# Each key character contributes its own shift: letters use A=0..Z=25, digits use their face value
def key_char_shift(c):
    if c.isalpha():
        return ord(c.upper()) - ord('A')
    if c.isdigit():
        return int(c)
    return None

def build_shift_cycle(key):
    return [key_char_shift(c) for c in key if key_char_shift(c) is not None]

def vigenere_encode(text, key):
    shifts = build_shift_cycle(key)
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = shifts[key_index % len(shifts)]
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def vigenere_decode(text, key):
    shifts = build_shift_cycle(key)
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = shifts[key_index % len(shifts)]
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

# Flag to key mapping
FLAG_KEY_MAP = {
    "|XRX": "RZ",      # Default: Reversed Zodiac
    "|HM": "HK"        # Hiyama Kiyoteru Anniversary - Daily
}

# Get key from flag
def get_key_from_flag(flag):
    if flag in FLAG_KEY_MAP:
        key_type = FLAG_KEY_MAP[flag]
        if key_type == "RZ":
            return get_today_constellation()[::-1].lower()  # Reverse and lowercase
        elif key_type == "HK":
            return get_hk_key().lower()  # HKxxx in lowercase
    return None

# Detect passcode type from its format: hk### -> HK, letters-only -> RZ
def detect_key_type(passcode):
    trimmed = passcode.strip()
    if trimmed[:2].lower() == "hk" and trimmed[2:].isdigit():
        return "HK"
    if trimmed.isalpha():
        return "RZ"
    return "UNKNOWN"

# Extract flag from message (flag is at the end, format: |XX or |XXX)
def extract_flag(message):
    if "|" in message:
        last_pipe_idx = message.rfind("|")
        potential_flag = message[last_pipe_idx:]
        # Check if it looks like a valid flag (pipe followed by 2-3 letters)
        if len(potential_flag) >= 3 and len(potential_flag) <= 4 and potential_flag[0] == "|" and potential_flag[1:].isalpha():
            if potential_flag in FLAG_KEY_MAP:
                return potential_flag, message[:last_pipe_idx]
    return "|XRX", message  # Default flag if none provided or unrecognized flag



print("Hello, welcome to SCYTER! Do you want to encode or decode? \nNOTE: please enter your response as \"encode\" or \"decode\", in all lowercase; otherwise, your response may be considered as invalid.")
ende = input()
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","/"]
numbers = ["001","002","010","011","012","020","021","022","100","101","102","110","111","112","120","121","122","200","201","202","210","211","212","220","221","222","000"]
while ende != "encode" and ende != "decode":
  print("I beg your pardon?")
  ende = input()
if ende == "encode":
  print("Great! What's your message?\nNOTE: pipe characters (|) are reserved for flags and are not allowed in the plaintext.")
  message = input()
  
  # Extract flag and validate plaintext
  flag, plaintext = extract_flag(message)
  
  # Validate that plaintext doesn't contain pipe characters
  if "|" in plaintext:
    print("ERROR: Pipe character (|) is reserved for flags and cannot appear in plaintext.")
    exit()
  
  # Get the key for this flag
  key = get_key_from_flag(flag)
  if key is None:
    print(f"ERROR: Unknown flag '{flag}'. Valid flags are: {', '.join(FLAG_KEY_MAP.keys())}")
    exit()
  
  print(f"Using flag: {flag} \u2014 passcode: {key}")
  
  unicodes = []
  m = 0
  while m < len(plaintext):
      unicodes.append(ord(plaintext[m]))
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
  
  # Apply Vigenère cipher with the determined key
  Final = vigenere_encode(Final, key)
  
  print("Here\'s the cipher:\n" + Final.replace(" ","/"))
if ende == "decode":
  print("Cool! Can you show me your cipher?\n NOTE: your cipher shouldn't contain spaces, so make sure there is no spacing when copying and pasting.")
  code = input()
  
  # Prompt for passcode
  print("Please enter the passcode (e.g. xxxxx for zodiac, or hkxxx for Hiyama Kiyoteru):")
  key = input().strip()
  
  # Auto-detect the passcode type
  key_type = detect_key_type(key)
  if key_type == "UNKNOWN":
    print("ERROR: Unrecognized passcode format. Expected a zodiac word or an hk### code.")
    exit()
  print(f"Detected key type: {key_type}")
  
  # Apply Vigenère decoding directly with the entered passcode
  code = vigenere_decode(code, key)
  
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
