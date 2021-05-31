using System.Drawing;

namespace Reader.ImageSources
{
    class FileSystem : IImageSource
    {
        Bitmap IImageSource.loadImage(string filename)
        {
            return new Bitmap(filename);
        }
    }
}
