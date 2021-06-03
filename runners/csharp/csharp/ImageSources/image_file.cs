using System.Drawing;

namespace Runner.ImageSources
{
    class ImageFile : IImageSource
    {
        Bitmap IImageSource.load(string filename)
        {
            return new Bitmap(filename);
        }
    }
}
