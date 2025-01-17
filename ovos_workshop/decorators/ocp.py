try:
    # backwards compat imports
    from ovos_utils.ocp import MediaType, PlayerState, MediaState, MatchConfidence, \
        PlaybackType, PlaybackMode, LoopState, TrackState
except ImportError:
    from ovos_utils.log import LOG
    from enum import IntEnum
    LOG.warning("Please update to ovos-utils~=0.1. Patching missing imports")


    class MediaType(IntEnum):
        GENERIC = 0  # nothing else matches
        AUDIO = 1  # things like ambient noises
        MUSIC = 2
        VIDEO = 3  # eg, youtube videos
        AUDIOBOOK = 4
        GAME = 5  # because it shares the verb "play", mostly for disambguation
        PODCAST = 6
        RADIO = 7  # live radio
        NEWS = 8  # news reports
        TV = 9  # live tv stream
        MOVIE = 10
        TRAILER = 11
        AUDIO_DESCRIPTION = 12  # narrated movie for the blind
        VISUAL_STORY = 13  # things like animated comic books
        BEHIND_THE_SCENES = 14
        DOCUMENTARY = 15
        RADIO_THEATRE = 16
        SHORT_FILM = 17  # typically movies under 45 min
        SILENT_MOVIE = 18
        VIDEO_EPISODES = 19  # tv series etc
        BLACK_WHITE_MOVIE = 20
        CARTOON = 21
        ANIME = 22
        ASMR = 23

        ADULT = 69  # for content filtering
        HENTAI = 70  # for content filtering
        ADULT_AUDIO = 71  # for content filtering


    class PlayerState(IntEnum):
        # https://doc.qt.io/qt-5/qmediaplayer.html#State-enum
        STOPPED = 0
        PLAYING = 1
        PAUSED = 2


    class MediaState(IntEnum):
        # https://doc.qt.io/qt-5/qmediaplayer.html#MediaStatus-enum
        # The status of the media cannot be determined.
        UNKNOWN = 0
        # There is no current media. PlayerState == STOPPED
        NO_MEDIA = 1
        # The current media is being loaded. The player may be in any state.
        LOADING_MEDIA = 2
        # The current media has been loaded. PlayerState== STOPPED
        LOADED_MEDIA = 3
        # Playback of the current media has stalled due to
        # insufficient buffering or some other temporary interruption.
        # PlayerState != STOPPED
        STALLED_MEDIA = 4
        # The player is buffering data but has enough data buffered
        # for playback to continue for the immediate future.
        # PlayerState != STOPPED
        BUFFERING_MEDIA = 5
        # The player has fully buffered the current media. PlayerState != STOPPED
        BUFFERED_MEDIA = 6
        # Playback has reached the end of the current media. PlayerState == STOPPED
        END_OF_MEDIA = 7
        # The current media cannot be played. PlayerState == STOPPED
        INVALID_MEDIA = 8


    class MatchConfidence(IntEnum):
        EXACT = 95
        VERY_HIGH = 90
        HIGH = 80
        AVERAGE_HIGH = 70
        AVERAGE = 50
        AVERAGE_LOW = 30
        LOW = 15
        VERY_LOW = 1


    class PlaybackType(IntEnum):
        SKILL = 0  # skills handle playback whatever way they see fit,
        # eg spotify / mycroft common play
        VIDEO = 1  # Video results
        AUDIO = 2  # Results should be played audio only
        AUDIO_SERVICE = 3  ## DEPRECATED - used in ovos 0.0.7
        MPRIS = 4  # External MPRIS compliant player
        WEBVIEW = 5  # webview, render a url instead of media player
        UNDEFINED = 100  # data not available, hopefully status will be updated soon..


    class PlaybackMode(IntEnum):
        AUTO = 0  # play each entry as considered appropriate,
        # ie, make it happen the best way possible
        AUDIO_ONLY = 10  # only consider audio entries
        VIDEO_ONLY = 20  # only consider video entries
        FORCE_AUDIO = 30  # cast video to audio unconditionally
        FORCE_AUDIOSERVICE = 40  ## DEPRECATED - used in ovos 0.0.7
        EVENTS_ONLY = 50  # only emit ocp events, do not display or play anything.
        # allows integration with external interfaces


    class LoopState(IntEnum):
        NONE = 0
        REPEAT = 1
        REPEAT_TRACK = 2


    class TrackState(IntEnum):
        DISAMBIGUATION = 1  # media result, not queued for playback
        PLAYING_SKILL = 20  # Skill is handling playback internally
        PLAYING_AUDIOSERVICE = 21  ## DEPRECATED - used in ovos 0.0.7
        PLAYING_VIDEO = 22  # Skill forwarded playback to video service
        PLAYING_AUDIO = 23  # Skill forwarded playback to audio service
        PLAYING_MPRIS = 24  # External media player is handling playback
        PLAYING_WEBVIEW = 25  # Media playback handled in browser (eg. javascript)

        QUEUED_SKILL = 30  # Waiting playback to be handled inside skill
        QUEUED_AUDIOSERVICE = 31  ## DEPRECATED - used in ovos 0.0.7
        QUEUED_VIDEO = 32  # Waiting playback in video service
        QUEUED_AUDIO = 33  # Waiting playback in audio service
        QUEUED_WEBVIEW = 34  # Waiting playback in browser service


def ocp_search():
    """
    Decorator for adding a method as a common play search handler.
    Decorated methods should either yield or return a list of dict results:
    {
      "media_type": <MediaType>,
      "playback": <PlaybackType>,
      "image": <(optional) str image/cover art URI>,
      "skill_icon": <(optional) str skill icon URI>,
      "bg_image": <(optional) str background image URI>,
      "uri": <str media URI>,
      "title": <str media title>,
      "artist": <str media artist/author>,
      "length": <(optional) int media length in milliseconds>,
      "match_confidence": <int 0-100 confidence this result matches request>
    }
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_search_handler'):
            func.is_ocp_search_handler = True

        return func

    return real_decorator


def ocp_play():
    """
    Decorator for adding a method to handle media playback.
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_playback_handler'):
            func.is_ocp_playback_handler = True

        return func

    return real_decorator


def ocp_previous():
    """
    Decorator for adding a method to handle requests to skip backward.
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_prev_handler'):
            func.is_ocp_prev_handler = True

        return func

    return real_decorator


def ocp_next():
    """
    Decorator for adding a method to handle requests to skip forward.
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_next_handler'):
            func.is_ocp_next_handler = True

        return func

    return real_decorator


def ocp_pause():
    """
    Decorator for adding a method to handle requests to pause playback.
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_pause_handler'):
            func.is_ocp_pause_handler = True

        return func

    return real_decorator


def ocp_resume():
    """
    Decorator for adding a method to handle requests to resume playback.
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_resume_handler'):
            func.is_ocp_resume_handler = True

        return func

    return real_decorator


def ocp_featured_media():
    """
    Decorator for adding a method to handle requests to provide featured media.
    """

    def real_decorator(func):
        # Store the flag inside the function
        # This will be used later to identify the method
        if not hasattr(func, 'is_ocp_featured_handler'):
            func.is_ocp_featured_handler = True

        return func

    return real_decorator

