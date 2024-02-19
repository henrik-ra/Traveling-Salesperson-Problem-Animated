from manim import *
from manim_svg_animations import *

import os
import random
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
from itertools import permutations

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from basics import CustomGraph

from scipy.special import gamma
import math

# voices: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts

DARK_BLUE_COLOR = "#00008b"

class TSP(MovingCameraScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural",
                style="newscast-casual",
            )
        ) 

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
       
        # Intro

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        with self.voiceover(text="Welcome back guys! Today, we're diving into the Traveling Salesperson Problem."):
            
            # draw circle with TSP text
            c = Circle(2, color= RED, fill_opacity = 0.1)
            self.play(DrawBorderThenFill(c), run_time = 0.5)
            title0 = Text("TSP", font_size = 96, slant = "ITALIC")
            self.play(Write(title0))

            a = Arc(2.2, TAU * 1/4, -TAU*2.6/4, color= BLUE, stroke_width=15)
            self.play(Create(a))

            self.wait(4)
            self.remove(a, c, title0)
            # self.remove(c)
            # self.remove(title0)

        with self.voiceover(text="Imagine we have a traveling salesperson - tasked with selling your products in various cities."):

            # Salesperson
            salesperson = ImageMobject("Salesman.png").scale(0.3)
            start_pos = salesperson.get_center()
            self.add(salesperson)

        with self.voiceover(text="This guy is Alex, a salesperson with a big challenge."):
            alex_label = Text("Alex", font_size=48).next_to(salesperson, UP*2, buff=0.1)

            # Add the label to the scene
            self.play(Write(alex_label))
            self.wait(3)
            self.remove(alex_label)
            self.remove(salesperson)


        with self.voiceover(text="Alex has to sell products in various cities and wants to take the shortest route to save time. But how does Alex figure out the best route? Let's dive in and help Alex solve this puzzle."):

            svg_object = SVGMobject("world.svg").scale(3).set_color(WHITE)
            self.add(svg_object)
            self.add(salesperson)

            # Move salesperson to different positions
            move_up_right = start_pos + 0.5*DOWN + 2.6*RIGHT
            move_down_left = start_pos + 1.5*DOWN + 2*LEFT
            move_up_left = start_pos + 1.5*UP + 2.5*LEFT

            self.play(salesperson.animate.move_to(move_up_right).scale(0.25))
            self.play(salesperson.animate.move_to(start_pos).scale(4))

            self.play(salesperson.animate.move_to(move_down_left).scale(0.25))
            self.play(salesperson.animate.move_to(start_pos).scale(4))

            self.play(salesperson.animate.move_to(move_up_left).scale(0.25))
            self.play(salesperson.animate.move_to(start_pos).scale(4))

            self.wait(4)
            self.remove(salesperson) 

        with self.voiceover(text="Let's say he needs to visit 4 cities."):
    
            # add warehouses to map
            warehouse_png = "warehouse.png"
            points0 = [
                ImageMobject(warehouse_png).scale(0.2).move_to(np.array([0, 0.5, 0])), # DE
                ImageMobject(warehouse_png).scale(0.2).move_to(np.array([3, -1.75, 0])), # Australia
                ImageMobject(warehouse_png).scale(0.2).move_to(np.array([0.5, -1.75, 0])), # Afrika
                ImageMobject(warehouse_png).scale(0.2).move_to(np.array([-3.35, 0, 0])), # USA
            ]

            for point in points0:
                self.add(point)

        with self.voiceover(text="Sounds straightforward, right? What do you think happens if we add one more city to Alex's route?"):

            connections = [
            (0, 1),  # connection between Germany and Africa
            (1, 2),  # connection between Africa and Australia
            (2, 3),  # connection betwwen Australia and USA
            (3, 0)   # connection between USA and Germany
            ]

            # add connections and move salesperson
            lines = []
            for start_index, end_index in connections:
                line = Line(points0[start_index].get_center(), points0[end_index].get_center(), color=BLUE)
                lines.append(line)

                temp_plane = salesperson.copy()
                temp_plane.move_to(points0[start_index].get_center())

                self.play(Create(line), MoveAlongPath(temp_plane, line), run_time=0.5)
                self.play(FadeOut(temp_plane), run_time=0.05)

            self.wait(4)

            for line in lines:
                self.remove(line)
            for point in points0:
                self.remove(point)

        with self.voiceover(text="Of course, if we add more cities it get's more complex. So how do you determine the shortest possible route that connects all these cities?"):
            # complex example for paths
            points = [
                Dot(np.array([0, 0.22, 0]), color=DARK_GREY), # Germany
                Dot(np.array([-0.28, -0.16, 0]), color=DARK_GREY), # Spain
                Dot(np.array([2.5, -0.5, 0]), color=DARK_GREY), # Asia
                Dot(np.array([2.5, 0.3, 0]), color=DARK_GREY), # Asia
                Dot(np.array([0.5, -2, 0]), color=DARK_GREY), # Africa
                Dot(np.array([3, -2, 0]), color=DARK_GREY), # Australia
                Dot(np.array([-1.5, -1.6, 0]), color=DARK_GREY), # South AMerica
                Dot(np.array([-3.35, 0, 0]), color=DARK_GREY), # USA
                Dot(np.array([-3, 0.5, 0]), color=DARK_GREY), # Canada
            ]

            for point in points:
                self.add(point)

        with self.voiceover(text="One approach is to try out every possible route. But here lies the problem: Complexity! So, with every new city Alex adds to the trip, the challenge of finding the shortest route grows significantly."):
            
            # Generate all permutations of points and animate - it's not real Brute Force but just for visualization
            point_indices = range(len(points))  
            all_routes = list(permutations(point_indices))

            for route in all_routes[:100]:
                path = VMobject(color=BLUE)
                path.set_points_as_corners([points[i].get_center() for i in route] + [points[route[0]].get_center()])
                self.play(Create(path), run_time=0.1)
                self.wait(0.05)
                self.remove(path) # Remove the path before drawing the next one

        for point in points:
            self.remove(point)
        self.play(FadeOut(svg_object))
 
 # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # self.next_section("Definitions") # Definitions

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # write TSP definition and conditions
        
        with self.voiceover(text="The Problem to find the shortest way between multiple points is called the Traveling Salesperson Problem (TSP). Alex goal is to keep the distance traveled as low as possible. "):
            definition = Text("find the shortest way between multiple points", font_size=30).move_to(ORIGIN).shift(UP)
            self.play(Write(definition))
            intro_text = Text("Traveling Salesperson Problem (TSP)").to_edge(UP)
            self.play(Write(intro_text))
 
        with self.voiceover(text="There are 2 main conditions: He needs to visit every city exactly once, starting from a specific one and returning to the starting city."):
            
            conditions = VGroup(
            Text("• visit every city once", font_size=24).next_to(definition, DOWN*2),
            Text("• return to the starting city", font_size=24).next_to(definition, DOWN*4)
        )
            self.play(Write(conditions))
            self.wait(3)
        
        self.wait(1)
        self.clear()

#  # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
#         # self.next_section("Assumptions") # Assumptions
        
# # -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#          # create plain graph
        with self.voiceover(text="To solve it, we'll think of each city as a point, or 'node', on a graph. The edges symbolize possible paths Alex can take. "):
            
            # self.remove(intro_text)
            
            # Define vertices and edges
            vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            edges = [(i, j) for i in vertices for j in vertices if i < j]

            graph = CustomGraph(vertices, edges)
            labels = graph.add_labels()

            # Animate the nodes and labels
            for vertex in graph.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.wait(1)

            # Group the graph and labels together and shift
            graph_with_labels = VGroup(graph, labels)
            self.play(graph_with_labels.animate.shift(LEFT*3).scale(0.8), run_time=1)
        
        # draw edges between nodes
        with self.voiceover(text="The graph is complete, this means there's a direct path from every city to every other city."):

            # Create and animate the text
            point_1 = Text("1. Complete graph", font_size=36)
            point_1.next_to(graph_with_labels, RIGHT, buff=1).shift(UP)   # Position the text to the right of the graph
            self.play(Write(point_1))
            
            # Animate the edges
            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(edge.animate.set_opacity(1), run_time=0.1)
            self.wait(1)

        # triangle inequality
        with self.voiceover(text="Also, in our model, the direct path between any two cities is always the shortest. This means for two cities A and B there is no path with an added point that is shorter than the direct connection.  adhering to the triangle inequality principle."):
                
                # adjust edge color back to grey
                self.play(graph.edges[(2,7)].animate.set_color(GREY), run_time=0.5) 
                
                # explain triangle inquality
                point_2 = Text("2. triangle inequality", font_size=36)
                point_2.next_to(point_1, DOWN, aligned_edge=LEFT)
                self.play(Write(point_2))

                # create visualized graph example
                vertices = [1, 2, 3]
                edges = [(1, 2), (2, 3)]

                layout = {
                    1: LEFT,
                    2: ORIGIN,
                    3: RIGHT
                }

                graph2 = CustomGraph(vertices, edges, layout=layout)

                label_a = Text("A", font_size=24).next_to(graph2.vertices[1], UP, buff=0.1)
                label_n = Text("n", font_size=24).next_to(graph2.vertices[2], UP, buff=0.1)
                label_b = Text("B", font_size=24).next_to(graph2.vertices[3], UP, buff=0.1)

                graph_with_labels = VGroup(graph2, label_a, label_n, label_b)
                graph_with_labels.shift(RIGHT*2.5 + DOWN*2)
                self.play(Create(graph_with_labels))

                # draw directed edges
                arrows = []
                for edge in edges:
                    start_pos = graph2.vertices[edge[0]].get_center()
                    end_pos = graph2.vertices[edge[1]].get_center()
                    arrow = Arrow(start_pos, end_pos, buff=0.3, tip_length=0.2, stroke_width=3, stroke_color=GREY)
                    self.add(arrow)
                    arrows.append(arrow)
                self.wait(2)

                for arrow in arrows: # delete arrows
                    self.play(FadeOut(arrow), run_time=0.5)

                # delete and create new graph with 2 nodes
                self.play(
                    FadeOut(graph2.vertices[2]), 
                    FadeOut(graph2.edges[(1, 2)]), 
                    FadeOut(graph2.edges[(2, 3)]),
                    FadeOut(label_n),
                    run_time=1
                )
                new_edge = Line(graph2.vertices[1].get_center(), graph2.vertices[3].get_center(), buff=0.3)
                new_edge.set_z_index(-1)  # Setzt die Z-Ebene der Kante hinter die Knoten
                self.play(Create(new_edge), run_time=1)
                self.wait(2)

                # delete
                self.remove(new_edge)
                self.play(FadeOut(graph_with_labels))
                

        # visualize connection from B to A and A to B
        with self.voiceover(text="Our TSP is symmetric. It means the distance from city A to B is identical to the distance from B to A."):

                # glow_effect.clear_updaters() # clear glow
                point_3 = Text("3. symmetric", font_size=36)
                point_3.next_to(point_2, DOWN, aligned_edge=LEFT)
                self.play(Write(point_3))

                # highlight edge
                self.play(graph.edges[(2,7)].animate.set_color(RED), run_time=0.5)
                self.wait(2)

                # add point and glow effect
                moving_dot = Dot(color=RED, radius=0.1)
                glow_effect = Circle(radius=0.15, color=RED, fill_opacity=0.5)
                glow_effect.add_updater(lambda m: m.move_to(moving_dot.get_center()))

                start_pos = graph.vertices[2].get_center()
                end_pos = graph.vertices[7].get_center()

                edge_path = Line(start_pos, end_pos)
                self.add(moving_dot, glow_effect)

                # animate point
                self.play(MoveAlongPath(moving_dot, edge_path), run_time=1.5)
                self.wait(1)
                self.play(MoveAlongPath(moving_dot, edge_path.reverse_direction()), run_time=1.5)

        # with self.voiceover(text="With these rules in mind, let's explore how Alex can find the shortest route."):
        #     None
        self.play(FadeOut(moving_dot), FadeOut(glow_effect), run_time=0.5)       
        

        self.asymmetric()

 # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # self.next_section("Algorithms Overview") # Algorithms Overview
        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        with self.voiceover(text="To solve the TSP, we have two primary approaches: the Optimal and the Approximation methods."):
            self.wait(2)

            # Optimal approach
            box1 = Rectangle(width=3, height=1, fill_color=DARK_BLUE, fill_opacity=1).shift(LEFT*2.5)
            box1_text = Text("Optimal", color=WHITE).scale(0.5)
            box1_text.move_to(box1.get_center())
            box1_label = Text("Brute Force\n\nBranch and Bound", color=WHITE, font_size=40).scale(0.5)
            box1_label.next_to(box1, DOWN)

            # Approximation
            box2 = Rectangle(width=3, height=1, fill_color=DARK_BLUE, fill_opacity=1).shift(RIGHT*2.5)
            box2_text = Text("Approximation", color=WHITE).scale(0.5)
            box2_text.move_to(box2.get_center())
            box2_label = Text("Christofides\n\nkNN", color=WHITE, font_size=40).scale(0.5)
            box2_label.next_to(box2, DOWN)

            # Animate both categories
            self.play(DrawBorderThenFill(box1, run_time=0.5))
            self.play(Write(box1_text))

            self.play(DrawBorderThenFill(box2, run_time=0.5))
            self.play(Write(box2_text))
        
        with self.voiceover(text="In the Optimal category, we have two prominent algorithms: Brute Force and Branch and Bound."):
            self.wait(3)
            self.add(box1_label)

        with self.voiceover(text="Moving on to the Approximation approach, we'll explain the algorithms Christofides and k nearest neighbors (kNN). But let's start with the optimal solutions first."):
            self.wait(3)
            self.add(box2_label)

        self.clear()
        self.wait(1)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # self.next_section("Brute Force") # Brute Force
        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # add graph
        with self.voiceover(text="The Brute Force method is a straightforward but time-consuming approach to solve the TSP. It involves trying out all possible orders in which the cities can be visited."):
            intro_text = Text("Brute Force").to_edge(UP)
            self.play(Write(intro_text))

            vertices = [1, 2, 3, 4, 5]
            edges = [(i, j) for i in vertices for j in vertices if i != j]

            original_graph = CustomGraph(vertices, edges, layout="circular", layout_scale=2.5).scale(0.6).shift(LEFT * 5)
            labels = original_graph.add_labels(font_size=20)
            self.play(Create(original_graph))
            self.add(labels)

        # generate all possible and unique paths
        with self.voiceover(text="As the first step in our Brute-Force algorithm, we generate all possible permutations of the cities. This means creating every possible order in which the cities can be visited."):
            
            shift_value = [UP * 1.5 + RIGHT * 4, UP * 1.5 + RIGHT * 6, UP * 1.5 + RIGHT * 8, UP * 1.5 + RIGHT * 10, 
                        RIGHT * 4 + DOWN*0.5, RIGHT * 6 + DOWN*0.5, RIGHT * 8 + DOWN*0.5, RIGHT * 10 + DOWN*0.5, 
                        DOWN * 2.5 + RIGHT * 4, DOWN * 2.5 + RIGHT * 6, DOWN * 2.5 + RIGHT * 8, DOWN * 2.5 + RIGHT * 10]

            values_distance = ["5", "5.83", "5.83", "6.24", "6.24", "5.83","5.83", "6.24", "6.24", "7.07", "5.83", "6.24"] # lengt of path

            hamiltonian_cycles = [
                [1, 2, 3, 4, 5, 1],
                [1, 2, 3, 5, 4, 1],
                [1, 2, 4, 3, 5, 1],
                [1, 2, 4, 5, 3, 1],
                [1, 2, 5, 3, 4, 1],
                [1, 2, 5, 4, 3, 1],
                [1, 3, 2, 4, 5, 1],
                [1, 3, 2, 5, 4, 1],
                [1, 3, 4, 2, 5, 1],
                [1, 3, 5, 2, 4, 1],
                [1, 4, 3, 2, 5, 1],
                [1, 4, 2, 3, 5, 1],
            ] # all unique paths

            # animate graph creation and move graph afterwards
            value_pos = []
            for i, cycle in enumerate(hamiltonian_cycles):
                graph_raw = original_graph.copy()
                self.add(graph_raw)
                labels = graph_raw.add_labels(font_size=20)

                graph = VGroup(graph_raw, labels)
                self.add(graph)

                for j in range(len(cycle) - 1):
                    edge = (cycle[j], cycle[j + 1])
                    if edge in graph[0].edges:
                        self.play(graph[0].edges[edge].animate.set_opacity(1), run_time=0.05)
                    elif (edge[1], edge[0]) in graph[0].edges:
                        self.play(graph[0].edges[(edge[1], edge[0])].animate.set_opacity(1), run_time=0.05)

                self.wait(0.1)
                self.play(graph.animate.shift(shift_value[i]).scale(0.42), run_time=0.4)
                
                value_text = Text(values_distance[i], font_size=15)
                value_text.next_to(graph, DOWN)
                value_pos.append(value_text)
                self.wait(0.2)

        # add distances
        with self.voiceover(text="Then, For each generated permutation, we calculate the length of the tour by summing the distances between the visited cities."):
            self.wait(5)
            for i in value_pos:
                self.play(Write(i), run_time=0.1)
            
        self.wait(1)

        # highlight shortest path
        with self.voiceover(text="Now, we need to Identify the tour with the shortest length among all the calculated tours. This is the optimal solution to the Traveling Salesperson Problem."):
            self.wait(7)
            empty_rectangle = Rectangle(width=1.7, height=2, fill_opacity=0, color=ORANGE).shift(UP*1.35+LEFT*0.8)
            self.play(Create(empty_rectangle))
        
        self.wait(1)
        self.clear()

        # number of possible paths formula      
        with self.voiceover(text="We can calculate the number of possible paths as the number of possible permutations of n elements when each permutation is counted as a separate operation"):
            formula_text = MathTex(r"\frac{(n-1)!}{2}").scale(1)
            formula_text.move_to(UP * 2)
            self.play(Write(formula_text))
            self.wait(2)

        # 5 nodes
        with self.voiceover(text="For the example we've seen before we used 5 nodes, so we get 12 possible routes."):
            transformed_formula = MathTex(r"\frac{(5-1)!}{2} = 12").scale(1)
            transformed_formula.next_to(formula_text, DOWN)
            self.play(Transform(formula_text, transformed_formula))
            self.wait(2)

        # 6 nodes   
        with self.voiceover(text="If we just increase the number of nodes by 1, we already get 60 possible routes."):
            transformed_formula = MathTex(r"\frac{(6-1)!}{2} = 60").scale(1.5)
            self.play(Transform(formula_text, transformed_formula))
            self.wait(2)
        
        # 10 nodes
        with self.voiceover(text="For 10 nodes, it's already 181440 potential shortest paths!!"):
            transformed_formula = MathTex(r"\frac{(10-1)!}{2} = 181440").scale(2)
            self.play(Transform(formula_text, transformed_formula))
            self.wait(2)
        
        self.clear()
        self.wait(1)
       
#        # time complexity
        with self.voiceover(text="So we got a factorial time complexity for the Brute Force algorithm."):
            
            axes = Axes(
                x_range=[0, 20],  
                y_range=[0, 720], 
                y_length=5,
                x_length=8,
                tips=False,  
                axis_config={"include_ticks": False, "color": WHITE},
            )

            # Erstellen der x-Achsenbeschriftung
            x_label = Tex("nodes/cities")
            x_label.next_to(axes.x_axis.get_end(), DOWN + LEFT, buff=0.2).scale(0.7)  # Positionierung unter der x-Achse, rechtsbündig

            # Erstellen der y-Achsenbeschriftung
            y_label = Tex("time\_complexity").rotate(PI / 2, about_point=ORIGIN).scale(0.7)  # Drehung um 90 Grad
            y_label.next_to(axes.y_axis, LEFT, buff=0.2)  # Positionierung links neben der y-Achse
            self.add(axes, x_label, y_label)

            self.wait(2)

            bold_template = TexTemplate()
            bold_template.add_to_preamble(r"\usepackage{bm}")

            def plot_function(function, color, label, position=RIGHT, range=[0,20]):
                function0 = axes.plot(function, x_range=range).set_stroke(width=3).set_color(color)
                return function0, Tex(label, tex_template=bold_template).set_color(color).scale(0.6).next_to(function0.point_from_proportion(1), position)
    
            fact, fact_tag  = plot_function(lambda x: gamma(x) if x > 1 else x**2, YELLOW, r"$\bm{O(n!)}$\\Brute Force", range=[0,7], position=LEFT)
            self.play(LaggedStart(fact.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(fact_tag))

            self.wait(1)

            self.play(FadeOut(axes), FadeOut(fact, fact_tag, x_label, y_label))
            self.wait(1)

            self.clear()
            self.wait(1)

# # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
#         # self.next_section("Branch and Bound") # Branch and Bound
        
# # -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    

        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5]
        edges = [(1,2), (2,3), (3,4), (4,5), (5,1)]

        # function to create an edge from the center of two vertices
        def create_edge_from_vertex_centers(graph, start_node, end_node, buffer=0.32):

            direction = graph.vertices[end_node].get_center() - graph.vertices[start_node].get_center()
            direction = direction / np.linalg.norm(direction) * buffer

            start_point = graph.vertices[start_node].get_center() + direction
            end_point = graph.vertices[end_node].get_center() - direction
            edge = Line(start_point, end_point)
            edge.set_stroke(GREY, width=3)
            return edge


        with self.voiceover(text="Another way of solving the TSP is with the help of the branch and bound method. Let's start with a simple TSP example. Again we have a set of cities and need to find the shortest possible route visiting each city exactly once.") as tracker:

            self.wait(3)
            bab_text = Text("Branch and Bound").shift(UP*3.5)
            self.play(Write(bab_text))

            # create graph
            graph = CustomGraph(vertices, edges).shift(RIGHT * 0)

            labels = graph.add_labels()

            self.wait(3.5)

            # animate the nodes
            for vertex in graph.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)
            
            # add and animate the labels
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.wait(4)

            # create edges
            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(edge.animate.set_opacity(1), run_time=0.5)

            self.wait(1)

            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(FadeOut(edge), run_time=0.1)
            
            self.play(FadeOut(bab_text))

            # group the graph and labels together
            graph_with_labels = VGroup(graph, labels) 

            # scale camera
            self.play(
                self.camera.frame.animate.scale(1.1)
            )

            self.play(graph_with_labels.animate.shift(LEFT*5).scale(0.5), run_time=0.5)

            
        # create tree
        with self.voiceover(text="The Branch-and-Bound method begins by constructing a tree of all possibilities. First we need a Graph. Let's use the same graph and start at node one. ") as tracker:
            
            self.wait(4.5)

            graph2 = CustomGraph(vertices, edges).shift(RIGHT * 4)

            labels = graph2.add_labels()

            vertex_groups = {}
            for vertex in graph2.vertices:
                label = labels[vertex - 1] 
                vertex_groups[vertex] = VGroup(graph2.vertices[vertex], label)

            # animate the nodes
            for vertex in graph2.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)
            
            # add and animate the labels
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.wait(2)

            kreis_um_knoten1 = Circle(color=RED)
            kreis_um_knoten1.surround(graph.vertices[1])

            self.play(Create(kreis_um_knoten1))

        with self.voiceover(text="Now we have to look at the next possible nodes. In this case we have four options. We can go to node 2, 3, 4 or 5. ") as tracker:
            
            # surround the nodes with a circle
            self.wait(3)
            kreis_um_knoten2 = Circle(color=RED)
            kreis_um_knoten2.surround(graph.vertices[2])

            kreis_um_knoten3 = Circle(color=RED)
            kreis_um_knoten3.surround(graph.vertices[3])

            kreis_um_knoten4 = Circle(color=RED)
            kreis_um_knoten4.surround(graph.vertices[4])

            kreis_um_knoten5 = Circle(color=RED)
            kreis_um_knoten5.surround(graph.vertices[5])
            

            # draw a red line between the centers of the circles
            linie_zwischen_kreis1_und_2 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten2.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_2.set_color(RED)

            linie_zwischen_kreis1_und_3 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten3.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_3.set_color(RED)

            linie_zwischen_kreis1_und_4 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten4.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_4.set_color(RED)

            linie_zwischen_kreis1_und_5 = Line(kreis_um_knoten1.get_center(), kreis_um_knoten5.get_center(), buff=0.3)
            linie_zwischen_kreis1_und_5.set_color(RED)

            self.play(Create(linie_zwischen_kreis1_und_2))
            self.play(Create(kreis_um_knoten2))

            self.play(Create(linie_zwischen_kreis1_und_3))
            self.play(Create(kreis_um_knoten3))

            self.play(Create(linie_zwischen_kreis1_und_4))
            self.play(Create(kreis_um_knoten4))

            self.play(Create(linie_zwischen_kreis1_und_5))
            self.play(Create(kreis_um_knoten5))

            

        with self.voiceover(text="At the same time we can transform the graph on the right to a tree with node one as the root. This tree will show all the possible routes that the salesperson can use. As explained, starting with node one the next possible nodes could be node 2, 3, 4 or 5.") as tracker:

            self.wait(3)
            
            # move node
            self.play(vertex_groups[1].animate.move_to(UP * 3.75 + RIGHT * 2))

            # new positions for the nodes
            positions = [
                    LEFT  + UP * 2.25,  # node 2
                    RIGHT + UP * 2.25,  # node 3
                    RIGHT * 3 + UP * 2.25,  # node 4
                    RIGHT * 5 + UP * 2.25  # node 5
            ]
            for i, node in enumerate([2, 3, 4, 5], start=0):
                self.play(vertex_groups[node].animate.move_to(positions[i]))

            self.wait(5)

            # create edges between node one and the others
            for node in [2, 3, 4, 5]:
                edge = create_edge_from_vertex_centers(graph2, 1, node)
                self.play(Create(edge), run_time=0.5)

        with self.voiceover(text="This would be the first version of the tree. Now we have to take a look at the next steps. Let's say we choose node 2 as the second node to travel to.") as tracker:

            self.wait(7)
            
            # connect nodes
            linie_zwischen_kreis1_und_2_weiß = Line(kreis_um_knoten1.get_center(), kreis_um_knoten2.get_center(), buff=0.2)


            self.play(FadeOut(linie_zwischen_kreis1_und_2, 
                              linie_zwischen_kreis1_und_3, 
                              linie_zwischen_kreis1_und_4, 
                              linie_zwischen_kreis1_und_5, 
                              kreis_um_knoten1,
                              kreis_um_knoten2,
                              kreis_um_knoten3, 
                              kreis_um_knoten4, 
                              kreis_um_knoten5))
            
            self.play(Create(linie_zwischen_kreis1_und_2_weiß))


        with self.voiceover(text="Starting from node 2, the next options would be node 3, 4 or 5.") as tracker:

            # new circle and lines
            kreis_um_knoten2 = Circle(color=RED)
            kreis_um_knoten2.surround(graph.vertices[2])

            kreis_um_knoten3 = Circle(color=RED)
            kreis_um_knoten3.surround(graph.vertices[3])

            kreis_um_knoten4 = Circle(color=RED)
            kreis_um_knoten4.surround(graph.vertices[4])

            kreis_um_knoten5 = Circle(color=RED)
            kreis_um_knoten5.surround(graph.vertices[5])
            

            linie_zwischen_kreis2_und_3 = Line(kreis_um_knoten2.get_center(), kreis_um_knoten3.get_center(), buff=0.3)
            linie_zwischen_kreis2_und_3.set_color(RED)

            linie_zwischen_kreis2_und_4 = Line(kreis_um_knoten2.get_center(), kreis_um_knoten4.get_center(), buff=0.3)
            linie_zwischen_kreis2_und_4.set_color(RED)

            linie_zwischen_kreis2_und_5 = Line(kreis_um_knoten2.get_center(), kreis_um_knoten5.get_center(), buff=0.3)
            linie_zwischen_kreis2_und_5.set_color(RED)

            self.play(Create(kreis_um_knoten2))
            
            self.play(Create(linie_zwischen_kreis2_und_3))
            self.play(Create(kreis_um_knoten3))

            self.play(Create(linie_zwischen_kreis2_und_4))
            self.play(Create(kreis_um_knoten4))

            self.play(Create(linie_zwischen_kreis2_und_5))
            self.play(Create(kreis_um_knoten5))

        with self.voiceover(text="Now we can create the next step at the tree. Again the next possible nodes to travel to would be node 3, 4 and 5. ") as tracker:

            self.camera.frame.save_state()

            # move camera and scale
            self.play(
                self.camera.frame.animate.move_to(LEFT * 0.5).scale(0.7)
            )

            self.wait(2)

            # graph in tree
            vertex3 = [3, 4, 5]
            graph3 = CustomGraph(vertex3, [])

            

            relative_positionen = {
                3: LEFT * 1.5 + DOWN * 1.5,  
                4: DOWN * 1.5,         
                5: RIGHT * 1.5 + DOWN * 1.5  
            }

            
            for node in vertex3:
                graph3.vertices[node].move_to(graph2.vertices[2].get_center() + relative_positionen[node])


            for vertex in graph3.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)


            for node in vertex3:
                kante_von_2_zu_node = Line(graph2.vertices[2].get_center(), graph3.vertices[node].get_center(), buff=0.3)
                kante_von_2_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_2_zu_node), run_time=0.5)

            labels = graph3.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            # restore camera
            self.play(Restore(self.camera.frame))


        with self.voiceover(text="Let's continue creating one possible route. We decide to travel to node 5 as our next city. ") as tracker:

            self.wait(3)

            # create new circle and lines for next node
            linie_zwischen_kreis2_und_5_weiß = Line(kreis_um_knoten2.get_center(), kreis_um_knoten5.get_center(), buff=0.2)


            self.play(FadeOut(kreis_um_knoten2, linie_zwischen_kreis2_und_3, linie_zwischen_kreis2_und_4, linie_zwischen_kreis2_und_5, kreis_um_knoten3, kreis_um_knoten4, kreis_um_knoten5))
            
            self.play(Create(linie_zwischen_kreis2_und_5_weiß))



        with self.voiceover(text="Starting from node 5, there are two cities left that have not been visited yet. Node 3 and 4.") as tracker:

            self.wait(2)

            # same steps as before for new node
            kreis_um_knoten5 = Circle(color=RED)
            kreis_um_knoten5.surround(graph.vertices[5])

            kreis_um_knoten3 = Circle(color=RED)
            kreis_um_knoten3.surround(graph.vertices[3])

            kreis_um_knoten4 = Circle(color=RED)
            kreis_um_knoten4.surround(graph.vertices[4])

            linie_zwischen_kreis5_und_3 = Line(kreis_um_knoten5.get_center(), kreis_um_knoten3.get_center(), buff=0.3)
            linie_zwischen_kreis5_und_3.set_color(RED)

            linie_zwischen_kreis5_und_4 = Line(kreis_um_knoten5.get_center(), kreis_um_knoten4.get_center(), buff=0.3)
            linie_zwischen_kreis5_und_4.set_color(RED)

            self.play(Create(kreis_um_knoten5))

            self.play(Create(linie_zwischen_kreis5_und_3))
            self.play(Create(kreis_um_knoten3))
            
            self.play(Create(linie_zwischen_kreis5_und_4))
            self.play(Create(kreis_um_knoten4))
            


        with self.voiceover(text="Let's go back to the tree and add the last two options, node 3 and 4") as tracker:

            self.camera.frame.save_state()

            # same steps as before for new node
            self.play(
                self.camera.frame.animate.move_to(DOWN * 1 + 0.5 * RIGHT).scale(0.7)
            )
            self.wait(4)

            vertex4 = [3, 4]
            graph4 = CustomGraph(vertex4, [])

            relative_positionen4 = {
                3: LEFT * 0.75 + DOWN * 1.5,  
                4: RIGHT * 0.75 + DOWN * 1.5,         
            }

            for node in vertex4:
                graph4.vertices[node].move_to(graph3.vertices[5].get_center() + relative_positionen4[node])

            for vertex in graph4.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)


            for node in vertex4:
                kante_von_5_zu_node = Line(graph3.vertices[5].get_center(), graph4.vertices[node].get_center(), buff=0.3)
                kante_von_5_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_5_zu_node), run_time=0.5)

            labels = graph4.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            self.play(Restore(self.camera.frame))


        with self.voiceover(text="This time we choose node 3 as the next city.") as tracker:

            self.wait(3)

            # same steps as before for new node
            linie_zwischen_kreis5_und_3_weiß = Line(kreis_um_knoten5.get_center(), kreis_um_knoten3.get_center(), buff=0.2)


            self.play(FadeOut(kreis_um_knoten5, kreis_um_knoten3, kreis_um_knoten4, linie_zwischen_kreis5_und_3, linie_zwischen_kreis5_und_4))
            
            self.play(Create(linie_zwischen_kreis5_und_3_weiß))


        with self.voiceover(text="As you can see the last city, that we have not visited is city 4.") as tracker:

            self.wait(2)
            linie_zwischen_kreis3_und_4_weiß = Line(kreis_um_knoten3.get_center(), kreis_um_knoten4.get_center(), buff=0.2)

            self.play(Create(linie_zwischen_kreis3_und_4_weiß))


        with self.voiceover(text="Let's also add node 4 in the tree. Now we have visited every city.") as tracker:


            self.camera.frame.save_state()

            self.play(
                self.camera.frame.animate.move_to(DOWN * 2).scale(0.7)
            )

            vertex5 = [4]
            graph5 = CustomGraph(vertex5, [])

            relative_positionen5 = {
                4: DOWN * 1.5,         
            }

            for node in vertex5:
                graph5.vertices[node].move_to(graph4.vertices[3].get_center() + relative_positionen5[node])

            for vertex in graph5.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)

            for node in vertex5:
                kante_von_3_zu_node = Line(graph4.vertices[3].get_center(), graph5.vertices[node].get_center(), buff=0.3)
                kante_von_3_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_3_zu_node), run_time=0.5)
            
            labels = graph5.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            self.play(Restore(self.camera.frame))

        with self.voiceover(text="At the end we have to travel to the city where we started the tour. Let's finish our route by traveling back to city 1.") as tracker:

            self.wait(3)

            linie_zwischen_kreis4_und_1_weiß = Line(kreis_um_knoten4.get_center(), kreis_um_knoten1.get_center(), buff=0.2)
            
            self.play(Create(linie_zwischen_kreis4_und_1_weiß))

        with self.voiceover(text="Now we can also finish our route on the tree by adding node 1 as our last node.") as tracker:

            self.camera.frame.save_state()

            self.play(
                self.camera.frame.animate.move_to(DOWN * 3 + RIGHT * 0.5).scale(0.7)
            )

            vertex6 = [1]
            graph6 = CustomGraph(vertex6, [])

            relative_positionen6 = {
                1: DOWN * 1.5,         
            }

            for node in vertex6:
                graph6.vertices[node].move_to(graph5.vertices[4].get_center() + relative_positionen6[node])

            for vertex in graph6.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)

            for node in vertex6:
                kante_von_4_zu_node = Line(graph5.vertices[4].get_center(), graph6.vertices[node].get_center(), buff=0.3)
                kante_von_4_zu_node.set_stroke(WHITE, width=2)
                self.play(Create(kante_von_4_zu_node), run_time=0.5)
            
            labels = graph6.add_labels()
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)

            self.play(Restore(self.camera.frame))


# create complete tree
# tree consists of mulltiple graphs which are connected through edges
# # -----------------------------------------------------------------------------------------------------------------------------------------------------------------

        with self.voiceover(text="As you can see this is one possible route and the tree is not complete. Let's create the complete tree.") as tracker:

            self.wait(3)

        # create group for complete tree
        gesamter_baum = VGroup()

        self.camera.frame.save_state()

        # fade out all elements
        self.play(
        *[FadeOut(mob)for mob in self.mobjects]
        )
            
        self.play(
            self.camera.frame.animate.scale(2.2)
        )

        # first part of tree
        vertex1_1 = [1]

        graph1_1 = CustomGraph(vertex1_1, [])

        # position of node
        relative_positionen1_1 = {
            1: UP * 6,       
        }

        for node in vertex1_1:
            graph1_1.vertices[node].move_to(relative_positionen1_1[node])

        # add labels
        labels1_1 = graph1_1.add_labels()
        self.add(labels1_1)             
            
        # second part of tree
        vertex2_1 = [2, 3, 4, 5]

        graph2_1 = CustomGraph(vertex2_1, [])

        relative_positionen2_1 = {
            2: LEFT * 12 + DOWN * 2.5,  
            3: LEFT * 4 + DOWN * 2.5,        
            4: RIGHT * 4 + DOWN * 2.5,  
            5: RIGHT * 12 + DOWN * 2.5  
        }

  
        for node in vertex2_1:
            graph2_1.vertices[node].move_to(graph1_1.vertices[1].get_center() + relative_positionen2_1[node])


        for node in vertex2_1:
            kante_von_1_zu_node = Line(graph1_1.vertices[1].get_center(), graph2_1.vertices[node].get_center(), buff=0.3)
            kante_von_1_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_1_zu_node)


        labels2_1 = graph2_1.add_labels()
        self.add(labels2_1)

        # third part of tree
        vertex3_1 = [3, 4, 5]

        graph3_1 = CustomGraph(vertex3_1, [])

        relative_positionen3_1 = {
            3: LEFT * 2.5 + DOWN * 2,  
            4: DOWN * 2,         
            5: RIGHT * 2.5 + DOWN * 2  
        }

        for node in vertex3_1:
            graph3_1.vertices[node].move_to(graph2_1.vertices[2].get_center() + relative_positionen3_1[node])


        for node in vertex3_1:
            kante_von_2_zu_node = Line(graph2_1.vertices[2].get_center(), graph3_1.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)


        labels3_1 = graph3_1.add_labels()
        self.add(labels3_1)

        # third level has more parts
        vertex3_2 = [2, 4, 5]

        graph3_2 = CustomGraph(vertex3_2, [])

        relative_positionen3_2 = {
            2: LEFT * 2.5 + DOWN * 2,  
            4: DOWN * 2,        
            5: RIGHT * 2.5 + DOWN * 2  
        }

        for node in vertex3_2:
            graph3_2.vertices[node].move_to(graph2_1.vertices[3].get_center() + relative_positionen3_2[node])


        for node in vertex3_2:
            kante_von_3_zu_node = Line(graph2_1.vertices[3].get_center(), graph3_2.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)



        labels3_2 = graph3_2.add_labels()
        self.add(labels3_2)


        vertex3_3 = [2, 3, 5]

        graph3_3 = CustomGraph(vertex3_3, [])

        relative_positionen3_3 = {
            2: LEFT * 2.5 + DOWN * 2,  
            3: DOWN * 2,         
            5: RIGHT * 2.5 + DOWN * 2  
        }

        for node in vertex3_3:
            graph3_3.vertices[node].move_to(graph2_1.vertices[4].get_center() + relative_positionen3_3[node])


        for node in vertex3_3:
            kante_von_4_zu_node = Line(graph2_1.vertices[4].get_center(), graph3_3.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)


        labels3_3 = graph3_3.add_labels()
        self.add(labels3_3)

        # last part of third level
        vertex3_4 = [2, 3, 4]

        graph3_4 = CustomGraph(vertex3_4, [])

        relative_positionen3_4 = {
            2: LEFT * 2.5 + DOWN * 2,  
            3: DOWN * 2,         
            4: RIGHT * 2.5 + DOWN * 2 
        }

        for node in vertex3_4:
            graph3_4.vertices[node].move_to(graph2_1.vertices[5].get_center() + relative_positionen3_4[node])



        for node in vertex3_4:
            kante_von_5_zu_node = Line(graph2_1.vertices[5].get_center(), graph3_4.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)


        labels3_4 = graph3_4.add_labels()
        self.add(labels3_4)

        # fourth level

        vertex4_1 = [4, 5]

        graph4_1 = CustomGraph(vertex4_1, [])

        relative_positionen4_1 = {
            4: LEFT * 0.75 + DOWN * 1.5,         
            5: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_1:
            graph4_1.vertices[node].move_to(graph3_1.vertices[3].get_center() + relative_positionen4_1[node])

        for node in vertex4_1:
            kante_von_3_zu_node = Line(graph3_1.vertices[3].get_center(), graph4_1.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels4_1 = graph4_1.add_labels()
        self.add(labels4_1)

        vertex4_2 = [3, 5]	

        graph4_2 = CustomGraph(vertex4_2, [])

        relative_positionen4_2 = {
            3: LEFT * 0.75 + DOWN * 1.5, 
            5: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_2:
            graph4_2.vertices[node].move_to(graph3_1.vertices[4].get_center() + relative_positionen4_2[node])

        for node in vertex4_2:
            kante_von_2_zu_node = Line(graph3_1.vertices[4].get_center(), graph4_2.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels4_2 = graph4_2.add_labels()
        self.add(labels4_2)

        vertex4_3 = [3, 4]

        graph4_3 = CustomGraph(vertex4_3, [])

        relative_positionen4_3 = {
            3: LEFT * 0.75 + DOWN * 1.5, 
            4: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_3:
            graph4_3.vertices[node].move_to(graph3_1.vertices[5].get_center() + relative_positionen4_3[node])

        for node in vertex4_3:
            kante_von_2_zu_node = Line(graph3_1.vertices[5].get_center(), graph4_3.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels4_3 = graph4_3.add_labels()
        self.add(labels4_3)

        vertex4_4 = [4,5]

        graph4_4 = CustomGraph(vertex4_4, [])

        relative_positionen4_4 = {
            4: LEFT * 0.75 + DOWN * 1.5, 
            5: RIGHT * 0.75 + DOWN * 1.5 
        }

        for node in vertex4_4:
            graph4_4.vertices[node].move_to(graph3_2.vertices[2].get_center() + relative_positionen4_4[node])

        for node in vertex4_4:
            kante_von_2_zu_node = Line(graph3_2.vertices[2].get_center(), graph4_4.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels4_4 = graph4_4.add_labels()
        self.add(labels4_4)

        vertex4_5 = [2, 5]

        graph4_5 = CustomGraph(vertex4_5, [])

        relative_positionen4_5 = {
            2: LEFT * 0.75 + DOWN * 1.5,  
            5: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_5:
            graph4_5.vertices[node].move_to(graph3_2.vertices[4].get_center() + relative_positionen4_5[node])

        for node in vertex4_5:
            kante_von_4_zu_node = Line(graph3_2.vertices[4].get_center(), graph4_5.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels4_5 = graph4_5.add_labels()
        self.add(labels4_5)

        vertex4_6 = [2, 4]

        graph4_6 = CustomGraph(vertex4_6, [])

        relative_positionen4_6 = {
            2: LEFT * 0.75 + DOWN * 1.5,  
            4: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_6:
            graph4_6.vertices[node].move_to(graph3_2.vertices[5].get_center() + relative_positionen4_6[node])

        for node in vertex4_6:
            kante_von_4_zu_node = Line(graph3_2.vertices[5].get_center(), graph4_6.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels4_6 = graph4_6.add_labels()
        self.add(labels4_6)

        vertex4_7 = [3, 5]

        graph4_7 = CustomGraph(vertex4_7, [])

        relative_positionen4_7 = {
            3: LEFT * 0.75 + DOWN * 1.5,  
            5: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_7:
            graph4_7.vertices[node].move_to(graph3_3.vertices[2].get_center() + relative_positionen4_7[node])


        for node in vertex4_7:
            kante_von_2_zu_node = Line(graph3_3.vertices[2].get_center(), graph4_7.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels4_7 = graph4_7.add_labels()
        self.add(labels4_7)

        vertex4_8 = [2, 5]

        graph4_8 = CustomGraph(vertex4_8, [])

        relative_positionen4_8 = {
            2: LEFT * 0.75 + DOWN * 1.5,  
            5: RIGHT * 0.75 + DOWN * 1.5 
        }

        for node in vertex4_8:
            graph4_8.vertices[node].move_to(graph3_3.vertices[3].get_center() + relative_positionen4_8[node])

        for node in vertex4_8:
            kante_von_3_zu_node = Line(graph3_3.vertices[3].get_center(), graph4_8.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels4_8 = graph4_8.add_labels()
        self.add(labels4_8)

        vertex4_9 = [2, 3]

        graph4_9 = CustomGraph(vertex4_9, [])

        relative_positionen4_9 = {
            2: LEFT * 0.75 + DOWN * 1.5,  
            3: RIGHT * 0.75 + DOWN * 1.5  
        }

        for node in vertex4_9:
            graph4_9.vertices[node].move_to(graph3_3.vertices[5].get_center() + relative_positionen4_9[node])

        for node in vertex4_9:
            kante_von_3_zu_node = Line(graph3_3.vertices[5].get_center(), graph4_9.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels4_9 = graph4_9.add_labels()
        self.add(labels4_9)

        vertex4_10 = [3, 4]

        graph4_10 = CustomGraph(vertex4_10, [])

        relative_positionen4_10 = {
            3: LEFT * 0.75 + DOWN * 1.5, 
            4: RIGHT * 0.75 + DOWN * 1.5 
        }

        for node in vertex4_10:
            graph4_10.vertices[node].move_to(graph3_4.vertices[2].get_center() + relative_positionen4_10[node])

        for node in vertex4_10:
            kante_von_2_zu_node = Line(graph3_4.vertices[2].get_center(), graph4_10.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels4_10 = graph4_10.add_labels()
        self.add(labels4_10)

        vertex4_11 = [2, 4]
            
        graph4_11 = CustomGraph(vertex4_11, [])

        relative_positionen4_11 = {
            2: LEFT * 0.75 + DOWN * 1.5,  
            4: RIGHT * 0.75 + DOWN * 1.5 
        }

        for node in vertex4_11:
            graph4_11.vertices[node].move_to(graph3_4.vertices[3].get_center() + relative_positionen4_11[node])

        for node in vertex4_11:
            kante_von_3_zu_node = Line(graph3_4.vertices[3].get_center(), graph4_11.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels4_11 = graph4_11.add_labels()
        self.add(labels4_11)

        vertex4_12 = [2, 3]
            
        graph4_12 = CustomGraph(vertex4_12, [])

        relative_positionen4_12 = {
            2: LEFT * 0.75 + DOWN * 1.5,
            3: RIGHT * 0.75 + DOWN * 1.5 
        }

        for node in vertex4_12:
            graph4_12.vertices[node].move_to(graph3_4.vertices[4].get_center() + relative_positionen4_12[node])

        for node in vertex4_12:
            kante_von_3_zu_node = Line(graph3_4.vertices[4].get_center(), graph4_12.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels4_12 = graph4_12.add_labels()
        self.add(labels4_12)

        # fifth level

        vertex5_1 = [5]

        graph5_1 = CustomGraph(vertex5_1, [])

        relative_positionen5_1 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_1:
            graph5_1.vertices[node].move_to(graph4_1.vertices[4].get_center() + relative_positionen5_1[node])

        for node in vertex5_1:
            kante_von_4_zu_node = Line(graph4_1.vertices[4].get_center(), graph5_1.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_1 = graph5_1.add_labels()
        self.add(labels5_1)

        vertex5_2 = [4]

        graph5_2 = CustomGraph(vertex5_2, [])

        relative_positionen5_2 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_2:
            graph5_2.vertices[node].move_to(graph4_1.vertices[5].get_center() + relative_positionen5_2[node])

        for node in vertex5_2:
            kante_von_2_zu_node = Line(graph4_1.vertices[5].get_center(), graph5_2.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_2 = graph5_2.add_labels()
        self.add(labels5_2)

        vertex5_3 = [5]

        graph5_3 = CustomGraph(vertex5_3, [])

        relative_positionen5_3 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_3:
            graph5_3.vertices[node].move_to(graph4_2.vertices[3].get_center() + relative_positionen5_3[node])

        for node in vertex5_3:
            kante_von_4_zu_node = Line(graph4_2.vertices[3].get_center(), graph5_3.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_3 = graph5_3.add_labels()
        self.add(labels5_3)

        vertex5_4 = [3]

        graph5_4 = CustomGraph(vertex5_4, [])

        relative_positionen5_4 = {
            3: DOWN * 1.5,        
        }

        for node in vertex5_4:
            graph5_4.vertices[node].move_to(graph4_2.vertices[5].get_center() + relative_positionen5_4[node])

        for node in vertex5_4:
            kante_von_2_zu_node = Line(graph4_2.vertices[5].get_center(), graph5_4.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_4 = graph5_4.add_labels()
        self.add(labels5_4)

        vertex5_5 = [4]

        graph5_5 = CustomGraph(vertex5_5, [])

        relative_positionen5_5 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_5:
            graph5_5.vertices[node].move_to(graph4_3.vertices[3].get_center() + relative_positionen5_5[node])

        for node in vertex5_5:
            kante_von_3_zu_node = Line(graph4_3.vertices[3].get_center(), graph5_5.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels5_5 = graph5_5.add_labels()
        self.add(labels5_5)

        vertex5_6 = [3]

        graph5_6 = CustomGraph(vertex5_6, [])

        relative_positionen5_6 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_6:
            graph5_6.vertices[node].move_to(graph4_3.vertices[4].get_center() + relative_positionen5_6[node])

        for node in vertex5_6:
            kante_von_2_zu_node = Line(graph4_3.vertices[4].get_center(), graph5_6.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_6 = graph5_6.add_labels()
        self.add(labels5_6)

        vertex5_7 = [5]

        graph5_7 = CustomGraph(vertex5_7, [])

        relative_positionen5_7 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_7:
            graph5_7.vertices[node].move_to(graph4_4.vertices[4].get_center() + relative_positionen5_7[node])

        for node in vertex5_7:
            kante_von_2_zu_node = Line(graph4_4.vertices[4].get_center(), graph5_7.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_7 = graph5_7.add_labels()
        self.add(labels5_7)

        vertex5_8 = [4]
        graph5_8 = CustomGraph(vertex5_8, [])
        relative_positionen5_8 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_8:
            graph5_8.vertices[node].move_to(graph4_4.vertices[5].get_center() + relative_positionen5_8[node])

        for node in vertex5_8:
            kante_von_3_zu_node = Line(graph4_4.vertices[5].get_center(), graph5_8.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels5_8 = graph5_8.add_labels()
        self.add(labels5_8)

        vertex5_9 = [5]
        graph5_9 = CustomGraph(vertex5_9, [])
        relative_positionen5_9 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_9:
            graph5_9.vertices[node].move_to(graph4_5.vertices[2].get_center() + relative_positionen5_9[node])

        for node in vertex5_9:
            kante_von_2_zu_node = Line(graph4_5.vertices[2].get_center(), graph5_9.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_9 = graph5_9.add_labels()
        self.add(labels5_9)

        vertex5_10 = [2]
        graph5_10 = CustomGraph(vertex5_10, [])
        relative_positionen5_10 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_10:
            graph5_10.vertices[node].move_to(graph4_5.vertices[5].get_center() + relative_positionen5_10[node])

        for node in vertex5_10:
            kante_von_3_zu_node = Line(graph4_5.vertices[5].get_center(), graph5_10.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels5_10 = graph5_10.add_labels()
        self.add(labels5_10)

        vertex5_11 = [4]
        graph5_11 = CustomGraph(vertex5_11, [])
        relative_positionen5_11 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_11:
            graph5_11.vertices[node].move_to(graph4_6.vertices[2].get_center() + relative_positionen5_11[node])

        for node in vertex5_11:
            kante_von_2_zu_node = Line(graph4_6.vertices[2].get_center(), graph5_11.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_11 = graph5_11.add_labels()
        self.add(labels5_11)

        vertex5_12 = [2]
        graph5_12 = CustomGraph(vertex5_12, [])
        relative_positionen5_12 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_12:
            graph5_12.vertices[node].move_to(graph4_6.vertices[4].get_center() + relative_positionen5_12[node])

        for node in vertex5_12:
            kante_von_4_zu_node = Line(graph4_6.vertices[4].get_center(), graph5_12.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_12 = graph5_12.add_labels()
        self.add(labels5_12)

        vertex5_13 = [5]
        graph5_13 = CustomGraph(vertex5_13, [])
        relative_positionen5_13 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_13:
            graph5_13.vertices[node].move_to(graph4_7.vertices[3].get_center() + relative_positionen5_13[node])

        for node in vertex5_13:
            kante_von_4_zu_node = Line(graph4_7.vertices[3].get_center(), graph5_13.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_13 = graph5_13.add_labels()
        self.add(labels5_13)

        vertex5_14 = [3]
        graph5_14 = CustomGraph(vertex5_14, [])
        relative_positionen5_14 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_14:
            graph5_14.vertices[node].move_to(graph4_7.vertices[5].get_center() + relative_positionen5_14[node])

        for node in vertex5_14:
            kante_von_4_zu_node = Line(graph4_7.vertices[5].get_center(), graph5_14.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_14 = graph5_14.add_labels()
        self.add(labels5_14)

        vertex5_15 = [5]
        graph5_15 = CustomGraph(vertex5_15, [])
        relative_positionen5_15 = {
            5: DOWN * 1.5,         
        }

        for node in vertex5_15:
            graph5_15.vertices[node].move_to(graph4_8.vertices[2].get_center() + relative_positionen5_15[node])

        for node in vertex5_15:
            kante_von_2_zu_node = Line(graph4_8.vertices[2].get_center(), graph5_15.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_15 = graph5_15.add_labels()
        self.add(labels5_15)

        vertex5_16 = [2]
        graph5_16 = CustomGraph(vertex5_16, [])
        relative_positionen5_16 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_16:
            graph5_16.vertices[node].move_to(graph4_8.vertices[5].get_center() + relative_positionen5_16[node])

        for node in vertex5_16:
            kante_von_3_zu_node = Line(graph4_8.vertices[5].get_center(), graph5_16.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels5_16 = graph5_16.add_labels()
        self.add(labels5_16)

        vertex5_17 = [3]
        graph5_17 = CustomGraph(vertex5_17, [])
        relative_positionen5_17 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_17:
            graph5_17.vertices[node].move_to(graph4_9.vertices[2].get_center() + relative_positionen5_17[node])

        for node in vertex5_17:
            kante_von_2_zu_node = Line(graph4_9.vertices[2].get_center(), graph5_17.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_17 = graph5_17.add_labels()
        self.add(labels5_17)

        vertex5_18 = [2]
        graph5_18 = CustomGraph(vertex5_18, [])
        relative_positionen5_18 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_18:
            graph5_18.vertices[node].move_to(graph4_9.vertices[3].get_center() + relative_positionen5_18[node])

        for node in vertex5_18:
            kante_von_3_zu_node = Line(graph4_9.vertices[3].get_center(), graph5_18.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels5_18 = graph5_18.add_labels()
        self.add(labels5_18)

        vertex5_19 = [4]
        graph5_19 = CustomGraph(vertex5_19, [])
        relative_positionen5_19 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_19:
            graph5_19.vertices[node].move_to(graph4_10.vertices[3].get_center() + relative_positionen5_19[node])

        for node in vertex5_19:
            kante_von_2_zu_node = Line(graph4_10.vertices[3].get_center(), graph5_19.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_19 = graph5_19.add_labels()
        self.add(labels5_19)

        vertex5_20 = [3]
        graph5_20 = CustomGraph(vertex5_20, [])
        relative_positionen5_20 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_20:
            graph5_20.vertices[node].move_to(graph4_10.vertices[4].get_center() + relative_positionen5_20[node])

        for node in vertex5_20:
            kante_von_4_zu_node = Line(graph4_10.vertices[4].get_center(), graph5_20.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_20 = graph5_20.add_labels()
        self.add(labels5_20)

        vertex5_21 = [4]
        graph5_21 = CustomGraph(vertex5_21, [])
        relative_positionen5_21 = {
            4: DOWN * 1.5,         
        }

        for node in vertex5_21:
            graph5_21.vertices[node].move_to(graph4_11.vertices[2].get_center() + relative_positionen5_21[node])


        for node in vertex5_21:
            kante_von_2_zu_node = Line(graph4_11.vertices[2].get_center(), graph5_21.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_21 = graph5_21.add_labels()
        self.add(labels5_21)

        vertex5_22 = [2]
        graph5_22 = CustomGraph(vertex5_22, [])
        relative_positionen5_22 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_22:
            graph5_22.vertices[node].move_to(graph4_11.vertices[4].get_center() + relative_positionen5_22[node])

        for node in vertex5_22:
            kante_von_4_zu_node = Line(graph4_11.vertices[4].get_center(), graph5_22.vertices[node].get_center(), buff=0.3)
            kante_von_4_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_4_zu_node)

        labels5_22 = graph5_22.add_labels()
        self.add(labels5_22)

        vertex5_23 = [3]
        graph5_23 = CustomGraph(vertex5_23, [])
        relative_positionen5_23 = {
            3: DOWN * 1.5,         
        }

        for node in vertex5_23:
            graph5_23.vertices[node].move_to(graph4_12.vertices[2].get_center() + relative_positionen5_23[node])

        for node in vertex5_23:
            kante_von_2_zu_node = Line(graph4_12.vertices[2].get_center(), graph5_23.vertices[node].get_center(), buff=0.3)
            kante_von_2_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_2_zu_node)

        labels5_23 = graph5_23.add_labels()
        self.add(labels5_23)

        vertex5_24 = [2]
        graph5_24 = CustomGraph(vertex5_24, [])
        relative_positionen5_24 = {
            2: DOWN * 1.5,         
        }

        for node in vertex5_24:
            graph5_24.vertices[node].move_to(graph4_12.vertices[3].get_center() + relative_positionen5_24[node])
        
        for node in vertex5_24:
            kante_von_3_zu_node = Line(graph4_12.vertices[3].get_center(), graph5_24.vertices[node].get_center(), buff=0.3)
            kante_von_3_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_3_zu_node)

        labels5_24 = graph5_24.add_labels()
        self.add(labels5_24)

        # node one as last node, sixth level

        vertex6_1 = [1]
        graph6_1 = CustomGraph(vertex6_1, [])
        relative_positionen6_1 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_1:
            graph6_1.vertices[node].move_to(graph5_1.vertices[5].get_center() + relative_positionen6_1[node])

        for node in vertex6_1:
            kante_von_5_zu_node = Line(graph5_1.vertices[5].get_center(), graph6_1.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_1 = graph6_1.add_labels()
        self.add(labels6_1)

        vertex6_2 = [1]
        graph6_2 = CustomGraph(vertex6_2, [])
        relative_positionen6_2 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_2:
            graph6_2.vertices[node].move_to(graph5_2.vertices[4].get_center() + relative_positionen6_2[node])

        for node in vertex6_2:
            kante_von_5_zu_node = Line(graph5_2.vertices[4].get_center(), graph6_2.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_2 = graph6_2.add_labels()
        self.add(labels6_2)

        vertex6_3 = [1]
        graph6_3 = CustomGraph(vertex6_3, [])
        relative_positionen6_3 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_3:
            graph6_3.vertices[node].move_to(graph5_3.vertices[5].get_center() + relative_positionen6_3[node])

        for node in vertex6_3:
            kante_von_5_zu_node = Line(graph5_3.vertices[5].get_center(), graph6_3.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_3 = graph6_3.add_labels()
        self.add(labels6_3)

        vertex6_4 = [1]
        graph6_4 = CustomGraph(vertex6_4, [])
        relative_positionen6_4 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_4:
            graph6_4.vertices[node].move_to(graph5_4.vertices[3].get_center() + relative_positionen6_4[node])

        for node in vertex6_4:
            kante_von_5_zu_node = Line(graph5_4.vertices[3].get_center(), graph6_4.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_4 = graph6_4.add_labels()
        self.add(labels6_4)

        vertex6_5 = [1]
        graph6_5 = CustomGraph(vertex6_5, [])
        relative_positionen6_5 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_5:
            graph6_5.vertices[node].move_to(graph5_5.vertices[4].get_center() + relative_positionen6_5[node])

        for node in vertex6_5:
            kante_von_5_zu_node = Line(graph5_5.vertices[4].get_center(), graph6_5.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_5 = graph6_5.add_labels()
        self.add(labels6_5)

        vertex6_6 = [1]
        graph6_6 = CustomGraph(vertex6_6, [])
        relative_positionen6_6 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_6:
            graph6_6.vertices[node].move_to(graph5_6.vertices[3].get_center() + relative_positionen6_6[node])

        for node in vertex6_6:
            kante_von_5_zu_node = Line(graph5_6.vertices[3].get_center(), graph6_6.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_6 = graph6_6.add_labels()
        self.add(labels6_6)

        vertex6_7 = [1]
        graph6_7 = CustomGraph(vertex6_7, [])
        relative_positionen6_7 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_7:
            graph6_7.vertices[node].move_to(graph5_7.vertices[5].get_center() + relative_positionen6_7[node])

        for node in vertex6_7:
            kante_von_5_zu_node = Line(graph5_7.vertices[5].get_center(), graph6_7.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_7 = graph6_7.add_labels()
        self.add(labels6_7)

        vertex6_8 = [1]
        graph6_8 = CustomGraph(vertex6_8, [])
        relative_positionen6_8 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_8:
            graph6_8.vertices[node].move_to(graph5_8.vertices[4].get_center() + relative_positionen6_8[node])

        for node in vertex6_8:
            kante_von_5_zu_node = Line(graph5_8.vertices[4].get_center(), graph6_8.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_8 = graph6_8.add_labels()
        self.add(labels6_8)

        vertex6_9 = [1]
        graph6_9 = CustomGraph(vertex6_9, [])
        relative_positionen6_9 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_9:
            graph6_9.vertices[node].move_to(graph5_9.vertices[5].get_center() + relative_positionen6_9[node])
        
        for node in vertex6_9:
            kante_von_5_zu_node = Line(graph5_9.vertices[5].get_center(), graph6_9.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_9 = graph6_9.add_labels()
        self.add(labels6_9)

        vertex6_10 = [1]
        graph6_10 = CustomGraph(vertex6_10, [])
        relative_positionen6_10 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_10:
            graph6_10.vertices[node].move_to(graph5_10.vertices[2].get_center() + relative_positionen6_10[node])

        for node in vertex6_10:
            kante_von_5_zu_node = Line(graph5_10.vertices[2].get_center(), graph6_10.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_10 = graph6_10.add_labels()
        self.add(labels6_10)

        vertex6_11 = [1]
        graph6_11 = CustomGraph(vertex6_11, [])
        relative_positionen6_11 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_11:
            graph6_11.vertices[node].move_to(graph5_11.vertices[4].get_center() + relative_positionen6_11[node])


        for node in vertex6_11:
            kante_von_5_zu_node = Line(graph5_11.vertices[4].get_center(), graph6_11.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_11 = graph6_11.add_labels()
        self.add(labels6_11)

        vertex6_12 = [1]
        graph6_12 = CustomGraph(vertex6_12, [])
        relative_positionen6_12 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_12:
            graph6_12.vertices[node].move_to(graph5_12.vertices[2].get_center() + relative_positionen6_12[node])

        for node in vertex6_12:
            kante_von_5_zu_node = Line(graph5_12.vertices[2].get_center(), graph6_12.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_12 = graph6_12.add_labels()
        self.add(labels6_12)

        vertex6_13 = [1]
        graph6_13 = CustomGraph(vertex6_13, [])
        relative_positionen6_13 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_13:
            graph6_13.vertices[node].move_to(graph5_13.vertices[5].get_center() + relative_positionen6_13[node])

        for node in vertex6_13:
            kante_von_5_zu_node = Line(graph5_13.vertices[5].get_center(), graph6_13.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_13 = graph6_13.add_labels()
        self.add(labels6_13)

        vertex6_14 = [1]
        graph6_14 = CustomGraph(vertex6_14, [])
        relative_positionen6_14 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_14:
            graph6_14.vertices[node].move_to(graph5_14.vertices[3].get_center() + relative_positionen6_14[node])

        for node in vertex6_14:
            kante_von_5_zu_node = Line(graph5_14.vertices[3].get_center(), graph6_14.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_14 = graph6_14.add_labels()
        self.add(labels6_14)

        vertex6_15 = [1]
        graph6_15 = CustomGraph(vertex6_15, [])
        relative_positionen6_15 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_15:
            graph6_15.vertices[node].move_to(graph5_15.vertices[5].get_center() + relative_positionen6_15[node])

        for node in vertex6_15:
            kante_von_5_zu_node = Line(graph5_15.vertices[5].get_center(), graph6_15.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_15 = graph6_15.add_labels()
        self.add(labels6_15)

        vertex6_16 = [1]
        graph6_16 = CustomGraph(vertex6_16, [])
        relative_positionen6_16 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_16:
            graph6_16.vertices[node].move_to(graph5_16.vertices[2].get_center() + relative_positionen6_16[node])

        for node in vertex6_16:
            kante_von_5_zu_node = Line(graph5_16.vertices[2].get_center(), graph6_16.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_16 = graph6_16.add_labels()
        self.add(labels6_16)

        vertex6_17 = [1]
        graph6_17 = CustomGraph(vertex6_17, [])
        relative_positionen6_17 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_17:
            graph6_17.vertices[node].move_to(graph5_17.vertices[3].get_center() + relative_positionen6_17[node])

        for node in vertex6_17:
            kante_von_5_zu_node = Line(graph5_17.vertices[3].get_center(), graph6_17.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_17 = graph6_17.add_labels()
        self.add(labels6_17)

        vertex6_18 = [1]
        graph6_18 = CustomGraph(vertex6_18, [])
        relative_positionen6_18 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_18:
            graph6_18.vertices[node].move_to(graph5_18.vertices[2].get_center() + relative_positionen6_18[node])

        for node in vertex6_18:
            kante_von_5_zu_node = Line(graph5_18.vertices[2].get_center(), graph6_18.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_18 = graph6_18.add_labels()
        self.add(labels6_18)

        vertex6_19 = [1]
        graph6_19 = CustomGraph(vertex6_19, [])
        relative_positionen6_19 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_19:
            graph6_19.vertices[node].move_to(graph5_19.vertices[4].get_center() + relative_positionen6_19[node])

        for node in vertex6_19:
            kante_von_5_zu_node = Line(graph5_19.vertices[4].get_center(), graph6_19.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_19 = graph6_19.add_labels()
        self.add(labels6_19)

        vertex6_20 = [1]
        graph6_20 = CustomGraph(vertex6_20, [])
        relative_positionen6_20 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_20:
            graph6_20.vertices[node].move_to(graph5_20.vertices[3].get_center() + relative_positionen6_20[node])

        for node in vertex6_20:
            kante_von_5_zu_node = Line(graph5_20.vertices[3].get_center(), graph6_20.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_20 = graph6_20.add_labels()
        self.add(labels6_20)

        vertex6_21 = [1]
        graph6_21 = CustomGraph(vertex6_21, [])
        relative_positionen6_21 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_21:
            graph6_21.vertices[node].move_to(graph5_21.vertices[4].get_center() + relative_positionen6_21[node])
        
        for node in vertex6_21:
            kante_von_5_zu_node = Line(graph5_21.vertices[4].get_center(), graph6_21.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_21 = graph6_21.add_labels()
        self.add(labels6_21)

        vertex6_22 = [1]
        graph6_22 = CustomGraph(vertex6_22, [])
        relative_positionen6_22 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_22:
            graph6_22.vertices[node].move_to(graph5_22.vertices[2].get_center() + relative_positionen6_22[node])

        for node in vertex6_22:
            kante_von_5_zu_node = Line(graph5_22.vertices[2].get_center(), graph6_22.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_22 = graph6_22.add_labels()
        self.add(labels6_22)

        vertex6_23 = [1]
        graph6_23 = CustomGraph(vertex6_23, [])
        relative_positionen6_23 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_23:
            graph6_23.vertices[node].move_to(graph5_23.vertices[3].get_center() + relative_positionen6_23[node])

        for node in vertex6_23:
            kante_von_5_zu_node = Line(graph5_23.vertices[3].get_center(), graph6_23.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_23 = graph6_23.add_labels()
        self.add(labels6_23)

        vertex6_24 = [1]
        graph6_24 = CustomGraph(vertex6_24, [])
        relative_positionen6_24 = {
            1: DOWN * 1.5,         
        }

        for node in vertex6_24:
            graph6_24.vertices[node].move_to(graph5_24.vertices[2].get_center() + relative_positionen6_24[node])

        for node in vertex6_24:
            kante_von_5_zu_node = Line(graph5_24.vertices[2].get_center(), graph6_24.vertices[node].get_center(), buff=0.3)
            kante_von_5_zu_node.set_stroke(WHITE, width=2)
            gesamter_baum.add(kante_von_5_zu_node)

        labels6_24 = graph6_24.add_labels()
        self.add(labels6_24)

        # group whole graph with all nodes, labels and edges

        gesamter_baum.add(graph1_1, graph2_1, graph3_1, graph3_2, graph3_3, graph3_4, graph4_1, graph4_2, graph4_3, graph4_4, graph4_5, graph4_6, graph4_7, graph4_8, graph4_9, graph4_10, graph4_11, graph4_12, graph5_1, graph5_2, graph5_3, graph5_4, graph5_5, graph5_6, graph5_7, graph5_8, graph5_9, graph5_10, graph5_11, graph5_12, graph5_13, graph5_14, graph5_15, graph5_16, graph5_17, graph5_18, graph5_19, graph5_20, graph5_21, graph5_22, graph5_23, graph5_24, graph6_1, graph6_2, graph6_3, graph6_4, graph6_5, graph6_6, graph6_7, graph6_8, graph6_9, graph6_10, graph6_11, graph6_12, graph6_13, graph6_14, graph6_15, graph6_16, graph6_17, graph6_18, graph6_19, graph6_20, graph6_21, graph6_22, graph6_23, graph6_24, labels1_1, labels2_1, labels3_1, labels3_2, labels3_3, labels3_4, labels4_1, labels4_2, labels4_3, labels4_4, labels4_5, labels4_6, labels4_7, labels4_8, labels4_9, labels4_10, labels4_11, labels4_12, labels5_1, labels5_2, labels5_3, labels5_4, labels5_5, labels5_6, labels5_7, labels5_8, labels5_9, labels5_10, labels5_11, labels5_12, labels5_13, labels5_14, labels5_15, labels5_16, labels5_17, labels5_18, labels5_19, labels5_20, labels5_21, labels5_22, labels5_23, labels5_24, labels6_1, labels6_2, labels6_3, labels6_4, labels6_5, labels6_6, labels6_7, labels6_8, labels6_9, labels6_10, labels6_11, labels6_12, labels6_13, labels6_14, labels6_15, labels6_16, labels6_17, labels6_18, labels6_19, labels6_20, labels6_21, labels6_22, labels6_23, labels6_24)

        # fade in whole graph
        self.play(FadeIn(gesamter_baum), run_time=1)

# tree is done
# # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        


        with self.voiceover(text="This tree shows every possible route, if you start from node one. Here we can now see that there are 24 possible routes to get to the last node. But is you take a closer look at the first and last route, you can see that the routes are identical, if we have a symmetrical TSP. That means if we have a symmetrical TSP, as in our example, we can ignore half of the routes."):
            
            self.wait(10)

            # show first and last route on tree

            # first route, nodes
            kreis_um_1 = Circle(color=RED, radius=0.5)
            kreis_um_1.surround(graph1_1.vertices[1])

            kreis_um_2 = Circle(color=RED, radius=0.6)
            kreis_um_2.surround(graph2_1.vertices[2])

            kreis_um_3 = Circle(color=RED)
            kreis_um_3.surround(graph3_1.vertices[3])

            kreis_um_4 = Circle(color=RED)
            kreis_um_4.surround(graph4_1.vertices[4])

            kreis_um_5 = Circle(color=RED, radius=0.7)
            kreis_um_5.surround(graph5_1.vertices[5])
            
            kreis_um_1_2 = Circle(color=RED)
            kreis_um_1_2.surround(graph6_1.vertices[1])

            # first route, edges
            linie_zw_1_2 = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie_zw_1_2.set_stroke(RED)

            linie_zw_2_3 = Line(kreis_um_2.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie_zw_2_3.set_stroke(RED)

            linie_zw_3_4 = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie_zw_3_4.set_stroke(RED)

            linie_zw_4_5 = Line(kreis_um_4.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie_zw_4_5.set_stroke(RED)

            linie_zw_5_1 = Line(kreis_um_5.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie_zw_5_1.set_stroke(RED)

            # last route, nodes
            kreis2_um_5 = Circle(color=RED)
            kreis2_um_5.surround(graph2_1.vertices[5]) 

            kreis2_um_4 = Circle(color=RED)
            kreis2_um_4.surround(graph3_4.vertices[4])

            kreis2_um_3 = Circle(color=RED)
            kreis2_um_3.surround(graph4_12.vertices[3])

            kreis2_um_2 = Circle(color=RED)
            kreis2_um_2.surround(graph5_24.vertices[2])

            kreis2_um_1 = Circle(color=RED)
            kreis2_um_1.surround(graph6_24.vertices[1])

            # last route, edges
            linie2_zw_1_5 = Line(kreis2_um_5.get_center(), kreis_um_1.get_center(), buff=0.3)
            linie2_zw_1_5.set_stroke(RED)

            linie2_zw_5_4 = Line(kreis2_um_4.get_center(), kreis2_um_5.get_center(), buff=0.3)
            linie2_zw_5_4.set_stroke(RED)

            linie2_zw_4_3 = Line(kreis2_um_3.get_center(), kreis2_um_4.get_center(), buff=0.3)
            linie2_zw_4_3.set_stroke(RED)

            linie2_zw_3_2 = Line(kreis2_um_2.get_center(), kreis2_um_3.get_center(), buff=0.3)
            linie2_zw_3_2.set_stroke(RED)

            linie2_zw_2_1 = Line(kreis2_um_1.get_center(), kreis2_um_2.get_center(), buff=0.3)
            linie2_zw_2_1.set_stroke(RED)

            # show first and last route on tree
            self.play(Create(linie_zw_1_2), run_time=0.5)
            self.play(Create(linie_zw_2_3), run_time=0.5)
            self.play(Create(linie_zw_3_4), run_time=0.5)
            self.play(Create(linie_zw_4_5), run_time=0.5)
            self.play(Create(linie_zw_5_1), run_time=0.5)

            self.play(Create(linie2_zw_2_1), run_time=0.5)
            self.play(Create(linie2_zw_3_2), run_time=0.5)
            self.play(Create(linie2_zw_4_3), run_time=0.5)
            self.play(Create(linie2_zw_5_4), run_time=0.5)
            self.play(Create(linie2_zw_1_5), run_time=0.5)
            
            self.wait(5)

            # fade out first and last route
            self.play(FadeOut(linie_zw_1_2, linie_zw_2_3, linie_zw_3_4, linie_zw_4_5, linie_zw_5_1), run_time=1)
            self.play(FadeOut(linie2_zw_1_5, linie2_zw_5_4, linie2_zw_4_3, linie2_zw_3_2, linie2_zw_2_1), run_time=1)

        # mark out redundant routes
        kreis1 = Circle(color=RED, radius=0.5)
        kreis1.set_fill(RED, opacity=1.0)
        kreis1.surround(graph6_10.vertices[1])

        kreis2 = Circle(color=RED, radius=0.5)
        kreis2.set_fill(RED, opacity=1.0)
        kreis2.surround(graph6_12.vertices[1])

        kreis3 = Circle(color=RED, radius=0.5)
        kreis3.set_fill(RED, opacity=1.0)
        kreis3.surround(graph6_14.vertices[1])

        kreis4 = Circle(color=RED, radius=0.5)
        kreis4.set_fill(RED, opacity=1.0)
        kreis4.surround(graph6_16.vertices[1])

        kreis5 = Circle(color=RED, radius=0.5)
        kreis5.set_fill(RED, opacity=1.0)
        kreis5.surround(graph6_17.vertices[1])

        kreis6 = Circle(color=RED, radius=0.5)
        kreis6.set_fill(RED, opacity=1.0)
        kreis6.surround(graph6_18.vertices[1])

        kreis7 = Circle(color=RED, radius=0.5)
        kreis7.set_fill(RED, opacity=1.0)
        kreis7.surround(graph6_19.vertices[1])

        kreis8 = Circle(color=RED, radius=0.5)
        kreis8.set_fill(RED, opacity=1.0)
        kreis8.surround(graph6_20.vertices[1])

        kreis9 = Circle(color=RED, radius=0.5)
        kreis9.set_fill(RED, opacity=1.0)
        kreis9.surround(graph6_21.vertices[1])

        kreis10 = Circle(color=RED, radius=0.5)
        kreis10.set_fill(RED, opacity=1.0)
        kreis10.surround(graph6_22.vertices[1])

        kreis11 = Circle(color=RED, radius=0.5)
        kreis11.set_fill(RED, opacity=1.0)
        kreis11.surround(graph6_23.vertices[1])

        kreis12 = Circle(color=RED, radius=0.5)
        kreis12.set_fill(RED, opacity=1.0)
        kreis12.surround(graph6_24.vertices[1])

        with self.voiceover(text="Let's mark out the routes that we can ignore."):

            self.wait(2)
            self.play(Create(kreis1), Create(kreis2),Create(kreis3),Create(kreis4), Create(kreis5),  Create(kreis6), Create(kreis7), Create(kreis8), Create(kreis9), Create(kreis10), Create(kreis11), Create(kreis12), run_time=0.5)
  

        self.wait(2)



        with self.voiceover(text="Here we can also visualize which route we took in the first example."):

            self.wait(2)

            # red line from node one to node two, then node two to node 5, then node 5 to node 3, then to node 4, then to node 1
            kreis_um_1 = Circle(color=RED, radius=0.5)
            kreis_um_1.surround(graph1_1.vertices[1])

            kreis_um_2 = Circle(color=RED, radius=0.6)
            kreis_um_2.surround(graph2_1.vertices[2])

            kreis_um_5 = Circle(color=RED, radius=0.7)
            kreis_um_5.surround(graph3_1.vertices[5])

            kreis_um_3 = Circle(color=RED)
            kreis_um_3.surround(graph4_3.vertices[3])

            kreis_um_4 = Circle(color=RED)
            kreis_um_4.surround(graph5_5.vertices[4])

            kreis_um_1_2 = Circle(color=RED)
            kreis_um_1_2.surround(graph6_5.vertices[1])

            # edges
            linie_zw_1_2 = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie_zw_1_2.set_stroke(RED)

            linie_zw_2_5 = Line(kreis_um_2.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie_zw_2_5.set_stroke(RED)

            linie_zw_5_3 = Line(kreis_um_5.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie_zw_5_3.set_stroke(RED)

            linie_zw_3_4 = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie_zw_3_4.set_stroke(RED)

            linie_zw_4_1 = Line(kreis_um_4.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie_zw_4_1.set_stroke(RED)

            self.play(Create(linie_zw_1_2), run_time=0.5)
            self.play(Create(linie_zw_2_5), run_time=0.5)
            self.play(Create(linie_zw_5_3), run_time=0.5)
            self.play(Create(linie_zw_3_4), run_time=0.5)
            self.play(Create(linie_zw_4_1), run_time=0.5)



        with self.voiceover(text="After having created a tree for every possible route, the branch and bound method calculates the cost for every route and compares it to the best route so far. If the cost of the current route is higher than the cost of the best route so far, the current route will be discarded."):
            self.wait(6)

        with self.voiceover(text="Let's take a look at an example. Lets say the algorithm calculated our route first with the cost of 15. As it is the first route, it is also the best route so far."):
            self.wait(6)

            number15 = Text("15", font_size=30)
            number15.next_to(graph6_5.vertices[1], DOWN, buff=1)
            self.play(FadeIn(number15), run_time=0.5)

            self.wait(4)

            # yellow line for best route
            linie_zw_1_2_o = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie_zw_1_2_o.set_stroke(YELLOW)

            linie_zw_2_5_o = Line(kreis_um_2.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie_zw_2_5_o.set_stroke(YELLOW)

            linie_zw_5_3_o = Line(kreis_um_5.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie_zw_5_3_o.set_stroke(YELLOW)

            linie_zw_3_4_o = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie_zw_3_4_o.set_stroke(YELLOW)

            linie_zw_4_1_o = Line(kreis_um_4.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie_zw_4_1_o.set_stroke(YELLOW)

            self.play(Create(linie_zw_1_2_o), run_time=0.5)
            self.play(Create(linie_zw_2_5_o), run_time=0.5)
            self.play(Create(linie_zw_5_3_o), run_time=0.5)
            self.play(Create(linie_zw_3_4_o), run_time=0.5)
            self.play(Create(linie_zw_4_1_o), run_time=0.5)

            self.play(FadeOut(linie_zw_1_2, linie_zw_2_5,linie_zw_5_3, linie_zw_3_4, linie_zw_4_1), run_time=0)

        with self.voiceover(text="Next, the algorithm calculates the route on the left. The cost of this route is 12. As this route is better than the best route so far, it becomes the new best route."):


            self.wait(2)
            
            # new route
            kreis_um_1 = Circle(color=RED, radius=0.5)
            kreis_um_1.surround(graph1_1.vertices[1])

            kreis_um_2 = Circle(color=RED, radius=0.6)
            kreis_um_2.surround(graph2_1.vertices[2])

            kreis_um_3 = Circle(color=RED)
            kreis_um_3.surround(graph3_1.vertices[3])

            kreis_um_4 = Circle(color=RED)
            kreis_um_4.surround(graph4_1.vertices[4])

            kreis_um_5 = Circle(color=RED, radius=0.7)
            kreis_um_5.surround(graph5_1.vertices[5])
            
            kreis_um_1_2 = Circle(color=RED)
            kreis_um_1_2.surround(graph6_1.vertices[1])

            # edges of new route
            linie2_zw_1_2 = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie2_zw_1_2.set_stroke(RED)

            linie2_zw_2_3 = Line(kreis_um_2.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie2_zw_2_3.set_stroke(RED)

            linie2_zw_3_4 = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie2_zw_3_4.set_stroke(RED)

            linie2_zw_4_5 = Line(kreis_um_4.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie2_zw_4_5.set_stroke(RED)

            linie2_zw_5_1 = Line(kreis_um_5.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie2_zw_5_1.set_stroke(RED)

            self.play(Create(linie2_zw_1_2), run_time=0.5)
            self.play(Create(linie2_zw_2_3), run_time=0.5)
            self.play(Create(linie2_zw_3_4), run_time=0.5)
            self.play(Create(linie2_zw_4_5), run_time=0.5)
            self.play(Create(linie2_zw_5_1), run_time=0.5)

            number12 = Text("12", font_size=30)
            number12.next_to(graph6_1.vertices[1], DOWN, buff=1)
            self.play(FadeIn(number12), run_time=0.5)


            # new best route
            linie2_zw_1_2_o = Line(kreis_um_1.get_center(), kreis_um_2.get_center(), buff=0.3)
            linie2_zw_1_2_o.set_stroke(YELLOW)

            linie2_zw_2_3_o = Line(kreis_um_2.get_center(), kreis_um_3.get_center(), buff=0.3)
            linie2_zw_2_3_o.set_stroke(YELLOW)

            linie2_zw_3_4_o = Line(kreis_um_3.get_center(), kreis_um_4.get_center(), buff=0.3)
            linie2_zw_3_4_o.set_stroke(YELLOW)

            linie2_zw_4_5_o = Line(kreis_um_4.get_center(), kreis_um_5.get_center(), buff=0.3)
            linie2_zw_4_5_o.set_stroke(YELLOW)

            linie2_zw_5_1_o = Line(kreis_um_5.get_center(), kreis_um_1_2.get_center(), buff=0.3)
            linie2_zw_5_1_o.set_stroke(YELLOW)

            self.wait(1)

            self.play(FadeOut(linie_zw_1_2_o, linie_zw_2_5_o, linie_zw_5_3_o, linie_zw_3_4_o, linie_zw_4_1_o), run_time=0.5)
            self.play(FadeOut(linie2_zw_1_2, linie2_zw_2_3, linie2_zw_3_4, linie2_zw_4_5, linie2_zw_5_1), run_time=0.05)
            self.play(FadeOut(number15), run_time=0.5)

            self.wait(2)

            self.play(Create(linie2_zw_1_2_o), run_time=0.5)
            self.play(Create(linie2_zw_2_3_o), run_time=0.5)
            self.play(Create(linie2_zw_3_4_o), run_time=0.5)
            self.play(Create(linie2_zw_4_5_o), run_time=0.5)
            self.play(Create(linie2_zw_5_1_o), run_time=0.5)

        with self.voiceover(text="Now the algorithm calculates the next route. In our example it will be the seventh possible route."):
            self.wait(2)


            # new route
            kreis2_um_1 = Circle(color=RED, radius=0.5)
            kreis2_um_1.surround(graph1_1.vertices[1])

            kreis2_um_2 = Circle(color=RED, radius=0.6)
            kreis2_um_2.surround(graph2_1.vertices[3])

            kreis2_um_3 = Circle(color=RED)
            kreis2_um_3.surround(graph3_2.vertices[2])

            kreis2_um_4 = Circle(color=RED)
            kreis2_um_4.surround(graph4_4.vertices[4])

            kreis2_um_5 = Circle(color=RED, radius=0.7)
            kreis2_um_5.surround(graph5_7.vertices[5])

            kreis2_um_1_2 = Circle(color=RED)
            kreis2_um_1_2.surround(graph6_7.vertices[1])

            # edges of new route
            linie3_zw_1_2 = Line(kreis2_um_1.get_center(), kreis2_um_2.get_center(), buff=0.3)
            linie3_zw_1_2.set_stroke(RED)

            linie3_zw_2_3 = Line(kreis2_um_2.get_center(), kreis2_um_3.get_center(), buff=0.3)
            linie3_zw_2_3.set_stroke(RED)

            linie3_zw_3_4 = Line(kreis2_um_3.get_center(), kreis2_um_4.get_center(), buff=0.3)
            linie3_zw_3_4.set_stroke(RED)

            linie3_zw_4_5 = Line(kreis2_um_4.get_center(), kreis2_um_5.get_center(), buff=0.3)
            linie3_zw_4_5.set_stroke(RED)

            linie3_zw_5_1 = Line(kreis2_um_5.get_center(), kreis2_um_1_2.get_center(), buff=0.3)
            linie3_zw_5_1.set_stroke(RED)


        with self.voiceover(text="In this route the algorithm realizes at the third node that the added costs are at 14. Since the cost of the route till the third node is already higher than the cost of the best route, the algorithm can discard this route without calculating it untill the end."):
            
            # route until third node
            self.play(Create(linie3_zw_1_2), run_time=0.5)
            self.play(Create(linie3_zw_2_3), run_time=0.5)
            
            number14 = Text("14", font_size=30)
            number14.next_to(graph3_2.vertices[2], LEFT*0.5, buff=1)
            self.play(FadeIn(number14), run_time=0.5)

            self.wait(4)

            self.play(FadeOut(linie3_zw_1_2, linie3_zw_2_3, linie3_zw_3_4), run_time=0.5)

        
        with self.voiceover(text="This way of calculating the best route is applied to every route. At the end the algorithm will have found the best route. In this example it is the first one."):

            self.play(FadeOut(number14, number12, linie2_zw_1_2_o, linie2_zw_2_3_o, linie2_zw_3_4_o, linie2_zw_4_5_o, linie2_zw_5_1_o), run_time=0.5)
            self.wait(4)

            # recreate first route as best route
            self.play(Create(linie2_zw_1_2_o), run_time=0.5)
            self.play(Create(linie2_zw_2_3_o), run_time=0.5)
            self.play(Create(linie2_zw_3_4_o), run_time=0.5)
            self.play(Create(linie2_zw_4_5_o), run_time=0.5)
            self.play(Create(linie2_zw_5_1_o), run_time=0.5)


        with self.voiceover(text="As explained, the algorithm calculates every possible route. But as we have seen before, it can discard routes that are worse than the best route."):
            None

        with self.voiceover(text="That means the algorithm does not have to calculate every route untill the end. Nevertheless, in the worst case the algorithm has to calculate every possible route untill the end and the time complexity is the same as the brute force method."):
            None
            
        with self.voiceover(text="Thats it for the optimal solutions so far."):
            None

        self.play(
                *[FadeOut(mob)for mob in self.mobjects]
            )
        self.play(Restore(self.camera.frame))
        
        with self.voiceover(text="For the approximation methods, one problem is to evaluate how good the algorithm performed."):
            None

        #     self.wait(5)
            
        #     axes = Axes(
        #         x_range=[0, 20],  # x-Achsenbereich von 0 bis 5
        #         y_range=[0, 300], # y-Achsenbereich von 0 bis 32, um die Kurve im Diagramm zu halten
        #         y_length=5,
        #         x_length=8,
        #         tips=False,  
        #         axis_config={"include_ticks": False, "color": WHITE},  # Achsenfarbe
        #     )

        #         # Hinzufügen der Achsen und des Graphen zur Szene
        #     # self.play(Create(exponential_curve), Write(exponential_label).next_to(exponential_curve, UP, buff=0.1))
        #     self.wait()  # Warten am Ende der Animation

        #     bold_template = TexTemplate()
        #     bold_template.add_to_preamble(r"\usepackage{bm}")

        #     def plot_function(function, color, label, position=RIGHT, range=[0,20]):
        #         function0 = axes.plot(function, x_range=range).set_stroke(width=3).set_color(color)
        #         return function0, Tex(label, tex_template=bold_template).set_color(color).scale(0.6).next_to(function0.point_from_proportion(1), position)


        #     self.wait(5)
        #     # exponential
        #     exp, exp_tag  = plot_function(lambda x: 2**x, BLUE, r"$\bm{O(2^n)}$", position=LEFT, range=[0,8.229])
        #     self.play(LaggedStart(exp.animate.set_stroke(opacity=0.3)))
        #     self.play(FadeIn(exp_tag))

        #     # diagram = VGroup(axes, exp_tag, exp)

        #     # self.wait(2)
        #     # self.play(diagram.animate.shift(LEFT*2).scale(0.6))
        #     # self.wait(2)
        #     # self.play(FadeOut(axes), FadeOut(exp, exp_tag))
        #     # self.wait(2)

        # with self.voiceover(text="However the algorithm performs very well in practice and it is mostly better than the brute force method. For that reason the time complexity of the branch and bound method is mostly better then the brute force algorithm, but still exponential."):
        #     self.wait(3)
        #     # exponential but a little bit faster
        #     exp2, exp2_tag  = plot_function(lambda x: 2**(x-1), GREEN, r"$\bm{O(2^{n-1})}$", position=RIGHT, range=[0,9.229])
        #     self.play(LaggedStart(exp2.animate.set_stroke(opacity=0.3)))
        #     self.play(FadeIn(exp2_tag))
        
        self.clear()

        self.lower_bound()

        self.christofides_algorithm()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # self.next_section("kNN") # kNN
        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.clear()
        def distance(p1, p2): # calculate distance between 2 points
            return np.linalg.norm(p1.get_center() - p2.get_center())

        # create points
        def create_points(num_points, color=DARK_BLUE, radius=0.15, height_points0=-4, height_points1=2):
            """Erstellt eine Liste von zufälligen Punkten."""
            np_random = np.random.RandomState(42)
            return [
                Dot(np.array([np_random.uniform(-4, 4), np_random.uniform(height_points0, height_points1), 0]), 
                    color=color, radius=radius, stroke_color=WHITE, stroke_width=1.5, fill_opacity=1) 
                for _ in range(num_points)
            ]

        # connect points
        def connect_points(points, line_color=ORANGE, temp_line_opacity=0.3, run_time=0.5, run_time_all_lines=0.1, draw_lines=True):
            """Verbindet eine Liste von Punkten mit Linien."""
            current_point = random.choice(points)
            start_point = current_point
            visited = {current_point}
            self.wait(3)
            for _ in range(len(points) - 1):
                unvisited_points = [p for p in points if p not in visited]
                temp_lines = [
                    Line(current_point.get_center(), p.get_center(), color=WHITE).set_opacity(temp_line_opacity)
                    for p in unvisited_points
                ]
                if draw_lines:
                    for line in temp_lines:
                        self.play(Create(line), run_time=run_time_all_lines)

                next_point = min(unvisited_points, key=lambda p: distance(current_point, p))
                visited.add(next_point)

                line_to_next = Line(current_point.get_center(), next_point.get_center(), color=line_color)
                self.play(Transform(temp_lines[unvisited_points.index(next_point)], line_to_next), run_time=run_time)

                if draw_lines: 
                    for line in temp_lines:
                        if line != temp_lines[unvisited_points.index(next_point)]:
                            self.remove(line)

                current_point = next_point

            if draw_lines:
                self.wait(2.5)
            else:  
                self.wait(0.5)
            # line back to starting point
            line_to_start = Line(current_point.get_center(), start_point.get_center(), color=line_color)
            self.play(Create(line_to_start), run_time=run_time_all_lines)

        # write kNN
        with self.voiceover(text="Our second approximation approach is k nearest neighbors (kNN)."):        
            intro_text = Text("k Nearest Neighbors (kNN)").shift(UP*3.5)
            self.play(Write(intro_text))

        # kNN visualized
        with self.voiceover(text="We start at a specific city (any city can be the starting point). Then we check the shortest path and add this point to the tour. Same for the next node and so on ... we repeat this until there is no unvisited node."):
            
            points = create_points(10)  # Erstelle Punkte
            self.add(*points)  # Füge Punkte der Szene hinzu
            connect_points(points)

        with self.voiceover(text="Finally, we draw a connection back to the starting point."):
            None

        self.wait(2)
        self.clear()
        self.wait(1)

        # kNN with more nodes
        with self.voiceover(text="This is how it can look like with more nodes, so more cities Alex has to visit."):

            points = create_points(50, color=DARK_BLUE, height_points0=-3, height_points1=3)
            self.add(*points)
            connect_points(points, line_color=ORANGE, run_time=0.005, run_time_all_lines=0.005, draw_lines=False)

            self.wait(1)
            self.clear()
            self.wait(1)

        # kNN complexity
        with self.voiceover(text="For a dataset with n cities, the time complexity of applying kNN to TSP is O of n squared. For kNN, time complexity is a bit better compared to O of n to the power of 3 by using Christofides. Both are faster than using Brute Force with a factorial time complexity, but in most cases we won't find the optimal shortest path."):

            axes = Axes(
                x_range=[0, 20],  
                y_range=[0, 720], 
                y_length=5,
                x_length=8,
                tips=False,  
                axis_config={"include_ticks": False, "color": WHITE},
            )

            # Erstellen der x-Achsenbeschriftung
            x_label = Tex("nodes/cities")
            x_label.next_to(axes.x_axis.get_end(), DOWN + LEFT, buff=0.2).scale(0.7)  # Positionierung unter der x-Achse, rechtsbündig

            # Erstellen der y-Achsenbeschriftung
            y_label = Tex("time\_complexity").rotate(PI / 2, about_point=ORIGIN).scale(0.7)  # Drehung um 90 Grad
            y_label.next_to(axes.y_axis, LEFT, buff=0.2)  # Positionierung links neben der y-Achse
            self.add(axes, x_label, y_label)
            self.wait(2)

            bold_template = TexTemplate()
            bold_template.add_to_preamble(r"\usepackage{bm}")

            def plot_function(function, color, label, position=RIGHT, range=[0,20]):
                function0 = axes.plot(function, x_range=range).set_stroke(width=3).set_color(color)
                return function0, Tex(label, tex_template=bold_template).set_color(color).scale(0.6).next_to(function0.point_from_proportion(1), position)
    
            # quadratic
            quad, quad_tag  = plot_function(lambda x: x**2, YELLOW, r"$\bm{O(n^2)}$ kNN", range=[0,20])
            self.play(LaggedStart(quad.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(quad_tag))

            self.wait(5)
            
            # Christofides
            chris, chris_tag  = plot_function(lambda x: x**3, ORANGE, r"$\bm{O(n^3)}$ Christofides", range=[0,8.96])
            self.play(LaggedStart(chris.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(chris_tag))

            self.wait(4)

            fact, fact_tag  = plot_function(lambda x: gamma(x) if x > 1 else x**2, DARK_BLUE, r"$\bm{O(n!)}$\\Brute Force", range=[0,7], position=LEFT)
            self.play(LaggedStart(fact.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(fact_tag))

            self.wait(1)

        self.play(FadeOut(axes, x_label, y_label), FadeOut(chris, chris_tag, quad, quad_tag, fact, fact_tag))
        self.clear()
        self.wait(1)

        # Ending

        bf = ImageMobject("pics\/brute_force.png").scale(0.3).move_to(LEFT * 3 + UP * 2)
        bab = ImageMobject("./pics/bab.png").scale(0.3).move_to(RIGHT * 3 + UP * 2)
        ch = ImageMobject("./pics/christofides.png").scale(0.3).move_to(LEFT * 3 + DOWN * 2)
        knn = ImageMobject("./pics/knn.png").scale(0.3).move_to(RIGHT * 3 + DOWN * 2)
        
        with self.voiceover(text="In this video, we showed you different methods to solve the traveling salesperson problem. Every method has its own advantages and disadvantages. The brute force algorithm is the most accurate, but it is also the slowest."):

            self.wait(1)
            self.play(FadeIn(bab, bf, ch, knn))
            self.wait(8)
            self.play(bf.animate.scale(1.5))
            self.wait(3)
            self.play(bf.animate.scale(1/1.5))

        with self.voiceover(text="The branch and bound method is faster, but it is still not efficient for large graphs."):

            self.wait(1)
            self.play(bab.animate.scale(1.5))
            self.wait(2)
            self.play(bab.animate.scale(1/1.5))

        with self.voiceover(text="The Christofides algorithm is a heuristic algorithm, which means it is not guaranteed to find the optimal solution, but it is much faster than the previous solutions."):


            self.play(ch.animate.scale(1.5))
            self.wait(7)
            self.play(ch.animate.scale(1/1.5))

        with self.voiceover(text="The k-nearest neighbor algorithm is also a heuristic algorithm. Even though it is faster than the Christofides algorithm, results are often worse. In the end depending on the size of the graph, you have to decide which solution is best suited for your problem."):

            self.play(knn.animate.scale(1.5))
            self.wait(5)
            self.play(knn.animate.scale(1/1.5))

            self.wait(5)



        with self.voiceover(text="Thanks for joining us today! If you enjoyed the video and learned something new, please give it a thumbs up"):
            None
            # self.wait(3)
            # self.wait(2)
            # salesperson = ImageMobject("Salesman.png").scale(0.6)
            # self.add(salesperson)
            # self.wait(2)
            # self.remove(salesperson)
        self.clear()
        self.wait(0.5)
        with self.voiceover(text="Don't forget to subscribe and hit the bell so you won't miss our next adventure. Until next time, stay curious and take care. Bye!"):

            like = ImageMobject("./pics/like.jpg")
            self.play(FadeIn(like))

        
    def asymmetric(self):

        with self.voiceover(text = "This isn't really accurate in real life because of conditions of the landscape or construction sites."):
            None
            
        with self.voiceover(text="Thats why there is also a asymmetrical TSP."):
            self.clear()
            text_asymmetrical = Text("Asymmetrical").move_to(ORIGIN).to_edge(UP)

            self.play(Write(text_asymmetrical))

        with self.voiceover(text="The TSP is called asymmetrical if there are two edges between every node and they don't have the same weight. As you can see the graph is then directed. This is way more accurate to the real world, but this is also more complex to solve then the symmetrical. In this video we will only show you ways of solving the symmetrical TSP."):
            
            # Define positions of the nodes of the graph
            positions_asym = {
            0: LEFT * 2,
            1: ORIGIN + UP,
            2: RIGHT * 2,
            3: RIGHT  + DOWN*2,
            4: LEFT  + DOWN*2,
            }
             
            graph_asym = CustomGraph(list(positions_asym.keys()), [], layout=positions_asym)
            labels_asym = graph_asym.add_labels()

            self.play(Create(graph_asym))
            self.add(labels_asym)
            self.play(FadeIn(labels_asym), run_time=0.5)
        
            # Define edges
            edges_asym = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 0), (2, 1), (3, 2), (4, 3), (0, 4)]

            # Shift of the labels of the outer edges
            label_offsets_asym = {
            (0, 1): (LEFT+UP) * 0.3,
            (1, 2): (UP + RIGHT) * 0.3,
            (2, 3): (DOWN + RIGHT) * 0.3,
            (3, 4): DOWN * 0.3,
            (4, 0): (DOWN+LEFT) * 0.3,
            
            # Shift of the labels of the inner edgess
            (1, 0): (RIGHT+DOWN) * 0.3,
            (2, 1): (DOWN + LEFT) * 0.3,
            (3, 2): (UP + LEFT) * 0.3,
            (4, 3): UP * 0.3,
            (0, 4): (UP+RIGHT) * 0.3,
                }
            
            edge_labels_asym = [
                # Labels of the outer edges
                "4", "3", "7", "8", "5", 
                # Labels of the inner edges
                "2", "5", "6", "6", "4"
                ]
            
            line_positions_asym = {
            # Start and endpoints of the outer edges
            (0, 1): (positions_asym[0] + RIGHT * 0.1 + UP * 0.3, positions_asym[1] + LEFT * 0.2 + UP*0.2),
            (1, 2): (positions_asym[1] + RIGHT * 0.2 + UP * 0.2, positions_asym[2] + 0.3* UP + LEFT * 0.1),
            (2, 3): (positions_asym[2] + DOWN * 0.3 + RIGHT * 0.1, positions_asym[3] + UP * 0.2 + RIGHT * 0.2),
            (3, 4): (positions_asym[3] + LEFT * 0.3 + DOWN * 0.1, positions_asym[4] + RIGHT * 0.3 + DOWN * 0.1),
            (4, 0): (positions_asym[4] + LEFT * 0.2 + UP * 0.2, positions_asym[0] + DOWN * 0.3 + LEFT * 0.1),
            # Start and endpoints of the inner edges
            (1, 0): (positions_asym[1] + LEFT * 0.2 + DOWN * 0.2, positions_asym[0] + RIGHT * 0.3),
            (2, 1): (positions_asym[2] + LEFT * 0.3, positions_asym[1] + 0.2 * DOWN + RIGHT * 0.2),
            (3, 2): (positions_asym[3] + UP * 0.3, positions_asym[2] + DOWN * 0.3 + LEFT * 0.2),
            (4, 3): (positions_asym[4] + UP * 0.1 + RIGHT * 0.3, positions_asym[3] + LEFT * 0.3 + UP * 0.1),
            (0, 4): (positions_asym[0] + RIGHT * 0.2 + DOWN * 0.3, positions_asym[4] + UP * 0.3),
                }
            
            # Creation of every edge and label
            for i, edge in enumerate(edges_asym):
                start_pos, end_pos = line_positions_asym[edge]
                mid_pos = (start_pos + end_pos) / 2  # Calculate the middle of the edge to assign the label

                line_asym = Arrow(start_pos, end_pos, color=WHITE)  # Create arrow
                
                label_pos_asym = mid_pos + label_offsets_asym[edge]  # Apply shift of labels
                
                label_asym = Text(edge_labels_asym[i], font_size=24).move_to(label_pos_asym)  # Create label

                self.play(Create(line_asym), Write(label_asym), run_time=0.5)
        
        with self.voiceover(text="Let's take a look at how the TSP can be solved"):
            None
        
        self.clear()

    def lower_bound(self):
        
        with self.voiceover(text="So we need to point out how good our approximated solution is, compared to the optimum. In some business cases there is a treshold given by the supervisor so you don't need to know how near the solution is to the optimum but in a theroetic case we want to know this. For large TSP to determine the optimum is not economically sensible because of the complexity so we need to find an other value to measure our solution."):
            
            solution_text = Text("How good is our solution?").move_to(ORIGIN)
        
            self.play(Write(solution_text))

        with self.voiceover(text="So lets imagine we have these nodes as a tsp"):
            
            self.play(FadeOut(solution_text))
            
            # Define positions of the nodes of the graph
            positions_ap = {
            0: LEFT * 4 + UP * 2,
            1: LEFT * 2 + UP * 2,
            2: LEFT * 2 + DOWN * 2,
            3: LEFT * 4 + DOWN * 2,
            4: ORIGIN,
            5: RIGHT * 2 + UP * 2,
            6: RIGHT * 4 + UP * 2,
            7: RIGHT * 2 + DOWN * 2,
            8: RIGHT * 4 + DOWN * 2,
            9: UP * 2,
            }

            graph_ap = CustomGraph(list(positions_ap.keys()), [], layout=positions_ap)
            labels_ap = graph_ap.add_labels()

            self.play(Create(graph_ap))
            self.add(labels_ap)
            self.play(FadeIn(labels_ap), run_time=0.5)
        
        with self.voiceover(text="and this is our approximated solution."):
            
            header_text = Text("Approximated").to_edge(UP)
        
            self.play(Write(header_text))
            
            # Define edges
            edges_ap = [
            (0, 1), (1, 9), (9, 5), (5, 6), (6, 8), (8, 7), (7, 4), (4, 2), (2, 3), (3, 0)]

            # Shift of the labels 
            label_offsets_ap = {
            (0, 1): UP * 0.2,
            (1, 9): UP * 0.2,
            (9, 5): UP * 0.2,
            (5, 6): UP * 0.2,
            (6, 8): LEFT * 0.2,
            (8, 7): UP * 0.2,
            (7, 4): (UP+RIGHT) * 0.2,
            (4, 2): (UP + LEFT) * 0.2,
            (2, 3): UP * 0.2,
            (3,0): LEFT * 0.2,
            }
            
            # Edges labels
            edge_labels_ap = ["4", "3", "7", "8", "15", "2", "9", "4", "8", "19"] 
            
            # Start and endpoints of the edges
            line_positions_ap = {
            (0, 1): (positions_ap[0] + RIGHT * 0.3, positions_ap[1] + LEFT * 0.3),
            (1, 9): (positions_ap[1] + RIGHT * 0.3, positions_ap[9] + LEFT * 0.3),
            (9, 5): (positions_ap[9] + RIGHT * 0.3, positions_ap[5] + LEFT * 0.3),
            (5, 6): (positions_ap[5] + RIGHT * 0.3, positions_ap[6] + LEFT * 0.3),
            (6, 8): (positions_ap[6] + DOWN * 0.3, positions_ap[8] + UP * 0.3),
            (8, 7): (positions_ap[8] + LEFT * 0.3, positions_ap[7] + RIGHT * 0.3),
            (7, 4): (positions_ap[7] + (LEFT+UP) * 0.2, positions_ap[4] + (RIGHT+DOWN) * 0.2),
            (4, 2): (positions_ap[4] + (LEFT+DOWN) * 0.2, positions_ap[2] + (RIGHT+UP) * 0.2),
            (2, 3): (positions_ap[2] + LEFT * 0.3, positions_ap[3] + RIGHT * 0.3),
            (3, 0): (positions_ap[3] + UP * 0.3, positions_ap[0] + DOWN * 0.3), 
            }

            # Create VGroup for edges and labels to fade them out later
            lines_and_labels_ap = VGroup()
            
            # Creation of every edge and label
            for i, edge in enumerate(edges_ap):
                start_pos, end_pos = line_positions_ap[edge]
                mid_pos = (start_pos + end_pos) / 2

                line_ap = Line(start_pos, end_pos, color=WHITE) # Create edge
                label_pos_ap = mid_pos + label_offsets_ap[edge]  # Apply shift of labels
                label_ap = Text(edge_labels_ap[i], font_size=24).move_to(label_pos_ap)
                
                lines_and_labels_ap.add(line_ap, label_ap)

                self.play(Create(line_ap), Write(label_ap), run_time=0.2)
        
            self.wait(2)

        with self.voiceover(text="We take a look at all the weights and sum them up."):
            
            equation_text_ap = Text("4 + 3 + 7 + 8 + 15 + 2 + 9 + 4 + 8 + 19 = 79", font_size=36).to_edge(DOWN, buff=1)

            self.play(Write(equation_text_ap))
            self.wait(2)

        with self.voiceover(text="This is the value for our approximated solution."):

            approximated_text = Text("Approximated = 79", font_size=36).next_to(equation_text_ap, DOWN)

            self.play(Write(approximated_text))
            self.wait(2)

        with self.voiceover(text="But now we still don't now how good this is compared to the optimum."):

            all_objects_ap = VGroup(graph_ap, equation_text_ap, header_text, lines_and_labels_ap, labels_ap) 

            self.play(FadeOut(all_objects_ap))
            self.play(approximated_text.animate.move_to(ORIGIN).to_edge(LEFT))
            
            greater_than_1 = Text(">", font_size=36).next_to(approximated_text, RIGHT)
            optimum_text = Text("Optimum = ?", font_size=36).next_to(greater_than_1, RIGHT)
            greater_than_2 = Text(">", font_size=36).next_to(optimum_text, RIGHT)
   
            header_lb = Text("Lower Bound", font_size=36)

            self.wait(0.5)

            self.play(
                Write(greater_than_1), 
                Write(optimum_text), 
                Write(greater_than_2)
            )
            
            self.wait(2)

        with self.voiceover(text="For this we use the lower bound."):

            header_lb.next_to(greater_than_2, RIGHT)
            self.play(Write(header_lb))
        
        with self.voiceover(text="The lower bound is the value of the sum of every weight of every edge in a minimum spanning tree."):
            
            all_objects = VGroup(approximated_text, greater_than_1, optimum_text, greater_than_2)
            
            self.play(FadeOut(all_objects))
            self.play(header_lb.animate.move_to(ORIGIN).to_edge(UP))

        with self.voiceover(text="So imagine we have these nodes from before."):
            
            # Define positions of the nodes of the graph
            positions_lb = {
            0: LEFT * 4 + UP * 2,
            1: LEFT * 2 + UP * 2,
            2: LEFT * 2 + DOWN * 2,
            3: LEFT * 4 + DOWN * 2,
            4: ORIGIN,
            5: RIGHT * 2 + UP * 2,
            6: RIGHT * 4 + UP * 2,
            7: RIGHT * 2 + DOWN * 2,
            8: RIGHT * 4 + DOWN * 2,
            9: UP * 2,
            }

            graph_lb = CustomGraph(list(positions_lb.keys()), [], layout=positions_lb,)
            labels_lb = graph_lb.add_labels()
            
            self.play(Create(graph_lb))
            
            self.add(labels_lb)
            self.play(FadeIn(labels_lb), run_time=0.5)
            
        with self.voiceover(text="We add the edges and their weights to the nodes so we get our minimal spanning tree."):
  
            # Define edges
            edges_lb = [(0, 1), (1, 9), (9, 5), (5, 6), (9, 4), (4, 7), (7, 8), (4, 2), (2, 3)]

            # Shift of the labels of the edges
            label_offsets_lb = {
            (0, 1): UP * 0.2,
            (1, 9): UP * 0.2,
            (9, 5): UP * 0.2,
            (5, 6): UP * 0.2,
            (9, 4): LEFT * 0.2,
            (4, 7): (UP + RIGHT) * 0.2,
            (7, 8): UP * 0.2,
            (4, 2): (UP + LEFT) * 0.2,
            (2, 3): UP * 0.2,
            }

            # Edge lables
            edge_labels_lb = ["4", "3", "7", "8", "5", "9", "2", "4", "8"] 
            
            # Start and endpoints of the edges
            line_positions_lb = {
            (0, 1): (positions_lb[0] + RIGHT * 0.3, positions_lb[1] + LEFT * 0.3),
            (1, 9): (positions_lb[1] + RIGHT * 0.3, positions_lb[9] + LEFT * 0.3),
            (9, 5): (positions_lb[9] + RIGHT * 0.3, positions_lb[5] + LEFT * 0.3),
            (5, 6): (positions_lb[5] + RIGHT * 0.3, positions_lb[6] + LEFT * 0.3),
            (9, 4): (positions_lb[9] + DOWN * 0.3, positions_lb[4] + UP * 0.3),
            (4, 7): (positions_lb[4] + (RIGHT+DOWN) * 0.2, positions_lb[7] + (LEFT+UP) * 0.2),
            (7, 8): (positions_lb[7] + RIGHT * 0.3, positions_lb[8] + LEFT * 0.3),
            (4, 2): (positions_lb[4] + (LEFT+DOWN) * 0.2, positions_lb[2] + (RIGHT+UP) * 0.2),
            (2, 3): (positions_lb[2] + LEFT * 0.3, positions_lb[3] + RIGHT * 0.3), 
            }
            
            # Create VGroup for edges and labels to fade them out later
            lines_and_labels_lb = VGroup()
            
            # Creation of every edge and label
            for i, edge in enumerate(edges_lb):
                start_pos, end_pos = line_positions_lb[edge]
                mid_pos = (start_pos + end_pos) / 2

                line_lb = Line(start_pos, end_pos, color=WHITE)
                label_pos_lb = mid_pos + label_offsets_lb[edge]  
                label_lb = Text(edge_labels_lb[i], font_size=24).move_to(label_pos_lb)
                lines_and_labels_lb.add(line_lb, label_lb)

                self.play(Create(line_lb), Write(label_lb), run_time=0.2)
        
   

        with self.voiceover(text="We take again a look at all the weights and sum them up."):
           
            equation_text = Text("4 + 3 + 7 + 8 + 5 + 9 + 2 + 4 + 8 = 50", font_size=36).to_edge(DOWN, buff=1)

            self.play(Write(equation_text))

        with self.voiceover(text="This is the value of our lower bound."):
            
            lower_bound_text = Text("Lower Bound = 50", font_size=36).next_to(equation_text, DOWN)

            self.play(Write(lower_bound_text))

        with self.voiceover(text="Now we have a value which we can compare to our approximated solution and we know how good it is!"):
            
            all_objects_lb = VGroup(graph_lb, equation_text, header_lb, lines_and_labels_lb, labels_lb) 
            self.play(FadeOut(all_objects_lb))
            
            self.wait(0.5)
            
            self.play(lower_bound_text.animate.move_to(ORIGIN+RIGHT*4))
            
            approximated_text = Text("Approximated = 79", font_size=36).move_to(4*LEFT + ORIGIN) 
            greater_than_3 =Text(">", font_size=36).move_to(ORIGIN)
            
            self.play(Write(approximated_text), Write(greater_than_3))
        
        with self.voiceover(text="Now we can continue with the approximated algorithms"):
            self.clear()

    def christofides_algorithm(self):
        with self.voiceover(text="In the following we will explain the christofides algorithm. This is an approximated algorithm to solve the TSP. This algorithm guarantees a solution that is at most fifthy percent longer than the optimal round trip."):
            
            title = Text("Christofides Algorithm").to_edge(UP)
            self.play(Write(title))

        with self.voiceover(text= "Let's take a look at the graph to visualize this algorithm."):
            
            # Define positions of the nodes of the graph
            positions_mst = {
            0: LEFT * 4 + UP * 2,
            1: LEFT * 2 + UP * 2,
            2: LEFT * 2 + DOWN * 2,
            3: LEFT * 4 + DOWN * 2,
            4: ORIGIN,
            5: RIGHT * 2 + UP * 2,
            6: RIGHT * 4 + UP * 2,
            7: RIGHT * 2 + DOWN * 2,
            8: RIGHT * 4 + DOWN * 2,
            9: UP * 2,
            }

            graph_mst = CustomGraph(list(positions_mst.keys()), [], layout=positions_mst)
            labels_mst = graph_mst.add_labels()
            self.play(Create(graph_mst))

            self.add(labels_mst)
            self.play(FadeIn(labels_mst), run_time=0.5)
        
        with self.voiceover(text= "First we will create a minimal spanning tree with every node."):
            
            # Define edges
            edges_mst = [(0, 1), (1, 9), (9, 5), (5, 6), (4, 9), (4, 7), (7, 8), (4, 2), (2, 3)]

            # Start and endpoints of the edges
            # Some edges are defined in both directions to create them in both directions
            # It is used to animate another path in the graph
            line_positions_mst = {
            (0, 1): (positions_mst[0] + RIGHT * 0.3, positions_mst[1] + LEFT * 0.3),
            (1, 9): (positions_mst[1] + RIGHT * 0.3, positions_mst[9] + LEFT * 0.3),
            (9, 5): (positions_mst[9] + RIGHT * 0.3, positions_mst[5] + LEFT * 0.3),
            (5, 6): (positions_mst[5] + RIGHT * 0.3, positions_mst[6] + LEFT * 0.3),
            (9, 4): (positions_mst[9] + RIGHT * 0.2 + DOWN * 0.2, positions_mst[4] + RIGHT * 0.2 + UP * 0.2, ),
            (4, 7): (positions_mst[4] + (RIGHT+DOWN) * 0.2, positions_mst[7] + (LEFT+UP) * 0.2),
            (7, 8): (positions_mst[7] + RIGHT * 0.3, positions_mst[8] + LEFT * 0.3),
            (4, 2): (positions_mst[4] + (LEFT+DOWN) * 0.2, positions_mst[2] + (RIGHT+UP) * 0.2),
            (2, 3): (positions_mst[2] + LEFT * 0.3, positions_mst[3] + RIGHT * 0.3),
            (0, 3): (positions_mst[0] + DOWN * 0.3, positions_mst[3] + UP * 0.3),
            (4, 9): (positions_mst[4] + UP * 0.2 + LEFT*0.2, positions_mst[9] + DOWN * 0.2 + LEFT*0.2),
            (6, 8): (positions_mst[6] + DOWN * 0.3, positions_mst[8] + UP * 0.3),
            (3, 2): (positions_mst[3] + RIGHT * 0.3, positions_mst[2] + LEFT * 0.3,),
            (2, 4): (positions_mst[2] + (RIGHT+UP) * 0.2, positions_mst[4] + (LEFT+DOWN) * 0.2,),
            (8, 6): (positions_mst[8] + UP * 0.3, positions_mst[6] + DOWN * 0.3),
            (6, 5): (positions_mst[6] + LEFT * 0.3, positions_mst[5] + RIGHT * 0.3),
            (9, 1): (positions_mst[9] + LEFT * 0.3, positions_mst[1] + RIGHT * 0.3),
            (1, 0): (positions_mst[1] + LEFT * 0.3, positions_mst[0] + RIGHT * 0.3),
            (5, 9): (positions_mst[5] + LEFT * 0.3, positions_mst[9] + RIGHT * 0.3),
            }
            
            # Create VGroup for edges and labels to fade them out later
            lines_mst = VGroup()
            
            # Create VGroup for edges and labels to fade them out separated from the others
            lines_to_remove = VGroup()
            
            # Edges which need to be removed earlier then the others
            edges_to_remove = [(9, 4), (4, 9)]
            
            # Creation of every edge and label
            for i, edge in enumerate(edges_mst): 
                start_pos_mst, end_pos_mst = line_positions_mst[edge]

                line_mst = Line(start_pos_mst, end_pos_mst, color=WHITE)
                
                # Add edges which need to be removed to the VGroup
                if edge in edges_to_remove:
                    lines_to_remove.add(line_mst)
                else:
                    lines_mst.add(line_mst)

                self.play(Create(line_mst), run_time=0.2)
        
        with self.voiceover(text= "Then we search for every node in the graph with an odd degree, meaning an odd number of edges."):
            
            # Nodes which need to be highlighted
            highlight_nodes = [0, 9, 6, 4, 3, 8]  

            # VGroup to erase the circles later
            circles = VGroup()
            
            # Highlight the defined nodes
            for node in highlight_nodes:
                highlight_circle = Circle(radius=0.5, color=RED).move_to(positions_mst[node])
                circles.add(highlight_circle)
               
                self.play(Create(highlight_circle), run_time=0.5)
        
        with self.voiceover(text= "After finding all the nodes with an odd degree we need to find a minimum perfect matching, so we need to find edges with minimum weight for every node to get an even degree. Then we combine them to obtain a multigraph in which every vertex has an even degree."):
            
            self.play(FadeOut(circles), run_time=0.2)
            
            # Define new edges to add
            edges_mst_2 = [(0, 3), (9, 4), (6, 8)]
            
            # Creation of every edge and label
            for i, edge in enumerate(edges_mst_2): 
                start_pos_mst, end_pos_mst = line_positions_mst[edge]

                line_mst = Line(start_pos_mst, end_pos_mst, color=RED)
                
                # Add edges which need to be removed to the VGroup
                if edge in edges_to_remove:
                    lines_to_remove.add(line_mst)
                else:
                    lines_mst.add(line_mst)

                self.play(Create(line_mst), run_time=0.5)
        
        with self.voiceover(text= "Since every vertex has an even degree, we can find an Eulerian circuit in this graph. An Eulerian circuit is a path that visits each edge exactly once. So as you can see we go through our multigraph and note down every visited node. "):
            
            # Edges which need to be highlighted in the correct order
            highlight_edges = [(0, 3), (3, 2), (2, 4), (4,7), (7,8), (8, 6), (6, 5), (5,9), (9,4), (4,9), (9, 1), (1,0)]
            
            # Text and arrows to display the path in the graph
            texts = ["0", "→", "3", "→", "2", "→", "4", "→", "7", "→", "8", "→", "6", "→", "5", "→", "9", "→ ", "4", "→", "9", "→", "1", "", "", ""]

            # Base position of the first text
            base_position = np.array([-5, -3, 0])  

            # VGroup where all textparts are added to create them next to the previous
            all_texts = VGroup()
            
            # Counter let the first text start at the base position and the following not and to call the right index in the text list
            j = 0 

            for i, edge in enumerate(highlight_edges):
                # Start and end postions of the edges
                start_pos, end_pos = line_positions_mst[edge]
                
                # Create edge which need to be highlighted
                highlight_line = Line(start_pos, end_pos, color=YELLOW, stroke_width=10)
                self.play(Create(highlight_line), run_time=0.2)
                
                # First text needs to be created at the base position
                if j == 0:  
                    text = Text(texts[j], font_size=24).move_to(base_position)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1  # Add counter to call the right position in the text list
                    text = Text(texts[j], font_size=24).next_to(all_texts, RIGHT)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1
                else:
                    text = Text(texts[j], font_size=24).next_to(all_texts, RIGHT)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1
                    text = Text(texts[j], font_size=24).next_to(all_texts, RIGHT)
                    all_texts.add(text)
                    self.play(Write(text), run_time=0.1)
                    j = j + 1

                self.wait(1)

                self.play(FadeOut(highlight_line), run_time=0.5)
        
        with self.voiceover(text= "The last step will be to convert the euleric circle into a hamilton circle, so we have to delete all edges which we have already seen before. In our case these are the edges between 9 and 4. There we got our solution!"):
            
            # Define positions where the red Xs need to be placed
            position_x1 = np.array([3.45, -3, 0])  
            position_x2 = np.array([4.4, -3, 0])  

            # Creation of the red Xs
            x_mark_1 = self.create_x_mark(position_x1)
            x_mark_2 = self.create_x_mark(position_x2)

            self.play(Create(x_mark_1), Create(x_mark_2), FadeOut(lines_to_remove))

        with self.voiceover(text="If we take a look at the time complexity of the Christofides algorithm it is mainly determined by the step of finding a minimum perfect matching, which is n to the third power. If time complexity is important, it could be preferable than using Brute Force or Branch and Bound."):

            self.clear()

            # Define the axes of the plot
            axes = Axes(
                x_range=[0, 20],  
                y_range=[0, 720], 
                y_length=5,
                x_length=8,
                tips=False,  
                axis_config={"include_ticks": False, "color": WHITE},
            )

            # Add labels to x axis
            x_label = Tex("nodes/cities")
            x_label.next_to(axes.x_axis.get_end(), DOWN + LEFT, buff=0.2).scale(0.7)  # Position below the x axis

            # Add labels to y axis
            y_label = Tex("time\_complexity").rotate(PI / 2, about_point=ORIGIN).scale(0.7)  # 90 degree turn
            y_label.next_to(axes.y_axis, LEFT, buff=0.2)  # position left to the y axis
            self.add(axes, x_label, y_label)
            self.wait(2)

            bold_template = TexTemplate()
            bold_template.add_to_preamble(r"\usepackage{bm}")

            def plot_function(function, color, label, position=RIGHT, range=[0,20]):
                function0 = axes.plot(function, x_range=range).set_stroke(width=3).set_color(color)
                return function0, Tex(label, tex_template=bold_template).set_color(color).scale(0.6).next_to(function0.point_from_proportion(1), position)
    
            self.wait(5)
            
            # Create label of Christofides time complexity
            chris, chris_tag  = plot_function(lambda x: x**3, ORANGE, r"$\bm{O(n^3)}$ Christofides", range=[0,8.96])
            self.play(LaggedStart(chris.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(chris_tag))

            # Create graph of Christofides time complexity
            fact, fact_tag  = plot_function(lambda x: gamma(x) if x > 1 else x**2, YELLOW, r"$\bm{O(n!)}$\\Brute Force", range=[0,7], position=LEFT)
            self.play(LaggedStart(fact.animate.set_stroke(opacity=0.3)))
            self.play(FadeIn(fact_tag))

            self.wait(1)

        self.play(FadeOut(axes, x_label, y_label), FadeOut(chris, chris_tag, fact, fact_tag))

    def create_x_mark(self, position):  # Function to create a red X on the screen
            
            # Line from up left to down right
            line1 = Line(position + np.array([-0.25, 0.25, 0]), position + np.array([0.25, -0.25, 0]), color=RED)
            
            # Line from down left to up right
            line2 = Line(position + np.array([-0.25, -0.25, 0]), position + np.array([0.25, 0.25, 0]), color=RED)
            
            return VGroup(line1, line2)
      
if __name__ == "__main__":
    os.system(f"manim --disable_caching --save_sections -pqh {__file__} TSP")