class TrackersError(Exception):
    pass

class TrackersAuthError(TrackersError):
    pass

class TrackersCaptchaError(TrackersError):
    pass
