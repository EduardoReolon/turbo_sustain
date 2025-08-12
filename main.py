import time

def heavy_work(n=10_000_000):
    total = 0
    for i in range(n):
        total += (i * i) % 1234567
    return total

# Configurações
queda_threshold = 0.85  # queda de 15% ou mais para considerar perda de pico
tempo_confirmacao = 3   # segundos para confirmar que o pico acabou

# Variáveis de controle
pico_ops = 0
tempo_pico = 0
queda_inicio = None
pico_terminou = False

print("Iniciando teste... (Ctrl+C para parar)")
while True:
    inicio = time.time()
    heavy_work()
    duracao = time.time() - inicio
    ops = 1 / duracao

    # Captura o maior valor como pico
    if ops > pico_ops:
        pico_ops = ops
        tempo_pico = time.time()
        queda_inicio = None

    # Verifica se caiu abaixo do threshold
    if ops < pico_ops * queda_threshold:
        if queda_inicio is None:
            queda_inicio = time.time()
        elif time.time() - queda_inicio >= tempo_confirmacao and not pico_terminou:
            pico_terminou = True
            duracao_pico = queda_inicio - tempo_pico
            print(f"\nPico terminou após {duracao_pico:.2f} segundos")
            print(f"Operações/s no pico: {pico_ops:.2f}")
            print(f"Operações/s sustentadas: {ops:.2f}")
            print(f"Queda: {(1 - ops/pico_ops) * 100:.1f}%\n")
            break
    else:
        queda_inicio = None

    print(f"Ops/s: {ops:.2f}", end="\r")