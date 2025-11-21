import pandas as pd

data = {
    "ClaimID": list(range(1, 12)),
    "ClaimNote": [
        "The driver mentioned feeling extremely tired after driving for over 12 hours without a break. They believed this fatigue might have caused them to lose focus on the road.",
        "At the time of the incident, it was late at night, and the road was not well-lit. The adjuster noted that the lack of lighting could have made it harder for the driver to see obstacles.",
        "The passenger stated that ever since the crash, they feel tired more easily, although they did not feel tired at all before the accident. The adjuster recorded this as a change post-accident rather than a cause.",
        "While reviewing the case, the adjuster noted that the driver was trying to adjust the navigation system right before the crash, which could have been a source of distraction.",
        "According to the report, the road had a sudden sharp turn that the driver did not expect. The adjuster believed this unexpected road design might have contributed to the loss of control.",
        "The driver had been feeling slightly drowsy and mentioned they might not have slept well the night before, which could have impacted their alertness.",
        "In the adjuster’s notes, it was recorded that the accident happened on a rainy night with very poor visibility due to the weather conditions.",
        "The passenger was talking loudly, and the driver turned their head briefly to respond, which might have caused a momentary distraction leading up to the incident.",
        "The adjuster noted that the driver mentioned feeling dizzy right before the accident, possibly due to not eating for several hours.",
        "It was recorded that the driver was unfamiliar with the area and was trying to read road signs, which could have contributed to their distraction.",
        "According to the notes, the driver had been driving for a long distance without rest and admitted they might have been feeling fatigued from the journey."
    ]
}

df = pd.DataFrame(data)


df.to_csv("synthetic_claim_data.csv", index=False)

print("Extended synthetic data CSV has been created.")
