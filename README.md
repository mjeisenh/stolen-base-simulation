
# Should I Stay or Should I Go? A Stochastic Simulation for Stolen Base Decision-Making

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MLB Statcast](https://img.shields.io/badge/Data-MLB%20Statcast-blue?style=for-the-badge)
![Simulation](https://img.shields.io/badge/Method-Monte%20Carlo-green?style=for-the-badge)

## Project Overview
This project utilizes a Monte Carlo discrete-event simulation framework designed to optimize in-game decision-making by quantifying the probability of a successfully stealing second base. Leveraging MLB Statcast data from the 2025 season, the model fits derived probability distributions to player-specific tendencies (pitcher time-to-plate, catcher pop-time, runner lead distance / sprint speed). Instead of relying on static league averages, this tool provides dynamic, matchup-specific probabilities with an aim to maximize run expectancy.  

## Go/No-Go via the Run Expectancy Matrix (RE24)
To quantify the value of a stolen base, the model utilizes the Run Expectancy Matrix (RE24) with a run environment set at 4.15 runs per game. 
* **The Threshold**: In a standard 0-out scenario with a runner on first, the penalty (caught stealing, -0.588 runs) significantly outweighs the reward for success (+0.237 runs).
* **Break-Even Point**: A runner requires a success probability ($P_{BE}$) of approximately **71.3%** to justify the attempt mathematically.
* **The Goal**: This simulation replaces guesswork with precise, real-time probability estimates based on specific player matchups.

## Technical Architecture
The simulation executes as a discrete-event system, where the stolen base is modeled as two asynchronous, parallel processes - Offense and Defense - competing for the same resource: Second Base.

### 1. Defensive Process ($t_{defense}$)
The defensive process is a linear sequence of three stochastic service times:
* **Pitcher Time-to-Plate ($t_{pitch}$)**: Time from first move to pitch received by the catcher, sampled from Statcast run game metrics. 
* **Catcher Pop Time ($t_{pop}$)**: Time from pitch reception to the ball reaching second base, sampled from Statcast catcher metrics. 
* **Tag Application ($t_{tag}$)**: A stochastic delay representing the infielder's catch-and-tag sequence, sampled from $N(0.15, 0.05)$.
* **Formula**: $t_{defense}=t_{pitch}+t_{pop}+t_{tag}$

### 2. Offensive Process ($t_{steal}$)
The offensive process is modeled as a kinematics-based lookup using Statcast 90ft split-arrays:
* **Reaction Phase**: The runner's initial delay ($t_{react}$) based on their assigned "Burst Tier", derived from Statcast's 5ft splits
* **Kinematic Phase**: Time required to traverse the effective distance ($d_{eff}=90ft-d_{lead}$)
* **Formula**: $t_{steal}=t_{react}+t_{run}-0.15$
	* Note that $-0.15s$ adjusts the runner service time assuming a stolen base jump occurs faster than a batter leaving the box on contact

## Model Validation & Verification

* **Statistical Verification**: Tiered distributions were verified using the OpenCV Python library to perform frame-by-frame video analysis of pitcher time-to-plate, using in-game video sourced from Baseball Savant. For example, Spencer Arrighetti's delivery was empiracally measured at 1.706s, validating the "Slow" tier distribution boundaries.
* **Backtesting Results**: The model achieved a 66.7% accuracy rate (4 out of 6) validation cases from the 2025 MLB season.
* **The Butler Case**: The model identified a marginal 52.6% probability for Lawrence Butler, who ended up with a split outcome in reality (one safe, one out) against a Kevin Gausman / Tyler Heinemen battery on 7/12/25, validating the model's ability to identify high-variance matchups.

## Known Limitations & Next Steps (The "Cruz Case")

In a test case involving Oneil Cruz, the model issued a "HOLD" recommendation (8.6% success probability), yet Cruz successfully stole second base. Video review revealed Cruz ran on a Yoshinobu Yamamoto 77-mph curveball, suggesting that the model does not account for off-speed pitches. Future iterations will aim to model delivery time as a conditional variable based on predicted pitch type (Fastball vs. Off-Speed) to further reduce uncertainty.

## Repository Structure
* `/docs`: Includes the full research paper detailing simulation foundations and exploratory notebook with coding methodologies explained in depth.
* `/src`: Standalone Python scripts for OpenCV video analysis and data ingestion.
* `main.py`: Available to use for demo purposes. Future enhancements will enable full simulation capabilities. 

## Requirements
* `numpy`
* `pandas`
* `scipy`
* `opencv-python`
* `matplotlib`
* `pybaseball`

---
