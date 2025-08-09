import multiprocessing
import psutil
import time
import math
import platform

def stress_test(q, interval=1):
    count = 0
    start = time.time()
    while True:
        math.sqrt(12345)
        count += 1
        elapsed = time.time() - start
        if elapsed >= interval:
            q.put(count / elapsed)  # ops por segundo nesse intervalo
            count = 0
            start = time.time()

def get_cpu_temp():
    if platform.system() == "Windows":
        return None
    temps = psutil.sensors_temperatures()
    if not temps:
        return None
    if "coretemp" in temps:
        return max(t.current for t in temps["coretemp"])
    elif "acpitz" in temps:
        return max(t.current for t in temps["acpitz"])
    return None

def detectar_limite(temp, temp_limite=90):
    if temp is None:
        return "limite de potência (possivelmente)"
    return "limite térmico" if temp >= temp_limite else "limite de potência"

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    print(f"Iniciando teste com {num_cores} processos...")

    q = multiprocessing.Queue()
    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=stress_test, args=(q,))
        p.start()
        processes.append(p)

    freqs_iniciais = []
    freq_estabilizada = None
    tempo_turbo = 0
    temp_max = None
    caiu = False
    desempenho_inicial = []
    desempenho_sustentado = []

    try:
        inicio = time.time()
        while time.time() - inicio < 60:
            freqs = psutil.cpu_freq(percpu=True)
            freq_media = sum(f.current for f in freqs) / len(freqs)
            temp_atual = get_cpu_temp()
            if temp_max is None or (temp_atual and temp_atual > temp_max):
                temp_max = temp_atual

            if not freqs_iniciais:
                freqs_iniciais = [f.current for f in freqs]

            freq_turbo_inicial = max(freqs_iniciais)

            try:
                ops = q.get_nowait()
                if not caiu:
                    desempenho_inicial.append(ops)
                else:
                    desempenho_sustentado.append(ops)
            except:
                pass

            if not caiu and freq_media < freq_turbo_inicial - 300:
                caiu = True
                tempo_turbo = round(time.time() - inicio, 1)
                freq_estabilizada = round(freq_media, 1)

            time.sleep(0.5)  # meio segundo para pegar dados com mais frequência

    except KeyboardInterrupt:
        pass
    finally:
        for p in processes:
            p.terminate()

    freq_turbo_inicial = round(max(freqs_iniciais), 1) if freqs_iniciais else 0
    if not caiu:
        tempo_turbo = 60
        freq_estabilizada = freq_turbo_inicial
        desempenho_sustentado = desempenho_inicial

    media_inicial = round(sum(desempenho_inicial) / len(desempenho_inicial), 2) if desempenho_inicial else 0
    media_sustentada = round(sum(desempenho_sustentado) / len(desempenho_sustentado), 2) if desempenho_sustentado else 0
    queda_percentual = round(100 - (media_sustentada / media_inicial * 100), 1) if media_inicial else 0

    print("\n📊 RESULTADO DO TESTE")
    print(f"Potencial inicial: {media_inicial} operações/s")
    print(f"Potencial sustentado: {media_sustentada} operações/s")
    print(f"Queda de desempenho: {queda_percentual}%")
    print(f"Tempo sustentando turbo: {tempo_turbo} segundos")
    print(f"Frequência turbo inicial: {freq_turbo_inicial} MHz")
    print(f"Frequência após estabilizar: {freq_estabilizada} MHz")
    print(f"Temperatura máxima: {temp_max if temp_max else 'N/A'} °C")
    print(f"Limitação provável: {detectar_limite(temp_max)}")
