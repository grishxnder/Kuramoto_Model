import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# объявляем переменные
# кол-во хлопающих
kol_obj = 88 
# длина видео
time = 50
# шаг дифф-я
dt = 0.025
# интеравал между двумя кадрами
interval = 0.05
# константный коэф. связи
K = 3

# создаем массивы и заполняем первоначальными данными
# фазы
array_fi = np.random.uniform(0, 2*np.pi, size=(kol_obj, 1))
# угловые частоты
array_omega = np.random.uniform(1/5.5, 1/1, size=(kol_obj, 1))
# связи
array_k = np.full((kol_obj, kol_obj), K)

# заполянем массивы, дифференцируем 
for st in range(int(time/interval)):
    #  добавляем в массивы новые столбики справа
    array_fi = np.append(array_fi, np.zeros((kol_obj, 1)), axis=1)
    array_omega = np.append(array_omega, np.zeros((kol_obj, 1)), axis=1)

    # диф-уем подсчет
    for i in range(int(interval / dt)):
        for j in range(kol_obj):
            sum_sin = 0
            for k in range(kol_obj):
                sum_sin += np.sin(array_fi[k][-1] - array_fi[j][-1]) * array_k[j][k]
            array_fi[j][-1] = array_fi[j][-2] + array_omega[j][0] * dt + (sum_sin / kol_obj) / kol_obj
            array_omega[j][-1] = (array_fi[j][-1] - array_fi[j][-2]) / dt



# создаем окно графиков и настраиваем его 
fig, (graph1, graph2, graph3) = plt.subplots(nrows=1, ncols=3)
fig.set_size_inches(13, 5)
plt.suptitle(f"Проект 'Модель Курамото'\nN = {kol_obj}, video duration = {time} с, fps = {int(1/interval)}, dt = {dt}\nK = {K}", fontname="Arial")
plt.subplots_adjust(wspace=0.3, hspace=0)
graph1.set_xlabel('t, с')
graph1.set_ylabel('φ(t), рад')
graph3.set_xlabel('t, с')
graph3.set_ylabel('ω(t), рад/с')

# время для осей ox
array_time = np.arange(0, time, interval)

# устанавливаем настройки для графиков
graph1.set_xlim(0, array_time[-1])
graph1.set_ylim(np.min(array_fi),
             np.max(array_fi))
graph2.set_xlim(-1.2, 1.2)
graph2.set_ylim(-1.2, 1.2)
graph2.set_aspect('equal')
graph3.set_xlim(0, array_time[-1])
graph3.set_ylim(np.min(array_omega),
             np.max(array_omega))
traectory_krug = np.linspace(0, 2*np.pi, 70)
# строим черную окружность
graph2.plot(np.sin(traectory_krug), np.cos(traectory_krug), color='black', lw=0.1)

# цвета для линий
array_colors = np.random.uniform(0, 1, size=(kol_obj, 3))

# создаем массивы объектов графиков, так как их много
line1_phi = []
for i in range(kol_obj):
    line1_phi.append(graph1.plot([], [], color=array_colors[i])[0])
graph_objects = graph2.scatter([], [], s=20)
line3_w = []
for i in range(kol_obj):
    line3_w.append(graph3.plot([], [], color=array_colors[i])[0])

# строим анимацию
def update(frame):
    x_data2, y_data2 = [], []
    for i in range(kol_obj):
        line1_phi[i].set_xdata(array_time[:frame])
        line1_phi[i].set_ydata(array_fi[i][:frame])
        x_data2.append(np.cos(array_fi[i][frame]))
        y_data2.append(np.sin(array_fi[i][frame]))
        line3_w[i].set_xdata(array_time[:frame])
        line3_w[i].set_ydata(array_omega[i][:frame])
    graph_objects.set_offsets(np.column_stack([x_data2, y_data2]))
    graph_objects.set_color(array_colors)
    return *line1_phi, graph_objects, *line3_w

# инициализируем анимацию и запускаем создание
animation = animation.FuncAnimation(fig, update, frames=int(time/interval), interval=int(interval*1000), blit=True)

# показываем animation
plt.show()