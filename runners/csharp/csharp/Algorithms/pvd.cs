using System;
using System.Collections;
using System.Drawing;
using static System.Net.Mime.MediaTypeNames;

namespace Runner.Algorithms
{
    class PVD : IAlgorithm
    {
        void IAlgorithm.Read(Bitmap bm, byte[] payload_data)
        {
            int length = payload_data.Length * 8;
            // worst case scenario -- every two pixels contain 1 bit of information
            byte[] pixel_pairs = new byte[length * 2]; 

            for (int i = 0, k = 0; i < bm.Height && k < length * 2; i++)
            {
                for (int j = 0; j < bm.Width && k < length * 2; j++)
                {
                    // in grayscale R,G,B values are the same
                    pixel_pairs[k] = bm.GetPixel(j, i).R;
                    k++;
                }
            }

            // add space for extra byte padding at the end
            BitArray payload_bits = new BitArray(length + 8);
            int bits_read = 0;

            for (int i = 0; i < length * 2; i += 2)
            {
                byte d_stego = (byte)Math.Abs(pixel_pairs[i + 1] - pixel_pairs[i]);
                byte n = GetClosestPerfectSquare(d_stego);
                if (d_stego >= 240)
                {
                    GetNLsb(payload_bits, bits_read, d_stego, 4);
                    bits_read += 4;
                }
                else
                {
                    byte m = (byte)Math.Floor(Math.Log(2 * n) / Math.Log(2));
                    byte range_mid = (byte)(Math.Pow(n, 2) + n - Math.Pow(2, m));
                    if (d_stego < range_mid)
                    {
                        GetNLsb(payload_bits, bits_read, d_stego, m + 1);
                        bits_read += m + 1;
                    }
                    else
                    {
                        GetNLsb(payload_bits, bits_read, d_stego, m);
                        bits_read += m;
                    }
                }

                if (bits_read >= length)
                {
                    Buffer.BlockCopy(ToByteArray(payload_bits), 0, payload_data, 0, payload_data.Length);
                    return;
                }
            }
        }

        private static void GetNLsb(BitArray payload_bits, int offset, byte source, int count)
        {
            for (int i = count - 1, j = 0; i >= 0; i--, j++)
            {
                bool lsb = Convert.ToBoolean((source >> i) & 1);
                payload_bits.Set(offset + j, lsb);
            }
        }


        private static byte[] ToByteArray(BitArray bit_array)
        {
            int byte_count = (int)Math.Ceiling(bit_array.Count / 8.0);

            byte[] byte_array = new byte[byte_count];
            int byte_pos = 0, bit_pos = 0;

            for (int i = 0; i < bit_array.Count; i++)
            {
                if (bit_array[i])
                {
                    byte_array[byte_pos] |= (byte)(1 << (7 - bit_pos));
                }
                    
                bit_pos++;

                if (bit_pos == 8)
                {
                    bit_pos = 0;
                    byte_pos++;
                }
            }

            return byte_array;
        }


        private static byte GetClosestPerfectSquare(byte d)
        {
            switch (d)
            {
                case byte n when (n < 2):
                    return 1;
                case byte n when (n >= 2 && n < 6):
                    return 2;
                case byte n when (n >= 6 && n < 12):
                    return 3;
                case byte n when (n >= 12 && n < 20):
                    return 4;
                case byte n when (n >= 20 && n < 30):
                    return 5;
                case byte n when (n >= 30 && n < 42):
                    return 6;
                case byte n when (n >= 42 && n < 56):
                    return 7;
                case byte n when (n >= 56 && n < 72):
                    return 8;
                case byte n when (n >= 72 && n < 90):
                    return 9;
                case byte n when (n >= 90 && n < 110):
                    return 10;
                case byte n when (n >= 110 && n < 132):
                    return 11;
                case byte n when (n >= 132 && n < 156):
                    return 12;
                case byte n when (n >= 156 && n < 182):
                    return 13;
                case byte n when (n >= 182 && n < 210):
                    return 14;
                case byte n when (n >= 210 && n < 240):
                    return 15;
                case byte n when (n >= 240):
                    return 16;
                default:
                    return 0;
            }
        }
    }
}
