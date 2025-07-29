from config import DOWN_THRESHOLD, UP_THRESHOLD, STATE_DELAY

class SquatCounter:
    def __init__(self):
        self.rep_count  = 0
        self.state      = 'up'
        self.down_cnt   = 0
        self.up_cnt     = 0

    def update(self, angle):
        counted = False
        if self.state == 'up':
            if angle <= DOWN_THRESHOLD:
                self.down_cnt += 1
                self.up_cnt = 0
                if self.down_cnt >= STATE_DELAY:
                    self.state = 'down'
            else:
                self.down_cnt = 0

        elif self.state == 'down':
            if angle >= UP_THRESHOLD:
                self.up_cnt += 1
                self.down_cnt = 0
                if self.up_cnt >= STATE_DELAY:
                    self.rep_count += 1
                    counted = True
                    self.state = 'up'
            else:
                self.up_cnt = 0
        return counted