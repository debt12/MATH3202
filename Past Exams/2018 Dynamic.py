""""
Notes and Assumptions:

Context: Iterated Prisoner’s Dilemma
Stages: t, 1 to 10 rounds
State: s, probability of cooperating or defecting (0,1) start at 0.6
Actions: a, cooperate or defect
Value Function: maximise your expected payoff from the	10 rounds
Payoffs (You,Opp) CC,CD,DC,DD: 3,0,5,1
"""

# Data
payoff = [3, 0, 5, 1]
Opp = 0.6

# Stages: t, rounds 1 to 10

# State: s, number of rounds won at stage t

# Action: a, Cooperate or Defect at stage t

# Value Function: maximise your expected payoff
def V(s,t):
    if t == 11:
        return(s, "Game Over")
    else:
        best = (0,0)
        for a in range(4+1):
             =
            round = (payoff[0] + V(t+1, Opp + 0.1) +
                     payoff[1] + V(t+1, Opp - 0.2) +
                     payoff[2] + V(t+1, Opp + 0.1) +
                     payoff[3] + V(t+1, Opp - 0.2))
            if round > best:
                round = best
        return best