using System.Drawing;

namespace Runner.Algorithms
{
    class LSBX : IAlgorithm
    {
        private int channel = 0;
        public LSBX(int channel) => this.channel = channel;


        void IAlgorithm.Read(Bitmap bm, byte[] payload_data)
        {
            int length = payload_data.Length * 8;
            int pos = 0;

            for (int i = 0; i < bm.Height; i++)
            {
                for (int j = 0; j < bm.Width; j++)
                {
                    Color pixel_color = bm.GetPixel(j, i);

                    byte[] channels = {
                        pixel_color.R,
                        pixel_color.G,
                        pixel_color.B
                    };

                    if (length <= 0)
                    {
                        return;
                    }

                    payload_data[pos / 8] = GetLsb(payload_data[pos / 8], channels[channel]);
                    pos++;
                    length--;
                }
            }
        }

        private static byte GetLsb(byte target, byte source)
        {
            return (byte)((target << 1) | (source & 1));
        }
    }
}
