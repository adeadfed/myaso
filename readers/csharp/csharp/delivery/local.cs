using System.Drawing;

namespace csharp.delivery
{
    class Local
    {
        public Bitmap load_image(string filename)
        {
            return new Bitmap(filename);
        }
    }
}
