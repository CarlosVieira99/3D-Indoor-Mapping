import serial
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import time

dist = []
streng = []
dist_sensor = []
dist_real = []
dist_error = []
count = 0

with open("testfile3.txt", "a") as f:
    with serial.Serial('COM3', 115200, timeout=1) as ser:
        while True:
            r_verdade = float(input("Value of next distance, S to stop: "))
            if(r_verdade== 0):
                break
            ser.write("C".encode("UTF-8"))
            time.sleep(1)
            while(ser.inWaiting()):
                data = ser.readline().decode("UTF-8")[:-2] # Read the newest output from the Arduino
                f.write(data+ "\n")
                data = data.split(',')
                dist.append(float(data[0])/1000)
                streng.append(float(data[1]))

            dist2 = np.array(dist)
            streng2 = np.array(streng)
            #print(dist)
            dist = []
            streng = []

            ###############################################
            ############# Calculus ( mean, media, std, var)
            N = 50
            # Precisão // Precision (diferença entre os valores medidos / Consistencia)
            t_student = 1
            r_medio         = np.mean(dist2)
            desvio_pad      = np.std(dist2)
            variancia       = np.var(dist2)
            incerteza_abs   = t_student * desvio_pad / (np.sqrt(N)) # Standard Error
            incerteza_rel   = incerteza_abs/r_medio

            #print(f"Ponto nº {count}")
            #print("Precisão:")
            #print(f"r = {round(r_medio, 3)} +- {round(incerteza_abs, 3)}")
            #print(f"r = {round(r_medio, 3)} +- {round(incerteza_rel*100, 3)}%")

            # Exactidão // Accuracy (diferença para o valor verdadeiro)
            erro_abs = abs(r_medio - r_verdade)
            erro_rel = erro_abs/r_verdade
            #print("Exatidão:")
            #print(f"r = {round(r_medio, 3)} +- {round(erro_abs, 3)}")
            #print(f"r = {round(r_medio, 3)} +- {round(erro_rel*100, 3)}%")

            # Total
            erro_total = incerteza_abs + erro_abs
            erro_total_rel = erro_total/r_verdade
            #print("Erro total:")
            #print(f"r = {round(r_medio, 3)} +- {round(erro_total, 3)}")
            #print(f"r = {round(r_medio, 3)} +- {round(erro_total_rel*100, 3)}%")

            print(f'{r_verdade} {round(r_medio, 3)} {round(incerteza_abs, 3)} {round(incerteza_rel*100, 3)} {round(erro_abs, 3)} {round(erro_rel*100, 3)} {round(erro_total, 3)} {round(erro_total_rel*100, 3)}')

            dist_sensor.append(r_medio)
            dist_real.append(r_verdade)
            dist_error.append(erro_total)

            dist = []
            streng = []
            count = count + 1

        ###############################################
        # Graphical Plot
        #relação linear y = mx + b (x -> sensor, y -> real) // Regressão linear

        dist_sensor = np.array(dist_sensor)
        dist_sensor = dist_sensor.reshape((-1, 1))
        dist_real = np.array(dist_real)

        model = LinearRegression()
        model.fit(dist_sensor, dist_real)
        model = LinearRegression().fit(dist_sensor, dist_real)

        r_sq = model.score(dist_sensor, dist_real) # R^2
        print('coefficient of determination (r^2):', r_sq)

        print('intercept (b):', model.intercept_) # b
        print('slope (m):', model.coef_) # m

        print(f"Equação de regressão linear: y = {model.coef_}x + {model.intercept_}")

        f.write(f'y=y = {model.coef_}x + {model.intercept_}, r^2={r_sq}'+ "\n")
        np.savetxt("array_dist_sensor3.txt", dist_sensor, delimiter=',', fmt="%s")
        np.savetxt("array_dist_real3.txt", dist_real, delimiter=',', fmt="%s")

        # Prever dados (metodo 1 igual 2)
        #y_pred = model.predict(dist_sensor)
        #print('predicted response:', y_pred, sep='\n')

        # Prever dados(metodo 2 igual a 1)
        #y_pred = model.intercept_ + model.coef_ * x
        #print('predicted response:', y_pred, sep='\n')

        d_x = np.linspace(min(dist_sensor), max(dist_sensor), 1000).reshape((-1, 1))
        d_y = model.predict(d_x)

        fig, ax = plt.subplots()
        ax.plot(dist_sensor, dist_real, 'o', label = "Measured points")
        ax.plot(d_x, d_y, '--', label = "Linear Regression:")

        plt.figure()

        plt.plot(dist_real, dist_error, 'o', label = "Measurement error")

        plt.xlim(0, max(dist_real))

        d1 = np.arange(0.00, 6.00, 0.01)
        error1 = np.ones(len(d1))*0.06

        plt.plot(d1, error1, '--', label="Datasheet error")
        plt.grid()
        #plt.plot(d_x, d_y, '-', label = "Linear Regression:")

        ax.legend()
        plt.legend()
        ax.set(xlabel='Distance (sensor)', ylabel='Distance (real)') #, title='Total Points vs Stepper Motor Resolution')
        ax.grid()
        plt.show()

        # Data for plotting

        #ax.set(xlabel='Detecting range (m)', ylabel='Error (m)', title='Lidar accuracy')