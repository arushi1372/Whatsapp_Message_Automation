# Whatsapp_Message_Automation

Developed to support Aveti Learning operations for online education during and after COVID-19.

*** work in progress ***

Once you have downloaded the files, run whatsapp.py from the terminal by using the command `python3 whatsapp.py`.

This program takes in a csv file as a command-line argument. The csv file should store two columns, one named `groups` and the other named `messages`. The groups column contains the name of the group and the messages column contains the name of the txt file that contains the message. The txt files should be in a folder called `Messages`. If no such txt file is present, the program will send the message in `default.txt`. The program is able to identify the search bar, and search for the contact. It is currently unable to identify contacts that contain spaces or emojis. 

In addition, you need to scan the QR code the first time around, but once you do that, the corresponding cookies are stored, preventing the need to scan a QR code every time. 

Scheduler is finicky and is being improved upon.

Update with capability to send image files coming soon.

# To Download the Chromedriver Executable
Download the corresponding chromedriver executable for your machine from this link: https://chromedriver.storage.googleapis.com/index.html?path=83.0.4103.39/.
Move it to the folder containing the code. All set.
