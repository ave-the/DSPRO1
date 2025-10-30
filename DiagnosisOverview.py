import matplotlib.pyplot as plt
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("diagnosed_cbc_data_v4.csv")


diag_counts = df['Diagnosis'].value_counts()

plt.figure(figsize=(8,5))
diag_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Häufigkeit der Diagnosen im Datensatz")
plt.xlabel("Diagnosis")
plt.ylabel("Anzahl")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()