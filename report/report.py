# libraries required: Panel, Pandas, hvplot, yfinance
        # Python implementation: CPython
        # Python version       : 3.7.13
        # IPython version      : 7.31.1
        # numpy   : 1.21.5
        # panel   : 0.13.0
        # pandas  : 1.3.5
        # hvplot  : 0.8.1
        # yfinance: 0.1.77
        # seaborn : 0.11.2

    # dfs required: prices_df, ratios_df, cumulative_returns_df
    # lists required: 'tickers' including all ticker names 

#bring in dfs from portfolio.py
"""
results_dict.get('Ratios')
results_dict.get('Prices')
results_dict.get('Cumulative Returns')
results_dict.get('MonteCarlo')
results_dict.get('Tickers')
"""

import pandas as pd
import yfinance as yf
import numpy as np
import panel as pn
pn.extension()
import hvplot.pandas
import seaborn as sns


# function to prepare visualzation of stock analysis report

def prepare_stock_report(results_dict):
    
    prepare_portfolio_report(results_dict)

    return True

# function to prepare visualzation of portfolio analysis report

def prepare_portfolio_report(results_dict):
    
    # get data out of results dictionary
    tickers = results_dict.get('tickers')
    ratios_df = results_dict.get('Ratios')
    prices_df = results_dict.get('Prices')
    returns_df = results_dict.get('Returns')
    portfolio_2y_sim = results_dict.get('MonteCarlo')
    cumulative_returns_df = (1 + returns_df).cumprod()
    
    #create widgets

    tickers_wd = pn.widgets.Select(options= [tickers[:]], name='Ticker')
    df_widget = pn.widgets.DataFrame(ratios_df, name='Key Ratios')
    ratio_wd = pn.widgets.Select(options= list(ratios_df.columns), name='Ratio')

    """
    #Define functions an interactive sidebar 
    def company_name(tickers_wd):
        name = pn.pane.Markdown("# " + yf.Ticker(tickers_wd).info['longName'])
        return name

    def company_desc(tickers_wd):
        desc = pn.pane.Markdown(yf.Ticker(tickers_wd).info['longBusinessSummary'])
        return desc

    def company_website(tickers_wd):
        website = pn.pane.Markdown(yf.Ticker(tickers_wd).info['website'])
        return website
    
    #side bar data pull based on user option from ticker selection widget

    company_name_sidebar = pn.bind(company_name,tickers_wd)
    company_desc_sidebar = pn.bind(company_desc,tickers_wd)
    company_website_sidebar = pn.bind(company_website,tickers_wd)
    """
    #prepare plots
    
    prices_plot = prices_df.drop(columns = "SPY").hvplot.line(
        title = "Historical Prices - 5 years",
        ylabel = "Stock Price"
    )
    
    cum_returns_plot = cumulative_returns_df.hvplot(
        title = "Historical Cummulative Returns - 5 years",
        ylabel = "Return %"
    )
    
    #function for interactive ratios bar chart

    def filter_by_val(ratio_wd):
        df = pd.DataFrame(ratios_df[ratio_wd])
        return df
    
    ratios_bar = hvplot.bind(filter_by_val, ratio_wd).interactive(width=600).hvplot.bar(
        title = "Key Ratios",
        xlabel = "Ticker"
    )
    
    #prepare montecarlo plots
    MC_line_plot = portfolio_2y_sim.plot_simulation()
    MC_hist = portfolio_2y_sim.plot_distribution()
    
    # Create dashboard using FastListTemplate from Panel Library

    template = pn.template.FastListTemplate(
        title = "Portfolio Analysis",
        #sidebar = [
        #    tickers_wd,
        #    company_name_sidebar,
        #    company_website_sidebar,
        #    company_desc_sidebar
        #],
        main=[
            pn.Row(pn.Column(prices_plot, margin=(0,25)), cum_returns_plot), 
            pn.Row(pn.Column(df_widget, margin=(0,25)), ratios_bar),
            pn.Row(pn.Column(MC_line_plot, margin=(0,25)),MC_hist)
        ],
        theme="dark"
    )

    #Show template
    template.servable();      
    template.show()

    return True
        