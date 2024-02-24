from manim import *
from manim_svg_animations import *
from manim import *


# custom graph with parameters and added functions that is being used in the final project
class CustomGraph(Graph):
    def __init__(self, vertices, edges, layout="circular", layout_scale=2.5, label_color=WHITE, *args, **kwargs):

        default_vertex_config = {
            "color": DARK_BLUE,  # dark blue nodes
            "radius": 0.3,
            "stroke_color": WHITE,
            "stroke_width": 3,
            "fill_opacity": 1
        }
        default_edge_config = {
            "stroke_color": GREY,
            "stroke_width": 3,
        }

        vertex_config = kwargs.pop("vertex_config", {})
        edge_config = kwargs.pop("edge_config", {})
        default_vertex_config.update(vertex_config)
        default_edge_config.update(edge_config)

        kwargs["layout"] = layout
        kwargs["layout_scale"] = layout_scale

        super().__init__(vertices, edges, vertex_config=default_vertex_config, edge_config=default_edge_config, *args, **kwargs)

        # Add labels
        self.label_color = label_color
        self.add_labels()

        # Make edges invisible initially
        for edge in self.edges:
            self.edges[edge].set_opacity(0)


    def get_edges_with_initial_opacity_zero(self):
    # Set initial opacity of edges to 0 and return them
        for edge in self.edges.values():
            edge.set_opacity(0)
        return self.edges.values()
    
    def add_labels(self, font_size=24):
        labels = VGroup()
        for vertex in self.vertices:
            label = Text(str(vertex), color=self.label_color, font_size=font_size)
            label.move_to(self[vertex].get_center())
            labels.add(label)
        return labels  # Return the group of labels

    # animation to resize nodes
    def resize_nodes(self, new_size):
        animations = []
        for vertex in self.vertices:
            resize_animation = self[vertex].animate.set_radius(new_size)
            if resize_animation is not None:
                animations.append(resize_animation)
        return animations
