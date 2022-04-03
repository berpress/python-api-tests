import copy
import logging
import os
from os.path import exists
from typing import Dict

import yaml
import requests

from common.models import SwaggerData, EndpointStatisticsHtml, PercentStatistic
from common.singltone_like import Singleton

logger = logging.getLogger("api")


class Swagger(metaclass=Singleton):
    """
    Tool for calculating status coverage in api tests
    First, you need to create a file for verification, for example

         swagger = Swagger(url)
         swagger.load_swagger()
         swagger.create_swagger_test_file(is_safe=True)

    Where you need to specify a link to the swagger.
    Next, you need to manually edit the file ${TEST_SWAGGER_FILE_NAME}, specifying the
    necessary statuses for verification and prepare data for tests

        swagger.create_coverage_data()
    """

    def __init__(self, url=None):
        self.url = url
        self.path_dict = None
        self.data = SwaggerData()
        self.prepare_data = None

    TEST_SWAGGER_FILE_NAME = "data_swagger.yaml"

    def _save_file(self, data: dict, file_name: str = TEST_SWAGGER_FILE_NAME) -> None:
        """
        Try so safe test data in ${TEST_SWAGGER_FILE_NAME} file
        :param data: dict data
        :param file_name: file name, default TEST_SWAGGER_FILE_NAME
        :return: None
        """
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(parent_dir, "report", file_name), "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    def _prepare_swagger_data(self, data) -> dict:
        """
        Preparing data for tests
        :param data:
        :return: swagger dict
        """
        res_dict = {}
        for key, value in data.items():
            list_values = list(value.values())
            for values in list_values:
                res_dict[values.get("operationId")] = []
            for k, v in value.items():
                res_dict[v.get("operationId")] = {
                    "method": k.upper(),
                    "description": v.get("summary")
                    if v.get("description") is None
                    else v.get("description"),
                    "path": key,
                    "statuses": [200, 400, 401, 403],
                    "tag": v.get("tags")[0],
                }
        return res_dict

    def load_swagger(self) -> Dict:
        """
        Load and get swagger data
        """
        res = requests.get(self.url)
        if res.status_code == 200:
            try:
                data = yaml.safe_load(res.text)
                self.path_dict = data.get("paths")
                return data.get("paths")
            except Exception:
                logger.info("Couldn't load yaml")
        else:
            logger.info(f"Couldn't get the file, status code is {res.status_code}")

    def create_swagger_test_file(self, is_safe: bool = False) -> None:
        """
        Create file for tests
        Prepare loaded swagger data
        """
        if self.path_dict is None:
            logger.info("Couldn't load yaml")
        else:
            prepare_data = self._prepare_swagger_data(self.path_dict)
            self.prepare_data = prepare_data
            if is_safe:
                self._save_file(prepare_data)

    def get_data(self) -> dict:
        return self.data

    def swagger_check(self, key, res) -> None:
        """
        Try to check response status code  and swagger data
        """
        swagger_data = self.get_data()
        dict_data = copy.deepcopy(swagger_data)
        new_data = self.set_check_result(key, res.status_code, dict_data)
        self.data = new_data

    @staticmethod
    def set_check_result(key, status_code, data) -> dict:
        """
        Set check result
        """
        endpoint = data.swagger_data.get(key)
        if endpoint:
            statuses = endpoint.get("statuses")
            pass
            for status in statuses:
                for key in status.keys():
                    if key == status_code:
                        status[key] = True
                        return data
        return data

    def _data_diff(self, swagger_data: dict, file_data: dict) -> dict:
        """
        Get diff between swagger and checked file
        """
        prepare_data = self._prepare_swagger_data(swagger_data)
        diff = {k: prepare_data[k] for k in set(prepare_data) - set(file_data)}
        return diff

    @staticmethod
    def _prepare_check_file_data(data: dict) -> dict:
        """
        Prepare data for check
        """
        for k, value in data.items():
            statuses = value.get("statuses")
            if statuses:
                new_statuses = []
                for s in statuses:
                    new_statuses.append({s: False})
                value["statuses"] = new_statuses
        return data

    def create_coverage_data(self, file_name: str = TEST_SWAGGER_FILE_NAME) -> None:
        """
        Create coverage data
        """
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_file = os.path.join(parent_dir, "report", file_name)
        if exists(path_to_file) is False:
            self.load_swagger()
            self.create_swagger_test_file(is_safe=True)
            pass
        with open(path_to_file, "r") as stream:
            data_loaded = yaml.safe_load(stream)
            dict_data = copy.deepcopy(data_loaded)
            data_new = self._prepare_check_file_data(dict_data)
            self.data.swagger_data = data_new

    def _get_summary(self, diff: dict) -> [EndpointStatisticsHtml, PercentStatistic]:
        """
        Calculate report summary
        """
        count_success = 0
        count_of_unverified = 0
        data = copy.deepcopy(self.data.swagger_data)
        for key, value in data.items():
            is_checked_list = [
                list(status.values())[0] for status in value.get("statuses")
            ]
            count_success += len(
                [status for status in is_checked_list if status is True]
            )
            count_of_unverified += len(
                [status for status in is_checked_list if status is False]
            )
        count_diff = len(list(diff.items()))
        count_total = count_success + count_of_unverified + count_diff
        # get percent
        percentage_success = self._percentage(count_success, count_total)
        percentage_unverified = self._percentage(count_of_unverified, count_total)
        return (
            EndpointStatisticsHtml(
                count_total, count_success, count_of_unverified, count_diff
            ),
            PercentStatistic(percentage_success, percentage_unverified),
        )

    @staticmethod
    def _percentage(part, whole) -> str:
        """
        Calculate percentage of verified statuses
        """
        res = 100 * float(part) / float(whole)
        return format(res, ".1f")

    def swagger_diff(self):
        """
        Get swagger diff
        """
        swagger_data = self.load_swagger()
        if swagger_data is not None:
            diff = self._data_diff(swagger_data, self.data.swagger_data)
        else:
            diff = {}
        return diff

    def result(self):
        """
        Get swagger check result, need for build html report
        """
        self.data.diff = self.swagger_diff()
        self.data.summary = self._get_summary(self.data.diff)
        return self.data
