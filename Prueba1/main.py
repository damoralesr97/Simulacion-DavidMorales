import papermill as pm

pm.execute_notebook(
    './morales.ipynb',
    './resultado.ipynb',
    parameters=dict(inicio='2021-02-01',fin='2021-03-12')
)