# 📡 Comunicação via STDIN com Código de Hamming (7,4)

<iframe width="560" height="315" src="https://youtu.be/7y7draDocxY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 📋 Descrição da Atividade - Ponderada de Enlace

A atividade consiste na criação de dois processos distintos — **remetente** e **destinatário** — que se comunicam via `stdin` e `stdout`, simulando a **camada de enlace de dados** de uma rede. A camada de enlace é responsável por garantir a entrega correta e confiável de quadros (frames) entre dois nós conectados diretamente.

O objetivo é:

- Codificar um **payload binário** com um protocolo próprio.
- Adicionar **códigos de detecção/correção de erro (Hamming)**.
- Transferir via `stdout`.
- Sincronizar e decodificar corretamente no destinatário.
- Corrigir **um único erro de bit**, se presente.

## 🧠 Conceitos Envolvidos

### 🧱 Camada de Enlace

A camada de enlace é a segunda camada do modelo OSI e trata da comunicação entre dois dispositivos na mesma rede. Ela é responsável por:
- Empacotar os dados em quadros (frames);
- Sincronizar a transmissão;
- Detectar e corrigir erros.

Nesta atividade, simulamos isso utilizando entrada/saída padrão e manipulando strings de bits com códigos de Hamming.

## 🔐 Protocolo Definido

Cada frame é composto por três partes:

```
Frame = [Cabeçalho][Payload Codificado com Hamming][Terminador]
```

- **Cabeçalho**: `"10101010"` (8 bits) → usado para sincronização.
- **Terminador**: `"01010101"` (8 bits) → marca o fim do frame.
- **Payload Codificado**: Para cada 4 bits de dados, aplicamos Hamming (7,4) → viram 7 bits.

## 🔢 Exemplo de Frame

Entrada original: `0110`

1. Aplicando Hamming (7,4) sobre `0110` → `1100110`
2. Adicionando cabeçalho e terminador:

```
Frame Final = 10101010 + 1100110 + 01010101
```

## 🔄 Funcionamento das Funções

### ✉️ `create_frame(payload)`

```python
def create_frame(payload):
    encoded_payload = "".join(hamming_encode(payload[i:i+4]) for i in range(0, len(payload), 4))
    return f"{header}{encoded_payload}{terminator}"
```

1. Divide o `payload` original em blocos de 4 bits.
2. Aplica `hamming_encode()` em cada bloco.
3. Junta todos os blocos codificados.
4. Adiciona cabeçalho e terminador.

### 🛠️ `hamming_encode(data_bits)`

Codifica 4 bits (`d1`, `d2`, `d3`, `d4`) em 7 bits, com bits de paridade `p1`, `p2`, `p3`.

```
Ordem dos bits: p1 p2 d1 p3 d2 d3 d4
```

Os bits de paridade são calculados para garantir que erros de 1 bit possam ser detectados e corrigidos.

### 🧪 `hamming_decode(hamming_code)`

```python
def hamming_decode(hamming_code):
    bits = [int(bit) for bit in hamming_code]
    p1, p2, d1, p3, d2, d3, d4 = bits
    c1 = p1 ^ d1 ^ d2 ^ d4
    c2 = p2 ^ d1 ^ d3 ^ d4
    c3 = p3 ^ d2 ^ d3 ^ d4
    error_pos = c1 * 1 + c2 * 2 + c3 * 4
    if error_pos:
        bits[error_pos - 1] ^= 1
    return f"{bits[2]}{bits[4]}{bits[5]}{bits[6]}"
```

1. Lê os 7 bits codificados.
2. Calcula os bits de verificação `c1`, `c2`, `c3`.
3. Se houver erro, determina qual é o bit incorreto.
4. Corrige o erro, se necessário.
5. Retorna os 4 bits originais.

## ✅ Testes Realizados

Durante o vídeo explicativo, os seguintes testes foram realizados:

### 🧪 1. Sincronização correta

- Mostrar que o destinatário ignora qualquer coisa antes do cabeçalho e só começa a processar depois do mesmo.

### 🧪 2. Transmissão sem erro

```bash
./remetente 0110 | ./destinatario
# Esperado: 0110
```

### 🧪 3. Transmissão com erro de 1 bit

Simular erro trocando um bit no frame antes de ser enviado ao destinatário.

```bash
echo "101010101100010000000000" | ./destinatario
# Esperado: 0110 (mesmo com erro)
```

## 🧰 Curiosidade: Outras Técnicas de Detecção/Correção

Mencionei no vídeo que o Hamming pega apenas erros de 1 bit para corrigí-los. Mas e quando há múltiplos erros? Abaixo temos diferentes técnicas para serem aplicadas de acordo com a necessidade da comunicação.


| Técnica                     | Corrige Erros? | Detecta Quantos? | Observações |
|----------------------------|----------------|------------------|-------------|
| Paridade simples           | ❌             | 1 bit            | Detecta, mas não corrige |
| CRC (Cyclic Redundancy Check) | ❌         | Vários           | Muito usado em redes reais |
| Hamming (7,4)              | ✅             | 1 bit            | Corrige 1 bit |
| Hamming (8,4) SECDED       | ✅             | Corrige 1, detecta 2 |
| Código de repetição        | ✅             | Corrige 1 (de 3) | Ineficiente |
