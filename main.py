import time
import multiprocessing as mp

def heavy_work(n):
    total = 0
    for i in range(n):
        total += (i * i) % 1234567
    return total

def run_test(total_iter=40_000_000, queda_threshold=0.85, tempo_confirmacao=3, limite_tempo=60):
    num_cores = mp.cpu_count()
    iter_por_core = total_iter // num_cores

    print(f"Usando {num_cores} núcleos...")
    pool = mp.Pool(processes=num_cores)

    pico_ops = 0
    tempo_inicio_pico = 0
    queda_inicio = None
    inicio_teste = time.time()

    while True:
        inicio = time.time()
        pool.map(heavy_work, [iter_por_core] * num_cores)
        duracao = time.time() - inicio
        ops = (total_iter / duracao)

        # Atualiza pico
        if ops > pico_ops:
            pico_ops = ops
            tempo_inicio_pico = time.time()
            queda_inicio = None

        # Detecta queda sustentada
        if ops < pico_ops * queda_threshold:
            if queda_inicio is None:
                queda_inicio = time.time()
            elif time.time() - queda_inicio >= tempo_confirmacao:
                duracao_pico = queda_inicio - tempo_inicio_pico
                print(f"\nPico terminou após {duracao_pico:.2f} segundos")
                print(f"Operações/s no pico: {pico_ops:,.2f}")
                print(f"Operações/s sustentadas: {ops:,.2f}")
                print(f"Queda: {(1 - ops/pico_ops) * 100:.1f}%")
                break
        else:
            queda_inicio = None

        print(f"Ops/s: {ops:,.2f}", end="\r")

        # Se passar do tempo limite sem queda
        if time.time() - inicio_teste >= limite_tempo:
            print("\n⚡ O desempenho não reduziu no período de teste.")
            print(f"Operações/s sustentadas: {ops:,.2f}")
            print(f"Operações/s de pico: {pico_ops:,.2f}")
            break

    pool.close()
    pool.join()

if __name__ == "__main__":
    run_test()
