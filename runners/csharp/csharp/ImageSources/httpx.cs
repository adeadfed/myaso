using System.IO;
using System.Net;
using System.Drawing;

namespace Reader.ImageSources
{
    class HTTPX : IImageSource
    {
        Bitmap IImageSource.load(string file_uri)
        {
            WebClient client = new WebClient();
            Stream stream = client.OpenRead(file_uri);
            return new Bitmap(stream);
        }
    }
}
