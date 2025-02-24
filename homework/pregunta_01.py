# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


import os
import pandas as pd
import matplotlib.pyplot as plt


import os
import pandas as pd
import matplotlib.pyplot as plt

def pregunta_01():
    """
    Lee el archivo 'files/input/shipping-data.csv' y genera un dashboard estático
    en 'docs/index.html' con 4 gráficos:
      1) Envíos por bodega (Warehouse_block)
      2) Distribución de modos de envío (Mode_of_Shipment)
      3) Calificación promedio por modo de envío (Customer_rating)
      4) Distribución del peso (Weight_in_gms)
    """
    # ---------------------------------------------------------------------
    # 1. Construir la ruta al CSV, relativo a este archivo .py
    # ---------------------------------------------------------------------
    base_dir = os.path.dirname(__file__)  # carpeta donde está pregunta_01.py
    csv_path = os.path.join(base_dir, '..', 'files', 'input', 'shipping-data.csv')

    # 2. Cargar el DataFrame
    df = pd.read_csv(csv_path)

    # 3. Crear carpeta docs/ si no existe
    docs_dir = os.path.join(base_dir, '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    # ---------------------------------------------------------------------
    # GRAFICO 1: Envíos por bodega (Warehouse_block) - Gráfico de barras
    # ---------------------------------------------------------------------
    plt.figure(figsize=(6, 4))
    counts_warehouse = df['Warehouse_block'].value_counts()
    counts_warehouse.plot(kind='bar', color='tab:blue')

    plt.title('Shipping per Warehouse')
    plt.xlabel('Warehouse_block')
    plt.ylabel('Record Count')

    # Quitar bordes superior y derecho
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    outpath_1 = os.path.join(docs_dir, 'shipping_per_warehouse.png')
    plt.savefig(outpath_1)
    plt.close()

    # ---------------------------------------------------------------------
    # GRAFICO 2: Distribución de modos de envío (Mode_of_Shipment) - Donut
    # ---------------------------------------------------------------------
    plt.figure(figsize=(6, 4))
    counts_mode = df['Mode_of_Shipment'].value_counts()

    # Gráfico de pastel con un "agujero" al centro (donut)
    plt.pie(
        counts_mode,
        labels=counts_mode.index,
        wedgeprops={'width': 0.35},  # ancho de la "dona"
    )
    plt.title('Mode of Shipment')

    plt.tight_layout()
    outpath_2 = os.path.join(docs_dir, 'mode_of_shipment.png')
    plt.savefig(outpath_2)
    plt.close()

    # ---------------------------------------------------------------------
    # GRAFICO 3: Calificación promedio por modo de envío (Customer_rating)
    #            Muestra min, max y la media resaltada
    # ---------------------------------------------------------------------
    plt.figure(figsize=(6, 4))
    stats = df.groupby('Mode_of_Shipment')['Customer_rating'].agg(['min', 'mean', 'max'])

    modes = stats.index
    y_pos = range(len(modes))
    min_vals = stats['min']
    mean_vals = stats['mean']
    max_vals = stats['max']

    # Barra de fondo gris (rango [min, max])
    plt.hlines(
        y=y_pos,
        xmin=min_vals,
        xmax=max_vals,
        color='lightgray',
        linewidth=6,
        alpha=0.8
    )

    # Resaltar la media con un trazo vertical
    # (verde si >=3, naranja si <3)
    colors = ['tab:green' if v >= 3 else 'tab:orange' for v in mean_vals]
    for i, val in enumerate(mean_vals):
        plt.plot([val, val], [i - 0.1, i + 0.1], color=colors[i], linewidth=5)

    plt.yticks(y_pos, modes)
    plt.title('Average Customer Rating by Mode')
    plt.xlim(1, 5)  # Calificaciones típicas de 1..5

    # Quitar spines (bordes)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.tight_layout()
    outpath_3 = os.path.join(docs_dir, 'average_customer_rating.png')
    plt.savefig(outpath_3)
    plt.close()

    # ---------------------------------------------------------------------
    # GRAFICO 4: Distribución del peso (Weight_in_gms) - Histograma
    # ---------------------------------------------------------------------
    plt.figure(figsize=(6, 4))
    plt.hist(
        df['Weight_in_gms'],
        bins=30,
        color='tab:blue',
        edgecolor='white'  # Para separar visualmente las barras
    )
    plt.title('Weight Distribution')
    plt.xlabel('Weight_in_gms')
    plt.ylabel('Frequency')

    # Quitar bordes superior y derecho
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    outpath_4 = os.path.join(docs_dir, 'weight_distribution.png')
    plt.savefig(outpath_4)
    plt.close()

    # ---------------------------------------------------------------------
    # CREAR EL INDEX.HTML EN 'docs'
    # ---------------------------------------------------------------------
    html_path = os.path.join(docs_dir, 'index.html')
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shipping Dashboard</title>
</head>
<body>
    <h1>Shipping Dashboard</h1>
    <div style="width: 45%; float:left;">
        <img src="shipping_per_warehouse.png" width="100%">
        <br><br>
        <img src="mode_of_shipment.png" width="100%">
    </div>
    <div style="width: 45%; float:left; margin-left: 5%;">
        <img src="average_customer_rating.png" width="100%">
        <br><br>
        <img src="weight_distribution.png" width="100%">
    </div>
</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("¡Dashboard creado en la carpeta 'docs'!")
