"""
Water Surface Profiles — GVF
Simple, clean schematic: bed + NDL + CDL + water surface curve
All 15 cells (5 slopes × 3 zones), missing ones show bed + reference lines only
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

plt.rcParams.update({'font.family': 'DejaVu Sans', 'mathtext.fontset': 'cm'})

# ─── slope angles (dy per unit x, positive = falling downstream) ───────────
SLOPE = {'M': 0.20, 'S': 0.38, 'C': 0.27, 'H': 0.00, 'A': -0.20}

# ─── profile data ────────────────────────────────────────────────────────────
# yn, yc : depth above bed (in data units 0-1 of panel height = 1.0)
# d_left, d_right : water depth at left/right edge (above bed)
# missing=True → no valid profile for this cell

PD = {
    # Mild  (yn > yc)
    'M1': dict(yn=0.42, yc=0.26, d0=0.44, d1=0.75),
    'M2': dict(yn=0.42, yc=0.26, d0=0.40, d1=0.28),
    'M3': dict(yn=0.42, yc=0.26, d0=0.10, d1=0.25),
    # Steep (yc > yn)
    'S1': dict(yn=0.26, yc=0.42, d0=0.44, d1=0.75),
    'S2': dict(yn=0.26, yc=0.42, d0=0.65, d1=0.28),
    'S3': dict(yn=0.26, yc=0.42, d0=0.10, d1=0.25),
    # Critical (yn = yc)
    'C1': dict(yn=0.34, yc=0.34, d0=0.36, d1=0.72),
    'C2': dict(yn=0.34, yc=0.34, d0=0.34, d1=0.34),   # parallel
    'C3': dict(yn=0.34, yc=0.34, d0=0.10, d1=0.33),
    # Horizontal (yn → ∞, no zone 1)
    'H1': dict(missing=True, note='Zone 1 not possible\n$(y_n \\to \\infty)$', yc=0.38),
    'H2': dict(yn=None,  yc=0.38, d0=0.65, d1=0.40),
    'H3': dict(yn=None,  yc=0.38, d0=0.12, d1=0.37),
    # Adverse (yn imaginary, no zone 1)
    'A1': dict(missing=True, note='Zone 1 not possible\n$(y_n$ imaginary$)$', yc=0.38),
    'A2': dict(yn=None,  yc=0.38, d0=0.65, d1=0.40),
    'A3': dict(yn=None,  yc=0.38, d0=0.12, d1=0.37),
}

ROW = [
    dict(key='M', label='MILD\n$S_0 < S_c$',       color='#1565C0'),
    dict(key='S', label='STEEP\n$S_0 > S_c$',      color='#6A1B9A'),
    dict(key='C', label='CRITICAL\n$S_0 = S_c$',   color='#00695C'),
    dict(key='H', label='HORIZONTAL\n$S_0=0$',     color='#E65100'),
    dict(key='A', label='ADVERSE\n$S_0<0$',        color='#B71C1C'),
]
ZONE_BG = ['#FFFDE7', '#E8F5E9', '#F3E5F5']

DEPTH_EQ = {
    'M1':'$y>y_n>y_c$','M2':'$y_n>y>y_c$','M3':'$y_n>y_c>y$',
    'S1':'$y>y_c>y_n$','S2':'$y_c>y>y_n$','S3':'$y_c>y_n>y$',
    'C1':'$y>y_c=y_n$','C2':'$y=y_c=y_n$','C3':'$y<y_c=y_n$',
    'H2':'$y>y_c$',    'H3':'$y<y_c$',
    'A2':'$y>y_c$',    'A3':'$y<y_c$',
}
NATURE = {
    'M1':'Backwater','M2':'Drawdown','M3':'Backwater',
    'S1':'Backwater','S2':'Drawdown','S3':'Backwater',
    'C1':'Backwater','C2':'Uniform', 'C3':'Backwater',
    'H2':'Drawdown', 'H3':'Backwater',
    'A2':'Drawdown', 'A3':'Backwater',
}

# ─── figure ──────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(5, 3, figsize=(12, 14),
                         gridspec_kw={'hspace': 0.38, 'wspace': 0.22})
fig.patch.set_facecolor('white')

fig.text(0.5, 0.995,
         'Water Surface Profiles — Gradually Varied Flow (GVF)',
         ha='center', va='top', fontsize=13, fontweight='bold', color='#111')
fig.text(0.5, 0.982,
         'Bed  ·  NDL = Normal Depth Line  ·  CDL = Critical Depth Line',
         ha='center', va='top', fontsize=8.5, color='#555')

for ci, (cl, bg) in enumerate(zip(['Zone 1','Zone 2','Zone 3'], ZONE_BG)):
    axes[0, ci].set_title(cl, fontsize=10, fontweight='bold',
                          color='#333', pad=6,
                          bbox=dict(boxstyle='round,pad=0.35',
                                    fc=bg, ec='#bbb', lw=0.7))

X = np.linspace(0, 1, 300)

def bed_y_arr(slope):
    """Bed height array; starts at 0.18 at x=0."""
    return 0.18 + slope * 0.5 - slope * X   # falls downstream if slope>0

def approach(d0, d1, k=7):
    t = np.linspace(-k/2, k/2, 300)
    return d0 + (d1 - d0) / (1 + np.exp(-t))

for ri, row_meta in enumerate(ROW):
    sk = row_meta['key']
    slope = SLOPE[sk]

    for ci in range(3):
        name = sk + str(ci + 1)
        ax = axes[ri, ci]
        p  = PD.get(name, {})

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_facecolor(ZONE_BG[ci])
        ax.tick_params(left=False, bottom=False,
                       labelleft=False, labelbottom=False)
        for sp in ax.spines.values():
            sp.set_linewidth(0.6)
            sp.set_edgecolor('#bbb')

        bed = bed_y_arr(slope)

        # ── bed fill ──
        ax.fill_between(X, 0, bed, color='#C8A97A', alpha=0.7, zorder=1)
        ax.plot(X, bed, color='#6B4C2A', lw=1.6, zorder=3)

        # hatch ticks
        for xi in np.linspace(0.06, 0.94, 10):
            by = np.interp(xi, X, bed)
            ax.plot([xi, xi - 0.025], [by, by - 0.04],
                    color='#6B4C2A', lw=0.9, zorder=3)

        # ── missing cell ──
        if p.get('missing'):
            # still draw CDL
            yc = p.get('yc', 0.38)
            cdl = bed + yc
            cdl = np.clip(cdl, 0.01, 0.99)
            ax.plot(X, cdl, color='#C62828', lw=1.1,
                    linestyle=(0,(2,2)), zorder=4, alpha=0.85)
            ax.text(0.97, cdl[-1], '$y_c$', ha='right', va='bottom',
                    fontsize=7, color='#C62828', fontweight='bold', zorder=5)
            ax.text(0.50, 0.62, p.get('note',''),
                    ha='center', va='center', fontsize=7.5,
                    color='#888', style='italic', linespacing=1.5,
                    transform=ax.transAxes)
            ax.text(0.05, 0.93, name, ha='left', va='top',
                    fontsize=9, fontweight='bold', color=row_meta['color'],
                    transform=ax.transAxes)
            continue

        yn_val = p.get('yn')
        yc_val = p.get('yc')

        # ── NDL ──
        if yn_val is not None:
            ndl = np.clip(bed + yn_val, 0.01, 0.99)
            ax.plot(X, ndl, color='#1565C0', lw=1.2,
                    linestyle=(0,(6,3)), zorder=4, alpha=0.9)
            ax.text(0.97, ndl[-1], '$y_n$', ha='right', va='bottom',
                    fontsize=7, color='#1565C0', fontweight='bold', zorder=5)
        else:
            # annotate yn → ∞ or imaginary
            label_ndl = ('$y_n \\to \\infty$' if sk == 'H'
                         else '$y_n$ imaginary')
            ax.text(0.50, 0.93, label_ndl,
                    ha='center', va='top', fontsize=6.8,
                    color='#1565C0', style='italic',
                    transform=ax.transAxes)

        # ── CDL ──
        if yc_val is not None:
            cdl = np.clip(bed + yc_val, 0.01, 0.99)
            ax.plot(X, cdl, color='#C62828', lw=1.1,
                    linestyle=(0,(2,2)), zorder=4, alpha=0.85)
            ax.text(0.97, cdl[-1], '$y_c$', ha='right', va='bottom',
                    fontsize=7, color='#C62828', fontweight='bold', zorder=5)

        # ── water surface ──
        d0, d1 = p['d0'], p['d1']
        if d0 == d1:   # C2 parallel
            depth = np.full_like(X, d0)
        else:
            depth = approach(d0, d1, k=6)

        ws = np.clip(bed + depth, bed + 0.02, 0.97)

        ax.fill_between(X, bed, ws, color='#64B5F6', alpha=0.40, zorder=2)
        ax.plot(X, ws, color='#0D47A1', lw=2.0, zorder=5,
                solid_capstyle='round')

        # flow arrow
        mid_ws = np.interp(0.5, X, ws)
        ax.annotate('', xy=(0.70, mid_ws + 0.04),
                    xytext=(0.38, mid_ws + 0.04),
                    xycoords='data', textcoords='data',
                    arrowprops=dict(arrowstyle='->', color='#0D47A1',
                                    lw=1.0, mutation_scale=9),
                    zorder=6)

        # ── label ──
        ax.text(0.05, 0.93, name, ha='left', va='top',
                fontsize=9, fontweight='bold', color=row_meta['color'],
                transform=ax.transAxes)

        # depth condition
        eq = DEPTH_EQ.get(name, '')
        nat = NATURE.get(name, '')
        nat_clr = ('#1B5E20' if nat == 'Backwater'
                   else '#B71C1C' if nat == 'Drawdown' else '#4A148C')
        ax.text(0.50, 0.055, eq,
                ha='center', va='bottom', fontsize=7,
                color='#444', style='italic', transform=ax.transAxes)
        ax.text(0.50, 0.01, nat,
                ha='center', va='bottom', fontsize=7,
                color=nat_clr, fontweight='bold', transform=ax.transAxes)

# ─── row labels ──────────────────────────────────────────────────────────────
for ri, row_meta in enumerate(ROW):
    axes[ri, 0].set_ylabel(row_meta['label'],
                           fontsize=8, fontweight='bold',
                           color=row_meta['color'],
                           rotation=90, labelpad=6,
                           multialignment='center')

# ─── legend ──────────────────────────────────────────────────────────────────
legend_handles = [
    Line2D([0],[0], color='#0D47A1', lw=2.0, label='Water surface'),
    Line2D([0],[0], color='#1565C0', lw=1.2,
           linestyle=(0,(6,3)), label='NDL  ($y_n$)'),
    Line2D([0],[0], color='#C62828', lw=1.1,
           linestyle=(0,(2,2)), label='CDL  ($y_c$)'),
    mpatches.Patch(fc='#C8A97A', alpha=0.8, label='Channel bed'),
    mpatches.Patch(fc='#64B5F6', alpha=0.5, label='Water body'),
]
fig.legend(handles=legend_handles, loc='lower center', ncol=5,
           fontsize=8.5, frameon=True, framealpha=0.95,
           edgecolor='#ccc', bbox_to_anchor=(0.5, 0.002))

plt.savefig('water_surface_profiles.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.savefig('water_surface_profiles.pdf',
            bbox_inches='tight', facecolor='white')
print("Saved: water_surface_profiles.png  and  water_surface_profiles.pdf")
plt.show()
