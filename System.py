class System:
    """Container for a system of n-bodies as a list. Includes a dict mapping the bodies name to its reference.
    Attributes:
        bodies          : list of bodies
        map             : dict mapping name -> body
        constants       : dict mapping constant to value
        history         : formatted list of full trajectory

    Methods:
        .get()          : gets the correct body from the list w/ dict access

        .add()

        .remove()

        .record()       : appends the snapshot of each body in systems current state at a given timestep
    """

    def __init__(self, bodies):
        self.bodies = []
        self.map = {}
        self.history = []
        self.constants = {'G': 6.674 * 10**(-11),}    
           
        for body in bodies:
            self.add(body)


    def __len__(self):
        """returns the number of bodies in the system"""
        return len(self.bodies)


    def __iter__(self):
        """initializes and returns an iterator object for a system
        iterates through all bodies in the system"""
        return iter(self.bodies)


    def add(self, body):
        """Adds body to: list, map, and its mu to constants"""
        assert body.name not in self.map, "Can't have duplicate object names."
        self.bodies.append(body)
        self.map[body.name] = body
        self.constants[f'{body.name}-mu'] = self.constants['G'] * body.mass


    def remove(self, body):
        """Removes body from: list, map, and its mu from constants"""
        self.bodies.remove(body)
        del self.map[body.name]
        del self.constants[f'{body.name}-mu']
    

    def get(self, name):
        return self.map[name]
    

    def record(self, time):
        """In a flat log, for each body in bodies append its current state to history list """
        for body in self.bodies:
            self.history.append((time, body.name, body.position.x, body.position.y, body.velocity.x, body.velocity.y))



    

        
        



