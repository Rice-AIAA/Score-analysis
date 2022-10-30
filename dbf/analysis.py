#%%
import pandas as pd
import matplotlib.pyplot as plt


#Define the baseline

# for mission 2
#base estimate: 60s
#50mph for the 2000ft straights (27.2s)
#24 seconds for takeoff and landing
#12 seconds for turns
M2_BASE_LAPS = 14
M2_BASE_PAYLOAD = 5.031702531
#50mph average 
M2_MAX_LAPS = 21
M2_MAX_PAYLOAD = 8

M2_MAX_DENOM = M2_MAX_LAPS*M2_MAX_PAYLOAD

#The baseline M2 score
BASELINE_M2 = 1 + ((M2_BASE_PAYLOAD*M2_BASE_LAPS)/M2_MAX_DENOM)


#for mission 3
# 39.2s/lap + 24seconds for takeoff and landing
M3_BASE_TIME = 141.6
M3_BASE_ANTENNA = 12

M3_MAX_TIME = 102.3
M3_MAX_ANTENNA = 20

BASELINE_M3 = M3_BASE_ANTENNA / M3_BASE_TIME
M3_MAX_DENOM = M3_MAX_ANTENNA / M3_MAX_TIME

BASELINE_M3 = 2 + ((M3_BASE_ANTENNA/M3_BASE_TIME)/M3_MAX_DENOM)

#for ground mission
GM_MAX_LIMIT = 20
GM_BASE_PAYLOAD = 5.031702531
GM_EMPTY_WEIGHT = 9.6879
BASELINE_GM = (GM_MAX_LIMIT/(GM_BASE_PAYLOAD+GM_EMPTY_WEIGHT))
BASELINE_TOTAL = BASELINE_M2 + BASELINE_M3+ BASELINE_GM


def ind_vars(ind_var):
    """
    Gets a list of the range of parameter values that will be input to find
    the change in total score
    """
    #get the different values of each parameter
    par_vals = []
    for i in range(-5,6):
        par_vals.append(ind_var*(1+(i/10)))
    return par_vals

def mission_formula(ind_var, par_vals):
    """
    Gets a list showing the percentage change in the total score
    """
    # list storing the perentage change in the total score
    total_changes = []
    if ind_var == 'payload':
        m2_scores = []
        #finds the resultant m2 score for each input of payload weight
        for par_val in par_vals:
            raw_score = par_val*M2_BASE_LAPS
            m2_scores.append(1+(raw_score/M2_MAX_DENOM))
        #gets the percentage change in total score as a function of m2 score
        for m2_score in m2_scores:
            total_score = m2_score + BASELINE_M3 + BASELINE_GM + 1
            total_changes.append(((total_score-BASELINE_TOTAL)/BASELINE_TOTAL)*100)
    
    if ind_var == 'laps':
        m2_scores = []
        #finds the resultant m2 score for each input of laps
        for par_val in par_vals:
            raw_score = int(par_val)*M2_BASE_PAYLOAD
            m2_scores.append(1+(raw_score/M2_MAX_DENOM))

        #gets the percentage change in total score as a function of m2 score
        for m2_score in m2_scores:
            total_score = m2_score + BASELINE_M3 + BASELINE_GM + 1
            print(total_score-BASELINE_TOTAL)
            total_changes.append(((total_score-BASELINE_TOTAL)/BASELINE_TOTAL)*100)

    if ind_var == 'time':
        m3_scores = []
        #finds the resultant m3 score for each input of antenna length
        for par_val in par_vals:
            raw_score = M3_BASE_ANTENNA/par_val
            m3_scores.append(2+(raw_score/M3_MAX_DENOM))
        
        #gets the percentage change in total score as a function of m2 score
        for m3_score in m3_scores:
            total_score = m3_score + BASELINE_M2 + BASELINE_GM + 1
            total_changes.append(((total_score-BASELINE_TOTAL)/BASELINE_TOTAL)*100)
    
    if ind_var == 'antenna':
        m3_scores = []
        #finds the resultant m3 score for each input of antenna length
        for par_val in par_vals:
            raw_score = par_val/M3_BASE_TIME
            m3_scores.append(2+(raw_score/M3_MAX_DENOM))
        
        #gets the percentage change in total score as a function of m2 score
        for m3_score in m3_scores:
            total_score = m3_score + BASELINE_M2 + BASELINE_GM + 1
            total_changes.append(((total_score-BASELINE_TOTAL)/BASELINE_TOTAL)*100)

    if ind_var == 'gm':
        gm_scores = []
        #finds the resultant ground mission score for each input of payload weight
        for par_val in par_vals:
            raw_score = (GM_EMPTY_WEIGHT+par_val)
            gm_scores.append(GM_MAX_LIMIT/raw_score)

        for gm_score in gm_scores:
                total_score = gm_score + BASELINE_M2 + BASELINE_M3 + 1
                total_changes.append(((total_score-BASELINE_TOTAL)/BASELINE_TOTAL)*100)
    return total_changes

# gets the percentage changes to be plotted on the x axis of the graph
percentage_changes = []
for i in range(-5,6):
    percentage_changes.append(i*10)

#plots graph of %change in total score vs %change in payload_weight
total_scores_payload = mission_formula('payload',ind_vars(M2_BASE_PAYLOAD))

#plots graph of %change in total score vs %change in laps
total_scores_laps = mission_formula('laps',ind_vars(M2_BASE_LAPS))

#plots graph of %change in total score vs %change in time
total_scores_time = mission_formula('time',ind_vars(M3_BASE_TIME))

#plots graph of %change in total score vs %change in antenna length
total_scores_antenna = mission_formula('antenna',ind_vars(M3_BASE_ANTENNA))

#plots graph of %change in total score vs %change in antenna length
total_scores_gm = mission_formula('gm', ind_vars(GM_BASE_PAYLOAD))


fig, ax = plt.subplots()
ax.set_title('Sensitivity Analysis')
ax.set_ylabel('% change in score')
plt.xticks([-50,-40,-30,-20,-10,0,10,20,30,40,50])
ax.set_xlabel('% change in parameter')
plt.plot(percentage_changes,total_scores_laps, label='M2: Number of laps')
plt.plot(percentage_changes,total_scores_payload, label='M2: Payload weight')
plt.plot(percentage_changes,total_scores_time, label='M3: Mission Time')
plt.plot(percentage_changes,total_scores_antenna, label='M3: Antenna Length')
plt.plot(percentage_changes, total_scores_gm, label = 'GM: Payload Weight')
plt.legend()
plt.grid()
plt.show()
# %%
