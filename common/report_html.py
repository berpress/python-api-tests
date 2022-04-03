import os

from common.models import EndpointStatisticsHtml, SwaggerData


class ReportHtml:
    """
    Create html swagger report

    Structure:
    body:
        navbar
        links
        result_table:
            endpoints count result
            progress_bar
            accordions
            diff accordion
    """

    def __init__(self, api_url: str = None, swagger_url: str = None, data=None):
        self.api_url = api_url
        self.swagger_url = swagger_url
        self.data: SwaggerData = data

    COLOR_RED = "#F47174"
    COLOR_GREEN = "#60d891"
    COLOR_ORANGE = "#F56b02"

    @staticmethod
    def html(title: str, body: str):
        """
        Create html tags
        """
        return f"""
        <html lang="en"> <head> <meta charset="UTF-8">
            <title>{title}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" # noqa
            rel="stylesheet" integrity="sha384 -1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                </head>
                    <body>
                        {body}
                    </body>
                    <script src="./src/script.js"></script>
        </html> """  # noqa

    @staticmethod
    def _navbar():
        return """
        <nav class="navbar navbar-dark bg-dark mb-4">
            <div class="container-md">
                <a class="navbar-brand" href="#">Swagger coverage</a>
            </div>
        </nav>
        """

    def body(self):
        test_statistic, percent_statistic = self.data.summary
        navbar = self._navbar()
        endpoints = self.endpoints_statistics(test_statistic)
        links = self._links()
        progress_bar = self._progress_bar_container(percent_statistic)
        accordion = []
        for endpoint, value in self.data.swagger_data.items():
            res = self._create_accordion(endpoint, value)
            accordion.append(res)
        accordions = "".join(accordion)
        diff_accordion = self._create_diff_accordion_html()
        result_table = self._result_table(
            endpoints_statistics=endpoints,
            progress_bar=progress_bar,
            accordions=accordions,
            diff_accordion=diff_accordion,
        )
        html = [navbar, links, result_table]
        return "".join(html)

    @staticmethod
    def _div(class_: str, text: str = ""):
        """
        Create div tag
        """
        return f'<div class="{class_}">{text}</div>'

    @staticmethod
    def _button(id_: str, class_: str, text: str, count: int):
        """
        Create button
        """
        return f'<button type="button" id="{id_}", class="{class_}">{text} <span class="badge bg-secondary">{count}</span></button>'  # noqa

    @staticmethod
    def _button_group(buttons: str):
        return f'<div class="btn-group" role="group" aria-label="Basic mixed styles example">{buttons}</div>'  # noqa

    @staticmethod
    def _link(text: str, link: str) -> str:
        return f'<p class="text-center"">{text}<a href={link}>{link}</a></p>'

    def _links(self):
        api_url = self._link("API url: ", self.api_url)
        swagger_url = self._link("Swagger url: ", self.swagger_url)
        return "".join([api_url, swagger_url])

    def endpoints_statistics(self, data: EndpointStatisticsHtml):
        """
        Create file description, like url and other.
        """
        button_endpoints = self._button(
            id_="all", class_="btn btn-primary", text="All", count=data.endpoints
        )
        button_checked_endpoints = self._button(
            id_="success",
            class_="btn btn-success",
            text="Checked",
            count=data.checked_endpoints,
        )
        button_not_checked_endpoints = self._button(
            id_="not-checked",
            class_="btn btn-danger",
            text="Not checked",
            count=data.not_checked_endpoints,
        )
        button_not_added_endpoints = self._button(
            id_="not-added",
            class_="btn btn-warning",
            text="Not added",
            count=data.not_added_endpoints,
        )
        buttons = "".join(
            [
                button_endpoints,
                button_checked_endpoints,
                button_not_checked_endpoints,
                button_not_added_endpoints,
            ]
        )
        data = self._button_group(buttons)
        content = self._div(class_="d-flex justify-content-center", text=data)
        return content

    def _progress_bar_container(self, data):
        success = self._progress_bar(result_class="success", percent=data.success)
        failed = self._progress_bar(result_class="danger", percent=data.failed)
        result = "".join([success, failed])
        return f"""
            <div class="container px-4 py-1">
                <div class="row gx-5">
                    <div class="progress gx-0">
                    {result}
                    </div>
                </div>
            </div>"""
        pass

    @staticmethod
    def _progress_bar(result_class: str, percent: float) -> str:
        return f"""
            <div class="progress-bar bg-{result_class} px-5"
                role="progressbar" style="width: {percent}%" aria-valuenow=20 aria-valuemin="0" aria-valuemax="100">{percent}%
            </div>
            """  # noqa

    @staticmethod
    def _result_table(
        progress_bar: str,
        accordions: str,
        endpoints_statistics: str,
        diff_accordion: str,
    ):
        return f"""
        <div class="container px-5">
            <div class="row gx-0">
            {endpoints_statistics}
            {progress_bar}
            <div id=accordions>
                {accordions}
                {diff_accordion}
            </div>
            </div>
        </div>
        """
        pass

    @staticmethod
    def _create_section(status: dict) -> str:
        st, result = list(status.items())[0]
        color = "green" if result else "red"
        return f"""
                <section>
                    <p style="color:{color};">{st}</p>
                </section>
            """

    def _create_accordion(self, endpoint, value, color: str = None):
        """
        id, color, description, sections
        """
        description = (
            f'<b>{value.get("description", "n/a")}</b> '
            f'({value.get("method")} {value.get("path")})'
        )
        is_checked_list = [list(status.values())[0] for status in value.get("statuses")]
        if color is None:
            color = self.COLOR_RED if False in is_checked_list else self.COLOR_GREEN

        sections = []
        for status in value.get("statuses"):
            res = self._create_section(status)
            sections.append(res)

        return f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="{endpoint}">
                    <button class="accordion-button collapsed" type="button"
                        data-bs-toggle="collapse" data-bs-target="#flush-collapseOne"
                        aria-expanded="false" aria-controls="flush-collapseOne"
                        style="background-color: {color};">
                        {description}
                    </button>
            </h2>
        <div class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
            data-bs-parent="#accordionFlushExample" data-state="collapse">
                <div class="accordion-body"> <section>
                    {"".join(sections)} </section>
        </div>
            </div>
                </div>
                """  # noqa

    @staticmethod
    def _create_accordion_diff(endpoint, value, color: str = None):
        """
        id, color, description, sections
        """
        description = "Missing endpoints"

        return f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="{endpoint}">
                    <button class="accordion-button collapsed" type="button"
                        data-bs-toggle="collapse" data-bs-target="#flush-collapseOne"
                        aria-expanded="false" aria-controls="flush-collapseOne"
                        style="background-color: {color};">
                        {description}
                    </button>
            </h2>
        <div class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
            data-bs-parent="#accordionFlushExample" data-state="collapse">
                <div class="accordion-body"> <section>
                    {value} </section>
        </div>
            </div>
                </div>
                """  # noqa

    @staticmethod
    def area(text: str):
        return f"""
                <textarea class="form-control" rows="3">{text}</textarea>
                """
        pass

    def _create_diff_accordion_html(self):
        """
        create diff html
        """
        diff_text = self._create_diff_text(self.data.diff)
        return self._create_accordion_diff(
            endpoint="endpoint", color=self.COLOR_ORANGE, value=self.area(diff_text)
        )

    @staticmethod
    def _create_diff_text(diff: dict) -> str:
        """
        Create diff text for data_swagger.yaml
        """
        text = []
        spaces = "  "
        for key, values in diff.items():
            text.append(f"{key}:\n")
            text.append(f'{spaces}description: {values.get("description")}\n')
            text.append(f'{spaces}method: {values.get("method")}\n')
            text.append(f'{spaces}path: {values.get("path")}\n')
            text.append(f"{spaces}statuses:\n")
            text.append(f"{spaces}- 200\n")
            text.append(f"{spaces}- 400\n")
            text.append(f"{spaces}- 401\n")
            text.append(f"{spaces}- 403\n")
            text.append(f'{spaces}tag: {values.get("tag")} \n')
        return "".join(text)

    def save_html(self, file_name: str = "index.html"):
        """
        Save html with swagger check diff
        """
        body = self.body()
        html = self.html("NCPS", body)
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(parent_dir, "report", file_name), "w") as outfile:
            outfile.write(html)
