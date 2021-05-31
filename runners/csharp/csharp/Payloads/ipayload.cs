namespace Reader.Payloads
{
    interface IPayload
    {
        void Run(byte[] payload_data);
    }
}
