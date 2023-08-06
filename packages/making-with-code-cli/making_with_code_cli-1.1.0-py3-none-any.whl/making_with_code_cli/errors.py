class MWCError(Exception):
    pass

class CurriculumSiteNotAvailable(MWCError):
    def __init__(self, site_url, *args, **kwargs):
        msg = f"Error reading curriculum metadata from {site_url}"
        super().__init__(msg)

class NoCurriculaAvailable(MWCError):
    pass
