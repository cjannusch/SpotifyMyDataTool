#!/usr/bin/env python
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('WebAgg')
import Main
import time
import inspect

"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.
Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
 
 Based on information from: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
 (Thank you Em-Bo & dirck)
"""

#Initial set up (replaces main() in Main.py as well as sets up PySimpleGui)
sg.theme('DarkGrey2')
sg.theme_button_color(('white','DarkOrange3'))
plt.style.use('seaborn')
data = Main.loadData()
sp = Main.createSpotifyAPIConnection()
#data = Main.subsetDataByDate(data,'2020-03-01','2020-05-01')


#print(plt.style.available)

#plt.figure(num=None, figsize=(12, 9), dpi=100, facecolor='w', edgecolor='k')

#data = Main.loadData()
#data = Main.subsetDataByDate(data,'2020-03-01','2020-05-01')
#fig = Main.countTimeOfDayListening(data)

#fig = Main.countArtistListens(data,10,True)

#fig = Main.countSongListens(data,10,True)

#time.sleep(1)

#fig.set_size_inches(11,11)
#plt.xticks([])


# ------------------------------- Beginning of Matplotlib helper code -----------------------

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# ------------------------------- Beginning of GUI CODE -------------------------------

# define the window layout

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')

figure_w, figure_h = 500,500

dictOfMethods = {'Count Artists Listens': Main.countArtistListens,
                 'Plot When I Listen To Music': Main.countTimeOfDayListening,
                 'Count Song Listens': Main.countSongListens,
                 'Count Most Consecutive Listens': Main.countMostConsecutiveListens,
                 'Get List Of playlists': Main.getAllUserPlaylists}

listbox_values = list(dictOfMethods)



col_listbox = [[sg.In(key='start1', enable_events=True, visible=False), sg.Text(' ' * 9),
                sg.CalendarButton('Pick Start Date',target = 'start1')], 
               [sg.In(key='end1', enable_events=True, visible=False),
                sg.Text(' ' * 9),sg.CalendarButton('Pick End Date',target = 'end1')],
               [sg.Text(' ' * 7),sg.Button('Submit Date Range')],
               [sg.Listbox(values=listbox_values, change_submits=True, size=(28, len(listbox_values)),key='-LISTBOX-')],
               [sg.Text(' ' * 14), sg.Exit(size=(5, 2))]]

col_multiline = sg.Col([[sg.MLine(size=(70, 35), key='-MULTILINE-')]])
col_canvas = sg.Col([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]])
col_instructions = sg.Col([[sg.Pane([col_canvas, col_multiline], size=(figure_w,figure_h))],
                           [sg.Text('Grab square above and slide upwards to view text output')]])

layout = [[sg.Text('Matplotlib Plot Test', font=('ANY 18'))],
          [sg.Col(col_listbox), col_instructions], ]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
                   layout, resizable=True, finalize=True)

canvas_elem = window['-CANVAS-']
#multiline_elem = window['-MULTILINE-']
figure_agg = None
startDate,endDate = Main.getTimePeriodOfData(data)
while True:
    event, values = window.read()
    print(event,values)
    if event in (sg.WIN_CLOSED, None, 'Exit'):
        plt.close('all')
        break
    if event == 'start1':
        startDate = window['start1']
        print(startDate)
    if event == 'end1':
        endDate = window['end1']
        print(startDate)
    if event == 'Submit Date Range':
        print(startDate,endDate)
    if figure_agg:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg)
    # get first listbox item chosen (returned as a list)
    #OTHER BUTTONS GO ABOVE THIS LINE YO
    #--------------------------------------------------------------------------
    if len(values['-LISTBOX-']) == 0:
        continue
    choice = values['-LISTBOX-'][0]
    print(choice)
    # get function to call from the dictionary
    func = dictOfMethods[choice]
    if func == Main.countArtistListens:
       fig = Main.countArtistListens(data,10,True)
    if func == Main.countTimeOfDayListening:
       fig = Main.countTimeOfDayListening(data)
    if func == Main.countSongListens:
        fig = Main.countSongListens(data,10,True)
    if func == Main.countMostConsecutiveListens:
        fig = Main.countMostConsecutiveListens(data,1)
    if func == Main.getAllUserPlaylists:
        plt.plot([69])
        fig = plt.gcf()
    # show source code to function in multiline
    #window['-MULTILINE-'].update(inspect.getsource(func))
    #fig = func
    #time.sleep(1)                                   # call function to get the figure
    figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)  # draw the figure
    fig = None
    
    
    
window.close()
'''

layout = [  [sg.Text('Chose Method:'),],
            [sg.Canvas(key='-GRAPH-')],
            [sg.Button('Ok')],
            [sg.CalendarButton('Pick Date')]    ]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='center', font='Helvetica 18')

#sg.theme('DarkTeal2')

# add the plot to the window
fig_canvas_agg = draw_figure(window['-GRAPH-'].TKCanvas, fig)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Ok', None):
        plt.close('all')
        break

window.close()
'''