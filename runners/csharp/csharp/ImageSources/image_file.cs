using System.Drawing;

namespace Reader.ImageSources
{
    class ImageFile : IImageSource
    {
        Bitmap IImageSource.load(string filename)
        {
            return new Bitmap(filename);
        }
    }
}
