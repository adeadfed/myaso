using System.IO;
using System.Net;
using System.Drawing;

namespace csharp.Delivery
{
    class Remote
    {
        public Bitmap load_image(string file_uri)
        {
            WebClient client = new WebClient();
            Stream stream = client.OpenRead(file_uri);
            return new Bitmap(stream);
        }
    }
}
