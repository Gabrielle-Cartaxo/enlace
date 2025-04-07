import sys

def hamming_encode(data):
    """Codifica a sequência de bits usando o código de Hamming (7,4)"""
    data = [int(bit) for bit in data]
    
    # Bits de dados (4 bits de entrada)
    d1, d2, d3, d4 = data[0], data[1], data[2], data[3]

    # Bits de paridade
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    return f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"

def create_frame(payload):
    header = "10101010"
    terminator = "01010101"
    encoded_payload = "".join(hamming_encode(payload[i:i+4]) for i in range(0, len(payload), 4))
    return f"{header}{encoded_payload}{terminator}"

if __name__ == "__main__":
    payload = sys.argv[1]  # Obtém entrada via argumento de linha de comando
    frame = create_frame(payload)
    print(frame)  # Envia para stdout
