using System.Drawing;

namespace Reader.ImageSources
{
    interface IImageSource
    {
        Bitmap loadImage(string filename);
    }
}
