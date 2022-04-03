import attr


@attr.s
class EndpointStatisticsHtml:
    """
    Class endpoint test report
    """

    endpoints: int = attr.ib()
    checked_endpoints: int = attr.ib()
    not_checked_endpoints: int = attr.ib()
    not_added_endpoints: int = attr.ib()


@attr.s
class PercentStatistic:
    success: str = attr.ib()
    failed: str = attr.ib()


@attr.s
class DescriptionHtml:
    api_url: str = attr.ib()
    swagger_url: str = attr.ib()


@attr.s
class SwaggerData:
    swagger_data: dict = attr.ib(default=None)
    diff: dict = attr.ib(default=None)
    summary: tuple = attr.ib(default=None)
