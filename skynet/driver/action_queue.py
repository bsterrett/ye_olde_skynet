import random
import numpy as np
from custom_logger import getLogger

logger = getLogger('action_queue')

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

class ActionQueueException(Exception): pass

class ActionQueue(object):
    def __init__(self, action_queue=None, insert_pause_action=None):
        if action_queue is None:
            self._action_queue = []
        else:
            self._action_queue = action_queue

        if insert_pause_action is None or callable(insert_pause_action):
            self._insert_pause_action = insert_pause_action
        else:
            raise ActionQueueException(f'Cannot use a non-callable pause type: {insert_pause_action}')

    def append(self, action):
        if callable(action):
            self._action_queue.append(action)
        else:
            raise ActionQueueException(f'Cannot add a non-callable action: {action}')

    def unordered_queue(self):
        working_queue = self.ordered_queue()
        random.shuffle(working_queue)
        return working_queue

    def ordered_queue(self):
        return self._action_queue[:]

    def queue(self, ordered=True):
        if ordered:
            return self.ordered_queue()
        else:
            return self.unordered_queue()

    def queue_with_interspersed_pauses(self, ordered=True):
        working_queue = self.queue(ordered)
        if self._insert_pause_action is None:
            return working_queue
        else:
            return intersperse(working_queue, self._insert_pause_action)

    def run(self, ordered=True):
        working_queue = self.queue_with_interspersed_pauses(ordered)
        results = []
        for action in working_queue:
            logger.debug(f"Executing {action}")
            result = action()
            results.append(results)
        self._action_queue = []
        return results

class DistractedActionQueue(ActionQueue):
    def __init__(self, action_queue=None, insert_pause_action=None, \
                        initial_distraction_probability=None, \
                        delta_distraction_probability=None, \
                        insert_distraction_action=None):

        if action_queue is None:
            self._action_queue = []
        else:
            self._action_queue = action_queue

        if insert_pause_action is None or callable(insert_pause_action):
            self._insert_pause_action = insert_pause_action
        else:
            raise ActionQueueException(f'Cannot use a non-callable pause type: {insert_pause_action}')

        if initial_distraction_probability is None or initial_distraction_probability > 1. or initial_distraction_probability < 0.:
            self._initial_distraction_probability = 0.
        else:
            self._initial_distraction_probability = initial_distraction_probability

        if delta_distraction_probability is None or delta_distraction_probability > 1. or delta_distraction_probability <= 0.:
            self._delta_distraction_probability = 0.25
        else:
            self._delta_distraction_probability = delta_distraction_probability

        if insert_distraction_action is None or callable(insert_distraction_action):
            self._insert_distraction_action = insert_distraction_action
        else:
            raise ActionQueueException(f'Cannot use a non-callable distraction type: {insert_distraction_action}')

    def run(self, ordered=True):
        if self._insert_distraction_action is None:
            # if there is no distraction action, just run as a regular action queue
            return super(DistractedActionQueue, self).run(ordered)

        working_queue = self.queue_with_interspersed_pauses(ordered)
        working_distraction_probability = self._initial_distraction_probability
        results = []
        for action in working_queue:
            if np.random.random() <= working_distraction_probability:
                working_distraction_probability = self._initial_distraction_probability
                self._insert_distraction_action()
            else:
                working_distraction_probability += self._delta_distraction_probability

            result = action()
            results.append(results)
        self._action_queue = []
        return results
