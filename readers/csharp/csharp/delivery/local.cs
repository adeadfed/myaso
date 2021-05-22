using System.Drawing;

namespace csharp.Delivery
{
    class Local
    {
        public Bitmap load_image(string filename)
        {
            return new Bitmap(filename);
        }
    }
}
