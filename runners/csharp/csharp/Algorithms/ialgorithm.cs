using System.Drawing;

namespace Reader.Algorithms
{
    interface IAlgorithm
    {
        void read(Bitmap bm, byte[] payload_data);
    }
}
