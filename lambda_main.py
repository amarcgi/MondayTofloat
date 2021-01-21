from com.icrossing.mondaydotcom.MondayDotComDetails import MondayDotcom
def startMondayToFLoat(event,context):
    print('Starting application ............')
    mondayDotcom=MondayDotcom()
    mondayDotcom.fetchMondayDotComDetsils()
    mondayDotcom.createProjecFloatDotcom()

#startMondayToFLoat('','');





