import numpy as np

class BaseballEntity:
    """Base class for entities involved in the stolen base simulation."""
    def __init__(self, name):
        self.name = name

class Runner(BaseballEntity):
    def __init__(self, name, lead_dist, split_array, burst_tier):
        super().__init__(name)
        self.lead_dist = lead_dist
        self.split_array = split_array  # Empirical 90ft split-time data
        self.burst_tier = burst_tier    # Elite, Average, or Poor

    def get_t_steal(self):
        """Calculates offensive service time based on kinematics."""
        # Mapping burst tiers to normal distributions 
        burst_map = {
            'Elite': (0.18, 0.02),
            'Average': (0.20, 0.05),
            'Poor': (0.24, 0.08)
        }
        mu, sigma = burst_map.get(self.burst_tier, (0.20, 0.05))
        t_react = np.random.normal(mu, sigma) # accounting for reaction time
        
        # Calculate effective distance (base path - lead distance) 
        # interpolate run time 
        d_eff = 90 - self.lead_dist
        # Simple linear interpolation proxy for split array lookup
        t_run = np.interp(d_eff, np.arange(0, 95, 5), self.split_array)
        
        return t_react + t_run - 0.15 # Static adjustment for steal start 

class Battery:
    """Represents the Pitcher and Catcher defensive unit."""
    def __init__(self, pitcher_name, pitcher_tier, catcher_name, avg_pop, pop_tier):
        self.pitcher_name = pitcher_name
        self.pitcher_tier = pitcher_tier # elite / average / poor (normal dist)
        self.catcher_name = catcher_name
        self.avg_pop = avg_pop
        self.pop_tier = pop_tier         # elite / average / poor (normal dist)

    def get_t_defense(self):
        """Calculates total defensive service time."""
        # Pitcher Delivery (Time to Plate) distributions
        p_map = {'Elite': (1.25, 0.05), 'Average': (1.35, 0.08), 'Slow': (1.55, 0.10)}
        p_mu, p_sigma = p_map.get(self.pitcher_tier, (1.35, 0.08))
        t_pitch = np.random.normal(p_mu, p_sigma)

        # Catcher Pop Time distributions 
        c_map = {'Elite': 0.03, 'Average': 0.08, 'Poor': 0.10}
        c_sigma = c_map.get(self.pop_tier, 0.08)
        t_pop = np.random.normal(self.avg_pop, c_sigma)

        # Stochastic tag application (delay) 
        t_tag = np.random.normal(0.15, 0.05)

        # total defensive service time
        return t_pitch + t_pop + t_tag

class StolenBaseSimulator:
    def __init__(self, runner, battery, iterations=10000):
        self.runner = runner
        self.battery = battery
        self.iterations = iterations
        self.break_even = 0.713 # Based on RE24 analysis 

    def run(self):
        """Executes Monte Carlo simulation and returns success probability."""
        safe_count = 0
        for _ in range(self.iterations):
            if self.runner.get_t_steal() <= self.battery.get_t_defense(): # Tie goes to runner 
                safe_count += 1
        
        prob_safe = safe_count / self.iterations
        decision = "STEAL" if prob_safe >= self.break_even else "HOLD"
        
        return prob_safe, decision
