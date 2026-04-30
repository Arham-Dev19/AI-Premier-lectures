import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# monthly data dengay static sa
dates = pd.date_range(start="2022-05-07", periods=10, freq='ME')

# ab idhr sales ka data dengay jo k 10 hoga q k periods 10 hain oper
sales = [200, 300, 250, 350, 400, 500, 450, 600, 700, 800]

data = pd.DataFrame({'Date': dates, 'Sales': sales})

# index set krengay ham array wise
data.set_index('Date', inplace=True)
print(data)  # issey terminal p sara data ajayega

# ab graph format mai show krne k liye
data.plot()
plt.title("Monthly Sales")  # graph ki heading
plt.show()