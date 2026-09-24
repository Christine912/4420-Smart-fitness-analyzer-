from data_generator import generate_fitness_data

#print(profile)
#print(observations)

class ReferenceProfile:
    def __init__(self, heart_rate, skin_response, temperature):
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature

class Participant:
    def __init__(self, participant_id, reference_profile):
        self.participant_id = participant_id
        self._reference_profile = reference_profile

    @property
    def reference_profile(self):
        return self._reference_profile   


class Observation:
    def __init__(
        self,
        timestamp,
        heart_rate,
        skin_response,
        temperature,
        activity_level,
        signal_quality
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    def is_valid(self):
        if self.heart_rate is None:
            return False

        if not 35 <= self.heart_rate <= 205:
            return False

        if self.activity_level is None:
            return False

        if not 0 <= self.activity_level <= 1:
            return False

        if self.signal_quality is None:
            return False

        if not 0 <= self.signal_quality <= 1:
            return False

        if self.signal_quality < 0.6:
            return False

        if self.skin_response is None:
            return False

        if self.skin_response < 0:
            return False

        if self.temperature is None:
            return False

        if not 25 <= self.temperature <= 42:
            return False
    
        return True
    @classmethod
    def from_dict(cls, data):
            return cls(
                data["timestamp"],
                data["heart_rate"],
                data["skin_response"],
                data["temperature"],
                data["activity_level"],
                data["signal_quality"]
            )

class FitnessSession:
    def __init__(self, participant):
        self.participant = participant
        self.observations = []

    def add_observation(self, observation):
        self.observations.append(observation)

def calculate_average(values):
    if not values:
        return None

    return sum(values) / len(values)

def calculate_min_max(values):
    if not values:
        return None, None

    return min(values), max(values)

def detect_recovery(observations):
    valid_observations = [
    obs for obs in observations
    if obs.is_valid()
]

    if len(valid_observations) < 4:
        return False

    first_half = valid_observations[:len(valid_observations) // 2]
    last_half = valid_observations[len(valid_observations) // 2:]

    first_hr = calculate_average([obs.heart_rate for obs in first_half])
    last_hr = calculate_average([obs.heart_rate for obs in last_half])

    first_activity = calculate_average([obs.activity_level for obs in first_half])
    last_activity = calculate_average([obs.activity_level for obs in last_half])

    return last_hr < first_hr and last_activity < first_activity

def classify_session(
    average_heart_rate,
    average_activity,
    baseline_heart_rate,
    recovery_detected,
    valid_count
):
    if valid_count < 3:
        return "insufficient data"
    
    if recovery_detected:
        return "recovering"
    
    if average_activity < 0.25 and average_heart_rate < baseline_heart_rate + 20:
        return "resting"

    if average_activity < 0.67:
        return "moderate activity"

    if average_activity >= 0.67:
        return "high activity"

    return "unknown"

def print_report(
    participant,
    total_observations,
    valid_observations,
    average_heart_rate,
    min_heart_rate,
    max_heart_rate,
    average_activity,
    classification
    ):

    print("\nSMART FITNESS SESSION REPORT")
    print("----------------------------")
    print("Participant:", participant.participant_id)
    print("Usable observations:", valid_observations, "/", total_observations)

    if average_heart_rate is None:
        print("Average heart rate: No usable data")
    else:
        print("Average heart rate:", round(average_heart_rate, 1))

    print("Minimum heart rate:", min_heart_rate)
    print("Maximum heart rate:", max_heart_rate)

    if average_activity is None:
        print("Average activity level: No usable data")
    else:
        print("Average activity level:", round(average_activity, 2))

    print("Classification:", classification)

    if classification == "recovering":
        print("Explanation: Heart rate and activity decreased during the session.")

    elif classification == "resting":
        print("Explanation: Activity level was low and heart rate stayed close to baseline.")

    elif classification == "moderate activity":
        print("Explanation: Activity level was in the moderate range.")

    elif classification == "high activity":
        print("Explanation: Activity level was in the high range.")

    elif classification == "insufficient data":
        print("Explanation: There were not enough valid observations to analyze the session.")



    return {
        "participant_id": participant.participant_id,
        "total_observations": total_observations,
        "valid_observations": valid_observations,
        "average_heart_rate": average_heart_rate,
        "min_heart_rate": min_heart_rate,
        "max_heart_rate": max_heart_rate,
        "average_activity": average_activity,
        "classification": classification
    }

profile, observations = generate_fitness_data(
    participant_id="P001",
    scenario="poor_quality",
    seed=42,
    number_of_windows=10
)

reference_profile = ReferenceProfile(
    profile["baseline_heart_rate"],
    profile["baseline_skin_response"],
    profile["baseline_temperature"]
)

participant = Participant(
    profile["participant_id"],
    reference_profile
)

session = FitnessSession(participant)

# WAs used to creating observation objects manually:
# for data in observations:
#     observation = Observation(
#         data["timestamp"],
#         data["heart_rate"],
#         data["skin_response"],
#         data["temperature"],
#         data["activity_level"],
#         data["signal_quality"]
#     )
#     session.add_observation(observation)

for data in observations:
    observation = Observation.from_dict(data)
    session.add_observation(observation)

#print(len(session.observations)) #To check total number of observations generated
#print(session.observations[0].is_valid()) #Used to check if the first observation is valid or not

valid_observations = 0

for observation in session.observations:
    if observation.is_valid():
        valid_observations += 1

#print(valid_observations) #Used to check the number of valid observations

valid_heart_rates = []

for observation in session.observations:
    if observation.is_valid():
        valid_heart_rates.append(observation.heart_rate)

average_heart_rate = calculate_average(valid_heart_rates)

#print(average_heart_rate) #Used to check the average heart rate

min_heart_rate, max_heart_rate = calculate_min_max(valid_heart_rates)

#print(min_heart_rate) #Used to check the minimum heart rate
#print(max_heart_rate) #Used to check the maximum heart rate

valid_activity_levels = []

for observation in session.observations:
    if observation.is_valid():
        valid_activity_levels.append(observation.activity_level)

average_activity = calculate_average(valid_activity_levels)

#print(round(average_activity, 2)) #checking if the average activity level is being calculated correctly


classification = classify_session(
    average_heart_rate,
    average_activity,
    reference_profile.heart_rate,
    detect_recovery(session.observations),
    valid_observations
)

#print(classification) #Quick check to see the classification result
# print(detect_recovery(session.observations)) #Checking the recovery detection function to see if it is working correctly

result = print_report(
    participant,
    len(session.observations),
    valid_observations,
    average_heart_rate,
    min_heart_rate,
    max_heart_rate,
    average_activity,
    classification
)
