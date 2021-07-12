# MYASO

Meet Yet Another Shellcode Obfuscator!

Evade AV by hiding cmd/shellcode/... payloads inside images and simply running them. 

## Installation

### Linux
```
apt update
apt install -y gcc libc-dev g++-mingw-w64-i686 g++-mingw-w64-x86-64 libgdiplus mono-devel golang-go
git clone https://github.com/adeadfed/myaso
cd myaso
pip3 install -r requirements.txt
```

### Docker
```
git clone https://github.com/adeadfed/myaso
cd myaso
docker build -t myaso:latest .
```

## Usage

![demo](myaso_demo.gif)

### Generate image
```sh
myaso embed -a sc.bin [-i image.bmp] [-a <algorithm>] -o evil_image.bmp
```

In Docker:
```sh
docker run --rm -it -v `pwd`:/mnt/ myaso embed -f /mnt/your_shellcode.bin -o /mnt/stego.png -a LSB
```
### Generate runner
```sh
myaso bake
```

You will be asked all the details interactively. 
At the end you'll be offered to save the configuration, 
which you can then use with:
```sh
myaso bake [--def saved_definition.yml]
```
```
[banner]

? Desired stego algorithm:  LSB
? Desired runner language:  C++
? Desired runner arch:  x64
? Desired payload type:  Shellcode
? Desired image source:  (Use arrow keys)
 ❯ ImageFile
   HTTPX
  ...
```

In Docker:
```sh
docker run --rm -it -v `pwd`:/mnt/ myaso bake 
```

(Set output to your mount dir!)

```
[banner]

? Desired stego algorithm:  LSB
...
? Output runner file:  /mnt/your_runner.exe
? Save config to file?  Yes
? Location:  /mnt/your_config.yml
```

### Execute shellcode
```cmd
c:\> reader.exe happy_cat.bmp PAYLOAD_BYTES
```


## Feature support

Supported stego algorithms:

| Algorithm | C++ | C# | Go | PS | VBA |
|-----------|-----|----|----|----|-----|
| LSB       |  ✓  |  ✓  | ✓  | ✓  | ✓  |
| LSBX      |  ✓  |  ✓  | ✓  | ✓  | ✓  |
| LSBM      |  ✓  |  ✓  | ✓  | ✓  | ✓  |
| ColorCode |  ✓  |  ✓  | ✓  | ✓  | ✓  |


Supported payload types:

| Payload   | C++ | C# | Go | PS | VBA |
|-----------|-----|----|----|----|-----|
| CMD       | ✓  | ✓  | ✓  | ✓  | ✓  |
| Shellcode | ✓  | ✓  | ✓  | ✓  | ✓  |
| PE        | WIP |    |    |    |     |


Supported image formats:

| Image format | C++ | C# | Go | PS | VBA |
|--------------|-----|----|----|----|-----|
| PNG          | ✓  | ✓  | ✓  | ✓  |    |
| BMP          | ✓  | ✓  | ✓  | ✓  | ✓  |
| JPEG         |     |    |    |    |     |


Supported payload delivery methods:

| Payload delivery | C++ | C# | Go | PS | VBA |
|------------------|-----|----|----|----|-----|
| HTTP             | ✓  | ✓  | ✓  | ✓  |    |
| Local file       | ✓  | ✓  | ✓  | ✓  |    |
| Document         |     |    |    |    | ✓ |



## Notes
[roadmap](https://github.com/adeadfed/myaso/projects/1)

### Is it any good?
[yes.](https://news.ycombinator.com/item?id=3067434)
