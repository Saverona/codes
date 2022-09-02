import math
import scipy.integrate
import csv



# Вспомогательный класс, имеет смысл точки с координатами x,y,z
class V_xyz():
    x_ = 0
    y_ = 0
    z_ = 0

    def __init__(self, x, y, z):
        self.x_ = x
        self.y_ = y
        self.z_ = z

# Функция для импортирования настроек из конфигурационного csv файла, принимает 1 аргумент - число - номер модуля
def import_csv_cofigs(module_num):
    try:
        # Начальная температура изделия
        T_n = 0

        # Время
        t_ = 0

        # Мощность
        q_ = 0

        # Теплоемкость материала
        cp_ = 0

        # Коэффициент температуропроводности
        alpha_ = 0

        # Скорость сварки
        v_ = 0

        # Коэффициент теплопроводности
        lambda_ = 0

        # Толщина
        delta_ = 0

        mainDialect = csv.Dialect
        mainDialect.doublequote = True
        mainDialect.quoting = csv.QUOTE_ALL
        mainDialect.delimiter = ';'
        mainDialect.lineterminator = '\n'
        mainDialect.quotechar = '"'
        with open(f'module_{module_num}/module_{module_num}_input.csv', 'r', encoding='utf8') as fr:
            file_reader = csv.reader(fr, dialect=mainDialect)

            for cnf_row in file_reader:
                if cnf_row[0] == '1':
                    T_n = float(cnf_row[2])
                if cnf_row[0] == '2':
                    t_ = float(cnf_row[2])
                if cnf_row[0] == '3':
                    q_ = float(cnf_row[2])
                if cnf_row[0] == '4':
                    cp_ = float(cnf_row[2])
                if cnf_row[0] == '5':
                    alpha_ = float(cnf_row[2])
                if cnf_row[0] == '6':
                    v_ = float(cnf_row[2])
                if cnf_row[0] == '7':
                    lambda_ = float(cnf_row[2])
                if cnf_row[0] == '8':
                    delta_ = float(cnf_row[2])

        return (T_n, t_, q_, cp_, alpha_, v_, lambda_, delta_)

    except Exception as e:
        print('[ERROR] Config import error!: ', e)

# Формула для состояния температурного поля при воздействии быстро движущегося точечного источника
def T_1(T_n, V_, t_, q_, cp_, a_, v_):
    """
    T_n - начальная температура изделия
    x_ - координата x
    t_ - время
    q_ - мощность
    cp_ - теплоемкость материала
    a_ - коэффициент температуропроводности
    v_ - скорость сварки
    R_ - длина радиус-вектора
    """

    R_ = math.sqrt(V_.x_**2 + V_.y_**2 + V_.z_**2)

    # Функция - подинтегральное выражение
    def f_(t_1):
        tau_ = t_1
        return math.exp((-v_**2 * tau_)/(4*a_) - (R_**2)/(4*a_*tau_))*(1/(tau_**(3/2)))

    i_ = scipy.integrate.quad(f_, 0, t_, limit=1)
    return T_n + ((2*q_)/(cp_*math.sqrt((4*math.pi*a_)**3))) * math.exp((-v_*V_.x_)/(2*a_)) * i_[0]

# Формула для состояния температурного поля при воздействии быстро движущегося линейного источника
def T_2(T_n, V_, t_, q_, cp_, a_, v_, lambda_, delta_):
    """
    T_n - начальная температура изделия
    x_ - координата x
    t_ - время
    q_ - мощность
    cp_ - теплоемкость материала
    a_ - коэффициент температуропроводности
    v_ - скорость сварки
    lambda_ - коэффициент теплопроводности
    delta_ - толщина
    """

    # Функция - подинтегральное выражение
    def f_(t_1):
        tau_ = t_1
        return math.exp( (-v_**2 * tau_)/(4*a_) - (2*lambda_*tau_)/(cp_*delta_) - (V_.x_**2+V_.y_**2)/(4*a_*tau_) ) * (1/tau_)

    i_ = scipy.integrate.quad(f_, 0, t_, limit=1)
    return T_n + ((q_)/(4*math.pi*lambda_*delta_)) * math.exp((-v_*V_.x_)/(2*a_)) * i_[0]

# Функция ψ(x, y, z, v, t, q)
def PSI_xyzvtq(T_n, V_, t_, q_, cp_, a_, v_, lambda_, delta_):
    """
    T_n - начальная температура изделия
    x_ - координата x
    t_ - время
    q_ - мощность
    cp_ - теплоемкость материала
    a_ - коэффициент температуропроводности
    v_ - скорость сварки
    lambda_ - коэффициент теплопроводности
    delta_ - толщина
    T_t - температура в стадии теплонасыщения
    """

    T_1_result = T_1(T_n, V_, t_, q_, cp_, a_, v_)
    T_2_result = T_2(T_n, V_, t_, q_, cp_, a_, v_, lambda_, delta_)
    T_t = (T_1_result + T_2_result) * 0.9
    return (T_t - T_n)/(T_1_result+T_2_result-T_n)
