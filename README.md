# MYASO

```
$ myaso embed -a LSB -i .\cat.bmp -o .\samples\shellcode\sc64.bmp -s .\sc_x64.bin --def .\go.yaml
88888b.d88b.  888  888  8888b.  .d8888b   .d88b.           
888 "888 "88b 888  888     "88b 88K      d88""88b          
888  888  888 888  888 .d888888 "Y8888b. 888  888          
888  888  888 Y88b 888 888  888      X88 Y88..88P          
888  888  888  "Y88888 "Y888888  88888P'  "Y88P"           
                   888                                     
by @adeadfed  Y8b d88P 
   @harpsiford "Y88P"       

[*] Payload size: 2208 bits (save this number!)
🥩 Saved the stego to .\samples\shellcode\sc64.bmp
[+] Builder configured
[*] Configuration: gorunner64_no_symbols (windows/x64/go/shellcode, algorithm=LSB, params={'MAX_BITS': 2208})
[*] Starting the build...
[+] Build was successful!
🥩 Runner is at readers\go\gorunner64_no_symbols.exe
[*] Usage: gorunner64_no_symbols.exe 2208 sc64.bmp

❯ py main.py embed -a LSB-X,G -i .\samples\cat.bmp -o .\samples\shellcode\sc_lsbx_green.bmp -s .\samples\shellcode\test_lsbx.txt --verbose --no-banner
[*] Reading shellcode from file...
[*] Shellcode: b'123456\r\n'
[*] Payload size: 64 bits (save this number!)
[*] Algorithm: LSB-X
[*] Source image: .\samples\cat.bmp
[*] LSB-X args: ('G',) 1
� Saved the stego to .\samples\shellcode\sc_lsbx_green.bmp

❯ py main.py read -a LSB-X,G -i .\samples\shellcode\sc_lsbx_green.bmp --verbose --max-bits 64 --no-banner
[*] Source image: .\samples\shellcode\sc_lsbx_green.bmp
[*] Algorithm: LSB-X
[*] Algorithm: LSB-X,G, extracting up to 64 bits
[*] LSB-X args: ('G',) 1
[+] Message: b'123456\r\n'

❯ py main.py read  -a LSB-X,G,64               -i samples/shellcode/sc_lsbx_green.bmp   --verbose --no-banner
❯ py main.py embed -a LSB-X,samples/cat.bmp,G  -o /samples/shellcode/sc_lsbx_green.bmp  --verbose --no-banner

```

A steganographic shellcode obfuscator. The executor reads data from a BMP image and executes it using VirtualAlloc/HeapAlloc. 

Has modules in the following languages:
- [x] C/C++
- [x] C#
- [x] Powershell
- [x] Go
- [x] Microsoft VBA (beta)

Available algorithms:
- [x] LSB (generic)
- [x] LSB-X (channel X only)
- [x] LSBM
- [x] ColorCode

Supported image formats:
- [x] BMP
- [x] PNG
- [ ] JPEG (TBD)

Supported payload types:
- [x] CMD commands
- [x] Shellcode 
- [ ] In-memory PE

Supported payload mutations:
- [ ] Obfuscate PS runner

## Usage

### Generate image
```sh
myaso embed -f sc.bin -i image.bmp -o evil_image.bmp [-a <algorithm>]
```

### Execute shellcode
```cmd
c:\> reader.exe SC_BITS happy_cat.bmp
```

## Is it any good?
[yes.](https://news.ycombinator.com/item?id=3067434)

## Known issues
- [ ] python script takes ages to process large payloads (>1 MB)
- [ ] PS builder templates wrong byte_length e.g. (should be 276 -> templates 2208 (276 * 8, length in bits))
- [ ] PS builder does not use minifier (/src/ps_minifier.py)
- [ ] C++ runners are not working and crash
- [ ] C# builder searches for csharp_runner.cs, not runner.cs
- [ ] Go builder not working (no template braces in the .mst file, searching for file with wrong name)

## Definition of Ready
- [x] parsing/embedding is abstract enough
- [x] console args
- [x] colored output
- [ ] write tests (at least for the Python part)
- [ ] proper error handling (in progress)
- [x] steak ascii art
- [x] algorithm args (`myaso -a ALGO,arg1,arg2`)
- [x] minify PS output after build
- [x] templating (all langs)
- [ ] test all build variants manually (oh god)
- [ ] docker image

## Roadmap
- [ ] JPEG support 
- [ ] interactive mode for embedding / generating
- [ ] add in-memory PE runners
- [ ] speed-up payload embedding in python
- [ ] payload mutations
