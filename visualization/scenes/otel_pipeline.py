from manim import *


class OTelPipelineScene(Scene):
    def construct(self):
        title = Text("OpenTelemetry Pipeline", weight=BOLD).to_edge(UP)
        self.play(Write(title))
        self.wait(0.2)

        # Nodes
        app = RoundedRectangle(corner_radius=0.2, width=3.2, height=1).set_fill(BLUE, 0.2).set_stroke(BLUE, 2)
        app_label = Text("Application\n(Flask Order Service)", font_size=28).move_to(app.get_center())
        VGroup(app, app_label).move_to(LEFT * 5 + DOWN * 1)

        collector = RoundedRectangle(corner_radius=0.2, width=3.5, height=1.2).set_fill(GREEN, 0.2).set_stroke(GREEN, 2)
        collector_label = Text("OTel Collector", font_size=30).move_to(collector.get_center())
        VGroup(collector, collector_label).move_to(LEFT * 1.5 + DOWN * 1)

        processors = RoundedRectangle(corner_radius=0.2, width=4.6, height=2).set_fill(YELLOW, 0.15).set_stroke(YELLOW, 2)
        p_title = Text("Processors", font_size=28, weight=BOLD)
        p_item1 = Text("transform (OTTL)", font_size=26).set_color(YELLOW)
        p_item2 = Text("tail_sampling", font_size=26).set_color(YELLOW)
        p_group = VGroup(p_title, p_item1, p_item2).arrange(DOWN, buff=0.15)
        p_group.move_to(processors.get_center())
        VGroup(processors, p_group).move_to(RIGHT * 2.5 + DOWN * 1)

        backend = RoundedRectangle(corner_radius=0.2, width=3.2, height=1).set_fill(PURPLE, 0.2).set_stroke(PURPLE, 2)
        backend_label = Text("Backend\n(Jaeger / Splunk)", font_size=28).move_to(backend.get_center())
        VGroup(backend, backend_label).move_to(RIGHT * 6 + DOWN * 1)

        # Animate nodes
        self.play(FadeIn(app), FadeIn(app_label))
        self.play(FadeIn(collector), FadeIn(collector_label))
        self.play(FadeIn(processors), FadeIn(p_group))
        self.play(FadeIn(backend), FadeIn(backend_label))

        # Arrows
        arrow_style = dict(stroke_width=3, max_tip_length_to_length_ratio=0.1)
        a1 = Arrow(app.get_right(), collector.get_left(), **arrow_style)
        a2 = Arrow(collector.get_right(), processors.get_left(), **arrow_style)
        a3 = Arrow(processors.get_right(), backend.get_left(), **arrow_style)
        self.play(Create(a1)); self.play(Create(a2)); self.play(Create(a3))

        # Highlight OTTL
        brace = BraceLabel(p_item1, "OTTL lives here", brace_direction=UP, label_constructor=Text)
        self.play(GrowFromCenter(brace.brace), Write(brace.label))
        self.wait(0.5)

        # Flow animation dots
        flow_dots = VGroup(*[Dot(color=BLUE, radius=0.06) for _ in range(12)])
        path = VMobject().set_points_as_corners([
            app.get_right(), collector.get_left(), collector.get_right(), processors.get_left(), processors.get_right(), backend.get_left()
        ])
        def move_dot(dot, t_offset):
            t = ValueTracker(0)
            def updater(mobj):
                alpha = (t.get_value() + t_offset) % 1
                mobj.move_to(path.point_from_proportion(alpha))
            dot.add_updater(updater)
            return t
        trackers = [move_dot(d, i * 0.08) for i, d in enumerate(flow_dots)]
        self.add(flow_dots)
        self.play(*[t.animate.set_value(1) for t in trackers], run_time=3, rate_func=linear)
        for d in flow_dots: d.clear_updaters()
        self.wait(0.3)

        # Emphasize Tail Sampling
        highlight = SurroundingRectangle(p_item2, color=YELLOW, buff=0.1)
        self.play(Create(highlight))
        self.wait(0.6)

        # Outro
        footer = Text("Transform, sample, export — presentation-ready", font_size=28).to_edge(DOWN)
        self.play(Write(footer))
        self.wait(1)
