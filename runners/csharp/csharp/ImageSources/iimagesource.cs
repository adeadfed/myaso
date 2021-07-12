using System.Drawing;

namespace Runner.ImageSources
{
    interface IImageSource
    {
        Bitmap load(string filename);
    }
}
