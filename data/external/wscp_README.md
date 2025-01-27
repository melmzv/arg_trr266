## This file contains information on the raw data files from Worldscope.
The two data files “wscp_static.txt” and “wscp_panel.xlsx” contain financial data from Worldscope, used for analyzing residual income.

wscp_static.txt
 - This file contains static data about firms.
 - Format: Tab-separated values (txt).
 - The columns contain various firm-specific information, including isin (International Securities Identification Number), firm name, and country.

wscp_panel.xlsx
 - This file contains panel data for the same firms over multiple years.
 - Format: Excel (xlsx).
 - The columns contain financial metrics of firms over time, including year_, mve (Market Value of Equity), bve (Book Value of Equity), and ninc (Net Income).

Notes:
 - Ensure column names are normalized (lowercase, no spaces) for consistency (implemented in Python script in `code/python`).
 - The isin column is used to merge static and panel data.
 - Handle missing or infinite values appropriately in calculations (implemented in Python script in `code/python`).

These files are placed in the `data/external` directory and are essential for running the analysis script in this repository.