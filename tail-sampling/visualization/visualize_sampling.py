#!/usr/bin/env python3
"""
Visualization of Head and Tail Sampling in OpenTelemetry

Requirements:
- matplotlib
- numpy
- pillow
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from PIL import Image, ImageDraw, ImageFont

# Constants for visualization
NUM_TRACES = 10
BOX_WIDTH = 2
BOX_HEIGHT = 4
SPACING = 6
ERROR_TRACE_IDX = 7  # Index of the error trace in tail sampling

# Colors
NORMAL_COLOR = 'blue'
KEPT_COLOR = 'green'
DROPPED_COLOR = 'gray'
ERROR_COLOR = 'red'
BOX_COLOR = 'skyblue'
BOX_EDGE_COLOR = 'navy'


def add_arrow_line(ax, x1, y1, x2, y2, color, width, arrow_size=0.3):
    """Draw a line with an arrow indicating direction."""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=width, zorder=2)
    
    # Add arrow in the middle of the line
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    
    # Calculate arrow direction
    dx = x2 - x1
    dy = y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    
    # Normalize to unit vector
    if length > 0:
        dx = dx / length
        dy = dy / length
    
        # Draw the arrow
        ax.arrow(mid_x - dx * arrow_size/2, mid_y - dy * arrow_size/2, 
                dx * arrow_size, dy * arrow_size, 
                head_width=arrow_size/2, head_length=arrow_size/2, 
                fc=color, ec=color, zorder=3)


def setup_figure():
    """Set up the figure and axis for plotting."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 10)
    ax.axis('off')
    return fig, ax


def draw_boxes(ax):
    """Draw the three component boxes: Web App, Collector, and Splunk Cloud."""
    # Web App
    webapp = patches.Rectangle((1, 3), BOX_WIDTH, BOX_HEIGHT, 
                              facecolor=BOX_COLOR, edgecolor=BOX_EDGE_COLOR, 
                              alpha=0.7, linewidth=2, zorder=1)
    ax.add_patch(webapp)
    ax.text(1 + BOX_WIDTH/2, 5.2, 'Web\nApp', ha='center', va='center', 
            fontweight='bold')

    # OTel Collector
    collector = patches.Rectangle((1 + BOX_WIDTH + SPACING, 3), BOX_WIDTH, BOX_HEIGHT, 
                                 facecolor=BOX_COLOR, edgecolor=BOX_EDGE_COLOR, 
                                 alpha=0.7, linewidth=2, zorder=1)
    ax.add_patch(collector)
    ax.text(1 + BOX_WIDTH + SPACING + BOX_WIDTH/2, 5.2, 'OTel\nCollector', 
            ha='center', va='center', fontweight='bold')

    # Splunk Cloud
    splunk = patches.Rectangle((1 + 2*BOX_WIDTH + 2*SPACING, 3), BOX_WIDTH, BOX_HEIGHT, 
                              facecolor=BOX_COLOR, edgecolor=BOX_EDGE_COLOR, 
                              alpha=0.7, linewidth=2, zorder=1)
    ax.add_patch(splunk)
    ax.text(1 + 2*BOX_WIDTH + 2*SPACING + BOX_WIDTH/2, 5.2, 'Splunk\nCloud', 
            ha='center', va='center', fontweight='bold')
    
    return webapp, collector, splunk


def generate_head_sampling_static():
    """Generate static visualization for head sampling."""
    fig, ax = setup_figure()
    webapp, collector, splunk = draw_boxes(ax)
    
    # Starting positions for traces
    start_x = 1 + BOX_WIDTH
    collector_x = 1 + BOX_WIDTH + SPACING
    end_x = 1 + 2*BOX_WIDTH + 2*SPACING
    
    # Draw traces
    kept_indices = [2, 8]  # Indices of traces that will be kept
    
    for i in range(NUM_TRACES):
        y = 3.2 + i * 0.4
        
        if i in kept_indices:
            color = KEPT_COLOR
            # Complete trace path with directional arrows
            # From webapp to collector
            add_arrow_line(ax, start_x, y, collector_x, y, color, 2)
            # From collector to splunk
            add_arrow_line(ax, collector_x, y, end_x, y, color, 2)
            # From splunk edge to inside splunk
            add_arrow_line(ax, end_x, y, end_x + BOX_WIDTH/2, y, color, 2)
        else:
            # Dropped at source - not sent at all
            # Small stub showing trace was dropped
            ax.plot([start_x, start_x + 0.5], [y, y], 
                    color=DROPPED_COLOR, linestyle='--', linewidth=1, alpha=0.5, zorder=2)
    
    # Add sampling decision label at webapp
    decision_x = start_x - 1
    ax.text(decision_x, 7.5, "Sampling Decision\n(at source)", 
            ha='center', va='center', fontsize=9,
            bbox=dict(facecolor='yellow', alpha=0.3, boxstyle='round,pad=0.5'))
    
    # Add arrow from decision to webapp
    ax.arrow(decision_x, 7.2, 0.5, -1, head_width=0.2, head_length=0.2, 
             fc='black', ec='black', zorder=3)
    
    # Add legend
    legend_elements = [
        Line2D([0], [0], color=KEPT_COLOR, lw=2, label='Sampled (Kept) Trace'),
        Line2D([0], [0], color=DROPPED_COLOR, linestyle='--', lw=1, alpha=0.5, label='Dropped Trace')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.95))
    
    # Add title
    ax.set_title('Head Sampling (Probabilistic Sampling)', fontsize=14, fontweight='bold')
    
    # Save figure
    plt.tight_layout()
    plt.savefig('head_sampling.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_tail_sampling_static():
    """Generate static visualization for tail sampling."""
    fig, ax = setup_figure()
    webapp, collector, splunk = draw_boxes(ax)
    
    # Starting positions for traces
    start_x = 1 + BOX_WIDTH
    collector_x = 1 + BOX_WIDTH + SPACING
    collector_mid_x = collector_x + BOX_WIDTH/2
    end_x = 1 + 2*BOX_WIDTH + 2*SPACING
    
    # Draw traces
    kept_indices = [2, ERROR_TRACE_IDX]  # Indices of traces that will be kept
    
    # Draw buffer inside collector
    buffer = patches.Rectangle((collector_x + 0.2, 3.2), BOX_WIDTH - 0.4, BOX_HEIGHT - 0.4, 
                             facecolor='white', edgecolor='darkgray', 
                             linestyle='--', alpha=0.5, linewidth=1, zorder=1.5)
    ax.add_patch(buffer)
    ax.text(collector_mid_x, 6.4, "Buffer", ha='center', va='center', fontsize=8)
    
    # Draw traces
    for i in range(NUM_TRACES):
        y = 3.2 + i * 0.4
        
        # Trace from web app to collector
        if i == ERROR_TRACE_IDX:
            color = ERROR_COLOR  # Error trace
        else:
            color = NORMAL_COLOR
            
        # All traces go into collector with directional arrows
        add_arrow_line(ax, start_x, y, collector_x, y, color, 2)
        
        # All traces inside collector (in buffer)
        buffer_y = 3.4 + i * 0.3  # Stacked inside buffer
        ax.plot([collector_x + 0.3, collector_x + BOX_WIDTH - 0.3], [buffer_y, buffer_y], 
                color=color, linestyle='-', linewidth=2, zorder=3)
        
        # Traces after decision
        if i in kept_indices:
            final_color = KEPT_COLOR if i != ERROR_TRACE_IDX else ERROR_COLOR
            # Trace from collector to splunk with directional arrow
            add_arrow_line(ax, collector_x + BOX_WIDTH, y, end_x, y, final_color, 2)
            # Final segment into splunk
            add_arrow_line(ax, end_x, y, end_x + BOX_WIDTH/2, y, final_color, 2)
        else:
            # Dropped traces (only show small segment after collector)
            ax.plot([collector_x + BOX_WIDTH, collector_x + BOX_WIDTH + 1], [y, y], 
                    color=DROPPED_COLOR, linestyle='--', linewidth=1, alpha=0.5, zorder=2)
    
    # Add sampling decision label inside collector
    ax.text(collector_mid_x, 4.2, "Sampling\nDecision", 
            ha='center', va='center', fontsize=8,
            bbox=dict(facecolor='yellow', alpha=0.3, boxstyle='round,pad=0.3'))
    
    # Add legend
    legend_elements = [
        Line2D([0], [0], color=NORMAL_COLOR, lw=2, label='Normal Trace'),
        Line2D([0], [0], color=ERROR_COLOR, lw=2, label='Error Trace'),
        Line2D([0], [0], color=KEPT_COLOR, lw=2, label='Kept Trace'),
        Line2D([0], [0], color=DROPPED_COLOR, linestyle='--', lw=1, alpha=0.5, label='Dropped Trace')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.95))
    
    # Add title
    ax.set_title('Tail Sampling (Decision-deferred Sampling)', fontsize=14, fontweight='bold')
    
    # Save figure
    plt.tight_layout()
    plt.savefig('tail_sampling.png', dpi=300, bbox_inches='tight')
    plt.close()


def generate_sampling_animation():
    """Generate an animated GIF demonstrating both head and tail sampling."""
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(top=0.85)  # Make room for title
    
    def init():
        ax.clear()
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 10)
        ax.axis('off')
        draw_boxes(ax)
        return []
    
    traces = []  # List to store trace objects
    title_text = ax.text(10, 9, '', ha='center', va='center', fontsize=16, 
                         fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
    
    def animate(i):
        # Clear old traces
        for trace in traces:
            if hasattr(trace, 'remove'):
                trace.remove()
        traces.clear()
        
        webapp_x = 1
        collector_x = 1 + BOX_WIDTH + SPACING
        splunk_x = 1 + 2*BOX_WIDTH + 2*SPACING
        
        # Frame 0-1: Display components
        if i < 2:
            title_text.set_text("")
            draw_boxes(ax)
            return [title_text]
        
        # Title Card 1: Head Sampling
        elif i == 2:
            title_text.set_text("Head Sampling")
            return [title_text]
        
        # Animation 1: Head Sampling (frames 3-32)
        elif i < 33:
            title_text.set_text("Head Sampling")
            head_frame = i - 3
            kept_indices = [2, 8]
            
            # Add sampling decision label at webapp
            if 5 <= head_frame < 25:
                decision_x = webapp_x + BOX_WIDTH - 1
                decision = ax.text(decision_x, 7.5, "Sampling Decision\n(at source)", 
                                  ha='center', va='center', fontsize=9,
                                  bbox=dict(facecolor='yellow', alpha=0.3, boxstyle='round,pad=0.5'))
                arrow = ax.arrow(decision_x, 7.2, 0.5, -1, head_width=0.2, head_length=0.2, 
                                fc='black', ec='black')
                traces.extend([decision, arrow])
            
            # Animate traces based on sampling decision at source
            for j in range(NUM_TRACES):
                y = 3.2 + j * 0.4
                
                # Different visualization based on whether trace is kept or dropped
                if j in kept_indices:
                    # For kept traces
                    if head_frame < 10:  # Initial movement from webapp
                        prog = head_frame / 10  # Progress from 0 to 1
                        x_end = webapp_x + BOX_WIDTH + prog * SPACING
                        # Draw arrow line with direction
                        if prog > 0.1:  # Only add arrow when line is long enough
                            arrow = ax.arrow(webapp_x + BOX_WIDTH + (prog * SPACING * 0.5),
                                           y, 0.3, 0, head_width=0.1, head_length=0.2,
                                           fc=KEPT_COLOR, ec=KEPT_COLOR, zorder=3)
                            traces.append(arrow)
                        line = Line2D([webapp_x + BOX_WIDTH, x_end], [y, y], 
                                     color=KEPT_COLOR, linestyle='-', linewidth=2)
                        ax.add_line(line)
                        traces.append(line)
                    
                    elif head_frame < 20:  # Movement to collector and beyond
                        # Complete path to collector
                        line1 = Line2D([webapp_x + BOX_WIDTH, collector_x], [y, y], 
                                       color=KEPT_COLOR, linestyle='-', linewidth=2)
                        ax.add_line(line1)
                        traces.append(line1)
                        
                        # Arrow indicating direction
                        arrow1 = ax.arrow(webapp_x + BOX_WIDTH + SPACING/2, y, 
                                         0.3, 0, head_width=0.1, head_length=0.2,
                                         fc=KEPT_COLOR, ec=KEPT_COLOR, zorder=3)
                        traces.append(arrow1)
                        
                        # Progress from collector to Splunk
                        prog = (head_frame - 10) / 10
                        if prog > 0:
                            x_end = collector_x + prog * SPACING
                            line2 = Line2D([collector_x, x_end], [y, y], 
                                          color=KEPT_COLOR, linestyle='-', linewidth=2)
                            ax.add_line(line2)
                            traces.append(line2)
                            
                            # Add arrow if line is long enough
                            if prog > 0.3:
                                arrow2 = ax.arrow(collector_x + (prog * SPACING * 0.5), 
                                                y, 0.3, 0, head_width=0.1, head_length=0.2,
                                                fc=KEPT_COLOR, ec=KEPT_COLOR, zorder=3)
                                traces.append(arrow2)
                    
                    else:  # Final movement to inside Splunk
                        # Complete path to collector
                        line1 = Line2D([webapp_x + BOX_WIDTH, collector_x], [y, y], 
                                       color=KEPT_COLOR, linestyle='-', linewidth=2)
                        ax.add_line(line1)
                        traces.append(line1)
                        
                        # Arrow for first segment
                        arrow1 = ax.arrow(webapp_x + BOX_WIDTH + SPACING/2, y, 
                                         0.3, 0, head_width=0.1, head_length=0.2,
                                         fc=KEPT_COLOR, ec=KEPT_COLOR, zorder=3)
                        traces.append(arrow1)
                        
                        # Complete path from collector to Splunk
                        line2 = Line2D([collector_x, splunk_x], [y, y], 
                                      color=KEPT_COLOR, linestyle='-', linewidth=2)
                        ax.add_line(line2)
                        traces.append(line2)
                        
                        # Arrow for second segment
                        arrow2 = ax.arrow(collector_x + SPACING/2, y, 
                                         0.3, 0, head_width=0.1, head_length=0.2,
                                         fc=KEPT_COLOR, ec=KEPT_COLOR, zorder=3)
                        traces.append(arrow2)
                        
                        # Progress into Splunk
                        prog = min(1, (head_frame - 20) / 10)
                        x_end = splunk_x + prog * BOX_WIDTH/2
                        line3 = Line2D([splunk_x, x_end], [y, y], 
                                      color=KEPT_COLOR, linestyle='-', linewidth=2)
                        ax.add_line(line3)
                        traces.append(line3)
                else:
                    # For dropped traces - just show small stub
                    if head_frame >= 5:  # Only show after initial pause
                        # Small stub showing trace was dropped at source
                        stub_length = min(0.5, (head_frame - 5) / 10)
                        line = Line2D([webapp_x + BOX_WIDTH, webapp_x + BOX_WIDTH + stub_length], 
                                      [y, y], color=DROPPED_COLOR, linestyle='--', 
                                      linewidth=1, alpha=0.5)
                        ax.add_line(line)
                        traces.append(line)
        
        # Title Card 2: Tail Sampling
        elif i == 33:
            title_text.set_text("Tail Sampling")
            return [title_text]
        
        # Animation 2: Tail Sampling (frames 34-63)
        elif i < 64:
            title_text.set_text("Tail Sampling")
            tail_frame = i - 34
            kept_indices = [2, ERROR_TRACE_IDX]
            
            # Draw buffer inside collector if past initial frames
            if tail_frame >= 10:
                buffer = patches.Rectangle((collector_x + 0.2, 3.2), BOX_WIDTH - 0.4, BOX_HEIGHT - 0.4, 
                                         facecolor='white', edgecolor='darkgray', 
                                         linestyle='--', alpha=0.5, linewidth=1)
                ax.add_patch(buffer)
                buffer_text = ax.text(collector_x + BOX_WIDTH/2, 6.4, "Buffer", 
                                     ha='center', va='center', fontsize=8)
                traces.extend([buffer, buffer_text])
            
            # Add sampling decision text inside collector at the right time
            if 20 <= tail_frame < 30:
                decision = ax.text(collector_x + BOX_WIDTH/2, 4.2, "Sampling\nDecision", 
                                  ha='center', va='center', fontsize=8,
                                  bbox=dict(facecolor='yellow', alpha=0.3, boxstyle='round,pad=0.3'))
                traces.append(decision)
            
            # Animate traces
            for j in range(NUM_TRACES):
                y = 3.2 + j * 0.4
                color = ERROR_COLOR if j == ERROR_TRACE_IDX else NORMAL_COLOR
                
                # Calculate positions based on animation frame
                if tail_frame < 10:  # Moving from webapp to collector
                    prog = tail_frame / 10  # Progress from 0 to 1
                    x_end = webapp_x + BOX_WIDTH + prog * SPACING
                    line = Line2D([webapp_x + BOX_WIDTH, x_end], [y, y], 
                                 color=color, linestyle='-', linewidth=2)
                    ax.add_line(line)
                    traces.append(line)
                    
                    # Add arrow when line is long enough
                    if prog > 0.3:
                        arrow = ax.arrow(webapp_x + BOX_WIDTH + (prog * SPACING * 0.5), 
                                       y, 0.3, 0, head_width=0.1, head_length=0.2,
                                       fc=color, ec=color, zorder=3)
                        traces.append(arrow)
                
                elif tail_frame < 20:  # All traces enter collector buffer
                    # Full trace from webapp to collector with arrow
                    line1 = Line2D([webapp_x + BOX_WIDTH, collector_x], [y, y], 
                                  color=color, linestyle='-', linewidth=2)
                    ax.add_line(line1)
                    traces.append(line1)
                    
                    # Add arrow in the middle
                    arrow1 = ax.arrow(webapp_x + BOX_WIDTH + SPACING/2, y, 
                                    0.3, 0, head_width=0.1, head_length=0.2,
                                    fc=color, ec=color, zorder=3)
                    traces.append(arrow1)
                    
                    # Trace inside buffer
                    buffer_y = 3.4 + j * 0.3  # Stacked inside buffer
                    buffer_prog = min(1, (tail_frame - 10) / 5)
                    buffer_x_end = collector_x + 0.3 + buffer_prog * (BOX_WIDTH - 0.6)
                    
                    line2 = Line2D([collector_x + 0.3, buffer_x_end], [buffer_y, buffer_y], 
                                  color=color, linestyle='-', linewidth=2)
                    ax.add_line(line2)
                    traces.append(line2)
                
                elif tail_frame < 25:  # Analysis pause
                    # Full trace from webapp to collector with arrow
                    line1 = Line2D([webapp_x + BOX_WIDTH, collector_x], [y, y], 
                                  color=color, linestyle='-', linewidth=2)
                    ax.add_line(line1)
                    traces.append(line1)
                    
                    # Add arrow in the middle
                    arrow1 = ax.arrow(webapp_x + BOX_WIDTH + SPACING/2, y, 
                                    0.3, 0, head_width=0.1, head_length=0.2,
                                    fc=color, ec=color, zorder=3)
                    traces.append(arrow1)
                    
                    # Full trace inside buffer
                    buffer_y = 3.4 + j * 0.3
                    line2 = Line2D([collector_x + 0.3, collector_x + BOX_WIDTH - 0.3], 
                                  [buffer_y, buffer_y], color=color, linestyle='-', linewidth=2)
                    ax.add_line(line2)
                    traces.append(line2)
                
                else:  # Final movement to Splunk for kept traces
                    # Full trace from webapp to collector with arrow
                    line1 = Line2D([webapp_x + BOX_WIDTH, collector_x], [y, y], 
                                  color=color, linestyle='-', linewidth=2)
                    ax.add_line(line1)
                    traces.append(line1)
                    
                    # Add arrow in the middle
                    arrow1 = ax.arrow(webapp_x + BOX_WIDTH + SPACING/2, y, 
                                    0.3, 0, head_width=0.1, head_length=0.2,
                                    fc=color, ec=color, zorder=3)
                    traces.append(arrow1)
                    
                    # Trace handling inside buffer and after decision
                    buffer_y = 3.4 + j * 0.3
                    
                    if j in kept_indices:
                        # Keep trace inside buffer
                        line2 = Line2D([collector_x + 0.3, collector_x + BOX_WIDTH - 0.3], 
                                      [buffer_y, buffer_y], color=color, linestyle='-', linewidth=2)
                        ax.add_line(line2)
                        traces.append(line2)
                        
                        # Traces moving from collector to Splunk
                        prog = min(1, (tail_frame - 25) / 10)
                        x_end = collector_x + BOX_WIDTH + prog * SPACING
                        final_color = color if j == ERROR_TRACE_IDX else KEPT_COLOR
                        
                        if prog > 0:
                            line3 = Line2D([collector_x + BOX_WIDTH, x_end], [y, y], 
                                          color=final_color, linestyle='-', linewidth=2)
                            ax.add_line(line3)
                            traces.append(line3)
                            
                            # Add arrow if line is long enough
                            if prog > 0.3:
                                arrow3 = ax.arrow(collector_x + BOX_WIDTH + (prog * SPACING * 0.5), 
                                                y, 0.3, 0, head_width=0.1, head_length=0.2,
                                                fc=final_color, ec=final_color, zorder=3)
                                traces.append(arrow3)
                                
                            # Add line into Splunk if we've reached it
                            if prog == 1 and (tail_frame - 25) > 10:
                                final_prog = min(1, (tail_frame - 35) / 5)  # Progress into Splunk
                                line4 = Line2D([splunk_x, splunk_x + final_prog * BOX_WIDTH/2], [y, y], 
                                              color=final_color, linestyle='-', linewidth=2)
                                ax.add_line(line4)
                                traces.append(line4)
                    else:
                        # Fading traces inside buffer
                        alpha = max(0, 1 - (tail_frame - 25) / 5)
                        line2 = Line2D([collector_x + 0.3, collector_x + BOX_WIDTH - 0.3], 
                                      [buffer_y, buffer_y], color=color, 
                                      alpha=alpha, linestyle='-', linewidth=2)
                        ax.add_line(line2)
                        traces.append(line2)
        
        # Final Frame
        else:
            title_text.set_text("Sampling Demonstration Complete")
        
        return traces + [title_text]
    
    # Create animation
    ani = animation.FuncAnimation(fig, animate, frames=65, 
                                  init_func=init, blit=True, interval=200)
    
    # Save as GIF
    ani.save('sampling_demonstration.gif', writer='pillow', fps=5, dpi=100)
    plt.close()


def main():
    """Main function to generate all visualizations."""
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Change working directory to output
    os.chdir('output')
    
    # Generate static visualizations
    print("Generating head sampling static visualization...")
    generate_head_sampling_static()
    
    print("Generating tail sampling static visualization...")
    generate_tail_sampling_static()
    
    print("Generating sampling animation...")
    generate_sampling_animation()
    
    print("All visualizations completed successfully!")
    print("Output files:")
    print("- head_sampling.png")
    print("- tail_sampling.png")
    print("- sampling_demonstration.gif")


if __name__ == "__main__":
    main()
