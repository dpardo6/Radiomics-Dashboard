# Standard plotly imports
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
# Using plotly + cufflinks in offline mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)

import pandas as pd

Data = pd.read_excel (r'C:\Users\pardo\OneDrive\Desktop\AI Lab Play Data\telehealth report_dashboard_manipulated.xlsx')

df = pd.DataFrame(Data, columns= ['Age'])

df['Age'].iplot(kind='hist', xTitle='Age',
                  yTitle='Count', title='Age Distribution')

print(df)
