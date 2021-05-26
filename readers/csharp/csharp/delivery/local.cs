using System.Drawing;

namespace Reader.Delivery
{
    class Local : IDelivery
    {
        Bitmap IDelivery.loadImage(string filename)
        {
            return new Bitmap(filename);
        }
    }
}
