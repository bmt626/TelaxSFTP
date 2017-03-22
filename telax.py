import logging
import os
import time

import pysftp

from pyemail import sendemail

TELAXSERVER = FTPSERVER
TELAXUSER = USERNAME
TELAXPWD = PASSWORD
LOCALDIR = LOCALHOST_DIR
# pysftp does not auto add known hosts I to sftp in from a server (linux)
# then copy my known host to a new file specified here
KH = PATHTOKNOWNHOSTSFILE
LOGDIR = DIR_TO_STORE_LOGS
CURTIMEDATE = time.strftime("%Y-%m-%d_%H.%M.%S")  # used to generate logname
FTP_ERRORS_LIMIT = 3
ftperrors = 0

# setup logging - save log to the specifed log dir with the name of the
# current time and a .txt extension, also only store info messages and above
logging.basicConfig(filename=LOGDIR + CURTIMEDATE + '.txt', level=logging.INFO)


def connect_to_telaxftp(ftperrors):
    # setup stfp connection
    try:
        cnopts = pysftp.CnOpts(knownhosts=KH)
        cnopts.hostkeys = None
        sftp = pysftp.Connection(TELAXSERVER, username=TELAXUSER,
                                 password=TELAXPWD, cnopts=cnopts)
        return sftp
    except Exception, e:
        # log the failure add to error count and relaunch the download
        ftperrors += 1
        logging.error(str(e))
        sftpdownload(ftperrors)


def sftpdownload(ftperrors):
    # check to make sure the error limit has not been reached
    # if it has abort and send the log as an email.
    if ftperrors >= FTP_ERRORS_LIMIT:
        print('Error limit reached aborting!')
        logging.error('Error limit reached aborting!')
        sendemail(LOGDIR + CURTIMEDATE + '.txt', 'Error')
        exit()
    # call the connect function and store the result to call on
    sftp = connect_to_telaxftp(ftperrors)
    # save the list of files and directorys so you can work with them
    remotedir = sftp.listdir()
    try:
        for file in remotedir:
            # Make sure the currently selected file is an actual file
            # and not a directory then proceed to downlaod if TRUE.
            if sftp.isfile(file):
                # check if file is already downloaded locally
                if os.path.exists(LOCALDIR + file):
                    # get local file size and remote file size
                    lfsize = os.path.getsize(LOCALDIR + file)
                    rfsize = sftp.stat(file).st_size
                    # check if local size and remote match and skip
                    # the download and log the event if they do
                    if lfsize == rfsize:
                        print(file + ' already exist'
                              + ' and matches remote file size')
                        logging.info(file + ' already exist'
                                     + ' and matches remote file size')
                    # if local and remote sizes don't match delete local file
                    # and attempt to download the file again
                    if lfsize != rfsize:
                        print(file + ' has a size mismatch - '
                              + 'local size is ' + str(lfsize)
                              + ' and remote size is ' + str(rfsize))
                        logging.info(file + ' has a size mismatch - '
                                     + 'local size is ' + str(lfsize)
                                     + ' and remote size is ' + str(rfsize))
                        print('Removing corrupt file named ' + file)
                        logging.info('Removing corrupt file named ' + file)
                        os.remove(LOCALDIR + file)
                        print('Redownloading ' + file + ' from server')
                        logging.info('Redownloading ' + file + ' from server')
                        sftp.get(file, LOCALDIR + file)
                        print('Download of ' + file + ' completed')
                        logging.info('Download of ' + file + ' completed')
                else:
                    # file does not exist locally proceed to download
                    print('Downloading ' + file + ' from server')
                    logging.info('Downloading ' + file + ' from server')
                    sftp.get(file, LOCALDIR + file)
                    print('Download of ' + file + ' completed')
                    logging.info('Download of ' + file + ' completed')
        print('All downloads have been completed')
        logging.info('All downloads have been completed')
        # close the connection to the server
        sftp.close()
        logging.info('SFTP connection closed - Downloads Completed at '
                     + time.strftime("%Y/%m/%d %H:%M:%S"))
        # send email with the log file
        sendemail(LOGDIR + CURTIMEDATE + '.txt', 'Success')

    except Exception, e:
        logging.error(str(e))
        # update error count and reattempt the downloads
        ftperrors += 1
        sftpdownload(ftperrors)


def main():
    sftpdownload(ftperrors)


if __name__ == '__main__':
    main()
