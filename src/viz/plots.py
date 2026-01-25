"""
A utility class providing static methods for creating various plots from a DataFrame.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Plots:
    def bar_graph(df, column, x_label: str, y_label: str, title: str = None, figsize=(11, 6)):

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title if title else str(column))
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        if column in df.columns and not df.empty:
            counts = df[column].value_counts().sort_index()
            ax.bar(counts.index.astype(str), counts.values)

        ax = sns.countplot(data=df, x=column, ax=ax, hue=column, palette='bright', legend=False)
        ax.bar_label(ax.containers[0])   

        return fig, ax
    
    def pie_graph(df, column, title: str = None, figsize=(10, 10)):

        if column not in df.columns or df.empty:
            raise ValueError("Invalid column or empty DataFrame")

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title if title else str(column))

        clean_col = df[column].dropna()
        max_bin = int(clean_col.max() // 10)

        value_bin = {i: 0 for i in range(max_bin + 1)}
        bins = [f"{i*10}-{i*10+9}" for i in range(max_bin + 1)]

        for value in clean_col:
            value_bin[int(value) // 10] += 1

        def autopct_hide_small(pct):
            return f'{pct:.1f}%' if pct > 0.4 else ''

        wedges, label_texts, pct_texts = ax.pie(
            value_bin.values(),
            labels=bins,              # needed for legend
            autopct=autopct_hide_small,
            labeldistance=1.15,
            pctdistance=0.75,
            startangle=90
        )

        # Hide the wedge labels (but keep percentages if visible)
        for label in label_texts:
            label.set_visible(False)

        # Hide percentage text for small slices
        for pct in pct_texts:
            if pct.get_text() == '':
                pct.set_visible(False)

        # Add legend manually
        ax.legend(wedges, bins, title=column, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        return ax
