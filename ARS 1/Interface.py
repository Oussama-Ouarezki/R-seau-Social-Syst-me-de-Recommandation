
import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter

# Set plotting style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

# Page configuration
st.set_page_config(page_title="Graph Analysis Dashboard", layout="wide", page_icon="📊")

# Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the adjacency matrix
@st.cache_data
def get_initial_matrix():
    return np.array([
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    ], dtype=int)

# Initialize session state
if 'adj_matrix' not in st.session_state:
    st.session_state.adj_matrix = get_initial_matrix()

# Title
st.markdown('<p class="main-header">🥋 Zachary\'s Karate Club Network Analysis</p>', unsafe_allow_html=True)
st.markdown("**Zachary's Karate Club (1977)**: A social network of 34 members of a university karate club. An internal dispute led to the club splitting into two groups, making it an emblematic case study in social network analysis.")

# Sidebar for controls
st.sidebar.header("🔧 Network Controls")

# Node operations
st.sidebar.subheader("Member Operations")
if st.sidebar.button("➕ Add New Member", use_container_width=True):
    n = len(st.session_state.adj_matrix)
    new_matrix = np.zeros((n+1, n+1), dtype=int)
    new_matrix[:n, :n] = st.session_state.adj_matrix
    st.session_state.adj_matrix = new_matrix
    st.success(f"New member added! Now have {n+1} members.")
    st.rerun()

# Remove node
remove_node = st.sidebar.number_input(
    "Member to Remove", 
    min_value=0, 
    max_value=max(0, len(st.session_state.adj_matrix)-1), 
    value=0, 
    key="remove_node"
)

if st.sidebar.button("➖ Remove Member", use_container_width=True):
    n = len(st.session_state.adj_matrix)
    if n > 1:
        mask = np.ones(n, dtype=bool)
        mask[remove_node] = False
        new_matrix = st.session_state.adj_matrix[mask][:, mask]
        st.session_state.adj_matrix = new_matrix
        st.success(f"Member {remove_node} removed! Now have {n-1} members.")
        st.rerun()
    else:
        st.error("Cannot remove the last member!")

st.sidebar.markdown("---")

# Add/Remove edges
st.sidebar.subheader("Friendship Operations")
n_nodes = len(st.session_state.adj_matrix)
col1, col2 = st.sidebar.columns(2)
node1 = col1.number_input("Member 1", min_value=0, max_value=n_nodes-1, value=0, key="node1")
node2 = col2.number_input("Member 2", min_value=0, max_value=n_nodes-1, value=min(1, n_nodes-1), key="node2")

col_add, col_remove = st.sidebar.columns(2)
if col_add.button("➕ Add Friendship", use_container_width=True):
    if node1 != node2:
        st.session_state.adj_matrix[node1][node2] = 1
        st.session_state.adj_matrix[node2][node1] = 1
        st.success(f"Friendship added: {node1} ↔ {node2}")
        st.rerun()
    else:
        st.error("A member cannot be friends with themselves!")

if col_remove.button("➖ Remove Friendship", use_container_width=True):
    if node1 != node2:
        st.session_state.adj_matrix[node1][node2] = 0
        st.session_state.adj_matrix[node2][node1] = 0
        st.success(f"Friendship removed: {node1} ↔ {node2}")
        st.rerun()
    else:
        st.error("A member cannot be friends with themselves!")

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset Network", use_container_width=True):
    st.session_state.adj_matrix = get_initial_matrix()
    st.success("Network reset to original Karate Club!")
    st.rerun()

# Create graph from adjacency matrix
A = st.session_state.adj_matrix
G = nx.from_numpy_array(A)

# Calculate metrics
order = G.number_of_nodes()
size = G.number_of_edges()
degrees = [deg for _, deg in G.degree()]
degree_count = Counter(degrees)
clustering_coeffs = nx.clustering(G)
avg_clustering = nx.average_clustering(G)
triangles_per_node = nx.triangles(G)
total_triangles = sum(triangles_per_node.values()) // 3
core_numbers = nx.core_number(G)
max_kcore = max(core_numbers.values()) if core_numbers else 0

# K-core distribution - Calculate cumulative (nodes in k-core or higher)
kcore_cumulative = {}
for k in range(max_kcore + 1):
    kcore_cumulative[k] = sum(1 for v in core_numbers.values() if v >= k)

# Centrality measures
deg_centrality = nx.degree_centrality(G)
bet_centrality = nx.betweenness_centrality(G)
close_centrality = nx.closeness_centrality(G)
eig_centrality = nx.eigenvector_centrality(G, max_iter=1000)

def top_nodes(centrality_dict, n=5):
    return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:n]

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview", 
    "📊 Degree Distribution", 
    "🔗 Clustering", 
    "🔺 Motifs", 
    "🎯 K-Core", 
    "⭐ Centrality"
])

with tab1:
    st.header("Network Overview")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Club Members", order, help="Number of members in the karate club")
    with col2:
        st.metric("Friendships", size, help="Number of friendship connections")
    with col3:
        st.metric("Avg Clustering", f"{avg_clustering:.3f}")
    with col4:
        st.metric("Friend Triangles", total_triangles)
    
    st.markdown("---")
    
    # Graph visualization
    st.subheader("Karate Club Social Network")
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42, k=0.5)
    
    # Color nodes by degree
    node_colors = [deg for node, deg in G.degree()]
    
    nx.draw(G, pos, 
            node_color=node_colors,
            node_size=500,
            cmap='viridis',
            with_labels=True,
            font_size=8,
            font_color='white',
            edge_color='gray',
            alpha=0.7,
            ax=ax)
    
    sm = plt.cm.ScalarMappable(cmap='viridis', 
                               norm=plt.Normalize(vmin=min(node_colors) if node_colors else 0, 
                                                 vmax=max(node_colors) if node_colors else 1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Number of Friends', rotation=270, labelpad=20)
    
    plt.title("Karate Club Network (colored by number of friends)", fontsize=16, fontweight='bold')
    st.pyplot(fig)
    plt.close()

with tab2:
    st.header("Friendship Connections Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar plot using seaborn
        fig, ax = plt.subplots(figsize=(10, 6))
        degrees_sorted = sorted(degree_count.items())
        x_vals = [d[0] for d in degrees_sorted]
        y_vals = [d[1] for d in degrees_sorted]
        
        sns.barplot(x=x_vals, y=y_vals, palette="viridis", ax=ax)
        ax.set_xlabel("Number of Friends", fontsize=12, fontweight='bold')
        ax.set_ylabel("Number of Members", fontsize=12, fontweight='bold')
        ax.set_title("Distribution of Friendship Connections", fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Statistics")
        st.write(f"**Min Friends:** {min(degrees)}")
        st.write(f"**Max Friends:** {max(degrees)}")
        st.write(f"**Average Friends:** {np.mean(degrees):.2f}")
        st.write(f"**Median Friends:** {np.median(degrees):.1f}")
        
        st.subheader("Distribution")
        df_deg = pd.DataFrame(list(degree_count.items()), 
                              columns=['Friends', 'Members'])
        df_deg = df_deg.sort_values('Friends')
        st.dataframe(df_deg, use_container_width=True, hide_index=True)

with tab3:
    st.header("Social Cohesion (Clustering Coefficient)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Overall Statistics")
        st.metric("Average Clustering Coefficient", f"{avg_clustering:.4f}")
        
        interpretation = ""
        if avg_clustering > 0.5:
            interpretation = "🟢 High cohesion - members form tight-knit groups"
        elif avg_clustering > 0.3:
            interpretation = "🟡 Moderate cohesion - mixed group dynamics"
        else:
            interpretation = "🔴 Low cohesion - sparse connections"
        
        st.info(interpretation)
        
        st.write(f"**Min Clustering:** {min(clustering_coeffs.values()):.4f}")
        st.write(f"**Max Clustering:** {max(clustering_coeffs.values()):.4f}")
    
    with col2:
        st.subheader("Top 10 Members by Local Cohesion")
        top_clustering = sorted(clustering_coeffs.items(), 
                               key=lambda x: x[1], 
                               reverse=True)[:10]
        
        df_clust = pd.DataFrame(top_clustering, 
                               columns=['Member', 'Clustering Coefficient'])
        st.dataframe(df_clust, use_container_width=True, hide_index=True)
    
    # Histogram of clustering coefficients
    st.subheader("Distribution of Clustering Coefficients")
    fig, ax = plt.subplots(figsize=(10, 5))
    clustering_vals = list(clustering_coeffs.values())
    sns.histplot(clustering_vals, bins=20, kde=True, color='skyblue', ax=ax)
    ax.set_xlabel("Clustering Coefficient", fontsize=12, fontweight='bold')
    ax.set_ylabel("Frequency", fontsize=12, fontweight='bold')
    ax.set_title("Distribution of Local Cohesion across Members", fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with tab4:
    st.header("Friendship Triangles (Social Motifs)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.metric("Total Friendship Triangles", total_triangles)
        st.info("Triangles represent groups of three members who are all friends with each other - a fundamental social structure indicating strong group cohesion.")
    
    with col2:
        st.subheader("Top 10 Members by Triangle Participation")
        top_triangles = sorted(triangles_per_node.items(), 
                              key=lambda x: x[1], 
                              reverse=True)[:10]
        
        df_tri = pd.DataFrame(top_triangles, 
                             columns=['Member', 'Triangle Count'])
        st.dataframe(df_tri, use_container_width=True, hide_index=True)
    
    # Bar plot of triangle participation using seaborn
    st.subheader("Triangle Participation by Member")
    fig, ax = plt.subplots(figsize=(12, 5))
    nodes = list(range(len(triangles_per_node)))
    tri_counts = [triangles_per_node[i] for i in nodes]
    
    df_triangles = pd.DataFrame({'Member': nodes, 'Triangles': tri_counts})
    sns.barplot(data=df_triangles, x='Member', y='Triangles', color='coral', ax=ax)
    ax.set_xlabel("Member ID", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Triangles", fontsize=12, fontweight='bold')
    ax.set_title("Friendship Triangle Participation per Member", fontsize=14, fontweight='bold')
    
    # Show every 5th label if too many nodes
    if len(nodes) > 20:
        ax.set_xticks(range(0, len(nodes), max(1, len(nodes)//20)))
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with tab5:
    st.header("K-Core Analysis: Network Cohesiveness")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Maximum K-Core", max_kcore)
        st.write("The k-core represents the most cohesive subgroup where every member has at least k friends within the group. Higher k-cores indicate tighter, more interconnected social circles.")
        
        # K-core distribution - CORRECTED (cumulative)
        st.subheader("K-Core Distribution")
        st.write("Shows how many members belong to each k-core level (cumulative - members in k-core or higher)")
        
        df_core = pd.DataFrame(list(kcore_cumulative.items()), 
                              columns=['K-Core', 'Number of Members'])
        df_core = df_core.sort_values('K-Core', ascending=False)
        st.dataframe(df_core, use_container_width=True, hide_index=True)
        
        # Show detailed node assignments
        st.subheader("Member Core Assignments")
        df_node_cores = pd.DataFrame(list(core_numbers.items()),
                                    columns=['Member', 'Core Number'])
        df_node_cores = df_node_cores.sort_values('Core Number', ascending=False)
        with st.expander("View all member core assignments"):
            st.dataframe(df_node_cores, use_container_width=True, hide_index=True)
    
    with col2:
        # Bar plot of k-core distribution (cumulative)
        st.subheader("Cumulative K-Core Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        df_core_plot = df_core.sort_values('K-Core')
        sns.barplot(data=df_core_plot, x='K-Core', y='Number of Members', 
                   palette='coolwarm', ax=ax)
        ax.set_xlabel("K-Core Value", fontsize=12, fontweight='bold')
        ax.set_ylabel("Number of Members (cumulative)", fontsize=12, fontweight='bold')
        ax.set_title("Members in Each K-Core Level (decreases with higher k)", fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Visualize the max k-core
        st.subheader(f"Visualization of {max_kcore}-Core (Inner Circle)")
        
        if max_kcore > 0:
            kcore_subgraph = nx.k_core(G, max_kcore)
            
            fig, ax = plt.subplots(figsize=(10, 8))
            pos = nx.spring_layout(kcore_subgraph, seed=42)
            
            nx.draw(kcore_subgraph, pos,
                   node_color='lightblue',
                   node_size=700,
                   with_labels=True,
                   font_size=10,
                   font_weight='bold',
                   edge_color='gray',
                   alpha=0.8,
                   ax=ax)
            
            plt.title(f"{max_kcore}-Core: Most Connected Members ({kcore_subgraph.number_of_nodes()} members, {kcore_subgraph.number_of_edges()} friendships)", 
                     fontsize=14, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        else:
            st.warning("No k-core found in the network.")

with tab6:
    st.header("Centrality Measures")
    
    # Top nodes for each centrality
    st.subheader("Top 5 Most Central Nodes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Degree Centrality**")
        for node, val in top_nodes(deg_centrality):
            st.write(f"Node {node}: {val:.4f}")
        
        st.write("**Betweenness Centrality**")
        for node, val in top_nodes(bet_centrality):
            st.write(f"Node {node}: {val:.4f}")
    
    with col2:
        st.write("**Closeness Centrality**")
        for node, val in top_nodes(close_centrality):
            st.write(f"Node {node}: {val:.4f}")
        
        st.write("**Eigenvector Centrality**")
        for node, val in top_nodes(eig_centrality):
            st.write(f"Node {node}: {val:.4f}")
    
    st.markdown("---")
    
    # Comparative bar plot using seaborn
    st.subheader("Comparative Centrality Analysis")
    
    centrality_data = []
    for name, cent_dict in [
        ("Degree", deg_centrality),
        ("Betweenness", bet_centrality),
        ("Closeness", close_centrality),
        ("Eigenvector", eig_centrality)
    ]:
        for node, value in top_nodes(cent_dict, n=5):
            centrality_data.append({
                "Node": str(node),
                "Centrality Type": name,
                "Centrality Value": value
            })
    
    df_centrality = pd.DataFrame(centrality_data)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Create grouped bar plot using seaborn
    sns.barplot(
        data=df_centrality,
        x="Centrality Type",
        y="Centrality Value",
        hue="Node",
        palette="Set2",
        ax=ax
    )
    
    ax.set_xlabel('Centrality Measure', fontsize=12, fontweight='bold')
    ax.set_ylabel('Centrality Value', fontsize=12, fontweight='bold')
    ax.set_title('Top 5 Most Central Nodes per Centrality Measure', 
                fontsize=14, fontweight='bold')
    ax.legend(title='Node', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Footer
st.markdown("---")
st.markdown("**💡 Tip:** Use the sidebar to add/remove nodes and edges to see how it affects the graph metrics in real-time!")
