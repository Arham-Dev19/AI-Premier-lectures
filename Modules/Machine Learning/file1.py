from sklearn.linear_model import LinearRegression

# Data
x = [[1], [2], [3], [4]] #Study hour
y = [40, 50, 60, 70] #Marks

# Made Model
model = LinearRegression()

# Train Model with Data
model.fit(x,y)

# Prediction
print(model.predict([[5]])) # Study 5hr 