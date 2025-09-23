from scipy.optimize import curve_fit 
from numpy import array, exp, log
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from math import sqrt


values_x = array([1,1.71,2.42,3.13,3.84,4.55,5.26,5.97])
values_y = array([12.49,4.76,2.55,1.6,1.11,0.82,0.63,0.5]) 
def mapping1(values_x, a, b): 
    return a * values_x + b 

def mapping2(values_x, a): 
    return a ** values_x

def mapping3(values_x, a, b): 
    return a * exp(b * values_x)

def mapping4(values_x, a, b,c): 
    return a * (values_x ** 2) + b * values_x + c

def mapping5(values_x, a, b): 
    return a * (values_x ** b)

def mapping6(values_x, a, b): 
    return a * log(values_x) + b

args, covar = curve_fit(mapping1, values_x, values_y) 
print("Arguments: ", args) 
print("Co-Variance: ", covar)
a, b = args[0], args[1]
model1= a * values_x + b

args, covar = curve_fit(mapping2, values_x, values_y) 
print("Arguments: ", args)
print("Co-Variance: ", covar)
a = args[0]
model2=a ** values_x

args, covar = curve_fit(mapping3, values_x, values_y) 
print("Arguments: ", args)
print("Co-Variance: ", covar)
a, b = args[0], args[1]
model3= a * exp(b * values_x)

args, covar = curve_fit(mapping4, values_x, values_y) 
print("Arguments: ", args)
print("Co-Variance: ", covar)
a, b, c = args[0], args[1], args[2]
model4= a * (values_x ** 2) + b * values_x + c

args, covar = curve_fit(mapping5, values_x, values_y) 
print("Arguments: ", args)
print("Co-Variance: ", covar)
a, b = args[0], args[1]
model5= a * (values_x ** b)

args, covar = curve_fit(mapping6, values_x, values_y) 
print("Arguments: ", args)
print("Co-Variance: ", covar)
a, b = args[0], args[1]
model6= a * log(values_x) + b

model=model6
print("RMSE=",sqrt(mean_squared_error(values_y,model)),"\nMAPE=",mean_absolute_percentage_error(values_y,model),"\nR^2=",r2_score(values_y,model))

plt.plot(values_x, model1, label="Линейная")
plt.plot(values_x, model2, label="Показательная")
plt.plot(values_x, model3, label="Экспоненциальная")
plt.plot(values_x, model4, label="Полиномиальная")
plt.plot(values_x, model5, label="Степенная")
plt.plot(values_x, model6, label="Логарифмическая")

plt.scatter(values_x,values_y, label="Данные")
plt.xlabel('x') 
plt.ylabel('y') 
plt.legend(loc = 'best', fancybox = True, shadow = True) 
plt.grid(True) 
plt.show()

