from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def learning_model(dataset):
    data = pd.read_csv(dataset)

    X = data.drop(columns=['Score'])
    y = data['Score']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Создание модели линейной регрессии
    model = LinearRegression()

    # Обучение модели на обучающей выборке
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Оценка модели
    mse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--', lw=2, color='red')

    plt.xlabel("Фактические значения")
    plt.ylabel("Предсказанные значения")
    plt.title("Фактические vs Предсказанные значения")
    plt.grid(True)
    plt.show()

    # Создание гистограммы ошибок с наложенной линией плотности распределения
    residuals = y_test - y_pred
    sns.histplot(residuals, kde=True)

    plt.title('Распределение ошибок')
    plt.xlabel('Ошибки')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()


    coefficients = model.coef_
    print("Параметры модели:")
    for i in range(4):
        print(f"W{i+1} = {coefficients[i]}")
        
    print(f"\nСреднеквадратичная ошибка (MSE): {mse}")
    print(f"Cредняя абсолютная ошибка (MAE) : {mae}")
    print(f"Коэффициент детерминации (R^2): {r2}")


