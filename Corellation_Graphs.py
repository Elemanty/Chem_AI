# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:42:13 2024

@author: Adelina
"""

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.feature_selection import VarianceThreshold

# Получаем путь к директории, где находится скрипт
base_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу с данными
data_path = os.path.join(base_dir, 'full_dataset.csv')

# Загрузка датасета
df = pd.read_csv(data_path)
df_numeric = df.select_dtypes(exclude=['object']).copy()

# Хитмап всего датасета
correlation_matrix = df_numeric.corr()
plt.figure(figsize=(20, 16))  
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
# # plt.show()

# Вычисление корреляционной матрицы
correlation_matrix = df_numeric.corr().abs()
# Создание маски для верхнего треугольника корреляционной матрицы
upper_triangle = np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
# Применение маски к корреляционной матрице
upper_corr_matrix = correlation_matrix.where(upper_triangle)
# Удаление признаков с высокой корреляцией
threshold = 0.9  
to_drop = [column for column in upper_corr_matrix.columns if any(upper_corr_matrix[column] > threshold)]
# Создание нового DataFrame без сильно коррелированных признаков
df_reduced = df_numeric.drop(columns=to_drop)
# # print(f"Удаленные признаки: {to_drop}")

# Хитмап для очищенного датасета
plt.figure(figsize=(20, 16))
sns.heatmap(df_reduced.corr(), annot=False, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Reduced Dataset')
# # plt.show()

# # df_reduced.info()

def variance_threshold(df,th):
    var_thres=VarianceThreshold(threshold=th)
    var_thres.fit(df)
    new_cols = var_thres.get_support()
    return df.iloc[:,new_cols]

df_variance = variance_threshold(df_reduced, 0)

# Хитмап для очищенного очищенного датасета
plt.figure(figsize = (20, 16))
sns.heatmap(df_variance.corr(), annot=False, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Reduced Dataset 2')
# # plt.show()