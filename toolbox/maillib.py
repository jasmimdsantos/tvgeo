# -*- coding: utf-8 -*-
#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText

FROMNAME = 'Fire Monitor'
USERNAME = 'firemonitor2015@gmail.com'
PASSWORD = 'wilci5w7'
TLS      = True
HOST     = 'smtp.gmail.com:587'




class Email:

    def __init__(self):

        self.server = smtplib.SMTP(HOST)
        if TLS:
            self.server.starttls()
        self.server.login(USERNAME,PASSWORD)


    def mask(self):
        return u"\
Olá,<br><br>\
\
{0}<br>\
<br><br>\
Esta é uma menssagem enviada automaticamene pelo sistema. <br>\
Esta mensagem foi envia em virtude de seu cadastro no sistema FireMonitor.\
<br>\
Respostas não serão consideradas, esta conta não é monitorada <br>\
<br>\
Atenciosamente, <br>\
Equipe Firemonitor <br>\
www.firemonitor.com.br <br>\
"


    def EnviaMSG(self, titulo, message, destinatarios, mask=None  ):

        if mask == None:
            message = self.mask().format(message)
        msg = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
        msg['Subject']  = titulo
        msg['From']     =  '{0} <{1}>'.format(FROMNAME, USERNAME)
        msg['To'] = ", ".join(destinatarios)

        self.server.sendmail(USERNAME, destinatarios, msg.as_string())

    def __del__(self):
        self.server.quit()
