import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# Columnas del CSV de stderr (logs_*.txt)
COLUMNS = ['rows', 'cols', 'block_size', 'time_zorder', 'time_col', 'time_row', 'time_total']


def load_logs(output_folder):
    pattern = os.path.join('outputs', output_folder, 'logs_*.txt')
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No se encontraron archivos en: {pattern}")
    return pd.concat(
        [pd.read_csv(f, header=None, names=COLUMNS) for f in files],
        ignore_index=True
    )


def compare_block_sizes(df):
    """Z-order: tiempo medio por tamaño de matriz para b=256 y b=512, resta respecto a b=256."""
    pivot = df.groupby(['rows', 'block_size'])['time_zorder'].mean().unstack('block_size')
    pivot['diff (512-256)'] = pivot[512] - pivot[256]
    pivot.columns = ['b=256 (s)', 'b=512 (s)', 'diff (512-256) (s)']
    print("\nComparación de tamaños de bloque (referencia b=256):")
    print(pivot.to_string(float_format=lambda x: f'{x:.4f}'))
    return pivot


def table_times(df_analysis, label):
    """Tabla de tiempos medios por método y tamaño de matriz."""
    tbl = df_analysis[['time_row', 'time_col', 'time_zorder']].copy()
    tbl.columns = ['Row-major (s)', 'Column-major (s)', 'Z-order (s)']
    print(f"\nTiempos por método y tamaño de matriz — {label}:")
    print(tbl.to_string(float_format=lambda x: f'{x:.4f}'))
    return tbl


def table_diff_vs_row(df_analysis, label):
    """Tabla de diferencias de cada método vs Row-major (base). Negativo = más rápido que row."""
    base = df_analysis['time_row']
    diff = pd.DataFrame({
        'Row-major (s)': (df_analysis['time_row'] - base).round(4),
        'Column-major (s)': (df_analysis['time_col'] - base).round(4),
        'Z-order (s)': (df_analysis['time_zorder'] - base).round(4),
    }, index=df_analysis.index)
    print(f"\nDiferencia vs Row-major (seg) — {label}:")
    print(diff.to_string(
        float_format=lambda x: f'{x:.4f}*' if x == 0.0 else f'{x:.4f} '
    ))
    return diff


def plot_total_vs_sum(df_analysis, title, save_path):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df_analysis.index, df_analysis['time_total'], marker='o', label='Tiempo total', color='steelblue')
    ax.plot(df_analysis.index, df_analysis['Sum_times'], marker='s', linestyle='--', label='Suma métodos', color='tomato')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
    ax.set_ylabel('Tiempo (seg)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4)
    sns.despine(ax=ax)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def plot_methods(df_analysis, title, save_path):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.suptitle(title, fontsize=14, fontweight='bold')
    for col, label, color in zip(
        ['time_row', 'time_col', 'time_zorder'],
        ['Row-major', 'Column-major', 'Z-order'],
        ['seagreen', 'tomato', 'steelblue']
    ):
        ax.plot(df_analysis.index, df_analysis[col], marker='o', label=label, color=color)
    ax.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
    ax.set_ylabel('Tiempo promedio (seg)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4)
    sns.despine(ax=ax)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Multiplicación en Python puro
# ─────────────────────────────────────────────────────────────────────────────
F1_FOLDER = 'F1_met_size_2026-04-22_10-59-59'

print("\n" + "="*70)
print("FASE 1: Multiplicación en Python puro")
print("="*70)

df_f1 = load_logs(F1_FOLDER)

compare_block_sizes(df_f1)

### se selecciona 256 que fue el ganador de la comparación de tamaños de bloque para el análisis detallado por método y tamaño de matriz
df_f1_analysis = df_f1[df_f1['block_size'] == 256].groupby('rows')[['time_zorder','time_row', 'time_col', 'time_total']].mean()
df_f1_analysis["Sum_times"] = df_f1_analysis[['time_zorder','time_row', 'time_col']].sum(axis=1)


table_times(df_f1_analysis, 'F1')
table_diff_vs_row(df_f1_analysis, 'F1')
plot_methods(df_f1_analysis, 'F1: Tiempo por método y tamaño de matriz', 'outputs/graphs/F1_methods.pdf')

plot_total_vs_sum(df_f1_analysis, 'F1: Tiempo total vs suma de métodos', 'outputs/graphs/F1_total_vs_sum.pdf')


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Python llama a C via ctypes (Python convierte las matrices)
# ─────────────────────────────────────────────────────────────────────────────
F2_FOLDER = 'F2_met_size_2026-04-22_11-00-04'

print("\n" + "="*70)
print("FASE 2: Python llama a C via ctypes (Python convierte las matrices)")
print("="*70)

df_f2 = load_logs(F2_FOLDER)

compare_block_sizes(df_f2)

df_f2_analysis = df_f2[df_f2['block_size'] == 256].groupby('rows')[['time_zorder','time_row', 'time_col', 'time_total']].mean()
df_f2_analysis["Sum_times"] = df_f2_analysis[['time_zorder','time_row', 'time_col']].sum(axis=1)

table_times(df_f2_analysis, 'F2')
table_diff_vs_row(df_f2_analysis, 'F2')
plot_methods(df_f2_analysis, 'F2: Tiempo por método y tamaño de matriz', 'outputs/graphs/F2_methods.pdf')
plot_total_vs_sum(df_f2_analysis, 'F2: Tiempo total vs suma de métodos', 'outputs/graphs/F2_total_vs_sum.pdf')


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Python llama a C via ctypes (C gestiona toda la memoria)
# ─────────────────────────────────────────────────────────────────────────────
F3_FOLDER = 'F3_met_size_2026-04-22_11-00-09'

print("\n" + "="*70)
print("FASE 3: Python llama a C via ctypes (C gestiona toda la memoria)")
print("="*70)

df_f3 = load_logs(F3_FOLDER)

compare_block_sizes(df_f3)

df_f3_analysis = df_f3[df_f3['block_size'] == 256].groupby('rows')[['time_zorder','time_row', 'time_col', 'time_total']].mean()
df_f3_analysis["Sum_times"] = df_f3_analysis[['time_zorder','time_row', 'time_col']].sum(axis=1)

table_times(df_f3_analysis, 'F3')
table_diff_vs_row(df_f3_analysis, 'F3')
plot_methods(df_f3_analysis, 'F3: Tiempo por método y tamaño de matriz', 'outputs/graphs/F3_methods.pdf')
plot_total_vs_sum(df_f3_analysis, 'F3: Tiempo total vs suma de métodos', 'outputs/graphs/F3_total_vs_sum.pdf')


# ─────────────────────────────────────────────────────────────────────────────
# COMPARATIVA: F1 vs F2 vs F3
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("COMPARATIVA: F1 vs F2 vs F3")
print("="*70)

phases = {'F1': df_f1_analysis, 'F2': df_f2_analysis, 'F3': df_f3_analysis}
colors = {'F1': 'tomato', 'F2': 'steelblue', 'F3': 'seagreen'}

# Gráfica 1: layout total + suma lado a lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Comparativa F1/F2/F3: tiempos globales', fontsize=14, fontweight='bold')
for label, df in phases.items():
    ax1.plot(df.index, df['time_total'], marker='o', label=label, color=colors[label])
    ax2.plot(df.index, df['Sum_times'], marker='o', label=label, color=colors[label])
ax1.set_title('Tiempo total de ejecución', fontsize=11)
ax1.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
ax1.set_ylabel('Tiempo (seg)', fontsize=11)
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.4)
sns.despine(ax=ax1)
ax2.set_title('Suma de tiempos de métodos', fontsize=11)
ax2.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
ax2.set_ylabel('Tiempo (seg)', fontsize=11)
ax2.legend(fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.4)
sns.despine(ax=ax2)
plt.tight_layout()
plt.savefig('outputs/graphs/comp_total_sum.pdf', bbox_inches='tight')
plt.show()

# Gráfica 2: layout con los tres métodos comparados por fase
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
fig.suptitle('Comparativa F1/F2/F3 por método', fontsize=14, fontweight='bold')
for ax, (method, col) in zip(axes, [
    ('Row-major',    'time_row'),
    ('Column-major', 'time_col'),
    ('Z-order',      'time_zorder'),
]):
    for label, df in phases.items():
        ax.plot(df.index, df[col], marker='o', label=label, color=colors[label])
    ax.set_title(method, fontsize=11)
    ax.set_xlabel('Tamaño de matriz (N×N)', fontsize=11)
    ax.set_ylabel('Tiempo (seg)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4)
    sns.despine(ax=ax)
plt.tight_layout()
plt.savefig('outputs/graphs/comp_metodos.pdf', bbox_inches='tight')
plt.show()
