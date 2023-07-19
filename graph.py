import matplotlib.pyplot as plt

n_values = [2, 4, 8, 16]
time_values = [21418, 74361, 237297, 442852]  # Valores de tempo em milissegundos

plt.plot(n_values, time_values, marker='o')
plt.xlabel('Número de Processos (n)')
plt.ylabel('Tempo (ms)')
plt.title('Tempo necessário para gerar o arquivo completo')
plt.grid(True)
plt.show()
