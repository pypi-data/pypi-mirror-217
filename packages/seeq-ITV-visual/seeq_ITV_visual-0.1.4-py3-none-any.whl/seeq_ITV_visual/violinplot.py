import pandas as pd
import numpy as np
import markdown
from ipywidgets import Layout, widgets
from IPython.display import display, clear_output
from seeq import spy
import plotly.graph_objects as go
import matplotlib.pyplot as plt

class Violinplot(object):
    
    def __init__(self, url:str):
        '''
        Initializes the Violinplot object by opening the logo file, retrieving the analysis worksheet and signals, and building the GUI widgets
        
        Parameters:
        -----------
        url : str
            The url of the workbook that will be used for the analysis and fetch data from.
         
        '''
        try:
            logo_jpg_open = open("static/itvizion_logo_black.png", "rb")
            self.logo_jpg = logo_jpg_open.read()
            
            seeq_logo_jpg_open = open("static/seeq_logo.png", "rb")
            self.seeq_logo_jpg = seeq_logo_jpg_open.read()
        except:
            self.logo_jpg = None
            self.seeq_logo_jpg = None
        
        #Get worksheet and Signals
        self.workbook_id = spy.utils.get_workbook_id_from_url(url)
        self.worksheet = spy.utils.get_analysis_worksheet_from_url(url, quiet=True)
        _avail_signals = self.worksheet.display_items
        
        # Masking to extract only signals and not conditions
        signals_mask = _avail_signals['Type'].str.contains('Signal')
        self.avail_signals = _avail_signals[signals_mask]

        #Build widgets
        self.build_widgets()
        
    
    def fetch_data(self, signal_ID, start_date, end_date, grid):
        '''
        The function fetch_data fetches data for a given signal ID from the Seeq platform within a specified time window and grid.
        It also renames the column with the signal name and its unit of measure if it has one.
        
        Parameters:
        -----------
        self: object
            The object instance of the class.
        signal_ID : str
            The ID of the signal(s) to fetch data for.
        start_date : str
            The start date of the time window in ISO format (YYYY-MM-DD).
        end_date : str
            The end date of the time window in ISO format (YYYY-MM-DD).
        grid : str
            The grid to fetch data from.

        Returns:
        -----------
        pd.DataFrame: A DataFrame containing the fetched data for the given signal ID(s).
        '''
        #Search for signal
        search_results = spy.search({"ID": signal_ID}, quiet=True)

        # Sanity check and  extraction unit of measure
        if 'Value Unit Of Measure' in search_results:
            unit = search_results['Value Unit Of Measure'].values[0]
        else:
            unit = None
            
        # Masking again to extract only signals and not conditions, as if capsule exists in workbook,
        # extra columns regarding capsule are fetched despite signal selection
        mask = search_results['Type'].str.contains('Signal')
        search_results = search_results[mask]

        #Pull signal
        signal_df = spy.pull(search_results, start=start_date, end=end_date, grid=grid, 
                          #calculation='$signal.aggregate(average(), hours(), startKey())'
                          header='Name', quiet=True)
        signal_df = signal_df.dropna()
        
        if unit and unit != 'string':
            _col = signal_df.columns[0]
            signal_df.rename(columns={_col: f'{_col} ({str(unit)})'}, inplace=True)
        
        return signal_df
        
                
    def signal_pull(self, signal_ID, start_date, end_date, grid):
        '''
        Method to pull data for a given signal ID(s) within a specified date range and grid specification.

        Parameters:
        -----------
        signal_ID : list or str
            ID or list of IDs of the signal(s) to pull data for.
        start_date : str
            start date of the data range to pull (format: 'YYYY-MM-DD HH:MM:SS').
        end_date : str
            end date of the data range to pull (format: 'YYYY-MM-DD HH:MM:SS').
        grid : str
            the grid specification to use for data interpolation.

        Returns:
        -----------
        pd.DataFrame: a DataFrame containing the data for the specified signal(s) within the specified date range and grid specification.
        '''        
        if isinstance(signal_ID, list):
            for i, sid in enumerate(signal_ID):
                if i == 0:
                    signal_df = self.fetch_data(sid, start_date, end_date, grid)
                    signal_df = signal_df.tz_localize(tz=None)
                else:
                    _signal = self.fetch_data(sid, start_date, end_date, grid)
                    _signal.index = pd.to_datetime(_signal.index)
                    _signal = _signal.tz_localize(tz=None)
                    signal_df = pd.concat([signal_df, _signal], axis=1)
                    
        elif isinstance(signal_ID, str):
            signal_df = self.fetch_data(signal_ID, start_date, end_date, grid)
                
        return signal_df
    
    
    def is_string_series(self, s:pd.Series):
        '''
        This method checks if a pandas Series contains only string values, either because it was explicitly created
        as a string series or because all of its values are strings. This is useful for determining whether a Series can
        be used as a categorical variable when plotting data.

        Parameters:
        -----------
        self : object
            An instance of the class that defines this function.
        s : pd.Series
            The pandas Series to check.

        Returns:
        -----------
        bool: True if the Series contains only string values, False otherwise.
        '''
        if isinstance(s.dtype, pd.StringDtype):
            # The series was explicitly created as a string series (Pandas>=1.0.0)
            return True
        elif s.dtype == 'object':
            # Object series, check each value
            return all((v is None) or isinstance(v, str) for v in s)
        else:
            return False
        
    
    def dist_plots(self, signal_df):
        '''
        The method creates and displays a violin plot for each column in the input Pandas DataFrame signal_df. 
        Only the positive part of the plot and thus, mimics a distribution plot. The method generates and displays the violin plots using Plotly.

        Parameters:
        -----------
        signal_df: a Pandas DataFrame containing the signals data to be plotted.
        
        Returns:
        -----------
        None
        '''
        for col in signal_df.columns.tolist():
            fig = go.Figure()

#             fig.add_trace(go.Violin(x=signal_df[col].values, box_visible=True, line_color='black', orientation='h',
#                            meanline_visible=True, fillcolor='lightseagreen', opacity=0.4, name='', side='positive'))

            fig.add_trace(go.Histogram(x=signal_df[col].values))
            
            if not self.is_string_series(signal_df[col]):
                mu = np.mean(signal_df[col].values)
                fig.add_vline(x=mu, line_dash = 'dash', line_color = 'firebrick', annotation_text=f'Mean: {mu:0.5f}')
        
            fig.update_layout(title=col,# violingap=0, violinmode='overlay',
                             autosize=False,
                             width=800,
                             height=950,
                             bargap=0.1,
                             )
            
            fig.update_layout(
                            title_text=col, # title of plot
                            xaxis_title_text=col, # xaxis label
                            yaxis_title_text='Count', # yaxis label
                        )

            with self.output:
                fig.show()
                
        
    def on_plot(self):
        """
        Generate a violin plot of signals and an additional line plot of the signal data for the selected signals and time period.


        Function takes into account the different scales of the signals and thus, if requested, will normalize the data and plot them on the same figure.
        If the data are not normalize, separate violin plots are created for each signal.

        Parameters:
        -----------
        self : object
            An instance of the class that defines this function.

        Returns:
        -----------
        None

        Raises:
        -----------
        None
        """
        self.plot_button.disabled = True

        start_date = self.start.value 
        end_date = self.end.value 
        grid_spec = self.grid.value
        signal_selection = list(self.signal_selection.value)

        if self.select_all.value:
            signal_selection = self.worksheet.display_items['Name'].unique().tolist()
            signal_IDs = self.worksheet.display_items['ID'].unique().tolist()
        else:
            signal_selection = list(self.signal_selection.value)
            signal_IDs = self.worksheet.display_items[self.worksheet.display_items['Name'].isin(signal_selection)]['ID'].values.tolist()
        signal_df = self.signal_pull(signal_IDs, start_date, end_date, grid_spec)
        
        # Mask on dataframe columns that don't contain string values 
        _mask = [not self.is_string_series(signal_df[col]) for col in signal_df.columns.tolist()]
        nonstring_cols = list(signal_df.columns[_mask])
        
        original_df = signal_df.copy()
        
        # Sanity check on the number of numeric columns
        if not nonstring_cols:
             with self.output:
                _text = widgets.HTML(value = "<h1>Violin plot of normalized signals</h1>")
                display(_text)
                _text = widgets.HTML(value = "No numerical data selected.")
                display(_text)
        else:
            with self.output:
                _text = widgets.HTML(value = "<h1>Violin plot of normalized signals</h1>")
                display(_text)

            if self.normalize.value:
                signal_df = signal_df[nonstring_cols]
                signal_df = (signal_df-signal_df.mean())/signal_df.std()

                fig = go.Figure()
                for col in signal_df.columns.tolist():          
                    fig.add_trace(go.Violin(y=signal_df[col].values,
                                   opacity=0.75, x0=col, name=col))


                fig.update_traces(meanline_visible=True, box_visible=True)

                fig.update_layout(
                                yaxis_title_text='Value',
                                autosize=False,
                                width=950,
                                height=750,)


                # Display plot in output widget
                with self.output:
                    fig.show()

            else:
                for col in signal_df.columns.tolist():                
                    fig = go.Figure()

                    fig.add_trace(go.Violin(y=signal_df[col].values, box_visible=True, line_color='black',
                                   meanline_visible=True, fillcolor='lightseagreen', opacity=0.4, x0=col))

                    fig.update_layout(
                                autosize=False,
                                width=800,
                                height=700,)

                    fig.update_layout(
                            title_text=col, # title of plot
                            yaxis_title_text=col, # yaxis label
                        )

                    with self.output:
                        fig.show()
                    
        box_layout = widgets.Layout(display='flex',
                justify_content='center',
                align_items='center',
                width='50%')
                    
        if self.show_dist.value:
            _sep = markdown.markdown('***', extensions=['markdown.extensions.tables'])
            sep = widgets.VBox(children=[widgets.HTML(value = _sep, layout=self.layout),
                                         widgets.HTML(value = "<h1>Signals' Frequency distribution plots and median</h1>")])
            display(sep)
            self.dist_plots(original_df)
 
        self.plot_button.disabled = False

        # Create plot
        try:
            if not nonstring_cols:
                 with self.output:
                    _sep = markdown.markdown('***', extensions=['markdown.extensions.tables'])
                    sep = widgets.VBox(children=[widgets.HTML(value = _sep, layout=self.layout),
                                                 widgets.HTML(value = '<h1>Line plot of signals</h1>', layout=box_layout)])
                    display(sep)
                    _text = widgets.HTML(value = "No numerical data selected.")
                    display(_text)
            else:
                with self.output:
                    _sep = markdown.markdown('***', extensions=['markdown.extensions.tables'])
                    sep = widgets.VBox(children=[widgets.HTML(value = _sep, layout=self.layout),
                                                 widgets.HTML(value = '<h1>Line plot of signals</h1>', layout=box_layout)])
                    display(sep)
                    original_df.plot(subplots=~self.normalize.value, figsize=(14, 10),
                                        xlabel='Time', ylabel='Value')
                    plt.show()
              
        except:
            self.progress.value ='Error, unable to generate plot.  Confirm tag has valid data present in the specified time window'
        
        
    def build_widgets(self):
        """Builds the graphical user interface (GUI) widgets for the violin plot add-on.

        This function creates various GUI elements, such as titles, checkboxes, textboxes, date pickers, and buttons, 
        and arranges them into a visual form. It also defines the properties and styles for each widget.

        Parameters:
        -----------
        self : object
            An instance of the class that defines this function.

        Returns:
        --------
        None
        """
        style = {'description_width': '150px'}
        layout = {'width': '500px'} 
        self.layout = layout
        
        #Build GUI Elements (widgets)
        self.title = widgets.HTML(value = '<h1><br>Violin Plot Add-On</br></h1>')
        self.support_text = widgets.HTML(value = 'For support, please contact: <a href="mailto:support@itvizion.com">support@itvizion.com</a><br>')
        #text_display = widgets.VBox(children=[self.title, self.support_text]) 
        
        if self.logo_jpg is not None:
            self.logo = widgets.Image(value=self.logo_jpg, format='jpg',
                                     width = 290,
                                     style=style)
            
            if self.seeq_logo_jpg is not None:
                self.seeq_logo = widgets.Image(value=self.seeq_logo_jpg, format='jpg',
                                     width = 75)
                
                logos = widgets.HBox(children=[self.logo, self.seeq_logo],
                                    layout=Layout(width='100%', min_width='300px', height='auto', display='inline-flex', flex_flow='row wrap'))
            else:
                logos = self.logo
            
            _sep = markdown.markdown('***', extensions=['markdown.extensions.tables'])
            sep = widgets.HTML(value = _sep, layout=layout)
            
            box_layout = Layout(display='inline-flex',
                                flex_flow='row',
                                width='450px', height='auto')
            header = widgets.HBox(children=[logos, self.title], layout=box_layout)

            self.header = widgets.VBox(children=[header, sep])
        else:
            self.header = self.title
        
        #User Inputs
        self.signal_selection = widgets.SelectMultiple(
            options=self.avail_signals['Name'].unique(),
            description='Signals from Worksheet:',
            disabled=False,
            style=style,
            layout=layout
        )
        
        self.normalize = widgets.Checkbox(
            value=False,
            description='Normalize data',
            disabled=False,
            indent=True,
            style=style,
            layout=layout
        )
        
        self.select_all = widgets.Checkbox(
            value=False,
            description='Select all',
            disabled=False,
            indent=True,
            style=style,
            layout=layout
        )

        self.grid = widgets.Text(
            value = '10 minutes',
            description='Sampling Interval: ',
            disabled=False,
            style=style,
            layout=layout
        )
        
        self.start = widgets.DatePicker(
            description='Start: ',
            value = self.worksheet.display_range['Start'],
            disabled=False,
            style=style,
            layout=layout
        )
        self.end = widgets.DatePicker(
            description='End: ',
            value = self.worksheet.display_range['End'],
            disabled=False,
            style=style,
            layout=layout
        )
        
        self.show_dist = widgets.Checkbox(
            value=False,
            description='Plot distribution',
            disabled=False,
            indent=True,
            style=style,
            layout=layout
        )
              
        #Progress/Status widget to keep user informed of progress
        self.progress = widgets.HTML(value = None)

        
        #Buttons
        self.plot_button = widgets.Button(description="Plot the Data", 
                                    icon='fa-area-chart',
                                   tooltip = 'Clicking here will plot the signal',
                                    style=style,
                                    layout=layout,
                                    button_style='primary')
        self.plot_button.on_click(self.on_button_click)    
    
        
        #Output widget to show figures, etc
        self.output = widgets.Output()

        #Arrange GUI Elements
        self.dates = widgets.HBox(children=[self.start,self.end])
        
        self.form = widgets.VBox(children=[self.header,
                                            self.signal_selection,
                                            self.select_all,
                                            self.grid,
                                            self.start,
                                            self.end,
                                            self.normalize,
                                            self.show_dist,
                                            self.plot_button,
                                            self.support_text,
                                            self.progress,
                                            self.output])
        
        with open("static/spinner-v2.gif", "rb") as file:
            # read file as string into `image` 
            image = file.read()
            
        self.spinner = widgets.Image(
            value=image,
            format='gif',
            style=style,
            layout=layout,
        )
        
    def on_button_click(self, click):
        """Handles a button click event.

        This function clears the current output, displays a spinner widget and 
        adds a markdown separator, calls the `on_plot` function that will generate the requested plots, 
        and finally hides the spinner widget after the plots appear.

        Parameters:
        -----------
        self : object
            An instance of the class that defines this function.
        click : object
            The click event object.

        Returns:
        --------
        None
        """
        if not self.signal_selection.value and not self.select_all.value:
            with self.output:
                clear_output(wait=False)
                print('Please, select signals to plot.')
        else:
            with self.output:
                clear_output(wait=False)

                display(self.spinner)

                _sep = markdown.markdown('***', extensions=['markdown.extensions.tables'])
                display(widgets.HTML(value = _sep, layout=self.layout))

                self.plot_button.disabled = False
                self.on_plot()

                self.spinner.layout.visibility = 'hidden'
                self.spinner.layout.display = 'none'
        
    def run_form(self):
        display(self.form)