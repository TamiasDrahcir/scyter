# SCYTER Flag System Documentation

## Overview
The SCYTER cipher has been enhanced to support custom keys and flags. The flag system allows users to specify which encryption key should be used for encrypting/decrypting messages.

## Flag System Details

### Flags Supported

1. **|XRX** (Default - Reversed Zodiac)
   - This is the default flag
   - Uses the RZ key: constellation name spelled backwards, all lowercase
   - Example: If today is in Libra, the key would be "arbil"
   - Does NOT need to be explicitly added to the plaintext

2. **|HM** (Hiyama Kiyoteru Anniversary - Daily)
   - Custom flag for your friend's relationship
   - Uses the HK key: "HK" + number of days since June 19
   - Example: If 100 days have passed since June 19, the key would be "hk100"
   - Must be explicitly added at the end of the plaintext: `message|HM`

### Flag Format
- Flags must appear at the **end** of the plaintext
- Format: `|` followed by 2-3 letters (|XX or |XXX)
- Example: `hello|HM` or `message|XRX`

## Restrictions

- **Pipe characters (|) are NOT allowed in plaintext**
  - This is because `|` is reserved as the flag separator
  - If a pipe is detected anywhere in the plaintext (except as part of a valid flag at the end), an error will be raised
  - This prevents accidental misinterpretation of content as flags

## Encoding Workflow

```
User input: "message|HM"
         ↓
Extract flag: "|HM" 
Remove flag from plaintext: "message"
         ↓
Validate no pipes in plaintext ✓
         ↓
Get key from flag: |HM → HK key (e.g., "hk100")
         ↓
Apply SCYTER transform to plaintext
         ↓
Apply Vigenère cipher with HK key
         ↓
Output: encrypted ciphertext
```

## Decoding Workflow

```
User input (ciphertext): "BPKREN/SEP//B///"
User input (flag): "|HM"
         ↓
Validate flag ✓
         ↓
Get key from flag: |HM → HK key (e.g., "hk100")
         ↓
Apply Vigenère decipher with HK key
         ↓
Apply inverse SCYTER transform
         ↓
Output: decrypted plaintext
```

## HK Key Calculation

The HK (Hiyama Kiyoteru Anniversary - Daily) key is calculated as follows:

- **Anniversary date**: June 19 (the day the relationship started)
- **Key format**: "HK" + number of days since June 19
- **Example**: 
  - If today is June 28, and the anniversary is June 19, the key is "HK9"
  - If today is December 28, and the anniversary was June 19 (same year), the key is "HK193"
  - If today is May 15, the anniversary date used is June 19 of the **previous year**

The key is always stored in lowercase (e.g., "hk100").

## Usage Examples

### Encoding with custom flag
```
> encode
> Enter message: "Meet at noon|HM"
> Output: [encrypted message using HK key]
```

### Encoding with default flag
```
> encode  
> Enter message: "Meet at noon"
> Output: [encrypted message using RZ key, |XRX flag implied]
```

### Decoding with custom flag
```
> decode
> Enter ciphertext: [encrypted message]
> Enter flag: "|HM"
> Output: decrypted message
```

### Decoding with default flag
```
> decode
> Enter ciphertext: [encrypted message]
> Enter flag: "|XRX"
> Output: decrypted message
```

## Error Handling

- **Invalid flag in encoding**: If a pipe appears in the middle of the plaintext, the program will show an error and exit
- **Unknown flag in decoding**: If a flag is not recognized (not in the supported flags list), the program will show an error and exit
- **Missing pytz module**: Make sure `pytz` is installed: `pip install pytz`

## Implementation Notes

The flag system is implemented in the Python file with the following key functions:

- `get_hk_key()`: Calculates the current HK key based on the number of days since June 19
- `extract_flag(message)`: Extracts the flag from the end of the message
- `get_key_from_flag(flag)`: Maps a flag to its corresponding encryption key
- `FLAG_KEY_MAP`: Dictionary mapping flags to their key types

The flag is removed from the plaintext before encryption, and decryption requires the user to specify which flag (and therefore which key) was used.
