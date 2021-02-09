from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, EdgesAndLinkedNodes, NodesAndLinkedEdges, \
    LabelSet
from bokeh.plotting import figure, from_networkx, output_file
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from networkx.algorithms import community

# degrees

degrees = dict(nx.degree(G))
nx.set_node_attributes(G, name='degree', values=degrees)

number_to_adjust_by = 15
adjusted_node_size = dict([(node, degree + number_to_adjust_by) for node, degree in nx.degree(G)])
nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

# modularity

communities = community.greedy_modularity_communities(G)

modularity_class = {}
modularity_color = {}

for community_number, community in enumerate(communities):
    for name in community:
        modularity_class[name] = community_number
        modularity_color[name] = Spectral8[community_number]

# highlighting

node_highlight_color = 'white'
edge_highlight_color = 'black'

size_by_this_attribute = 'adjusted_node_size'
color_by_this_attribute = 'modularity_color'

# setup plot

color_palette = Blues8

title = 'European policy network'

HOVER_TOOLTIPS = [("Character", "@index"), ("Degree", "@degree"), ("Modularity Class", "@modularity_class"),
                  ("Modularity Color", "$color[swatch]:modularity_color")]

plot = figure(tooltips=HOVER_TOOLTIPS, tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
              x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

# setup graph

network_graph = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))

network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)
network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                 line_width=2)
network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                     line_width=2)

network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.3, line_width=1)
network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

network_graph.selection_policy = NodesAndLinkedEdges()
network_graph.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(network_graph)

# labels

x, y = zip(*network_graph.layout_provider.graph_layout.values())
node_labels = list(G.nodes())
source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px',
                  background_fill_alpha=.7)

plot.renderers.append(labels)

# display graph

show(plot)

output_file(r'file:///C:/Users/Henri%20van%20Soest/Documents/GitHub/EuropeanCybersecurityElectricity/Test_graph.html')

