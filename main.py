import xml.sax
import glob 
import os
import pandas as pd
from XMLtest import FileHandler
import xml.etree.ElementTree as ET

"""
file_parse_xml: This function utilizes our xml handler class
                These function calls are all found on setup for this
                library on https://docs.python.org/3/library/xml.sax.html
    Parameters: path, path to the file we are accessing
        return: Returns a dictionary containing the data for the processed
                file that is created using the class file we created and imported
"""
def file_parse_xml(path):
    handler = FileHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(path)
    return handler.dict
"""
create_csv: This function creates our CSV using pandas dataframe functionality
            which allows us to convert dictionaries into CSV files
Parameters: data, which contains our dictionaries filled with data
            csvName, This contains the name of the CSV file we want to create
"""
def create_csv(data, csvName):
    csv_filename = csvName
    
    if not os.path.exists(csv_filename):
        df = pd.DataFrame(data)
        df.to_csv(csv_filename, index=False)
    else:
        df = pd.DataFrame(data)
        df.to_csv(csv_filename, mode='a', index=False, header=False)
"""
effect_table_creation: This function uses xml.etree to help us extract the exact
                       sections of data we want from the xml document. The methods
                       used in the function bellow were found at 
                       https://docs.python.org/3/library/xml.etree.elementtree.html
           Parameters: path, path to the given file
"""
def effect_table_creation(path):
    tree = ET.parse(path)
    root = tree.getroot()
    effectDict = {'fxName':[], 'fxNameID':[], 'fxType':[], 'fxTypeID':[], 'fxSetting':[],
                  'fxSettingID':[], 'genre':[], 'paramName':[], 'paramID':[]}
    
    for fxinformation in root.findall('.//fxinformation'):
        fxgroupID = fxinformation.find('.//fxgroup/ID').text
        fxtypeID = fxinformation.find('.//fxtype/ID').text
        fxsettingID = fxinformation.find('.//fxsetting/ID').text
        fxgroup = fxinformation.find('.//fxgroup/name').text
        fxtype = fxinformation.find('.//fxtype/name').text
        fxsetting = fxinformation.find('.//fxsetting/name').text
        effectDict['fxName'].append(fxgroup)
        effectDict['fxNameID'].append(fxgroupID)
        effectDict['fxSetting'].append(fxsetting)
        effectDict['fxSettingID'].append(fxsettingID)
        effectDict['fxType'].append(fxtype)
        effectDict['fxTypeID'].append(fxtypeID)
        
        genre = ""
        match fxsettingID: 
            case "1":
                genre += ""
            case "2":
                genre += "Alternative "
            case "3":
                genre += "Heavy "
            case default:
                genre += ""
        match fxtypeID:
            case "31":
                genre += "90s Rock"
            case "32":
                genre += "Classic Rock"
            case "35":
                genre += "Indie"
            case "33":
                genre += "70s Rock"
            case "34":
                genre += "Southern Rock"
            case "22":
                genre += "Country"
            case "21":
                genre += "80s Pop"
            case "42":
                genre += " Rock"
            case "41":
                genre += "Metal"
            case "23":
                genre += "Physcodelic"
            case "12":
                genre += "Rock & Roll"
            case "11":
                genre += "Folk"
            case default:
                genre += ""
        
        param_info = fxinformation.find('.//paraminformation')
        if param_info is not None:
            paramNameList = []
            paramIDList = []
            for param in param_info.findall('.//parameter'):
                param_name = param.find('name').text
                param_value = param.find('value').text
                match param_value:
                    case "4x12":
                        genre += "/indie"
                paramNameList.append(param_name)
                paramIDList.append(param_value)
            effectDict['paramName'].append(paramNameList)
            effectDict['paramID'].append(paramIDList)
            
        effectDict['genre'].append(genre)
            
    create_csv(effectDict, "effectData.csv")
"""
effect_xml_files: Main function is to produce a list of the first 3 files in each
                  Genre folder, this is done because the first 3 files contain all
                  the data needed for all sub effects of each main effect
      Parameters: root, root directory for our filesystem
          return: We return a list of lists each index contains a list of the first
                  3 file paths for each effect
""" 
def effect_xml_file(root):
    fnameList = []
    
    for effectDir in os.listdir(root):
        subDir = os.path.join(root, effectDir)
        # The [:3] asks for the first 3 files for each parent directory
        fnames = glob.glob(f"{subDir}/*.xml")[:3]
        fnameList.extend(fnames)
        
    return fnameList
        
def main():
    root = "dataset/monophonic/Lists"
    fnames = glob.glob(f"{root}/*/*.xml")
    path = ""
    
    # Collect the data for all the files in IDMT-SMT dataset
    for file in fnames:
        path = file
        fileData = file_parse_xml(path)
        create_csv(fileData, "fileData.csv") 
        
    fnameList = effect_xml_file(root)
    
    # Collect the data for all the effects in IDMT-SMT dataset
    for filePath in fnameList:
        effect_table_creation(filePath)
        
if __name__ == "__main__":
    main()