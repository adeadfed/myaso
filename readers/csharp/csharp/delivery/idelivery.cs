using System.Drawing;

namespace Reader.Delivery
{
    interface IDelivery
    {
        Bitmap loadImage(string filename);
    }
}
