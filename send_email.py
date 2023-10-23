from utils import collection_creation, fetch_records
import smtplib
from time import sleep
import pandas as pd

def send_email(from_address, to_address, subject, message, userid, password, smtpserver = 'smtp.gmail.com:587'):
    header = f'From: {from_address}'
    header += f"\r\nTo: {to_address}"
    header += f'\r\nSubject: {subject}\r\n'
    message = header + message
    print(header)
    try:
        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(userid, password)
        server.sendmail(from_address, to_address, message)
        server.quit()
        print(f'The email has been successfully sent to {to_address}\n\n')
    except Exception as e:
        print(f'An error occurred while sending email to {to_address}')
        print(e)


# Sender information
sender_userid = 'perfectpatterns2023@gmail.com'
sender_password = 'yflewqdzcipuxqul'
sender_address = 'perfectpatterns2023@gmail.com'
sender_subject = 'Doodle Job opportunity'

# Create dataframe after fetching candidates from database 
selected_candidates = collection_creation('Selected_Candidates')
candidates = [candidate for candidate in fetch_records(selected_candidates)]
df = pd.DataFrame(candidates)
df = df.set_index('_id')

interface_link = 'https://perfectpatterns2023.pythonanywhere.com/'
hiring_manager_doodle = 'Team Doodle'

# Send emails to selected candidates
for index, row in df.iterrows():
    name = str(row['display_name'].encode("utf-8")).split("\'")[1]
    message = (f'Hello {name},\n\nCongratulations!!!'
               'You have been selected for a coding round as part of the developer position interview process at Doodle.'
               'If interested,kindly complete our questionnaire by following the link below.'
               'You will be given 3 coding questions that you have to finish in 30 minutes.'
               'Once the time expires the form will be closed automatically.\n'
               'If you successfully complete all the 3 coding questions then you will be selected for the next round.\n\n'
               f'Link to the coding round: {interface_link}')
    message += (f'\n\nBest Regards,\n{hiring_manager_doodle}\n'
                'Doodle hiring manager')

    send_email(sender_address, row['email'], sender_subject, message, sender_userid, sender_password)

    # Add delay between sending emails to prevent triggering spam filters
    sleep(10)