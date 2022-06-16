import PySimpleGUI as sg
from PS6000 import PS6000

def main_window():

    sg.theme('LightBlue3')   # Add a touch of color 
    
    # All the stuff inside your window.
    
    csv_1 = [[sg.Checkbox('CSV',key='csv_1',auto_size_text=True)],
            [sg.T('File Destination:'), sg.I(key='folder_dest_1',size=(40,1)),sg.FolderBrowse(key='dest_1')],
            [sg.T('File name:',size=(8,1)),sg.I(key='fname_1',size=(30,1))]   ]

    csv_2 = [[sg.Checkbox('CSV',key='csv_2',auto_size_text=True)],
            [sg.T('File Destination:'), sg.I(key='folder_dest_2',size=(40,1)),sg.FolderBrowse(key='dest_2')],
            [sg.T('File name:',size=(8,1)),sg.I(key='fname_2',size=(30,1))]   ]
    
    layout = [[sg.Text('Distance:'), sg.I(size=(20,1), key='distance_1')],
            [sg.Frame('Saving details', csv_1), sg.Output(size=(40,10))],
            [sg.B('Run'), sg.B("Exit")]]
                
    csv_extract = [[sg.T('File to Extract:'), sg.I(key='file_dests',size=(40,1)), sg.FileBrowse(key='file_dests')],
                [sg.Text('Distance:'), sg.I(size=(20,1), key='distance_2')],
                [sg.Frame('Saving details', csv_2), sg.Output(size=(40,10))],
                [sg.B('Generate Stiffness'), sg.B("Exit")]]

    tab_group = [[sg.TabGroup([[sg.Tab('PicoTech', layout, title_color='Red',border_width=10, element_justification= 'left'),
                    sg.Tab('Run CSV', csv_extract , title_color='Blue')]], tab_location='topleft',
                    title_color='Black', tab_background_color='LightGray',selected_title_color='White',
                    selected_background_color='DarkBlue', border_width=5)]]
                       
    # Create the Window
    return sg.Window('Stiffness Testing', tab_group, default_element_size =(80,30), finalize=True)

window = main_window()

try:
# Event Loop to process "events" and get the "values" of the inputs
    while True:
        
        event, values = window.read(timeout = 1000)

        if window == sg.WIN_CLOSED:
            break

        if event in (sg.WIN_CLOSED,'Exit'):
            window.close() # if user closes window or clicks cancel
            break

        #runs once and saves values in desired file destination
        if event == 'Run':
            if values['csv_1'] == True:
                test = PS6000()
                print("Stiffness" + str(test.get_swv2stiffness()))
                test.savecsv(values['fname'], values['folder_dest'])

        if event == 'Generate Stiffness':
            test = PS6000()
            if values['csv_2'] == True:
                # test.plotgraph2checkwave(values['file_dests'])
                # test.getswv(values['file_dests'], values['distance'])
                test.savecsv(values['fname_2'], values['folder_dest_2'], values['file_dests'], float(values['distance_2']))
                print("Saved as CSV.")
            else:
                test.swv2stiffness_csvextract(values['file_dests'], float(values['distance_2']))

    window.close()
except Exception as e:
    sg.popup_error_with_traceback(f'An error happened.  Here is the info:', e)