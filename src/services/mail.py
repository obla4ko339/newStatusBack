import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# sender_email = "volodya.grab@yandex.ru"
# password = "akgwfljkznkdjshp"  
# # receiver_email = "volodya.grab@yandex.ru"
# receiver_email = "volodya.grab@gmail.com"

# message = MIMEMultipart()
# message['From'] = sender_email
# message['To'] = receiver_email 
# message['Subject'] = "Test"

# body = "Привет! Это письмо отправлено автоматически."

# message.attach(MIMEText(body, 'plain'))

# try:
#     server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
#     server.login(sender_email, password)
#     server.send_message(message)
#     server.quit()
#     print(f'Message success send')
# except Exception as error:
#     print(f'Error send message {error}')





class MailNewStatus:

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port 
        self.user = user
        self.password = password

    def send_message(self, to, subject, body):
        message = MIMEMultipart()
        message['From'] = self.user
        message['To'] = to 
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP_SSL(self.host, self.port)
            server.login(self.user, self.password)
            server.send_message(message)
            server.quit()
            print(f'Message success send')
        except Exception as error:
            print(f'Error send message {error}')


    

    


if __name__ == "__main__":
    mailer = MailService("smtp.yandex.ru", 465, "volodya.grab@yandex.ru", "akgwfljkznkdjshp")
    mailer.send_message("test@example.com", "Тест ООП", "Привет! Это отправка через класс.")
