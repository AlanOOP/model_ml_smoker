import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Cargar el dataset
url = 'https://raw.githubusercontent.com/AlanOOP/Datasets/main/Smoker_dataset.csv'
df = pd.read_csv(url)

# Llenar valores nulos
df['Gene2337'].fillna(df['Gene2337'].mode()[0], inplace=True)
df['Gene35715'].fillna(df['Gene35715'].mode()[0], inplace=True)
df['Gene12936'].fillna(df['Gene12936'].mode()[0], inplace=True)
df['Gene1689'].fillna(df['Gene1689'].mode()[0], inplace=True)
df['FGFR1'].fillna(df['FGFR1'].mode()[0], inplace=True)
df['GATA4'].fillna(df['GATA4'].mode()[0], inplace=True)

# Convertir atributos categóricos a numéricos
df = pd.get_dummies(df, columns=['type'], dtype=int)

# Escalar los datos
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop('Condition', axis=1))
data_scaled = pd.DataFrame(scaled_features, columns=df.columns.drop('Condition'))
data_scaled['Condition'] = df['Condition']

# Definir variables independientes y dependiente
X = data_scaled.drop('Condition', axis=1)
y = data_scaled['Condition']

# Convertir la variable dependiente a numérica
y = y.map({'Normal': 0, 'Cancer': 1})

# Selección de características con RFE
logreg = LogisticRegression(solver='lbfgs', max_iter=1000)
rfe = RFE(estimator=logreg, n_features_to_select=2, step=1)
rfe = rfe.fit(X, y)
X_optimal_rfe = X.loc[:, rfe.support_]
print("Características seleccionadas por RFE:", X_optimal_rfe.columns.tolist())

# Selección de características con Árbol de Decisión
tree_model = DecisionTreeClassifier(random_state=0)
tree_model.fit(X, y)
importances = tree_model.feature_importances_
indices = np.argsort(importances)[::-1]
selected_tree_features = X.columns[indices[:2]]
X_optimal_tree = X[selected_tree_features]
print("Características seleccionadas por el Árbol de Decisión:", selected_tree_features.tolist())

# Usar características seleccionadas por el Árbol de Decisión para entrenar el modelo Random Forest
X_optimal = X_optimal_tree

# Entrenar el modelo Random Forest
rf_model = RandomForestClassifier(random_state=0)
x_train, x_test, y_train, y_test = train_test_split(X_optimal, y, test_size=0.2, random_state=0)
rf_model.fit(x_train, y_train)

# Guardar el modelo en formato pkl
joblib.dump(rf_model, 'random_forest_model.pkl')
print("Modelo guardado como random_forest_model.pkl")
