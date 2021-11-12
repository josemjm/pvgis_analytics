# PVGIS Analytics

Collection of scripts to download and use PVGIS data

## What is PVGIS?
PVGIS is a web site that gives you information about solar radiation and PhotoVoltaic (PV) system performance. You can use PVGIS to calculate how much energy you can get from different kinds of PV systems at nearly any place in the world.

For more information, please to visit:

https://ec.europa.eu/jrc/en/PVGIS/docs/starting

## Tools

### Tracking PV systems

_This tool makes it possible to estimate the energy production from various types of sun-tracking PV systems connected to the electricity grid. The characteristic angles of the different sun tracking systems can be defined by the user or calculated by PVGIS in order to maximize the yearly energy production. As with the fixed-mounted PV system tool, the calculation takes into account the solar radiation, temperature, wind speed and type of PV module._ 

**tool_name:**   PVcalc


### Off-grid PV systems

_This part of PVGIS calculates the performance of PV systems that are not connected to the electricity grid but instead rely on battery storage to supply energy when the sun is not shining. The calculation uses information about the daily variation in electricity consumption for the system to simulate the flow of energy to the users and into and out of the battery. The calculations are made with the full temporal coverage of the solar radiation database chosen._

**tool_name:**   SHScalc


### Monthly radiation

_Here we calculate the monthly averages of solar radiation for the chosen location, showing in graphs or tables how the average solar irradiation varies over a multi-year period. The results are given for radiation on horizontal and/or inclined planes, as well as Direct Normal Irradiation (DNI)._

**tool_name:**   MRcalc


### Daily radiation

_In this section of PVGIS we show the average solar irradiation for each hour during the day for a chosen month, with the average taken over all days in that month during the multi-year time period for which we have data. In addition to calculating the average of the solar radiation, the daily radiation application also calculates the daily variation in the clear-sky radiation, both for fixed and for sun-tracking surfaces. The calculations are made by with the full temporal coverage of the radiation database chosen. The clear-sky estimations are only available for Europe and Africa._

**tool_name:**   DRcalc


### Hourly radiation

_In this tool you can get the full data set of solar radiation and other data needed to calculate PV power hour by hour for long time periods. PVGIS can also perform the hourly PV power calculation. The PV output values from the PVGIS interface "Hourly data" tool are calculated for a free-standing PV system. The hourly values of PV output from a building integrated system can be obtained using the Non-interactive service of the said "Hourly data" tool._

**tool_name:**   seriescalc


### TMY generator

_A typical meteorological year (TMY) is a set of meteorological data with data values for every hour in a year for a given geographical location. The data are selected from hourly data in a longer time period (normally 10 years or more). The TMY is generated in PVGIS following the procedure described in ISO 15927-4._

_The solar radiation database (DB) used is the default DB for the given location, either PVGIS-SARAH, PVGIS-NSRDB or PVGIS-ERA5. The other meteorological variables are obtained from the ERA-Interim reanalysis._

**tool_name:**   tmy


### Horizon profile

_The solar radiation and PV output will change if there are local hills or mountains that block the light of the sun during some periods of the day. PVGIS can calculate the effect of this using data about ground elevation with a resolution of 3 arc-seconds (around 90m). This calculation does not take into account shadows from very nearby things such as houses or trees. In this case you can upload your own horizon information._

**tool_name:**   printhorizon

