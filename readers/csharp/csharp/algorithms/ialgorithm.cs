using System.Drawing;

namespace Reader.Algorithms
{
    interface IAlgorithm
    {
        void readImage(Bitmap bm, byte[] payload_data);
    }
}
