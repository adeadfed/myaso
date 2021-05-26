using System.IO;
using System.Net;
using System.Drawing;

namespace Reader.Delivery
{
    class Remote : IDelivery
    {
        Bitmap IDelivery.loadImage(string file_uri)
        {
            WebClient client = new WebClient();
            Stream stream = client.OpenRead(file_uri);
            return new Bitmap(stream);
        }
    }
}
