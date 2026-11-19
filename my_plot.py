import matplotlib.pyplot as plt
import numpy as np
def apply_style(font_family='serif', font_size=12, axes_titlesize=14, figure_dpi=110, line_width=1.8, grid_alpha=0.3):
    plt.rcParams['font.family'] = font_family
    plt.rcParams['font.size'] = font_size
    plt.rcParams['axes.titlesize'] = axes_titlesize
    plt.rcParams['axes.labelsize'] = axes_titlesize - 2
    plt.rcParams["legend.fontsize"] = font_size
    plt.rcParams['figure.dpi'] = figure_dpi
    plt.rcParams['lines.linewidth'] = line_width
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = grid_alpha
def style_axes(ax, xlabel='X', ylabel='Y', title='', grid=True, legend=True, legend_loc='best', legend_ncol=1,
               legend_frame=True, legend_fontsize=None):
    n = 0
    if xlabel:
        ax.set_xlabel(xlabel)
        n += 1
    if ylabel:
        ax.set_ylabel(ylabel)
        n += 1
    if title:
        ax.set_title(title)
    if grid == True:
        ax.grid(True, alpha=0.3)
    if legend == True and n > 0:
        ax.legend(loc=legend_loc, ncol=legend_ncol, frameon=legend_frame, fontsize=legend_fontsize)


def plot_single(x, y, xlabel='X', ylabel='Y', title='График',
                label=None, style='b-', figsize=(8, 5),
                hlines=None, vlines=None,
                hlines_colors=None, vlines_colors=None,
                legend_loc='best', legend_ncol=1, legend_frame=True,
                save_path=None, paint=True, dpi=150):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, y, style, label=label)

    if isinstance(hlines, list):
        for i, h_val in enumerate(hlines):
            if hlines_colors and i < len(hlines_colors):
                ax.axhline(h_val, color=hlines_colors[i], linestyle='--')
            else:
                ax.axhline(h_val, color='grey', linestyle='--')

    if isinstance(vlines, list):
        for i, v_val in enumerate(vlines):
            if vlines_colors and i < len(vlines_colors):
                ax.axvline(v_val, color=vlines_colors[i], linestyle='--')
            else:
                ax.axvline(v_val, color='grey', linestyle='--')

    style_axes(ax, xlabel=xlabel, ylabel=ylabel, title=title, legend_loc=legend_loc, legend_ncol=legend_ncol,
               legend_frame=legend_frame)

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
    if paint:
        plt.show()
    return (fig, ax)


def plot_grid(rows, cols, items, figsize=None,
              suptitle=None, save_path=None, paint=True, dpi=150):
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = np.atleast_1d(axes).ravel()
    n = rows * cols

    for i in range(n):
        t = axes[i]
        if i < len(items):
            st = items[i]
            x = st.get('x')
            y = st.get('y')
            kind = st.get('kind', 'plot')
            style = st.get('style')
            label = st.get('label')
            color = st.get('color')
            alpha = st.get('alpha')
            marker = st.get('marker')
            s = st.get('s')
            bins = st.get('bins')

            if kind == 'plot':
                t.plot(x, y, style if style else '-', color=color, label=label, alpha=alpha, marker=marker)
            elif kind == 'bar':
                t.bar(x, y, color=color, label=label, alpha=alpha)
            elif kind == 'scatter':
                t.scatter(x, y, color=color, label=label, alpha=alpha, marker=marker, s=s)
            elif kind == 'hist':
                t.hist(x, bins=bins if bins else 10, color=color, label=label, alpha=alpha)

            vlines = st.get('vlines')
            vlines_colors = st.get('vlines_colors')
            if isinstance(vlines, list):
                for idx, v_val in enumerate(vlines):
                    if vlines_colors and idx < len(vlines_colors):
                        t.axvline(v_val, color=vlines_colors[idx], linestyle='--')
                    else:
                        t.axvline(v_val, color='grey', linestyle='--')

            hlines = st.get('hlines')
            hlines_colors = st.get('hlines_colors')
            if isinstance(hlines, list):
                for idx, h_val in enumerate(hlines):
                    if hlines_colors and idx < len(hlines_colors):
                        t.axhline(h_val, color=hlines_colors[idx], linestyle='--')
                    else:
                        t.axhline(h_val, color='grey', linestyle='--')

            xlabel = st.get('xlabel', 'X')
            ylabel = st.get('ylabel', 'Y')
            title = st.get('title', '')
            grid = st.get('grid', True)
            legend = st.get('legend', False)
            legend_loc = st.get('legend_loc', 'best')
            legend_ncol = st.get('legend_ncol', 1)
            legend_frame = st.get('legend_frame', True)
            legend_fontsize = st.get('legend_fontsize', None)

            style_axes(
                t, xlabel=xlabel, ylabel=ylabel, title=title,
                grid=grid, legend=legend, legend_loc=legend_loc,
                legend_ncol=legend_ncol, legend_frame=legend_frame,
                legend_fontsize=legend_fontsize
            )
        else:
            t.set_visible(False)

    if suptitle is not None:
        fig.suptitle(suptitle)
    fig.tight_layout()
    if paint:
        plt.show()
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
    return fig, axes
