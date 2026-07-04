import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

def colebrook(Re, ed, n=80):
    f = 0.02
    for _ in range(n):
        if ed == 0:
            rhs = -2.0 * np.log10(2.51 / (Re * np.sqrt(f)))
        else:
            rhs = -2.0 * np.log10(ed / 3.7 + 2.51 / (Re * np.sqrt(f)))
        f = 1.0 / rhs**2
    return f

fig, ax = plt.subplots(figsize=(13, 8.5), dpi=150)

# ---- roughness curves ----
ed_list   = [0, 1e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2]
ed_labels = ['smooth', '0.00001', '0.00005', '0.0001', '0.0002',
             '0.0005', '0.001', '0.002', '0.005', '0.01', '0.02', '0.05']
colors = plt.cm.turbo(np.linspace(0.05, 0.92, len(ed_list)))

Re_turb = np.logspace(np.log10(4000), 8, 600)

for ed, label, clr in zip(ed_list, ed_labels, colors):
    f_vals = np.array([colebrook(Re, ed) for Re in Re_turb])
    ax.loglog(Re_turb, f_vals, color=clr, linewidth=1.5, zorder=3)
    # label at right edge
    ax.text(Re_turb[-1] * 1.015, f_vals[-1], label,
            va='center', ha='left', fontsize=7.5, color=clr)

# ---- laminar ----
Re_lam = np.logspace(np.log10(200), np.log10(2000), 200)
f_lam  = 64.0 / Re_lam
ax.loglog(Re_lam, f_lam, 'r-', linewidth=2.2, zorder=4, label='Laminar  $f = 64/Re$')

# ---- fully rough asymptote (dashed) ----
f_rough = []
for ed in ed_list[1:]:
    rhs = -2.0 * np.log10(ed / 3.7)
    f_rough.append(1.0 / rhs**2)
Re_rough = np.full(len(f_rough), 1e8)
ax.loglog(Re_rough, f_rough, 'k--', linewidth=1.0, alpha=0.5, zorder=2)
ax.text(1e8 * 1.015, f_rough[-1], 'Fully\nrough', va='center', ha='left', fontsize=7.5, color='#555')

# ---- transition zone ----
ax.axvspan(2000, 4000, color='gold', alpha=0.18, zorder=1)
ax.text(2800, 0.0065, 'Transition', rotation=90, va='bottom', ha='center',
        fontsize=8, color='#9a7a00', style='italic')

# ---- grid ----
ax.set_xlim(5e2, 1.2e8)
ax.set_ylim(0.006, 0.105)
ax.grid(True, which='major', linestyle='-',  linewidth=0.5, color='#bbb', zorder=0)
ax.grid(True, which='minor', linestyle='-',  linewidth=0.3, color='#ddd', zorder=0)
ax.set_axisbelow(True)

# ---- axes formatting ----
ax.xaxis.set_major_formatter(ticker.LogFormatterMathtext())
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
ax.yaxis.set_minor_formatter(ticker.NullFormatter())

yticks_major = [0.008, 0.009, 0.01, 0.015, 0.02, 0.025, 0.03,
                0.04,  0.05,  0.06, 0.07,  0.08, 0.09,  0.1]
ax.set_yticks(yticks_major)
ax.set_yticklabels([str(v) for v in yticks_major], fontsize=9)

ax.set_xlabel('Reynolds Number,  $Re$', fontsize=12, labelpad=8)
ax.set_ylabel('Darcy Friction Factor,  $f$', fontsize=12, labelpad=8)
ax.set_title('Moody Chart', fontsize=14, fontweight='bold', pad=12)

# ---- region labels ----
ax.text(700,  0.072, 'Laminar\nFlow',    ha='center', va='center',
        fontsize=9, color='#c62828', style='italic')
ax.text(5e6, 0.0072, 'Turbulent Flow',  ha='center', va='center',
        fontsize=9, color='#1565c0', style='italic')

# ---- legend ----
custom_lines = [
    Line2D([0],[0], color='red',  linewidth=2.2),
    Line2D([0],[0], color='gray', linewidth=1.5),
    Line2D([0],[0], color='black',linewidth=1.0, linestyle='--'),
]
ax.legend(custom_lines,
          ['Laminar  $f = 64/Re$', 'Colebrook–White  (turbulent)', 'Fully rough asymptote'],
          loc='upper right', fontsize=8.5, framealpha=0.9)

# ---- ε/D axis label ----
ax.text(1.08, 0.5, r'Relative roughness  $\varepsilon/D$',
        transform=ax.transAxes, rotation=90,
        va='center', ha='left', fontsize=9, color='#333')

plt.tight_layout()
plt.savefig('moody_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('moody_chart.pdf', bbox_inches='tight', facecolor='white')
print("Saved: moody_chart.png  and  moody_chart.pdf")
plt.show()
