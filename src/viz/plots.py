"""
A utility class providing static methods for creating various plots from a DataFrame.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Plots:
    def bar_graph(df, column, x_label: str, y_label: str, title: str = None, figsize=(10, 6)):
        """
        Initialize figure and axes for animated live plotting.
        Returns (fig, ax) for use with FuncAnimation.
        """

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title if title else str(column))
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        if column in df.columns and not df.empty:
            counts = df[column].value_counts().sort_index()
            ax.bar(counts.index.astype(str), counts.values)

        ax = sns.countplot(data=df, x=column, ax=ax)
        ax.bar_label(ax.containers[0])   

        return fig, ax