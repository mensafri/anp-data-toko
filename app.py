from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)


def calculate_anp():
    # Membaca file CSV
    file_path = 'data/Penjualan_Item_berdasarkan_Tanggal-2024-07-01__2024-07-05.csv'
    data = pd.read_csv(file_path)

    # Mengumpulkan data berdasarkan kriteria
    total_sales_per_item = data.groupby('item sku')['qty'].sum()
    total_income_per_item = data.groupby('item sku')['amount'].sum()
    frequency_per_item = data['item sku'].value_counts()

    # Mengambil nama item
    item_names = data.drop_duplicates(
        'item sku')[['item sku', 'item name']].set_index('item sku')

    # Menggabungkan semua data ke dalam satu DataFrame
    criteria_data = pd.DataFrame({
        'Item Name': item_names['item name'],
        'Total Sales': total_sales_per_item,
        'Total Income': total_income_per_item,
        'Frequency': frequency_per_item
    }).reset_index()

    # Membuat matriks perbandingan berpasangan
    pairwise_matrix = np.array([
        [1, 1/2, 3],
        [2, 1, 4],
        [1/3, 1/4, 1]
    ])

    # Normalisasi matriks perbandingan berpasangan
    norm_matrix = pairwise_matrix / pairwise_matrix.sum(axis=0)

    # Menghitung bobot lokal (rata-rata)
    local_weights = norm_matrix.mean(axis=1)

    # Membentuk supermatrix awal
    supermatrix = np.array([
        local_weights,
        local_weights,
        local_weights
    ])

    # Menghitung limit supermatrix (konvergensi)
    limit_supermatrix = np.linalg.matrix_power(supermatrix, 100)

    # Membuat DataFrame untuk limit supermatrix dengan label kolom dan baris yang deskriptif
    limit_supermatrix_df = pd.DataFrame(limit_supermatrix, columns=[
                                        'Total Sales', 'Total Income', 'Frequency'], index=['Total Sales', 'Total Income', 'Frequency'])

    return criteria_data, local_weights, limit_supermatrix_df


@app.route('/')
def index():
    criteria_data, local_weights, limit_supermatrix_df = calculate_anp()
    return render_template('index.html', data=criteria_data.to_dict(orient='records'), weights=local_weights, limit_matrix=limit_supermatrix_df.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
