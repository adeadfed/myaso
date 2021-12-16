using System.Drawing;

namespace Runner.Algorithms
{
    interface IAlgorithm
    {
        void Read(Bitmap bm, byte[] payload_data);
    }
}
