import os
from lingpy.compare.phylogeny import PhyBo

# Directory where your tree files are located
trees_directory = 'trees/'
output_directory = 'output'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Function to analyze sound changes and borrowing events for each tree
def analyze_trees():
    # Get a list of all tree files in the directory
    tree_files = [f for f in os.listdir(trees_directory) if f.startswith('tree_cogid') and f.endswith('.nwk')]
    
    for tree_file in tree_files:
        tree_path = os.path.join(trees_directory, tree_file)
        print(f"Processing tree file: {tree_path}")
        
        # Initialize PhyBo with the tree file
        phybo = PhyBo(dataset="", tree=tree_path, output_dir=output_directory)
        
        # Perform borrowing detection and sound change analysis
        detect_sound_changes_and_borrowing(phybo)


# Function to detect sound changes and borrowing events for a given PhyBo object
def detect_sound_changes_and_borrowing(phybo):
    # Get the list of all edges in the tree (this assumes the best model is selected)
    edges = list(phybo.graph[phybo.best_model].edges())
    
    # Loop through each edge to analyze sound changes and borrowing events
    for edge1, edge2 in edges:
        print(f"Analyzing edge between {edge1} and {edge2}")
        
        # Detect borrowing events
        borrowing_events = phybo.get_edge(phybo.best_model, edge1, edge2)
        print(f"Borrowing events between {edge1} and {edge2}: {borrowing_events}")
        
        # Detect sound changes
        sound_changes = phybo.get_edge(phybo.best_model, edge1, edge2, msn=True)
        print(f"Sound changes between {edge1} and {edge2}: {sound_changes}")


# Run the analysis on all trees in the directory
analyze_trees()


# Optional: Plotting results (if needed)
def plot_results(phybo):
    # Plot GLS (Gain-Loss Scenarios) and MLN (Minimal Lateral Network)
    phybo.get_GLS(mode='weighted', force=True)
    glm = list(phybo.stats.keys())[0]
    phybo.plot_GLS(glm)
    
    # Plot Minimal Lateral Network
    phybo.plot_MLN(glm)
    
    # Plot Minimal Spatial Network
    phybo.plot_MSN(glm)

# (Optional) Run plotting for each tree if needed
# You can add this line inside `analyze_trees_in_directory` if you'd like to plot the results after each analysis
# plot_results(phybo)
