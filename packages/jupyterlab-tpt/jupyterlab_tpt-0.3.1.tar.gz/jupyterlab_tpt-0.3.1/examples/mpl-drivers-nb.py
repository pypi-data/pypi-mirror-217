# %%
import numpy as np

X = np.linspace(-10, 10)
Y = X ** 2

# %%
import matplotlib.pyplot as plt
#%matplotlib notebook
#%matplotlib widget
%matplotlib ipympl

# %%
plt.figure()
plt.plot(X, Y);

# %%
