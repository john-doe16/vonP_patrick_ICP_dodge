from laya import Router
from sympy import true

router = Router()

question = {"type": "choice",
             "instructions": "Choice?",
               "criteria": [
                   "Rock",
                    "Paper",
                    "Scissors"
                    ]}

answers = ""

while true:
    answers += input("Rock, Paper or Scissors?: ").lower()

    result = router.predict("Predict what the player will player based on these past responces: "+answers, {"topic": question})

    for name, ans in result["answers"].items():
        print(f"{name}: confidence {ans['confidence']:.0%}")