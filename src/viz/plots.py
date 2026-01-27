"""
A utility class providing static methods for creating various plots from a DataFrame.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Plots:
    def plot_age_range_comparison_avg(df, column_1, column_2, figsize=(11, 6)):
    
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlabel(f'{column_1}')
        ax.set_ylabel('averages')
        ax.set_title(f'{column_1} range vs. {column_2} average')

        max_age = int(df[column_1].max() // 10)
        age_bins = [f"{i*10}-{i*10+9}" for i in range(2, max_age + 1)]
        comparison_totals = [[0, 0] for _ in range(len(age_bins))] # list comprehension to create a list of lists
        comparison_avg = [0] * (len(age_bins)) # initialize int list the size of total age ranges

        for i, ratio in enumerate(df[column_2]):
            age_bin = int(df[column_1].iloc[i] // 10) - 2 # first bin is 20-29 at index 0
            comparison_totals[age_bin][0] += ratio
            comparison_totals[age_bin][1] += 1
        
        for i, (total, count) in enumerate(comparison_totals):
            if count > 0:
                comparison_avg[i] = total / count

        df_age_comparison_avg = pd.DataFrame({
            "age_range": age_bins,
            "averages": comparison_avg
        })

        df_age_comparison_avg.plot(
            x="age_range", 
            y="averages", 
            marker='o',
            grid=True,
            legend=True,
            ax=ax
            )

        return ax

    def plot_days_overdue_counts(df, column, x_label: str, y_label: str, title: str = None, figsize=(15, 10)):

        if column not in df.columns or df.empty:
            raise ValueError("Invalid column or empty DataFrame")

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title if title else str(column))
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        counts = df[column].value_counts().sort_index()
        ax.bar(counts.index.astype(str), counts.values)

        ax = sns.countplot(data=df, x=column, ax=ax, hue=column, palette='bright', legend=False)
        ax.bar_label(ax.containers[0])   

        return fig, ax
    
    def plot_age_ranges(df, column, title: str = None, figsize=(10, 10)):
        
        if column not in df.columns or df.empty:
            raise ValueError("Invalid column or empty DataFrame")

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title if title else str(column))

        max_age = int(df[column].max() // 10)
        age_range_counts = {i: 0 for i in range(2, max_age + 1)}
        age_bins = [f"{i*10}-{i*10+9}" for i in range(2, max_age + 1)]

        for value in df[column]:
            age_range_counts[int(value) // 10] += 1

        def autopct_hide_small(pct):
            return f'{pct:.1f}%' if pct > 0.4 else ''

        wedges, label_texts, pct_texts = ax.pie(
            age_range_counts.values(),
            labels=age_bins,           # needed for legend
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
        ax.legend(wedges, age_bins, title=column, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        return ax
