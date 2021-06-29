import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

line = "ACK"

dist = [3, 3, 3, 3, 3]
streng = [10, 10, 10, 10, 10]

# with open("C:/Users/litos/Desktop/IMU/Mag_static.txt", "r") as fileObject:
#     while True:
#         line = fileObject.readline()
#         if not line:
#             break
#         line = line[:-1]
#         linesplitted = line.split(',')
#         dist.append(float(linesplitted[0]))
#         streng.append(float(linesplitted[1]))

dist = np.array(dist)
streng = np.array(streng)

###############################################
############# Calculus ( mean, media, std, var)
N = 50
# Precisão // Precision (diferença entre os valores medidos / Consistencia)
t_student = 1
r_medio     = np.mean(dist)
desvio_pad  = np.std(dist)
variancia   = np.var(dist)
incerteza_abs  = t_student * desvio_pad / (np.sqrt(N)) # Standard Error
incerteza_rel   = incerteza_abs/r_medio

print("Precisão:")
print(f"r = {r_medio} +- {incerteza_abs}")
print(f"r = {r_medio} +- {incerteza_rel*100}%")
print("\n")

# Exactidão // Accuracy (diferença para o valor verdadeiro)
r_verdade = 4 # Mudar para valor verdadeiro
erro_abs = abs(r_medio - r_verdade)
erro_rel = erro_abs/r_verdade
print("Exatidão:")
print(f"r = {r_medio} +- {erro_abs}")
print(f"r = {r_medio} +- {erro_rel*100}%")
print("\n")

# Total
erro_total = incerteza_abs + erro_abs
erro_total_rel = erro_total/r_verdade
print("Erro total:")
print(f"r = {r_medio} +- {erro_total}")
print(f"r = {r_medio} +- {erro_total_rel*100}%")

###############################################
# Graphical Plot
#relação linear y = mx + b (x -> sensor, y -> real) // Regressão linear

x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
y = np.array([5, 15, 25, 35, 45, 55])

model = LinearRegression()
model.fit(x, y)
model = LinearRegression().fit(x, y)

r_sq = model.score(x, y) # R^2
print('coefficient of determination (r^2):', r_sq)

print('intercept (b):', model.intercept_) # b
print('slope (m):', model.coef_) # m

print(f"Equação de regressão linear: {model.coef_}x + {model.intercept_}")

# Prever dados (metodo 1 igual 2)
y_pred = model.predict(x)
print('predicted response:', y_pred, sep='\n')

# Prever dados(metodo 2 igual a 1)
y_pred = model.intercept_ + model.coef_ * x
print('predicted response:', y_pred, sep='\n')

d_x = np.linspace(0, 60, 100).reshape((-1, 1))
d_y = model.predict(d_x)

fig, ax = plt.subplots()
ax.plot(x, y, 'o', label = "Measured points")
ax.plot(d_x, d_y, '-', label = "Linear Regression:")

ax.legend()
ax.set(xlabel='Distance (sensor)', ylabel='Distance (real)') #, title='Total Points vs Stepper Motor Resolution')
ax.grid()
plt.show()