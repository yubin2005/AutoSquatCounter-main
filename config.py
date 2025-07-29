# Angle thresholds
DOWN_THRESHOLD   = 100     # Angle <= this => “down”
UP_THRESHOLD     = 140     # Angle >= this => “up”

# Smoothing & visibility
SMOOTH_ALPHA     = 0.7     # EMA factor for angle
VISIBILITY_TH    = 0.3     # Min landmark visibility

# State machine
STATE_DELAY      = 5       # Frames to confirm down/up transition

# Rendering
FONT_SCALE       = 2.0
FONT_THICKNESS   = 3
CARD_COLOR       = (0, 255, 0)   # BGR
SHADOW_COLOR     = (30, 30, 30)  # BGR

# Video / logging defaults
DEFAULT_SOURCE   = 0
DEFAULT_ROTATE   = 'none'
DEFAULT_SCALE    = 1.0
DEFAULT_OUTPUT   = 'squat_output.mp4'
DEFAULT_FPS      = 30.0
DEFAULT_CSV      = 'squat_log.csv'