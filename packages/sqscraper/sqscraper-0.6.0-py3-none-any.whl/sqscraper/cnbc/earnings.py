"""
"""

import datetime
import re
import typing

import numpy as np
import pandas as pd
import requests

from ._apps import Apps


class StockEarnings(Apps):
    """
    :param symbol:
    """
    _post_url = "https://apps.cnbc.com/resources/asp/getBufferedEarningsChart.asp"

    _columns = {
        "year": "Year", "qtr": "Quarter", "value": "Value", "high": "High", "low": "Low",
        "numEst": "Number of Estimates", "type": "Type", "mean": "Mean",
        "announceDate": "Announcement Date", "SurpriseMean": "Mean (Surprise)",
        "SurpriseAmount": "Amount (Surprise)",
        "SurpriseNumberOfEstimates": "Number of Estimates (Surprise)",
        "SurprisePct": "Percent (Surprise)", "surprise": "Surprise", "isPos": "Positive",
        "x0": "x0", "x1": "x1", "y0": "y0", "y1": "y1", "color": "Color",
        "labelInsideBar": "Label Inside Bar", "labelDir": "Label Direction",
        "estCount": "Estimated Count", "yS": "y (Surprise)", "etype": "Estimate Type"
    }

    def __init__(self, symbol: str):
        super().__init__(symbol, "stocks/earnings")

        self._quarterly_trends = self._scrape_quarterly_trends()
        self._annual_trends = self._scrape_annual_trends()
        self._growth_forecasts = self._scrape_growth_forecasts()

    @property
    def _javascript(self) -> str:
        """
        """
        for element in self._soup.select(
            "div#category > div.subsection > script[type='text/javascript']"
        ):
            if re.search(r"j1=\"FFFFFF\";", element.text) is not None:
                return element.text.strip()
        raise ValueError

    @property
    def quarterly_trends(self) -> pd.DataFrame:
        """
        """
        dataframe = self._quarterly_trends.copy()
        dataframe.rename(columns=self._columns, inplace=True)

        dataframe.replace("", np.nan, inplace=True)
        dataframe.replace("--", np.nan, inplace=True)

        columns_int = [
            "Year", "Quarter", "Number of Estimates", "Number of Estimates (Surprise)",
            "Estimate Type"
        ]
        dataframe.loc[:, columns_int] = dataframe.loc[:, columns_int].apply(
            lambda s: pd.Series(
                s.apply(lambda x: int(x) if isinstance(x, str) else np.nan), dtype="Int64"
            )
        )
        columns_float = [
            "Value", "High", "Low", "Mean", "Mean (Surprise)", "Amount (Surprise)",
            "Percent (Surprise)", "x0", "x1", "y0", "y1", "y (Surprise)"
        ]
        dataframe.loc[:, columns_float] = dataframe.loc[:, columns_float].applymap(float)
        dataframe.loc[:, "Announcement Date"] = dataframe.loc[:, "Announcement Date"].apply(
            lambda x: datetime.datetime.strptime(x, "%m/%d/%y") if isinstance(x, str) else np.nan
        )
        columns_bool = ["Positive", "Label Inside Bar"]
        dataframe.loc[:, columns_bool] = dataframe.loc[:, columns_bool].applymap(lambda x: x == "true")

        return dataframe

    @property
    def annual_trends(self) -> pd.DataFrame:
        """
        """
        dataframe = self._annual_trends.copy()
        dataframe.rename(columns=self._columns, inplace=True)

        dataframe.replace("", np.nan, inplace=True)
        dataframe.replace("--", np.nan, inplace=True)

        columns_int = [
            "Year", "Number of Estimates", "Number of Estimates (Surprise)", "Estimated Count",
            "Estimate Type"
        ]
        dataframe.loc[:, columns_int] = dataframe.loc[:, columns_int].apply(
            lambda s: pd.Series(
                s.apply(lambda x: int(x) if isinstance(x, str) else np.nan), dtype="Int64"
            )
        )
        columns_float = [
            "Value", "x0", "x1", "y0", "y1", "High", "Low", "Mean", "Mean (Surprise)",
            "Amount (Surprise)", "Percent (Surprise)"
        ]
        dataframe.loc[:, columns_float] = dataframe.loc[:, columns_float].applymap(float)
        dataframe.loc[:, "Announcement Date"] = dataframe.loc[:, "Announcement Date"].apply(
            lambda x: datetime.datetime.strptime(x, "%m/%d/%y") if isinstance(x, str) else np.nan
        )
        columns_bool = ["Positive", "Label Inside Bar"]
        dataframe.loc[:, columns_bool] = dataframe.loc[:, columns_bool].applymap(lambda x: x == "true")

        return dataframe

    @property
    def growth_forecasts(self) -> pd.DataFrame:
        """
        """
        dataframe = self._growth_forecasts.copy()
        dataframe.columns = [
            "Formatted Name", "Name", "Type", "P/E (TTM)", "P/E (Fwd 12M)", "PEG (TTM)",
            "EPS Growth Rate (Prev 1Y)", "EPS Growth Rate (Fwd 5Y)"
        ]

        dataframe.replace("", np.nan, inplace=True)
        dataframe.replace("--", np.nan, inplace=True)

        return dataframe
    
    def _earnings_trend_javascript(self, period: typing.Literal["quarterly", "annual"]) -> str:
        """
        :param period:
        :return:
        """
        data = {
            "cht": "earnings", "width": 436, "height": 146,
            "annQtr": ("qtr" if period == "quarterly" else "ann"),
            "IBESTicker": self.symbol, "..contenttype..": "test/javascript",
            "..requester..": "ContentBuffer"
        }

        with requests.post(self._post_url, data=data, timeout=100) as response:
            return response.text

    def _scrape_quarterly_trends(self) -> pd.DataFrame:
        """
        :return:
        """
        data = []
        regex = [
            re.compile(r"^j1=\[\]$"),
            re.compile(r"^j1\[\d\]=\[\]$"),
            re.compile(r"^j1\[(\d)\]\[\d\]=\{\}$"),
            re.compile(r"^j1\[(\d)\]\[(\d)\]\.(.*?)=\"?(.*?)\"?$")
        ]

        for statement in self._earnings_trend_javascript("quarterly").split(";"):
            results = [r.search(statement.strip()) for r in regex]
            nonnull_results = [(i, x) for (i, x) in enumerate(results) if x is not None]
            if len(nonnull_results) != 1:
                continue
            idx, res = nonnull_results[0]

            if idx == 0:
                continue
            elif idx == 1:
                data.append([])
            elif idx == 2:
                data[int(res.group(1))].append({})
            elif idx == 3:
                data[int(res.group(1))][int(res.group(2))].setdefault(
                    res.group(3), res.group(4)
                )

        return pd.DataFrame(
            {f"{int(x['year'])} Q{int(x['qtr']) + 1}": x for year in data for x in year}
        ).transpose()

    def _scrape_annual_trends(self) -> pd.DataFrame:
        """
        :return:
        """
        data = []
        regex = [
            re.compile(r"^j1=\[\]$"),
            re.compile(r"^j1\[\d\]=\{\}$"),
            re.compile(r"^j1\[(\d)\]\.(.*?)=\"?(.*?)\"?$")
        ]

        for statement in self._earnings_trend_javascript("annual").split(";"):
            results = [r.search(statement.strip()) for r in regex]
            nonnull_results = [(i, x) for (i, x) in enumerate(results) if x is not None]
            if len(nonnull_results) != 1:
                continue
            idx, res = nonnull_results[0]

            if idx == 0:
                continue
            elif idx == 1:
                data.append({})
            elif idx == 2:
                data[int(res.group(1))].setdefault(res.group(2), res.group(3))

        return pd.DataFrame({int(x["year"]): x for x in data}).transpose()

    def _scrape_growth_forecasts(self) -> pd.DataFrame:
        """
        :return:
        """
        data = []
        regex = [
            re.compile(r"^j2=\[\]$"),
            re.compile(r"^j2\[\d\]=\{\}$"),
            re.compile(r"^j2\[(\d)\]\.(.*?)=\"(.*?)\"$"),
            re.compile(r"^j2\[(\d)\]\.(.*?)=\{\}$"),
            re.compile(r"^j2\[(\d)\]\.(.*?)\.formatted=\"?(.*?)\"?$"),
            re.compile(r"^j2\[(\d)\]\.(.*?)\.raw=(.*?)$")
        ]

        for statement in self._javascript.split(";"):
            results = [r.search(statement.strip()) for r in regex]
            nonnull_results = [(i, x) for (i, x) in enumerate(results) if x is not None]
            if len(nonnull_results) != 1:
                continue
            idx, res = nonnull_results[0]

            if idx == 0:
                continue
            elif idx == 1:
                data.append({})
            elif idx == 2:
                data[int(res.group(1))].setdefault(res.group(2), res.group(3))
            elif idx == 3:
                continue
            elif idx == 4:
                continue
            elif idx == 5:
                data[int(res.group(1))].setdefault(res.group(2), float(res.group(3)))

        return pd.DataFrame(data)
