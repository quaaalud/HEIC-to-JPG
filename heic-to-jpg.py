# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 21:55:39 2022

@author: dludwinski
"""

import os, sys, getpass
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
user = getpass.getuser()

import PySimpleGUI as sg
from PIL import Image
from pillow_heif import register_heif_opener


def get_file_name(file_path:str):
    """
    RETURNS THE NAME OF A FILE FROM ANY GIVEN FILE PATH.
    
    Parameters
    ----------
    org_file : STRING
    
        FULL FILE PATH OF THE FILE YOU WISH TO CONVERT FROM .HEIC TO JPG.

    Returns
    -------
    STRING
        
        THE NAME OF THE FILE BEING CONVERTED.

    """
    return os.path.splitext(os.path.basename(file_path))[0]


def convert_heic_to_jpg(org_file:str, save_path=''):
    """
    CONVERTS ANY .HEIC IMAGE TO .JPG IMAGE.
    
    Parameters
    ----------
    org_file : STRING
    
        FULL FILE PATH OF THE FILE YOU WISH TO CONVERT FROM .HEIC TO JPG.
        
    save_path : STRING, optional
    
        NAME OF DIRECTORY TO SAVE THE CONVERTED FILE. The default is ''.
    
    Returns
    -------
    None.

    """
    if not save_path: save_path = f'C:/Users/{user}/Desktop'
    if str(org_file).endswith('.heic'):
        file_name = get_file_name(org_file)
        register_heif_opener()
        with Image.open(org_file) as image_1:
            image_1.format = 'jpg'
            image_1.save(f'{save_path}/{file_name}.jpg')    


def folder_heic_to_jpg(folder, save_path=''):
    """
    CONVERT ALL .HEIC FILES TO .JPG CONTAINED IN A GIVEN DIRECTORY.

    Parameters
    ----------
    folder : STRING
        
        PATH OF DIRECTORY CONTAINING .HEIC FILES TO BE CONVERTED TO .JPG.
        
    save_path : STRING, optional
        NAME OF DIRECTORY TO SAVE THE CONVERTED FILE. The default is ''.

    Returns
    -------
    None.

    """
    for file in os.listdir(folder):
        org_file = f'{folder}/{file}'
        convert_heic_to_jpg(org_file, save_path=save_path)
            

def main(): 
    """
    MAIN FUNCTION FOR .HEIC TO .JPG GUI APP
    
    """
    main_layout = [
        [sg.Text('CONVERT HEIC TO JPG', justification='center')],
        [sg.Text('Select a file to convert:',
                 size=(20, 1),
                 auto_size_text=False,
                 justification='center'),
         sg.InputText('', key='-FILE-'),
         sg.FileBrowse()
         ],
        [sg.Text('Select a save location:',
                 size=(20, 1),
                 auto_size_text=False,
                 justification='center'),
         sg.InputText('', key='-SAVE-'),
         sg.FolderBrowse()
         ],
        [[sg.Button('Convert File')], [sg.Button('Convert Folder')]],
        [sg.Button('Cancel')],
        ]
    
    window = sg.Window('CONVERT HEIC TO JPG APP', main_layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Convert Folder':
            gui_folder_popup()
        if event == 'Convert File':
            org_file = values['-FILE-']
            save = values['-SAVE-']
            try:
                convert_heic_to_jpg(org_file, save_path=save)
                sg.popup_auto_close(
                    '\nTHE FILE HAS BEEN CONVERTED TO .JPG\n'
                    )
            except os.error as e:
                sg.popup_auto_close(
                    f'\n{e}\n\n{os.error}\n'
                    )
            values['-SAVE-'] = ''
            values['-FOLDER-'] = ''
            window.refresh()
    window.close()

def gui_folder_popup():
    """
    GUI POP-UP FOR COMBINE FOLDER FUNCTION IN THE .HEIC TO .JPG APP
    
    """
    pop_up = [
        [sg.Text('\nCONVERT FOLDER TO JPG\n\n',
                 justification='center')
         ],
        [sg.Text('Select a folder:',
                 size=(20, 1),
                 auto_size_text=False,
                 justification='center'),
         sg.InputText('', key='-FOLDER-'),
         sg.FolderBrowse()
         ],
        [sg.Text('Select a save location:',
                 size=(20, 1),
                 auto_size_text=False,
                 justification='center'),
         sg.InputText('', key='-SAVE-'),
         sg.FolderBrowse()
         ],
        [sg.Button('Convert Folder')],
        [sg.Button('Back')],
        ]
    
    window1 = sg.Window('CONVERT HEIC TO JPG', pop_up,
                       resizable=True
                       )    
    
    while True:
        event, values = window1.read()
        if event == sg.WIN_CLOSED or event == 'Back':
            break
        if event == 'Convert Folder':
            folder = values['-FOLDER-']
            save = values['-SAVE-']
            if save == '': save = None
            try:
                folder_heic_to_jpg(folder, save_path=save)
                sg.popup_auto_close(
                    '\nTHE FILES HAVE BEEN CONVERTED TO .JPG\n'
                    )
            except os.error as e:
                sg.popup_auto_close(
                    f'\n{e}\n\n{os.error}\n'
                    )
            values['-SAVE-'] = ''
            values['-FOLDER-'] = ''
            window1.refresh()
    window1.close()


if __name__ == '__main__':
    main()
