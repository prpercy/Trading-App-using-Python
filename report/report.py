# libraries required: Panel, Pandas, hvplot, yfinance

# dfs required: prices_df, ratios_df, cumulative_returns_df
# lists required: 'tickers' including all ticker names 

#bring in dfs from portfolio.py

results_dict.get('Ratios')
results_dict.get('Prices')
results_dict.get('Cumulative Returns')
results_dict.get('MonteCarlo')
results_dict.get('Tickers')

#function for interactive ratios bar chart

def ratiosplot_df(ratio_wd):
    df = pd.DataFrame(ratios_df[ratio_wd])
    return df

# function to prepare visualzation of stock analysis report

def prepare_stock_report(results_dict):
    
    #create widgets

    tickers_wd = pn.widgets.Select(options= [tickers[:]], name='Ticker')
    df_widget = pn.widgets.DataFrame(ratios_df, name='Key Ratios')
    ratio_wd = pn.widgets.Select(options= list(ratios_df.columns), name='Ratio')

    #side bar data pull based on user option from ticker selection widget
    company_name = yf.Ticker(tickers_wd.value).info['longName']
    companydesc = yf.Ticker(tickers_wd.value).info['longBusinessSummary']
    companywebsite = yf.Ticker(tickers_wd.value).info['website']
    logourl = yf.Ticker(tickers_wd.value).info['logo_url']
    
    #prepare plots
    
    prices_plot = prices_df.drop(columns = "SPY").hvplot.line(
        title = "Historical Prices - 5 years",
        ylabel = "Stock Price"
        )
    
    cum_returns_plot = cumulative_returns_df.hvplot(
        title = "Historical Cummulative Returns - 5 years",
        ylabel = "Return %"
        )
    
    ratios_bar = hvplot.bind(ratiosplot_df, ratio_wd).interactive(width=600).hvplot.bar(
        title = "Key Ratios",
        xlabel = "Ticker"
        )
    
    #prepare montecarlo plots
    MC_line_plot = portfolio_2y_sim.plot_simulation()
    MC_hist = portfolio_2y_sim.plot_distribution()
    
    #prepare report
    template = pn.template.FastListTemplate(
        title = company_name + ' - Stock Analysis',
        sidebar = [
            tickers_wd.servable(area="sidebar"), #HAVING ISSUES TRYING TO USE TICKERS WIDGET TO AUTOMATICALLY UPDATE COMPANY NAME, DESC, AND WEBSITE WHEN USED.
            pn.pane.Markdown("# " + company_name),
            pn.pane.Markdown(companydesc)],
            # pn.bind(tickers,company_name,companydesc,companywebsite)],             HAVING ISSUES TRYING TO USE TICKERS WIDGET TO AUTOMATICALLY UPDATE COMPANY NAME, DESC, AND WEBSITE WHEN USED.
        sidebar_footer = companywebsite,
        main=[
            # tickers_wd,
            pn.Row(pn.Column(prices_plot, margin=(0,25)), 
                     cum_returns_plot), 
            pn.Row(pn.Column(df_widget, margin=(0,25)), 
                     ratios_bar)
                   ],
        theme="dark",
        logo = logourl,
        )
    
    #show report
    template.servable();      
    template.show()
    
    return True

# function to prepare visualzation of portfolio analysis report

def prepare_portfolio_report(results_dict):
    
    #create widgets

    tickers_wd = pn.widgets.Select(options= [tickers[:]], name='Ticker')
    df_widget = pn.widgets.DataFrame(ratios_df, name='Key Ratios')
    ratio_wd = pn.widgets.Select(options= list(ratios_df.columns), name='Ratio')

    #side bar data pull based on user option from ticker selection widget
    company_name = yf.Ticker(tickers_wd.value).info['longName']
    companydesc = yf.Ticker(tickers_wd.value).info['longBusinessSummary']
    companywebsite = yf.Ticker(tickers_wd.value).info['website']
    logourl = yf.Ticker(tickers_wd.value).info['logo_url']
    
    #prepare plots
    
    prices_plot = prices_df.drop(columns = "SPY").hvplot.line(
        title = "Historical Prices - 5 years",
        ylabel = "Stock Price"
        )
    
    cum_returns_plot = cumulative_returns_df.hvplot(
        title = "Historical Cummulative Returns - 5 years",
        ylabel = "Return %"
        )
    
    ratios_bar = hvplot.bind(ratiosplot_df, ratio_wd).interactive(width=600).hvplot.bar(
        title = "Key Ratios",
        xlabel = "Ticker"
        )
    
    #prepare montecarlo plots
    MC_line_plot = portfolio_2y_sim.plot_simulation()
    MC_hist = portfolio_2y_sim.plot_distribution()
    
    #prepare report
    template = pn.template.FastListTemplate(
        title = company_name + ' - Stock Analysis',
        sidebar = [
            tickers_wd.servable(area="sidebar"), #HAVING ISSUES TRYING TO USE TICKERS WIDGET TO AUTOMATICALLY UPDATE COMPANY NAME, DESC, AND WEBSITE WHEN USED.
            pn.pane.Markdown("# " + company_name),
            pn.pane.Markdown(companydesc)],
            # pn.bind(tickers,company_name,companydesc,companywebsite)],             HAVING ISSUES TRYING TO USE TICKERS WIDGET TO AUTOMATICALLY UPDATE COMPANY NAME, DESC, AND WEBSITE WHEN USED.
        sidebar_footer = companywebsite,
        main=[
            # tickers_wd,
            pn.Row(pn.Column(prices_plot, margin=(0,25)), 
                     cum_returns_plot), 
            pn.Row(pn.Column(df_widget, margin=(0,25)), 
                     ratios_bar)
            pn.Row(pn.Column(MC_line_plot, margin=(0,25)), 
                     MC_hist)
                   ],
        theme="dark",
        logo = logourl,
        )
    
    #show report
    template.servable();      
    template.show()
        
    return True