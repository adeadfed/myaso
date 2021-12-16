using System.Drawing;

namespace Runner.ImageSources
{
    class ImageFile : IImageSource
    {
        Bitmap IImageSource.Load(string filename) => new Bitmap(filename);
    }
}
