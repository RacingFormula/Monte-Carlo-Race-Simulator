import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MonteCarloRaceSimulator:
    def __init__(self, config):
        self.race_distance = config.get("race_distance", 50)
        self.lap_time_mean = config.get("lap_time_mean", 90)  # seconds
        self.lap_time_std_dev = config.get("lap_time_std_dev", 1.5)  # seconds
        self.pit_stop_time = config.get("pit_stop_time", 20)  # seconds
        self.tyre_degradation = config.get("tyre_degradation", 0.02)  # seconds per lap
        self.num_simulations = config.get("num_simulations", 10000)
        self.safety_car_chance = config.get("safety_car_chance", 0.1)  # Probability per lap
        self.safety_car_duration = config.get("safety_car_duration", 30)  # seconds per lap under safety car

    def simulate_lap(self, lap, fuel_load, safety_car_active):
        lap_time = np.random.normal(self.lap_time_mean, self.lap_time_std_dev)
        lap_time += self.tyre_degradation * lap

        # Adjust for fuel load
        fuel_penalty = (1 - fuel_load / 100) * 0.5  # seconds per percentage
        lap_time += fuel_penalty

        # Adjust for safety car
        if safety_car_active:
            lap_time += self.safety_car_duration

        return lap_time

    def run_simulation(self):
        results = []

        for _ in range(self.num_simulations):
            total_time = 0
            fuel_load = 100  # Starting fuel load
            safety_car_active = False

            for lap in range(1, self.race_distance + 1):
                # Determine if safety car is active for this lap
                if np.random.rand() < self.safety_car_chance:
                    safety_car_active = True
                else:
                    safety_car_active = False

                lap_time = self.simulate_lap(lap, fuel_load, safety_car_active)

                # Pit stop logic (e.g., every 15 laps or low fuel)
                if lap % 15 == 0 or fuel_load < 30:
                    lap_time += self.pit_stop_time
                    fuel_load = 100  # Refuel after pit stop

                total_time += lap_time
                fuel_load -= 2  # Fuel consumption per lap

            results.append(total_time)

        return results

    def analyse_results(self, results):
        results_df = pd.DataFrame({"total_time": results})
        stats = {
            "mean_time": results_df["total_time"].mean(),
            "std_dev": results_df["total_time"].std(),
            "min_time": results_df["total_time"].min(),
            "max_time": results_df["total_time"].max(),
        }
        return stats, results_df

    def plot_results(self, results_df):
        plt.hist(results_df["total_time"], bins=50, alpha=0.7, color="blue")
        plt.title("Distribution of Simulated Race Times")
        plt.xlabel("Total Time (s)")
        plt.ylabel("Frequency")
        plt.show()

if __name__ == "__main__":
    config = {
        "race_distance": 50,
        "lap_time_mean": 90,
        "lap_time_std_dev": 1.5,
        "pit_stop_time": 20,
        "tyre_degradation": 0.02,
        "num_simulations": 10000,
        "safety_car_chance": 0.1,
        "safety_car_duration": 30,
    }

    simulator = MonteCarloRaceSimulator(config)
    simulation_results = simulator.run_simulation()
    stats, results_df = simulator.analyse_results(simulation_results)

    print("Simulation Statistics:")
    print(stats)

    print("\nSample Results:")
    print(results_df.head())

    simulator.plot_results(results_df)