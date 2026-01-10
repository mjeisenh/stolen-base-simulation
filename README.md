# Stolen Base Digital Twin: A Kinematic Simulation for MLB Decision-Making

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MLB Statcast](https://img.shields.io/badge/Data-MLB%20Statcast-blue?style=for-the-badge)
![Simulation](https://img.shields.io/badge/Method-Monte%20Carlo-green?style=for-the-badge)

## Project Overview
This project explores the application of **Digital Twins**—virtual models of physical entities—to enhance in-game decision-making in professional baseball. Specifically, it focuses on simulating the **stolen base attempt** at second base. By converting kinematic physics into stochastic service times, this tool provides a high-speed decision tool for managers to evaluate the probability of a successful steal before a pitch is delivered.

## Repository Structure
* `/docs`: Includes the full research paper detailing simulation foundations and exploratory notebook with coding methodologies explained in depth.
* `/src`: Standalone Python scripts for OpenCV video analysis and data ingestion.
* `main.py`: Available to use for demo purposes. Future enhancements will enable full simulation capabilities. 

## The Strategic Framework: Run Expectancy (RE24)
To quantify the value of a stolen base, the model utilizes the **Run Expectancy Matrix (RE24)**. 
* **The Threshold**: In a standard 0-out scenario with a runner on first, the penalty for failure (-0.588 runs) significantly outweighs the reward for success (+0.237 runs).
* **Break-Even Point**: A runner requires a success probability ($P_{BE}$) of approximately **71.3%** to justify the attempt mathematically.
* **The Goal**: This Digital Twin replaces guesswork with precise, real-time probability estimates based on specific pitcher, catcher, and runner matchups.

## Technical Architecture
The simulation executes as a **discrete-event system** where the stolen base is modeled as two asynchronous, parallel processes—Offense and Defense—competing for the same resource: Second Base.

### 1. Defensive Process ($t_{defense}$)
The defensive timeline is a linear sequence of three stochastic service times:
* **Pitcher Delivery ($t_{pitch}$)**: Time from first move to pitch reception.
* **Catcher Pop Time ($t_{pop}$)**: Time from pitch reception to the ball reaching second base.
* **Tag Application ($t_{tag}$)**: A final stochastic delay representing the fielder's catch-and-tag, sampled from $N(0.15, 0.05)$.
* **Formula**: $t_{defense}=t_{pitch}+t_{pop}+t_{tag}$

### 2. Offensive Process ($t_{steal}$)
The offensive timeline is modeled as a physics-based lookup using Statcast 90ft split-arrays:
* **Reaction Phase**: The runner's initial delay ($t_{react}$) based on their assigned "Burst Tier".
* **Kinematic Phase**: Duration required to traverse the effective distance ($d_{eff}=90ft-d_{lead}$).
* **Formula**: $t_{steal}=t_{react}+t_{run}-0.15$

## Model Validation & Verification

* **Statistical Verification**: Tiered distributions were verified using the **OpenCV** Python library to perform frame-by-frame video analysis of MLB deliveries. For example, Spencer Arrighetti's delivery was measured at 1.706s, validating the "Slow" tier distribution.
* **Real-World Testing**: The model correctly predicted outcomes in **4 out of 6** validation cases from the 2025 MLB season.
* **The Butler Case**: The model identified a marginal 52.6% probability for Lawrence Butler, who ended up with a split outcome in reality (one safe, one out), validating the model's ability to identify high-variance matchups.

## Known Limitations (The "Cruz Case")

In a test case involving Oneil Cruz, the model issued a "HOLD" recommendation (8.6% probability), yet Cruz was safe.

* **Finding**: Video review revealed Cruz stole on a **77-mph off-speed pitch**.
* **Future Work**: Future iterations will model delivery time as a conditional variable based on predicted pitch type (Fastball vs. Off-speed) to further reduce uncertainty.

## Requirements
* `numpy`
* `pandas`
* `scipy`
* `opencv-python`
* `matplotlib`
* `pybaseball`

---
