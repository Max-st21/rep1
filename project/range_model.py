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


weights=[0.84665087,0.67125038,0.92194114,0.71525979]

def main():
    weights=[0.84665087,0.67125038,0.92194114,0.71525979]

if __name__ == '__main__':  
    main()
'''
np.random.seed(42)

# Генерация данных
data = {
    "I": np.random.randint(0, 6, 2000)*2,  # Количество совпадающих категорий (0-5)
    "R": np.round(np.random.uniform(0,1,2000),2)+ np.clip(np.random.normal(3.8, 0.6, 2000),1, 4),  # Средний рейтинг места (1.00-5.00)
    "F": np.random.choice([0, 10], 2000, p=[0.9, 0.1]),  # Наличие в избранном (0 или 10)
    "P": np.random.choice([0, -10], 2000, p=[0.8, 0.2]),  # Наличие в других маршрутах (0 или -10)
}

# Рассчитываем итоговый рейтинг R с хорошей корреляцией с I, F, P
data["Score"] = np.clip(
    data["I"] + data["R"] + data["F"] + data["P"] + np.random.normal(0, 3, 2000),
    1, 25  # Ограничиваем диапазон от 1 до 25
).astype(int)

# Создаем DataFrame
df = pd.DataFrame(data)

df.to_csv('algdata.csv', index=False)
'''

