from src.stolen_base_sim import Runner, Battery, StolenBaseSimulator

# sample demo
def main():
    # Chandler Simpson 90 ft splits -> sourced from Statcast
    simpson_splits = [0.0, 0.53, 0.81, 1.06, 1.27, 1.48, 1.67, 1.85, 2.03, 2.21, 
                      2.38, 2.54, 2.71, 2.87, 3.03, 3.19, 3.35, 3.52, 3.69]
    
    chandler_simpson = Runner(
        name="Chandler Simpson",
        lead_dist=11.0, # lead at pitcher first move (Statcast)
        split_array=simpson_splits,
        burst_tier="Elite" # Top 25% 5ft split 
    )

    # battery sample
    demo_battery = Battery(
        pitcher_name="Greg Weissert",
        pitcher_tier="Average", # time to plate tier (estimate)
        catcher_name="Connor Wong",
        avg_pop=1.975, # poptime (Statcast)
        pop_tier="Average"
    )

    # Initialize simulation, 10,000 iterations
    simulator = StolenBaseSimulator(
        runner=chandler_simpson,
        battery=demo_battery,
        iterations=10000 
    )

    prob, decision = simulator.run()

    #  Output Display
    print("-" * 30)
    print(f"STOLEN BASE SIMULATION RESULTS")
    print("-" * 30)
    print(f"Runner:  {chandler_simpson.name}")
    print(f"Battery: {demo_battery.pitcher_name} / {demo_battery.catcher_name}")
    print("-" * 30)
    print(f"Safe Probability: {prob:.1%}")
    print(f"Recommendation: {decision}")
    print("-" * 30)

if __name__ == "__main__":
    main()