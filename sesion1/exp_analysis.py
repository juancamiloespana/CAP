import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### nombres estandar salidas de los experimentos
columns = ['n_cols', 'n_rows', 'block_size', 'time_sec_Z','time_sec_col', 'time_sec_row']

###################################################################################################
########### analizar aleatoriedad de tiempos de una misma configuración ############
##################################################################################################


df_aleat = pd.read_table('outputs/aleatoriedad_tiempos.txt', delimiter=',', header=None)
df_aleat.columns = columns

time_cols = ['time_sec_Z', 'time_sec_col', 'time_sec_row']
std_tiempos = df_aleat[time_cols].std()
perc_Desv= std_tiempos / df_aleat[time_cols].mean() * 100
resumen = pd.DataFrame({'std (seg)': std_tiempos, 'std (%)': perc_Desv})
print('Estimación del error de medición:')
print(resumen.to_string(float_format=lambda x: f'{x:.4f}'))



###################################################################################################
########### analizar Tamaño de bloque #############################3
##################################################################################################


### el nombre del archivo generado fue modificado manualmente
df = pd.read_table('outputs/block_experiments_logs.txt', delimiter=',', header=None) 

df.columns = columns

# Tabla pivot: filas=tamaño de matriz, columnas=tamaño de bloque, valores=tiempo Z-order
pivot_Z = df.pivot_table(index='n_cols', columns='block_size', values='time_sec_Z')
print("\nTiempos Z-order (seg) por tamaño de matriz y bloque:")
print(pivot_Z.to_string(float_format=lambda x: f'{x:.4f}'))

# Diferencia respecto al bloque más rápido para cada tamaño de matriz
pivot_diff = pivot_Z.sub(pivot_Z.min(axis=1), axis=0)
print("\nDiferencia vs bloque óptimo (seg)  [* = óptimo]:")
print(pivot_diff.to_string(float_format=lambda x: f'{x:.4f}*' if x == 0.0 else f'{x:.4f} '))


n_cols_vals = sorted(df['n_cols'].unique())

fig, axes = plt.subplots(1, len(n_cols_vals), figsize=(6 * len(n_cols_vals), 5), sharey=False)
fig.suptitle('Tiempo de ejecución (Z) por tamaño de bloque', fontsize=16, fontweight='bold', y=1.02)

palette = sns.color_palette('viridis', len(n_cols_vals))

for ax, n_col, color in zip(axes, n_cols_vals, palette):
    subset = df[df['n_cols'] == n_col]
    sns.lineplot(data=subset, x='block_size', y='time_sec_Z', ax=ax, color=color, marker='o')
    ax.set_title(f'n_cols = {n_col}', fontsize=13)
    ax.set_xlabel('Tamaño de bloque', fontsize=11)
    ax.set_ylabel('Tiempo (seg)', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.4)
    sns.despine(ax=ax)

plt.tight_layout()
plt.savefig('outputs/graphs/block_experiments_Z.pdf', bbox_inches='tight')
plt.show()


###################################################################################################
########### analizar Tamaño matrices #############################3
##################################################################################################

import glob

#### cpodigo de combinación de archivos se deja activado el cargue del data set unido

# # Lee todos los .txt de la carpeta y los une en una sola tabla
# result_files = glob.glob('outputs/exp_matrices/*.txt')
# df_mat = pd.concat(
#     [pd.read_csv(f, header=None, names=columns) for f in result_files],
#     ignore_index=True
# # )

# df_mat.to_csv('outputs/comp_met_mat.csv', index=False)


df_mat = pd.read_csv('outputs/comp_met_mat.csv')

stats = df_mat.groupby('n_cols')[['time_sec_Z', 'time_sec_col', 'time_sec_row']].agg(['mean', 'std'])

metodos = [('time_sec_Z', 'Z-order'), ('time_sec_col', 'Column-major'), ('time_sec_row', 'Row-major')]
colores  = ['steelblue', 'tomato', 'seagreen']
x = stats.index

fig, ax = plt.subplots(figsize=(9, 5))
for (col, label), color in zip(metodos, colores):
    media = stats[(col, 'mean')].astype(float)
    std   = stats[(col, 'std')].fillna(0).astype(float)
    ax.plot(x, media, marker='o', label=label, color=color)
    ax.fill_between(x, media - std, media + std, alpha=0.2, color=color)

ax.set_title('Tiempo de ejecución por tamaño de matriz y método', fontsize=14, fontweight='bold')
ax.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
ax.set_ylabel('Tiempo promedio (seg)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.4)
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig('outputs/graphs/matrix_size_comparison.pdf', bbox_inches='tight')
plt.show()

# Tabla de diferencias entre métodos vs Row-major (óptimo)
medias = stats.xs('mean', axis=1, level=1)
medias.columns = ['Z-order', 'Column-major', 'Row-major']
diff_metodos = medias.sub(medias['Row-major'], axis=0)
print("\nDiferencia de tiempo vs Row-major (seg)  [* = óptimo]:")
print(diff_metodos.to_string(float_format=lambda x: f'{x:.4f}*' if x == 0.0 else f'{x:.4f} '))




# --- Comparación solo Row-major vs Z-order ---
metodos_rz = [('time_sec_Z', 'Z-order'), ('time_sec_row', 'Row-major')]
colores_rz  = ['steelblue', 'seagreen']

fig, ax = plt.subplots(figsize=(9, 5))
for (col, label), color in zip(metodos_rz, colores_rz):
    media = stats[(col, 'mean')].astype(float)
    std   = stats[(col, 'std')].fillna(0).astype(float)
    ax.plot(x, media, marker='o', label=label, color=color)
    ax.fill_between(x, media - std, media + std, alpha=0.2, color=color)

ax.set_title('Z-order vs Row-major por tamaño de matriz', fontsize=14, fontweight='bold')
ax.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
ax.set_ylabel('Tiempo promedio (seg)', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.4)
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig('outputs/graphs/matrix_size_zorder_vs_row.pdf', bbox_inches='tight')
plt.show()

# Tabla de diferencias Z-order vs Row-major
medias_rz = medias[['Z-order', 'Row-major']]
diff_rz = medias_rz.sub(medias_rz['Row-major'], axis=0)
print("\nDiferencia Z-order vs Row-major (seg)  [* = óptimo]:")
print(diff_rz.to_string(float_format=lambda x: f'{x:.4f}*' if x == 0.0 else f'{x:.4f} '))

# Tabla de desviaciones estándar por método y tamaño de matriz
stds = stats.xs('std', axis=1, level=1).fillna(0)
stds.columns = ['Z-order', 'Column-major', 'Row-major']
print("\nDesviación estándar por método y tamaño de matriz (seg):")
print(stds.to_string(float_format=lambda x: f'{x:.4f}'))
