# TurboSustain

**TurboSustain** é uma ferramenta simples em Python para testar o desempenho do processador de notebooks e medir:

- O desempenho inicial (pico turbo)  
- Por quanto tempo esse pico se mantém  
- O desempenho sustentado após estabilização  
- Uma indicação do motivo da limitação (térmica ou de potência)  

---

## Por que usar?

Muitos notebooks, especialmente modelos de entrada, limitam o desempenho do processador para economizar bateria e controlar temperatura. Com este teste, você pode:

- Comparar notebooks diferentes com uma métrica simples de “operações por segundo”  
- Saber se o seu notebook mantém o desempenho máximo ou reduz após um tempo  
- Ter uma ideia do motivo da limitação, quando possível  

---

## Como usar

1. Clone o repositório:  
```bash
git clone https://github.com/seu-usuario/TurboSustain.git
cd TurboSustain
