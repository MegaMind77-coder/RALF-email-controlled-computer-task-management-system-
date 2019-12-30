import time
import subprocess
import imapclient
import pyzmail


def magnet_list():
    Mailinstance = imapclient.IMAPClient(
        'this is your imap client id depends on the website on which you make your systems email-id'
        , ssl=True)
    Mailinstance.login(SYSTEM_EMAIL, SYSTEM_PASS)
    Mailinstance.select_folder('INBOX')
    unique_ids = Mailinstance.search(['ALL'])  # unique_ids here is the python list unique email keys

    magnets = []  # this is your list that would contain all the magnet links sent ny you to your email bot
    if unique_ids:
        for identifier in unique_ids:
            raw_message = Mailinstance.fetch([identifier], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[identifier][b'BODY[]'])
            text = message.text_part.get_payload().decode(message.text_part.charset)

            if VERIFICATION_PASS in text:  # don't forget to add this to your text partmake a unique password so that people knowing your SYSTEM_EMAIL cannot take advantage
                html = message.html_part.get_payload().decode(message.html_part.charset)
                magnets.append(html)

        Mailinstance.delete_messages(unique_ids)
        Mailinstance.expunge()

    Mailinstance.logout()
    return magnets




TORRENT_CLIENT = 'usr/share/applications/qbittorent'  # guys,qbittorent needs to be installed
# go to terminal type 'sudo apt-get install qbittorrent'
SYSTEM_EMAIL = 'system@___mail.com'
SYSTEM_PASS = 'system password'
VERIFIED_EMAIL = 'your email id'  # This is a feature that does not work because of changes in the imapclient library
# contributors are most welcome to introduce the feature of verified email
VERIFICATION_PASS = 'verify-this!'

while True:
    magnet_links = magnet_list()
    for link in magnet_links:
        subprocess.Popen(TORRENT_CLIENT + ' ' + link)

    time.sleep(60 * 15)
