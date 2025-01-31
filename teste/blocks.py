def split_into_blocks(data: bytes, block_size: int = 8):
    """Divide os dados em blocos de 64 bits (8 bytes)."""
    return [data[i: i + block_size] for i in range(0, len(data), block_size)]

def pad_block(block: bytes, block_size: int = 8):
    """Preenche o bloco para garantir 64 bits."""
    while len(block) < block_size:
        block += b' '
    return block
