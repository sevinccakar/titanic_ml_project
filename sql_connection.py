import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

server = r"DESKTOP-P1R5U4A"
database = "TitanicML"
connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?trusted_connection=yes"
    "&driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(connection_string)

query = "SELECT * FROM dbo.train"
df = pd.read_sql(query, engine)

print(df.head())
print(df.shape)
print(df.info())

print("\n--- NULL VALUES ---")
print(df.isnull().sum())

print("\n--- DESCRIBE ---")
print(df.describe())

df["Embarked"]=df["Embarked"].fillna(df["Embarked"].mode()[0])

df["HasCabin"] = df["Cabin"].notnull().astype(int)
df = df.drop(columns=["Cabin"])

df["Age"] = df.groupby(["Pclass", "Sex"])["Age"].transform(
    lambda x: x.fillna(x.median())
)
print(df.isnull().sum())

df["Sex"]=df["Sex"].map({"male":0,"female":1})
df = pd.get_dummies(df, columns=["Embarked"], drop_first=1)
df = df.drop(columns=["PassengerId", "Ticket"])
print(df.head())
print(df.dtypes)

df["Title"] = df["Name"].str.extract(r",\s*([^\.]+)\.")
print(df["Title"].value_counts())
common_titles = ["Mr", "Miss", "Mrs", "Master"]
df["Title"] = df["Title"].apply(lambda t: t if t in common_titles else "Other")
print(df["Title"].value_counts())
df = pd.get_dummies(df, columns=["Title"], drop_first=True)
df = df.drop(columns=["Name"])
print(df.head())
print(df.dtypes)

x=df.drop(columns=["Survived"])
y=df["Survived"]

x_train,x_test,y_train,y_test=train_test_split(
    x,y,test_size=0.2,random_state=23
)
print(x_train.shape, x_test.shape)

lg=LogisticRegression(max_iter=1000)
lg.fit(x_train,y_train)
y_pred=lg.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

tree_model=DecisionTreeClassifier(random_state=23)
tree_model.fit(x_train,y_train)
y_pred_tree=tree_model.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred_tree))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_tree))
print("\nClassification Report:\n", classification_report(y_test, y_pred_tree))

rf=RandomForestClassifier(random_state=23)
rf.fit(x_train,y_train)
y_pred_rf=rf.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))
print("\nClassification Report:\n", classification_report(y_test, y_pred_rf))

xgb_model=XGBClassifier(random_state=23,eval_metric="logloss" )
xgb_model.fit(x_train, y_train)
y_pred_xgb = xgb_model.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred_xgb))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_xgb))
print("\nClassification Report:\n", classification_report(y_test, y_pred_xgb))


scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

svm_model = SVC(random_state=23)
svm_model.fit(x_train_scaled, y_train)
y_pred_svm = svm_model.predict(x_test_scaled)
print("Accuracy:", accuracy_score(y_test, y_pred_svm))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_svm))
print("\nClassification Report:\n", classification_report(y_test, y_pred_svm))

gb_model = GradientBoostingClassifier(random_state=23)
gb_model.fit(x_train, y_train)
y_pred_gb = gb_model.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred_gb))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_gb))
print("\nClassification Report:\n", classification_report(y_test, y_pred_gb))

# 1) Survival Distribution
plt.figure(figsize=(5,4))
sns.countplot(x="Survived", data=df)
plt.title("Hayatta Kalma Dağılımı")
plt.show

# 2) Survival Rate by Passenger Class
plt.figure(figsize=(5,4))
sns.barplot(x="Pclass", y="Survived", data=df)
plt.title("Sınıfa (Pclass) Göre Hayatta Kalma Oranı")
plt.show()

# 3) Survival Rate by Gender
plt.figure(figsize=(5,4))
sns.barplot(x="Sex", y="Survived", data=df)
plt.title("Cinsiyete Göre Hayatta Kalma Oranı (0=Erkek, 1=Kadın)")
plt.show()

# 4) Age Distribution
plt.figure(figsize=(6,4))
sns.histplot(df["Age"], bins=30, kde=True)
plt.title("Yaş Dağılımı")
plt.show()

# 5) Fare Distribution
plt.figure(figsize=(6,4))
sns.histplot(df["Fare"], bins=30, kde=True)
plt.title("Bilet Ücreti (Fare) Dağılımı")
plt.show()

# 6) Correlation Matrix
plt.figure(figsize=(10, 8))
corr = df.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Korelasyon Matrisi")
plt.show()

# 7) Model Comparison
model_names = [
    "Logistic Regression",
    "Decision Tree",
    "Random Forest",
    "XGBoost",
    "SVM",
    "Gradient Boosting"
]
accuracies = [0.7877, 0.7989, 0.7821, 0.8101, 0.7989, 0.8212]
plt.bar(model_names, accuracies)
plt.ylim(0.75, 0.83)
plt.ylabel("Accuracy")
plt.title("Model Comparison")
plt.xticks(rotation=30)
plt.show()

models = {
    "Logistic Regression": y_pred,
    "Decision Tree": y_pred_tree,
    "Random Forest": y_pred_rf,
    "XGBoost": y_pred_xgb,
    "SVM": y_pred_svm,
    "Gradient Boosting": y_pred_gb
}
results = []

predictions = [
    ("Logistic Regression", y_pred),
    ("Decision Tree", y_pred_tree),
    ("Random Forest", y_pred_rf),
    ("XGBoost", y_pred_xgb),
    ("SVM", y_pred_svm),
    ("Gradient Boosting", y_pred_gb)
]

for name, prediction in predictions:

    acc = accuracy_score(y_test, prediction)
    prec = precision_score(y_test, prediction)
    rec = recall_score(y_test, prediction)
    f1 = f1_score(y_test, prediction)

    results.append([name, acc, prec, rec, f1])

results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1"]
)

print(results_df)
plt.bar(results_df["Model"], results_df["Accuracy"])

plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.ylim(0.75,0.83)
plt.xticks(rotation=30)

plt.show()

best_model = gb_model
print(x_train.columns)
print(x_train.head())

new_passenger = x_test.iloc[[0]]

prediction = best_model.predict(new_passenger)

print("Gerçek değer:", y_test.iloc[0])
print("Model tahmini:", prediction[0])

best_model = gb_model

new_passenger = pd.DataFrame([{
    "Pclass": 1,
    "Sex": 1,
    "Age": 25,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 50,
    "HasCabin": True,
    "Embarked_C": False,
    "Embarked_Q": False,
    "Embarked_S": True,
    "Title_Miss": False,
    "Title_Mr": False,
    "Title_Mrs": True,
    "Title_Other": False
}])

prediction = best_model.predict(new_passenger)

if prediction[0] == 1:
    print("Yolcu hayatta kaldı.")
else:
    print("Yolcu hayatta kalamadı.")
