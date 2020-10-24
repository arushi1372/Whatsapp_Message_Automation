# Whatsapp_Message_Automation

Developed to support [Aveti Learning](https://www.avetilearning.com/#/home) operations for online education during and after COVID-19.

*** work in progress ***

Once you have downloaded the files, run whatsapp.py from the terminal by using the command `python3 whatsapp.py`.

This program takes in a csv file as a command-line argument. The csv file should store four columns, `groups`, `messages`, `images`, and `attachments`. The groups column contains the name of the group and the messages column contains the name of the txt file that contains the message. The txt files should be in a folder called `Messages`. If no such txt file is present, the program will send the message in `default.txt`. There do not need to be filenames in the images and attachments columns, but the option exists and the columns themselves should exist. If you do include images and attachments, add the specific materials to folders called `Images` and `Files` respectively. The program is able to identify the search bar, and search for the contact. It is currently unable to identify contacts that contain emojis in the names. 

In addition, you need to scan the QR code the first time around, but once you do that, the corresponding cookies are stored, preventing the need to scan a QR code every time. 

Errors are outputted to error_logs.txt and unavailable groups that messages were not sent to are located in group_errors.txt.

Scheduler is finicky and is being improved upon.

# To Download the Chromedriver Executable
Download the corresponding chromedriver executable for your machine from this link: https://chromedriver.chromium.org/downloads. Make sure you get the same version as is specified for your current Google Chrome version!
Move it to the folder containing the code. All set.
