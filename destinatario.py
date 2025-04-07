import sys

def hamming_decode(hamming_code):
    """Decodifica e corrige erros usando código de Hamming (7,4)"""
    bits = [int(bit) for bit in hamming_code]
    
    # Bits de paridade e dados
    p1, p2, d1, p3, d2, d3, d4 = bits
    
    # Verificar erros
    c1 = p1 ^ d1 ^ d2 ^ d4
    c2 = p2 ^ d1 ^ d3 ^ d4
    c3 = p3 ^ d2 ^ d3 ^ d4

    error_pos = c1 * 1 + c2 * 2 + c3 * 4  # Determina a posição do erro

    if error_pos:
        bits[error_pos - 1] ^= 1  # Corrige o erro

    return f"{bits[2]}{bits[4]}{bits[5]}{bits[6]}"

def extract_payload(frame):
    """Extrai e decodifica o payload do frame"""
    header = "10101010"
    terminator = "01010101"

    if frame.startswith(header) and frame.endswith(terminator):
        frame = frame[len(header):-len(terminator)]
        return "".join(hamming_decode(frame[i:i+7]) for i in range(0, len(frame), 7))
    else:
        raise ValueError("Frame inválido ou corrompido!")

if __name__ == "__main__":
    frame = sys.stdin.read().strip()  # Lê da entrada padrão
    try:
        original_data = extract_payload(frame)
        print(original_data)
    except ValueError as e:
        print(e)
