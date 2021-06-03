using System.Drawing;

namespace Runner.Algorithms
{
    interface IAlgorithm
    {
        void read(Bitmap bm, byte[] payload_data);
    }
}
