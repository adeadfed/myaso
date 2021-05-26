from bitarray import bitarray


class IAlgorithm:
    @staticmethod
    def embed(payload: bitarray, output_file: str, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def extract(input_file: str, payload_bits: int, *args, **kwargs) -> bitarray:
        raise NotImplementedError
