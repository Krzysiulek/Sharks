import numpy as np

from mesa import Agent
import random

SUSPECTIBLE = "SUS"
INFECTED = "INF"
REMOVED = "REM"

# suspectible (może się zarazić z jakimś prawdopodobieństwiem)
# infected (zamienia się w removed po kilku krokach)
# removed

# wykres kazdego typu

# parametry:
# liczba agentów
# promień zarażania
# jak długo są zarażeni zanim przejdą do removed
# pradopodobieństwo zarażenia


# np. 5% całości może być stała.

class Boid(Agent):
    """
    A Boid-style flocker agent.

    The agent follows three behaviors to flock:
        - Cohesion: steering towards neighboring agents.
        - Separation: avoiding getting too close to any other agent.
        - Alignment: try to fly in the same direction as the neighbors.

    Boids have a vision that defines the radius in which they look for their
    neighbors to flock with. Their speed (a scalar) and velocity (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
        speed,
        velocity,
        vision,
        separation,
        cohere=0.025,
        separate=0.25,
        match=0.04,
    ):
        """
        Create a new Boid flocker agent.

        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
            cohere: the relative importance of matching neighbors' positions
            separate: the relative importance of avoiding close neighbors
            match: the relative importance of matching neighbors' headings

        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match

        numberList = [SUSPECTIBLE, INFECTED]
        # Choose elements with different probabilities
        sampleNumbers = np.random.choice(numberList, 2, p=[0.9, 0.1])
        self.illness_state = sampleNumbers[0]
        self.infected_steps = 0

    def cohere(self, neighbors):
        """
        Return the vector toward the center of mass of the local neighbors.
        """
        cohere = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                cohere += self.model.space.get_heading(self.pos, neighbor.pos)
            cohere /= len(neighbors)
        return cohere

    def separate(self, neighbors):
        """
        Return a vector away from any neighbors closer than separation dist.
        """
        me = self.pos
        them = (n.pos for n in neighbors)
        separation_vector = np.zeros(2)
        for other in them:
            if self.model.space.get_distance(me, other) < self.separation:
                separation_vector -= self.model.space.get_heading(me, other)
        return separation_vector

    def match_heading(self, neighbors):
        """
        Return a vector of the neighbors' average heading.
        """
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity
            match_vector /= len(neighbors)
        return match_vector

    def get_next_illness_state(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)

        had_contact = False
        for n in neighbors:
            if n.illness_state == INFECTED:
                had_contact = True
                break

        illness_probability = 0.2
        if had_contact is True and self.illness_state == SUSPECTIBLE and (random.random() < illness_probability):
            self.illness_state = INFECTED


        if self.illness_state == INFECTED:
            self.infected_steps += 1

        if self.infected_steps > 7:
            self.illness_state = REMOVED



    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """

        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.get_next_illness_state()
        self.velocity += (
            self.cohere(neighbors) * self.cohere_factor
            + self.separate(neighbors) * self.separate_factor
            + self.match_heading(neighbors) * self.match_factor
        ) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)
