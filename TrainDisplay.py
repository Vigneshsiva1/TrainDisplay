import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
import time
import traindata
import datetime

# Pin information and board size
pixel_pin = board.D18
pixel_number = 192


if __name__ == '__main__':
    ## Initialize Pixels
    pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_number,
    brightness=0.1,
    auto_write=False,
    )
    # Initialize FrameBuffer
    pixel_framebuf = PixelFramebuffer(
    pixels,
    24,
    8,
    orientation=0,
    rotation = 0
    )
    train_data = traindata.get_schedule()
    # Initialize counters and keys
    i = 0
    j = 0
    line = 'B'
    curr_min = -1
    while True:
        # Initialize string for messages



        curr_timeStruct = time.localtime()
        curr_hour = curr_timeStruct.tm_hour

        
        # Sleep from 11pm  - 5am
        if(curr_hour > 23 or curr_hour < 5):
            pixel_framebuf.fill(0x000000)
            pixel_framebuf.display()
            print('Asleep')
            time.sleep(60)
            
        else:
            # Get TrainData Every minute and update message every minute
            if curr_min != curr_timeStruct.tm_min:
                BrwnLoopMessage = "   Loop "
                BrwnKimballMessage = "   Kimball "
                PurpLoopMessage = "   Loop "
                PurpKimballMessage = "   Kimball "
                try:
                    train_data = traindata.get_schedule()
                    print('Api Call ')
                    #update Train messages
                    for train in train_data:
                        if((train['Destination']=='Loop')&(int(train['ETA'])>5)& (train['Line']=='Brn')):
                            BrwnLoopMessage += (str(train['ETA'] )+ "m ")
                        if((train['Destination']=='Kimball')&(int(train['ETA'])>5)& (train['Line']=='Brn')):
                        
                            BrwnKimballMessage += (str(train['ETA'] )+ "m ")
                        if((train['Destination']=='Kimball')&(int(train['ETA'])>5)& (train['Line']=='P')):
                            
                            PurpKimballMessage += (str(train['ETA'] )+ "m ")
                        if((train['Destination']=='Loop')&(int(train['ETA'])>5)& (train['Line']=='P')):
                            
                            PurpLoopMessage += (str(train['ETA'] )+ "m ")
                    curr_min = curr_timeStruct.tm_min
                    today = datetime.datetime.today()
                except:
                    print("Issue with Api Call")
                    BrwnLoopMessage = 'Refreshing '
                    PurpLoopMessage = 'Refreshing '
                    BrwnKimballMessage = 'Refreshing '
                    PurpKimballMessage = 'Refreshing '
                BrwnLoopMessage += "    " 
                PurpLoopMessage += "    "
                BrwnKimballMessage +="    "
                PurpKimballMessage +="    "

                
            # Display only loop trains during work hours
            if (curr_hour > 5) & (curr_hour<16)& ~(today.weekday() == 5 or today.weekday() == 6):
                
                finalBrwnMessage = BrwnLoopMessage
                finalPurpMessage = PurpLoopMessage
                # check if purple line message is blank
                if ('   L     '== finalPurpMessage):
                    pixel_framebuf.fill(0x000000)
                    printMessage = finalBrwnMessage[i: i+4]
                    pixel_framebuf.text(printMessage, 0, 0, 0xff2300)
                    pixel_framebuf.display()
                    time.sleep(0.23)
                    if i < len(finalBrwnMessage)-4:
                        i = i+1
                    else:
                        i = 0 
                # if purple line exists, Switch between the two               
                else:
                    if(line == 'B'):
                        pixel_framebuf.fill(0x000000)
                        printMessage = finalBrwnMessage[i: i+4]
                        pixel_framebuf.text(printMessage, 0, 0, 0xff2300)
                        pixel_framebuf.display()
                        time.sleep(0.23)
                        if i < len(finalBrwnMessage)-4:
                            i = i+1
                        else:
                            i = 0 
                        if (printMessage == "    " ):   
                            line = 'P'    
                                      
                    else:
                        pixel_framebuf.fill(0x000000)
                        printMessage = finalPurpMessage[j: j+4]
                        pixel_framebuf.text(printMessage, 0, 0, 0x800080)
                        pixel_framebuf.display()
                        time.sleep(0.23)
                        if j < len(finalPurpMessage)-4:
                            j = j+1
                        else:
                            j = 0  
                        if (printMessage == "    " ):   
                            line = 'B'     
                                          

            # if out side of work hours display kimball trains too
            else:
                #remove trailing spaces from loop train message
                BrwnLoopMessage = BrwnLoopMessage[:-5]
                PurpLoopMessage = PurpLoopMessage[:-5]
                finalBrwnMessage = BrwnLoopMessage +BrwnKimballMessage
                finalPurpMessage = PurpLoopMessage + PurpKimballMessage
                # check for no purple line trains
                if ('   L   K     '  == finalPurpMessage):
                    pixel_framebuf.fill(0x000000)
                    printMessage = finalBrwnMessage[i: i+4]
                    pixel_framebuf.text(printMessage, 0, 0, 0xff2300)
                    pixel_framebuf.display()
                    time.sleep(0.23)                
                    
                    if i < len(finalBrwnMessage)-4:
                        i = i+1
                    else:
                        i = 0
                   
                # if Purple line trains exist, switch between the two    
                else:
                    if(line == 'B'):
                        pixel_framebuf.fill(0x000000)
                        printMessage = finalBrwnMessage[i: i+4]
                        pixel_framebuf.text(printMessage, 0, 0, 0xff2300)
                        pixel_framebuf.display()
                        time.sleep(0.23)
                        if i < len(finalBrwnMessage)-4:
                            i = i+1
                        else:
                            i = 0  
                        if (printMessage == "    " ):   
                            line = 'P' 
                           
                      
                    else:
                        pixel_framebuf.fill(0x000000)
                        printMessage = finalPurpMessage[j: j+4]
                        pixel_framebuf.text(printMessage, 0, 0, 0x800080)
                        pixel_framebuf.display()
                        time.sleep(0.23)
                        if j < len(finalPurpMessage)-4:
                            j = j+1
                        else:
                            j = 0 
                        if (printMessage == "    " ):   
                            line = 'B'  
                                    
                    
            
            


