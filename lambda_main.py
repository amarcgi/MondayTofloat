from com.icrossing.mondaydotcom.MondayDotComDetails import MondayDotcom
def startMondayToFLoat(event,context):
    print('Starting application ............')
    mondayDotcomObj=MondayDotcom()

    mondayDotComDetails = mondayDotcomObj.fetchMondayDotComDetsils()

    mondayDotcomObj.createProjecFloatDotcom()
    #print('******** Sync Monday DashBoard Item with Float project Tasks*********')
    mondayDotcomObj.updateMondayDotcomDetails(mondayDotComDetails)
    #print('******** Finished Sync Monday DashBoard Item with Float project Tasks*********')

#startMondayToFLoat('','');





