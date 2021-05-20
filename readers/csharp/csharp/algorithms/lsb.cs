using System.Drawing;

namespace csharp.algorithms
{
    class Lsb
    {
        public void read_image(Bitmap bm, byte[] payload_data)
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

                    foreach (byte channel in channels)
                    {
                        if (length <= 0)
                        {
                            return;
                        }

                        payload_data[pos / 8] = get_lsb(payload_data[pos / 8], channel);
                        pos++;
                        length--;
                    }
                }
            }
        }

        private static byte get_lsb(byte target, byte source)
        {
            return (byte)((target << 1) | (source & 1));
        }
    }
}
