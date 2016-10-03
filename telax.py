import os, pysftp, time, logging

telaxServer = FTPSERVER
telaxUser = USERNAME
telaxPwd = PASSWORD
localdir = LOCALHOST_DIR
kh = PATHTOKNOWNHOSTSFILE # pysftp does not auto add known hosts I to sftp in from a server (linux) then copy my known host to a new file specified here
logDir = DIR_TO_STORE_LOGS
curTimeDate = time.strftime("%Y-%m-%d_%H.%M.%S") # used to generate logname

# setup logging - save log to the specifed log dir with the name of the current time and a .txt extension, also only store info messages and above
logging.basicConfig(filename=logDir + curTimeDate + '.txt', level=logging.INFO)

# setup stfp connection
try:
    cnopts = pysftp.CnOpts(knownhosts=kh)
    cnopts.hostkeys=None
    sftp = pysftp.Connection(telaxServer, username=telaxUser, password=telaxPwd, cnopts=cnopts)
except Exception, e:
    logging.error(str(e))

# store list of files on ftp to a list variable so you can check if the file already exist locally or not
# this way you are not copying a file that already exist on local storage
remoteDir = sftp.listdir()

# check if each file is already downloaded and downlaod if it isnt
try:
    for file in remoteDir:
        # if the file already exists locally skip it
        if os.path.exists(localdir + file):
            print file + '- already exist... skipping'
            logging.info(file + '- already exist... skipping')
        else:
            # check if the file is a file or directory and downlaod it if it is a file
            if sftp.isfile(file):
                print 'Downloading - ' + file + '....'
                logging.info('Downloading - ' + file + '....')
                saveTo = localdir + file
                sftp.get(file, saveTo)
                print file + ' - has been completed...'
                logging.info(file + ' - has been completed...')
            else:
                # if the file is a directory downlaod the contents of that folder from ftp
                print 'Downloading - ' + file + '....'
                logging.info('Downloading - ' + file + '....')
                sftp.get_r(file, localdir)
                print file + ' - has been completed...'
                logging.info(file + ' - has been completed...')
    sftp.close()
    logging.info('SFTP connection closed - Downloads Completed at ' + time.strftime("%Y/%m/%d %H:%M:%S"))
except Exception, e:
    logging.error(str(e))
