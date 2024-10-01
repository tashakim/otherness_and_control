# run via:
# python wonder.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch


class CosmicJourney:
    """
    We represent the sense of awe of the Universe discussed in `Gentleness and 
    the Artificial Other` and `Loving in a World You Don't Trust `. 
    The progress bar at the top keeps track of humanity's advancement and our 
    ability to shape the future. Challenges are seen as red X markers, which 
    represent the suffering and obstacles that humanity encounters. 
    The blue dot shows the continuous, oscillating journey that humanity takes, 
    through the unknown cosmic journey that unfolds in front of our very eyes. 
    """
    def __init__(self):
        """
        Initializes humanity, challenges, and other environmental setup.
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_facecolor('black')
        self.fig.patch.set_facecolor('black')
        self.stars, = self.ax.plot([], [], 'w.', markersize=1)
        # Humanity
        self.humanity_size = 10
        self.humanity, = self.ax.plot([], [], 'bo', markersize=self.humanity_size)
        # Challenges
        self.challenges, = self.ax.plot([], [], 'rx', markersize=6)
        self.challenge_sizes = []
        self.challenge_positions = np.empty((0, 2))
        # Humanity progress bar
        self.progress_bar = self.ax.bar(0, 5, width=0, bottom=95, color='green')[0]
        self.ax.text(2, 97, 'Progress', color='white')

        self.wonder_text = self.ax.text(50, 5, '', ha='center', color='yellow')
        self.story_text = self.ax.text(50, 92, '', ha='center', fontsize=12, color='lightblue', style='italic')
        # Track journey
        self.progress = 0
        self.wonder_level = 50
        self.challenge_count = 0
        self.frames_since_last_challenge = 0
        self.story_index = 0
        # Predefined story elements for narration
        self.story = [
            "Humanity embarks on its cosmic journey.",
            "Challenges arise, but the universe is full of wonder.",
            "As they progress, the path ahead becomes more difficult.",
            "The mysteries of the cosmos unfold.",
            "Will humanity overcome, or will the vastness swallow them whole?"
        ]
        self.boundary = FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=0.1", 
                                       linewidth=2, edgecolor='white', facecolor='none')
        self.ax.add_patch(self.boundary)

    def init_animation(self):
        """
        Initializes the visual elements of the simulation.
        """
        self.stars.set_data(np.random.rand(1000) * 100, np.random.rand(1000) * 100)
        self.humanity.set_data([], [])
        self.challenges.set_data([], [])
        self.challenge_sizes.clear()
        self.challenge_positions = np.empty((0, 2))
        self.progress_bar.set_width(0)
        self.wonder_text.set_text('')
        self.story_text.set_text('')
        return self.stars, self.humanity, self.challenges, self.progress_bar, self.wonder_text, self.story_text

    def update_animation(self, frame):
        # Move humanity in a spiral path through space
        x = 50 + np.cos(frame * 0.05) * 40
        y = 50 + np.sin(frame * 0.05) * 40
        # Increase humanity size at each time step
        self.humanity_size = min(self.humanity_size + 0.05, 50)  # Maximum size 30
        self.humanity.set_data([x], [y])
        self.humanity.set_markersize(self.humanity_size)  # Update marker size
        # Simulate twinkling stars
        if frame % 5 == 0:
            twinkle_factor = 0.05
            new_star_positions = np.random.rand(1000, 2) * 100 + np.random.normal(0, twinkle_factor, (1000, 2))
            self.stars.set_data(new_star_positions[:, 0], new_star_positions[:, 1])
        # Generate new challenges periodically
        if self.frames_since_last_challenge > 20 and np.random.random() < 0.15:
            new_challenge = np.random.rand(2) * 100
            new_size = 1
            self.challenge_positions = np.vstack([self.challenge_positions, new_challenge])
            self.challenge_sizes.append(new_size)
            self.frames_since_last_challenge = 0
        self.frames_since_last_challenge += 1
        # Check for collisions
        self.check_collisions(x, y)
        # Remove swallowed challenges
        self.challenges.set_data(self.challenge_positions[:, 0], self.challenge_positions[:, 1])
        for i, (pos, size) in enumerate(zip(self.challenge_positions, self.challenge_sizes)):
            self.ax.plot(pos[0], pos[1], 'rx', markersize=size)
        # Update progress
        self.progress = min(100, self.progress + 0.05)
        self.progress_bar.set_width(self.progress)
        # Update wonder level
        self.wonder_level = max(0, min(100, self.wonder_level + np.random.normal(0, 1.5)))
        wonder_message = self.get_wonder_message()
        self.wonder_text.set_text(wonder_message)
        # Update the story narration
        if frame % 100 == 0 and self.story_index < len(self.story):
            self.story_text.set_text(self.story[self.story_index])
            self.story_index += 1

        return self.stars, self.humanity, self.challenges, self.progress_bar, self.wonder_text, self.story_text

    def check_collisions(self, humanity_x, humanity_y):
        """
        Checks whether humanity (blue dot) collides into a challenge or not.
        If so, humanity overcomes the challenge and swallows it whole.
        """
        humanity_radius = self.humanity_size / 2
        distances = np.sqrt((self.challenge_positions[:, 0] - humanity_x) ** 2 +
                            (self.challenge_positions[:, 1] - humanity_y) ** 2)
        for i, distance in enumerate(distances):
            if distance < humanity_radius:
                if self.challenge_sizes[i] > self.humanity_size:
                    self.end_simulation()
                    return
                else:
                    # Swallow the red cross and remove it
                    self.challenge_positions = np.delete(self.challenge_positions, i, axis=0)
                    self.challenge_sizes.pop(i)
                    break  # Only handle one collision per frame

    def end_simulation(self):
        print("Humanity collided with a challenge too insurmountable! Simulation terminated.")
        plt.close(self.fig)

    def get_wonder_message(self):
        if self.wonder_level > 80:
            return "Awe-inspiring cosmic majesty!"
        elif self.wonder_level > 60:
            return "The universe unfolds its mysteries."
        elif self.wonder_level > 40:
            return "Balancing wonder and harsh realities."
        elif self.wonder_level > 20:
            return "Struggling against cosmic indifference."
        else:
            return "In the depths of existential challenge."

    def run(self):
        anim = FuncAnimation(self.fig, self.update_animation, init_func=self.init_animation,
                             frames=1000, interval=50, blit=True)
        plt.show()

if __name__ == "__main__":
    journey = CosmicJourney()
    journey.run()
