namespace Runner.Payloads
{
    interface IPayload
    {
        void Run(byte[] payload_data);
    }
}
