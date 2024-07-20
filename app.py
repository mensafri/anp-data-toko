from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)


def calculate_anp():
    # Membaca file Excel
    file_path = 'data/Rincian_Penjualan-2024-07-15__2024-07-21.xlsx'
    data = pd.read_excel(file_path)

    # Mengumpulkan data berdasarkan kriteria
    total_sales_per_item = data.groupby('sales name')['subtotal'].sum()
    total_income_per_item = data.groupby('sales name')['total amount'].sum()
    frequency_per_item = data['sales name'].value_counts()
    total_discount_per_item = data.groupby('sales name')['discount'].sum()
    total_cost_per_item = data.groupby('sales name')['product cost'].sum()
    total_profit_per_item = data.groupby('sales name')['nett profit'].sum()

    # Mengambil nama item
    item_names = data.drop_duplicates(
        'sales name')[['sales name', 'sales email']].set_index('sales name')

    # Menggabungkan semua data ke dalam satu DataFrame
    criteria_data = pd.DataFrame({
        'Sales Name': item_names['sales email'],
        'Total Sales': total_sales_per_item,
        'Total Income': total_income_per_item,
        'Frequency': frequency_per_item,
        'Total Discount': total_discount_per_item,
        'Total Cost': total_cost_per_item,
        'Total Profit': total_profit_per_item
    }).reset_index()

    # Membuat matriks perbandingan berpasangan (contoh asumsi)
    pairwise_matrix = np.array([
        [1, 1/3, 3, 1/2, 4, 1/4],
        [3, 1, 5, 2, 6, 1/2],
        [1/3, 1/5, 1, 1/4, 2, 1/5],
        [2, 1/2, 4, 1, 5, 1/3],
        [1/4, 1/6, 1/2, 1/5, 1, 1/6],
        [4, 2, 5, 3, 6, 1]
    ])

    # Normalisasi matriks perbandingan berpasangan
    norm_matrix = pairwise_matrix / pairwise_matrix.sum(axis=0)

    # Menghitung bobot lokal (rata-rata)
    local_weights = norm_matrix.mean(axis=1)

    # Membentuk supermatrix awal
    supermatrix = np.array([
        local_weights,
        local_weights,
        local_weights,
        local_weights,
        local_weights,
        local_weights
    ])

    # Menghitung limit supermatrix (konvergensi)
    limit_supermatrix = np.linalg.matrix_power(supermatrix, 100)

    # Membuat DataFrame untuk limit supermatrix dengan label kolom dan baris yang deskriptif
    limit_supermatrix_df = pd.DataFrame(limit_supermatrix,
                                        columns=['Total Sales', 'Total Income', 'Frequency',
                                                 'Total Discount', 'Total Cost', 'Total Profit'],
                                        index=['Total Sales', 'Total Income', 'Frequency', 'Total Discount', 'Total Cost', 'Total Profit'])

    return criteria_data, local_weights, limit_supermatrix_df


@app.route('/')
def index():
    criteria_data, local_weights, limit_supermatrix_df = calculate_anp()
    return render_template('index.html', data=criteria_data.to_dict(orient='records'), weights=local_weights, limit_matrix=limit_supermatrix_df.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
