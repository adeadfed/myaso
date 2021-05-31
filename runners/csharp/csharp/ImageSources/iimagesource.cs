using System.Drawing;

namespace Reader.ImageSources
{
    interface IImageSource
    {
        Bitmap load(string filename);
    }
}
