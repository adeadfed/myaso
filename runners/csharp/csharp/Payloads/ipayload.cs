namespace Runner.Payloads
{
    interface IPayload
    {
        void run(byte[] payload_data);
    }
}
