import ThingESP
import pin_control
from datetime import datetime

thing = ThingESP.Client('', '', '')


def handleResponse(query):
    if query == 'gate open':
        pin_control.open_gate()
        return "Gate Opened at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    elif query == 'gate close':
        pin_control.close_date()
        return "Gate Closed at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    else:
        return 'Invalid Command'
