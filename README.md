# Smart Fitness Session Analyzer

## Student information
Name: Christine Le
Student nr.: chle71530

## Selected Option
Option A: Smart Fitness Session Analyzer

## Description
This project analyzes simulated fitness data from the provided data generator. The program checks if the sensor data is valid, calculates values like average, minimum and maximum heart rate, and looks at the activity level during the session.

Based on the data, the session is classified as resting, moderate activity, high activity, recovering, or insufficient data.

## Class Design
The program has four main classes:
- `ReferenceProfile` stores the participant's normal values, such as heart rate, skin response  and temperature.
- `Participant` stores the participant ID and their reference profile.
- `Observation` represents one measurement from the sensor data.
- `FitnessSession` keeps the participant and all the observations from one session.

## Composition and Encapsulation
I used composition by connecting the classes together. A participant has a `ReferenceProfile`, and a `FitnessSession` contains several `Observation` objects.

For encapsulation, I used `_reference_profile` inside the `Participant` class and made it accessible through a property.

## Class Method
I used a `@classmethod` in the `Observation` class to create an observation directly from a dictionary. This made it easier to convert the data from the provided generator into `Observation` objects.

## Inheritance
I did not use inheritance in this project because the classes are used for different things. For example, a participant has a reference profile, and a fitness session has observations. Because of this, I thought composition was a better choice for the project.

## Classification Rules
The program uses the participant's heart rate and activity level to classify the session.
- Resting: low activity level and heart rate close to the participant's baseline.
- Moderate activity: activity level below 0.67.
- High activity: activity level from 0.67 and above.
- Recovering: heart rate and activity level are lower in the second half of the session than in the first half.
- Insufficient data: fewer than 3 valid observations.

## How to Run
1. Make sure Python is installed.
2. Open the project folder in VS Code.
3. Run `main.py`.

You can also run it from the terminal with:
```bash
python main.py

## Example Output
```text
SMART FITNESS SESSION REPORT
----------------------------
Participant: P001
Usable observations: 10 / 10
Average heart rate: 80.4
Minimum heart rate: 76
Maximum heart rate: 85
Average activity level: 0.11
Classification: resting

## Known Limitations
The program only works with the simulated data format provided for this assignment.
The classification rules are based on the ranges used in the provided generator, so they are not meant to be used as real medical or fitness advice.
The program also uses simple rules for recovery detection and does not use machine learning.

## Test Scenarios
I tested the program using the five scenarios provided by the data generator:
- `resting`
- `moderate_activity`
- `high_activity`
- `recovery`
- `poor_quality`

The program gave the expected classifications for the normal scenarios. The poor quality scenario resulted in insufficient data because the invalid observations were rejected.