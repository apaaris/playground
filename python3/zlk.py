import sys
import os
from dialog import Dialog
import time
d = Dialog(dialog="dialog")
# Compile with nuitka
# Zoom links
classes = [("Dim II","97881759782","","https://video.ethz.ch/live/lectures/zentrum/hg/hg-g-3.html"),
           ("Elektro I","99096506791","",""),
           ("Fertigung","tbd","",""),
           ("Fluid I","94766840677","",""),
           ("Materials","93540395449","",""),
           ("Physics II","95954692103","",""),
           ("Thermo II","91874419806","","https://video.ethz.ch/live/lectures/zentrum/hg/hg-f-7.html")]
names = []
for i in range(len(classes)):
    if classes[i][3] == "":
        names.append((classes[i][0], "zoom"))
    else:
        names.append((classes[i][0], "video.ethz"))

# Options
code, tag = d.menu("Zoom class launcher,          git: apaaris", choices=names)
if code == d.ESC or code == d.CANCEL:
    d.msgbox("Exiting.")
else:
    for i in range(len(classes)):
        if classes[i][0] == tag:
            index = i
    if names[index][1] == "video.ethz":
        url = classes[index][3]
        command = "xdg-open " + url
        text = "Opening video.ethz for {}".format(tag)

    elif names[index][1] == "zoom":
        url = str(classes[index][1])
        password = ""
        if classes[index][2] != "":
            password = "&pwd=" + classes[index][2]
        command = "xdg-open 'zoommtg://zoom.us/join?action=join&confno=" + url + password + "'"
        text = "Starting zoom call for {}".format(tag)
    d.msgbox(text + ".", width=40, height=10)
    os.system(command)

    # Uscita, gia' pronta
    d.infobox("See you...", width=0, height=0, title="Have fun") 
    time.sleep(2)
os.system("kill -9 %d" %(os.getppid()))

