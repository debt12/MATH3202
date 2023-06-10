# Data: Demand for sales
Sales = [14, 8, 17, 22, 12, 6]

# Stages: t, Weeks


# State: s, Books in stock at start of week t


# Action: a, boxes to order for week t


# Value Function: Maximise profit if we start week t with s books
def V(t, s):
    if t == 6:
        return (1*s, "end")
    else:
        best = (0, 0)
        for a in range(8+1):
            sales = min(s+10*a, Sales[t])
            profit = (12*sales - 0.5*s - 50*a + V(t+1, s+10*a-sales)[0], a)
            if profit > best:
                best = profit
        return best

# Part B: State now includes whether movie has been announced
def V2(t, s, n):
    if t == 6:
        return (1*s, "end")
    else:
        best = (0, 0)
        for a in range(8+1):
            # If movie not announced
            sales1 = min(s+10*a, Sales[t])
            profit1 = 12*sales1 - 0.5*s - 50*a + V2(t+1, s+10*a-sales1, "No")[0]
            # If movie is announced
            sales2 = min(s+10*a, 2*Sales[t])
            profit2 = 12*sales2 - 0.5*s - 50*a + V2(t+1, s+10*a-sales2, "Yes")[0]
            if n == "Yes":
                profit = profit2
            else:
                profit = 0.3*profit2 + 0.7*profit1

            if profit > best[0]:
                best = (profit, a)
        return best






