from time import sleep
import numpy as np

np.random.seed()
for _ in range(np.random.randint(0, 3)):
    np.random.seed()

def inter_field_delay():
    sleep(log_normal_pause_time(1))

def inter_button_delay():
    sleep(log_normal_pause_time(1.5))

def stop_and_look_delay():
    sleep(log_normal_pause_time(6, 0.7))

def brief_review_delay():
    sleep(log_normal_pause_time(3, 0.7))

def log_normal_pause_time(mu, sigma=None):
    if sigma is None:
        sigma = mu
    random_variable = np.random.lognormal(np.log(mu), sigma)
    maximum_allowable_value = (7 + (3. * np.random.random())) * sigma * mu
    return min(random_variable, maximum_allowable_value)
