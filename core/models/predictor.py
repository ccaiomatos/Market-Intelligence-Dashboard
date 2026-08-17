import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def train_model(feature: pd.DataFrame):
  """
  Treina um RandomForrestClassifier para prever a direção do prócimo retorno.
  shuffle=False no split para não "vazar inormação" do futuro durante o treinamento.
  """
  x = feature.drop(columns="target")
  y = feature["target"]

  x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    shuffle=False
  )

  model = RandomForestClassifier(n_estimators=400, max_depth=4, random_state= 42)
  model.fit(x_train, y_train)

  predictions = model.predict(x_test)
  accuracy = accuracy_score(y_test, predictions)

  return model, accuracy
