# MYASO

A steganographic shellcode obfuscator. The executor reads data from a BMP image and executes it using VirtualAlloc/HeapAlloc. 

Has modules in the following languages:
- [x] C/C++
- [x] C#
- [x] Powershell
- [] VB
- [] Python
- [] Rust
- [] Go

Available algorithms:
- [x] LSB (generic)
- [] LSB-X (channel X only)

Supproted image formats:
- [x] BMP
- [] PNG (in progress)
- [] JPEG

## Usage

### Generate image
```sh
python main.py -f sc.bin -i image.bmp -o evil_image.bmp [-a <algorithm>]
python main.py --sc "\xe4\xed..." -i image.bmp -o evil_image.bmp [-a <algorithm>]
```

### Execute shellcode
```cmd
c:\> reader.exe --size <sc_len> -f happy_cat.bmp
```

## Definition of Ready
- [] add length parsing
- [] parsing/embedding is abstract enough
- [x] console args
- [] colored output
- [] write tests (at least for the Python part)
- [] proper error handling
