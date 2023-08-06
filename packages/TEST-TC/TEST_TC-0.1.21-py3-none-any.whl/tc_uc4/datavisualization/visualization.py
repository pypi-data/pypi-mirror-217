from __future__ import annotations

import numpy as np
import pandas as pd
import geopandas as gpd

from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis

import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go

from typing_extensions import Self

from ..utility.resources import log_exception
from ..utility.tele_logger import logger

from ..utility.constants import code_to_region_name


class DataVisualization:

    def __init__(
        self,
        use_case: str,
        df: pd.DataFrame,
        target: str = "volumes"
    ) -> Self:
        
        """Initializing the DataVisualization class.
            A class for the visualization of general situation descript by dataframe (the class consider all value,
            for each aggregation level).

        Parameters
        ----------
        use_case : str
            specify the name of use case (necessary for the plot title)
        df : pd.DataFrame
            the original dataset
        target : str
            the name of column target, by default "volumes"
        dict_reg : dict
            a dictionary that convert codice_regione to name , by default None
        """

        self.use_case = use_case
        self.dict_regioni = code_to_region_name
        self.df = df
        self.target = target

        self.df[target] = 1

    @log_exception(logger)
    def conteggi(
        self,
        level1: str,
        level2: str = None,
        level3: str = None,
        freq: str = None,
    ) -> pd.Series:
        
        """Compute the aggregation by specify level

        Parameters
        ----------
        target : str
            name of target column
        level1 : str
            name of first level aggregation
        level2 : str
            name of second level aggregation, by default None
        level3: str
            name of third level aggregation, by default None

        Returns
        -------
        pd.Series
            Series of aggregation count

        Raises
        ------
        Exception
            _description_
        """

        # try:
        #     pd.Period(data_inizio)
        #     pd.Period(data_fine)
        # except:
        #     raise Exception("La data non è valida")

        livelli = list(filter(None, [level1, level2, level3]))
        livelli1 = [
            pd.Grouper(key=i, freq=freq) if self.df[i].dtype == "<M8[ns]" else i
            for i in livelli
        ]
        regioni = list(self.dict_regioni.values())

        logger.info(msg="START elaborate counting dataframe", important=True)

        # select DATA
        # i = " 23:59:59"
        # tab = self.df.query(f"({data} >= '{data_inizio}') & ({data} <= '{data_fine + i}')")

        # aggregazione per livelli specificati
        ris = (
            self.df.groupby(livelli1, as_index=False)[self.target]
            .sum()
            .sort_values([self.target], ascending=0)
            .set_index(livelli)
        )

        # regioni mancanti
        if self.df[level1].unique()[0] in regioni:
            regioniMancanti = np.setdiff1d(
                regioni, ris.index.get_level_values(0).unique()
            )
            if len(livelli) > 1:
                regioniMancanti = [(i, "null") for i in regioniMancanti]
        else:
            regioniMancanti = []

        zero = pd.Series(np.nan, index=regioniMancanti)

        if ris.shape[0] > 1:
            ris = pd.concat([ris.squeeze(), zero])
        else:
            ris = pd.concat([ris, zero])[self.target]

        ris = ris.to_frame()

        # indici e colonne
        if len(livelli) > 1:
            ris.index = pd.MultiIndex.from_tuples(ris.index, names=(i for i in livelli))

        ris.reset_index(inplace=True)
        ris.columns = livelli + [self.target]

        #self.cont = ris

        logger.info(msg="DONE elaborate counting dataframe", important=True)

        return ris

    def plot(
        self,
        df: pd.DataFrame,
        level1: str,
        level2: str = None,
        level3: str = None,
    ) -> plotly.graph_objs._figure.Figure:
        
        """Sunburst plot of aggregate data

        Parameters
        ----------
        df : pd.DataFrame
            dataframe of aggregate data (result of conteggi function)
        target : str
            name of target column (count column)
        level1 : str
            name of first level aggregation
        level2 : str, optional
            name of second level aggregation, by default None
        level3 : str, optional
            name of third level aggregation, by default None

        Returns
        -------
        plotly.graph_objs._figure.Figure
            sunburst plot
        """

        livelli = [level1, level2, level3]
        levels = list(filter(None, livelli))
        name_levels = " e ".join(levels).replace("_", " ").title()

        fig = px.sunburst(
            df,
            path=levels,
            values=self.target,
            width=600,
            height=600,
            title=f"Numero di {self.use_case} per {name_levels}",
            template=dict(
                layout=go.Layout(
                    title_font=dict(family="Rockwell", size=24, color="red"),
                    font=dict(color="green"),
                )
            ),
        )
        # fig.show()

        return fig

    def boxplot(self, df: pd.DataFrame, variable: str):
        
        """Boxplot of aggregated data

        Parameters
        ----------
        df : pd.DataFrame
            dataframe of aggregate data (result of conteggi function)
        variable : str
            name of variable on x axis 

        Results
        -------
        plotly.graph_objs._figure.Figure
            boxplot
        """

        fig = px.box(
            df,
            x=variable,
            y=self.target,
            template=dict(
                layout=go.Layout(
                    title_font=dict(family="Rockwell", size=24, color="red"),
                    font=dict(color="green"),
                )
            ),
        )

        return fig

    def DTW(self, df: pd.DataFrame, column: str, val1: str, val2: str):

        """compute distance between two time series

        Parameters
        ----------
        df : pd.DataFrame
            dataframe result of conteggi function
        column : str
            name of one column aggregate on
        val1: str
            name of column modality
        val2 : str
            name of column modality

        Returns
        -------
        tuple
            tuple containing a figure that representing distance between time series and the value of distance

        """

        x = df[df[column] == val1][self.target].values
        y = df[df[column] == val2][self.target].values

        distance = dtw.distance(x, y, use_pruning=True)
        path = dtw.warping_path(x, y)

        fig, ax = plt.subplots(2, 1, figsize=(20, 9))
        dtwvis.plot_warping(x, y, path, fig=fig, axs=ax)

        ax[0].set_title(
            f"Dynamic Time Warping, {column} ({val1}-{val2})",
            fontsize=20,
            y=1.1,
            color="gray",
            loc="left",
            family="serif",
        )
        ax[1].set_xlabel("time", fontsize=12)
        ax[0].set_ylabel(self.target, fontsize=12)
        ax[1].set_ylabel(self.target, fontsize=12)
        fig.tight_layout()

        normalized_distance = distance / np.sqrt(len(x) * len(y))

        return (fig, normalized_distance)
    
    def add_geographical_info(
        self, target: str, region: str, df_geo: gpd.GeoDataFrame, region_geo: str
    ) -> gpd.GeoDataFrame:
        
        """Aggregates df on "spatial_variable" and joins with the "regions" geodataframe on "join_variable"

        Parameters
        ----------
        target : str
            name of target column
        region : str
            name of region column
        df_geo : gpd.GeoDataFrame
            GeoDataFrame containing geometry for Italian region
        region_geo : str
            name of region column
        data : str
            name of data column
        data_inizio : str
            initial data to select
        data_fine : str
            final data to select

        Returns
        -------
        gpd.GeoDataFrame
            geodataframe containing geographical information and the aggregated "spatial_variable"
        """

        df_aggreg = self.conteggi(target, region)
        df_aggreg.set_index(region, inplace=True)
        df_aggreg = df_aggreg.reindex(df_geo[region_geo])

        df_geo[target] = df_aggreg.values

        return df_geo

    def plot_geo(
        self,
        df: gpd.GeoDataFrame,
        target: str,
        region_geo: str,
        confronto: str = None,
        express: str = None,
        title: str = "",
    ) -> plotly.graph_objs._figure.Figure:
        
        """Territorial plot of aggregated data for region

        Parameters
        ----------
        df : gpd.GeoDataFrame
            dataframe with gegographical info join with result of conteggi function
        target : str
            name of target column
        region_geo : str
            name of column with geographical info
        confronto : str 
            name of column with comparision value with target column (for example number of population),by default None
        express : str 
            expression that describe relationship between confronto column and target column
        title : str 
            title for the plot

        Results
        -------
        plotly.graph_objs._figure.Figure
            geographical plot
        """

        def generateColorScale(colors, naColor):
            colorArray = []
            colorArray.append([0, naColor])
            for grenze, color in zip(np.linspace(0.03, 1, len(colors)), colors):
                colorArray.append([grenze, color])
            return colorArray

        df = df.set_index(region_geo)
        df = df.fillna(0)

        target_name = target
        confronto_name = confronto

        if confronto:
            target = df[target_name]
            confronto = df[confronto_name]
            df[target_name] = eval(express).values

        fig = px.choropleth(
            df,
            geojson=df["geometry"],
            locations=df.index,
            color=target_name,
            projection="mercator",
            title=title,
            width=700,
            height=700,
            color_continuous_scale=generateColorScale(
                colors=["blue", "red"], naColor="grey"
            ),
        )
        fig.update_geos(fitbounds="locations", visible=False)

        return fig
