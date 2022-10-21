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

import pandas as pd
import yfinance as yf
import numpy as np
import panel as pn
pn.extension()
import hvplot.pandas
import seaborn as sns
from bokeh.models import Button
import sys

    
# function to prepare visualzation of stock analysis report
def prepare_stock_report(results_dict):
    
    prepare_portfolio_report(results_dict)
    return

# function to prepare visualzation of portfolio analysis report
def prepare_portfolio_report(results_dict):
    
    # get data out of results dictionary for further visualisation
    tickers = results_dict.get('tickers')
    ratios_df = results_dict.get('Ratios')
    prices_df = results_dict.get('Prices')
    returns_df = results_dict.get('Returns')
    portfolio_2y_sim = results_dict.get('MonteCarlo')
    user_stock = results_dict.get('user_stock')
    user_stock_weight = results_dict.get('user_stock_weight')
    cumulative_returns_df = (1 + returns_df).cumprod()
    
    #create widgets

    tickers_wd = pn.widgets.Select(options= tickers[:], name='Ticker')
    df_widget = pn.widgets.DataFrame(ratios_df, name='Key Ratios')
    ratio_wd = pn.widgets.Select(options= list(ratios_df.columns), name='Ratio')

    
    #Define functions an interactive sidebar 
    def company_name(tickers_wd):
        name = pn.pane.Markdown("# " + yf.Ticker(tickers_wd).info['longName'])
        return name

    def company_desc(tickers_wd):
        try:
            desc = pn.pane.Markdown(yf.Ticker(tickers_wd).info['longBusinessSummary'])
        except Exception as ex:
            desc='Not available'
        return desc

    def company_website(tickers_wd):
        try:
            website = pn.pane.Markdown(yf.Ticker(tickers_wd).info['website'])
        except Exception as ex:
            website='Not available'
        return website
    
    #side bar data pull based on user option from ticker selection widget

    company_name_sidebar = pn.bind(company_name,tickers_wd)
    company_desc_sidebar = pn.bind(company_desc,tickers_wd)
    company_website_sidebar = pn.bind(company_website,tickers_wd)
    
    #prepare plots
    
    prices_plot = prices_df.drop(columns = "SPY").interactive().hvplot(
        title = "Historical Prices - 5 years",
        ylabel = "Stock Price"
    )
    
    cum_returns_plot = cumulative_returns_df.interactive().hvplot(
        title = "Historical Cummulative Returns - 5 years",
        ylabel = "Return %"
    )
    
    #function for interactive ratios bar chart

    def filter_by_val(ratio_wd):
        df = pd.DataFrame(ratios_df[ratio_wd])
        return df
    
    ratios_bar = hvplot.bind(filter_by_val, ratio_wd).interactive(width=600).hvplot(
        kind="bar",
        title = "Key Ratios",
        xlabel = "Ticker"
    )
    
    #prepare montecarlo plots
    MC_line_plot = portfolio_2y_sim.plot_simulation()
    MC_hist = portfolio_2y_sim.plot_distribution()
    tbl_2y_summary_stats = portfolio_2y_sim.summarize_cumulative_return()
    tbl_2y_summary_stats.rename("Stat Values", inplace=True)
    
    # Compute summary statistics from the simulated daily returns
    dic_2y_simulated_returns = {'mean' : list(portfolio_2y_sim.simulated_return.mean(axis=1)),
                            'median': list(portfolio_2y_sim.simulated_return.median(axis=1)),
                            'min' : list(portfolio_2y_sim.simulated_return.min(axis=1)),
                            'max' : list(portfolio_2y_sim.simulated_return.max(axis=1))
            }

    #Create a DataFrame with the summary statistics
    df_2y_simulated_returns = pd.DataFrame(dic_2y_simulated_returns)

    # Use the 'plot' function to create a chart of the simulated cumulative returns
    sim_plot = df_2y_simulated_returns.hvplot(title='2 year simulated cumulative returns')

    
    # prepare template tile and description depending on whether its a stock analysis or portfolio analysis
    template_title = 'XPlytics: Portfolio Analysis'
    desc = 'Following Monte-Carlo simulation is performed for the user portfolio with weights calculated according to number of shares s/he holds : '
   
    if len(user_stock) > 0:
        template_title = f'XPlytics: {user_stock} Stock Analysis'
        desc = f'Following Monte-Carlo simulation is performed for the hypothetical portfolio with {user_stock_weight*100}% weight for the stock {user_stock} and remaining {(1-user_stock_weight)*100}% weight for the existing portfolio of the user : '
    # Create dashboard using FastListTemplate from Panel Library
    
    desc_pane = pn.pane.Str(desc)
    
    # define call back function for the bokeh button
    def callback():
         sys.exit()

    # add a button widget and configure with the call back
    button = Button(label="Press Me to Exit App")
    button.on_click(callback)

    # prepare template for the visualization report
    template = pn.template.FastListTemplate(
        title = template_title,
        sidebar = [
            button,
            tickers_wd,
            company_name_sidebar,
            company_website_sidebar,
            company_desc_sidebar
        ],
        main=[
            pn.Row(pn.Column(prices_plot, margin=(0,25)), cum_returns_plot), 
            pn.Row(pn.Column(df_widget, margin=(0,25)), ratios_bar),
            pn.Row(desc_pane, sizing_mode='stretch_width'),
            pn.Row(pn.Column(MC_line_plot, margin=(0,25)),MC_hist),
            pn.Row(pn.Column(sim_plot, margin=(0,25)),tbl_2y_summary_stats)
        ],
        theme="dark"
    )
    
    
    #Show template
    template.show(open=True)
    
    return True


    
        