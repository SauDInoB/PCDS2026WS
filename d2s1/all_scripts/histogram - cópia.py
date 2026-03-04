import pandas as pd
import numpy as np
import seaborn as sns

x = np.array([69,45,67,52,57,59,65,64,65,65,70,67,67,62,65])

df = pd.DataFrame({
    "nome": ["Ana", "João", "Maria"],
    "day": [20, 22, 21],
    "total_bill": [14, 16, 18]
})

flights = sns.load_dataset("flights")

sns.catplot(data=flights, x="day", y="total_bill")

