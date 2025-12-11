#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate an interactive HTML network graph using PyVis.
"""

import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network


def write_to_html():

    # Load the Excel file from project root
    data = pd.read_excel('data/processed/search_results_processed_concepts_v3.xlsx')

    # Prepare concept lists
    ls = [x for x in data.concepts.tolist() if str(x) != 'nan']
    ls = [x.split(',') for x in ls]
    lst = [[x.strip().replace(' ', '') for x in i] for i in ls]

    # -------------------------------
    # Create co-occurrence matrix
    # Modern Pandas version
    # -------------------------------

    # Convert list rows to a stacked Series
    stacked = pd.DataFrame(lst).stack()

    # One-hot encode and regroup by row index
    dummy_df = pd.get_dummies(stacked).groupby(level=0).sum()

    # Compute co-occurrence matrix
    v = dummy_df.T.dot(dummy_df)

    # Remove lower triangle
    v.values[np.tril(np.ones(v.shape)).astype(bool)] = 0

    # Convert to edge list
    a = v.stack()
    a = a[a >= 1].rename_axis(('source', 'target')).reset_index(name='weight')

    # Build NetworkX graph
    G = nx.from_pandas_edgelist(a, edge_attr=True)

    # Create PyVis interactive graph
    net = Network(height="800px", width="100%", bgcolor="white")
    net.from_nx(G)

    # Save HTML file
    output_path = "data/processed/network_graph.html"
    net.write_html(output_path)

    print(f"Interactive HTML graph saved to: {output_path}")


# Run the function
write_to_html()
