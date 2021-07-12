FROM python:3.9-slim

RUN apt update && apt install -y --no-install-recommends \
            # essentials 
            git \
            gcc \
            libc-dev \
            # cpp builder 
            g++-mingw-w64-i686 \
            g++-mingw-w64-x86-64 \
            # csharp bilder 
            libgdiplus \
            mono-devel  \
            # golang builder
            golang-go 

COPY . /app/myaso
WORKDIR /app/myaso

RUN pip3 install -r requirements.txt
RUN chmod +x /app/myaso/myaso.py
RUN ln -s /app/myaso/myaso.py /usr/bin/myaso
ENTRYPOINT ["/usr/bin/myaso"]
