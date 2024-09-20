# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:42:13 2024

@author: Adelina
"""

#%%
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import pearsonr
from scipy.stats import spearmanr

#%%
# Получаем путь к директории, где находится скрипт
base_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу с данными
data_path = os.path.join(base_dir, 'full_dataset.csv')

# Загрузка датасета
df = pd.read_csv(data_path)
df_numeric = df.select_dtypes(exclude=['object']).copy()
print(df.columns)

#%%
# Хитмап всего датасета
correlation_matrix = df_numeric.corr()
plt.figure(figsize=(20, 16))  
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')

#%%
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

#%%
# Хитмап для очищенного датасета
plt.figure(figsize=(20, 16))
sns.heatmap(df_reduced.corr(), annot=False, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Reduced Dataset')

#%%
def variance_threshold(df_reduced,th):
    var_thres=VarianceThreshold(threshold=th)
    var_thres.fit(df_reduced)
    new_cols = var_thres.get_support()
    return df_reduced.iloc[:,new_cols]

df_variance = variance_threshold(df_reduced, 0)

#%%
# Хитмап для очищенного очищенного датасета
plt.figure(figsize = (20, 16))
sns.heatmap(df_variance.corr(), annot=False, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Reduced Dataset 2')

#%%
is_psychedelic = 'is_psychedelic'
correlations = df_variance.corr()[is_psychedelic].drop(is_psychedelic)

#%%
# Создаем точечные графики для каждой переменной
features = df_variance.columns.drop(is_psychedelic)
for feature in features:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_variance, x=feature, y=is_psychedelic)
    correlation, p_value = pearsonr(df_variance[feature], df_variance[is_psychedelic])
    plt.title(f'Корреляция Пирсона между {feature} и {is_psychedelic}')
    plt.xlabel(feature)
    plt.ylabel(is_psychedelic)
    plt.grid(True)
    plt.text(0.05, 0.5, f'Корреляция: {correlation:.2f}, p-значение: {p_value:.4f}', 
             horizontalalignment='left', 
             verticalalignment='center', 
             transform=plt.gca().transAxes, 
             fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.5))
    plt.show()
    
# Создаем точечные графики для каждой переменной по спирмену
correlations = df_variance.corr(method='spearman')[is_psychedelic].drop(is_psychedelic)
for feature in features:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_variance, x=feature, y=is_psychedelic, color='red')
    correlation, p_value = spearmanr(df_variance[feature], df_variance['is_psychedelic'])
    plt.title(f'Корреляция Спирмена между {feature} и {is_psychedelic}')
    plt.xlabel(feature)
    plt.ylabel(is_psychedelic)
    plt.grid(True)
    plt.text(0.05, 0.5, f'Корреляция: {correlation:.2f}, p-значение: {p_value:.4f}', 
             horizontalalignment='left', 
             verticalalignment='center', 
             transform=plt.gca().transAxes, 
             fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.5))
    plt.show()
    
#%%
# Отбор коррелирующих признаков
corr_matrix = df_variance.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper.columns if 0.6 > any(upper[column] > 0.8)]
df_variance.drop(to_drop, axis=1, inplace=True)

df_variance['is_psychedelic'] = df['is_psychedelic']

sns.pairplot(df_variance, hue='is_psychedelic', palette={0: 'green', 1: 'violet'})
plt.show()
