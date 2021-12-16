using System.Drawing;

namespace Runner.ImageSources
{
    interface IImageSource
    {
        Bitmap Load(string filename);
    }
}
