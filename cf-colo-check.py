#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
import os


def subprocess_open(command):
        popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdoutdata, stderrdata) = popen.communicate()
        return stdoutdata, stderrdata


call_colo_status_prev = 'curl http://your-domain/cdn-cgi/trace | grep "colo" | cut -d= -f2 > colo_status_prev'
call_colo_status_now = 'curl http://your-domain/cdn-cgi/trace | grep "colo" | cut -d= -f2 > colo_status_now'


def prev():
    print subprocess_open(call_colo_status_prev)


def now():
    print subprocess_open(call_colo_status_now)


if __name__ == "__main__":
    now()



# The contents of the colo_status_prev file are compared with the contents of the colo_status_now file, 
# and a message indicating that the colo has been changed is sent to the telegram, 
# and the current colo state is recorded in the colo_status_prev file
with open('colo_status_prev') as f1, open('colo_status_now') as f2:
        for line1, line2 in zip(f1, f2):
                if line1 == line2:
                        print 'Currently the state of colo is not changed {}'.format(line2)
                else:
                        message = "Cloudflare colo has been changed to {}".format(line2)
                        subprocess.Popen('curl -g -s -X GET "http://your-telegram-api:8080/telegram/sendMessage.php?target=your-chat-group&message={}" > /dev/null '.format(message), shell=True)
                        prev()
# Colo_status_prev Writes the current colo status to the colo_status_prev file if the file is empty.
if os.stat('colo_status_prev').st_size == 0:
        prev()

#The information below is optional.
#       message = 'Warning! colo previous status is empty'
#       subprocess.Popen('curl -g -s -X GET "http://your-telegram-api:8080/telegram/sendMessage.php?target=your-chat-group&message={}" > /dev/null '.format(message), shell=True)
else:
        print 'prev status is not empty'
