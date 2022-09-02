import matplotlib.pyplot as plt
import numpy as np
import os,sys,inspect

import plotly.graph_objects as go

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from module_1.module_1 import T_1, T_2, PSI_xyzvtq, V_xyz, import_csv_cofigs


work_configs = import_csv_cofigs(2)

# Начальная температура изделия
T_n = work_configs[0]

# Время
t_ = work_configs[1]

# Мощность
q_ = work_configs[2]

# Теплоемкость материала
cp_ = work_configs[3]

# Коэффициент температуропроводности
alpha_ = work_configs[4]

# Скорость сварки
v_ = work_configs[5]

# Коэффициент теплопроводности
lambda_ = work_configs[6]

# Толщина
delta_ = work_configs[7]



def main():
    show_matrix = [[], [], []]

    for i in range(-50,100,5):
        for j in range(-50,100,5):
            V_ = V_xyz(i/100,j/100,0)

            #-----------------------------------------------------------------
            #
            # tmp_  -- переменная, которая по ходу работы основного цикцла
            #          принимает будущее значение Z в каждонй точке графика
            # 
            # Доступны функции:
            #   1) T_1(T_n, V_, t_, q_, cp_, alpha_, v_)
            #   2) T_2(T_n, V_, t_, q_, cp_, alpha_, v_, lambda_, delta_)
            #   3) T_2(T_n, V_, t_, q_, cp_, alpha_, v_, lambda_, delta_) + T_1(T_n, V_, t_, q_, cp_, alpha_, v_) -- Т_предельное
            #   4) PSI_xyzvtq(T_n, V_, t_, q_, cp_, alpha_, v_, lambda_, delta_)
            #
            # Это краткое руководство нужно для ручного тестирования алгоритма расчета распределения температуры
            # Необходимо менять значения для tmp_ -- как функции, так и аргументы
            #
            #-----------------------------------------------------------------

            tmp_ = T_2(T_n, V_, t_, q_, cp_, alpha_, v_, lambda_, delta_) + T_1(T_n, V_, t_, q_, cp_, alpha_, v_)
            


            show_matrix[0].append(V_.x_)
            show_matrix[1].append(V_.y_)
            show_matrix[2].append(tmp_)

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_trisurf(np.array(show_matrix[0]), np.array(show_matrix[1]), np.array(show_matrix[2]), cmap='plasma', linewidth=0, antialiased=False)
    # plt.show()

    fig = go.Figure(data=[go.Mesh3d(
                    x=show_matrix[0],
                    y=(show_matrix[1]),
                    z=(show_matrix[2]),
                    opacity=0.5,
                    color='rgba(244,22,100,0.6)'
                  )])

    fig.show()



if __name__ == "__main__":
    main()