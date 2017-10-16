import os
import os.path
import pwd
import shutil
import subprocess


MAVEN_URL = 'https://s3-us-west-2.amazonaws.com/rmay.pivotal.io.software/apache-maven-3.3.9-bin.tar.gz'
MAVEN_ARCHIVE_BASE_DIR = 'apache-maven-3.3.9'
MAVEN_NAME = 'Apache Maven 3.3.9'
OWNER = 'gfadmin'
LINK_NAME = 'maven'


def basename(url):
    i = url.rindex('/')
    return url[i+1:]

def runQuietly(*args):
    p = subprocess.Popen(list(args), stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = p.communicate()
    if p.returncode != 0:
        raise Exception('"{0}" failed with the following output: {1}'.format(' '.join(list(args)), output[0]))

if __name__ == '__main__':
    """
    This script expects the following environment variables
    GEMFIRE_USER
    """
    gemuser = os.environ['GEMFIRE_USER']
    parentDir = '/usr/local'
    archiveDir = MAVEN_ARCHIVE_BASE_DIR
    name = MAVEN_NAME
    archiveURL = MAVEN_URL

    archiveFile = basename(archiveURL)

    if os.path.exists(os.path.join( parentDir, archiveDir)):
        print '{0} is already installed - continuing'.format(name)
    else:
        runQuietly('wget', '-P', '/tmp', archiveURL)
        runQuietly('tar', '-C', parentDir, '-xzf', '/tmp/' + archiveFile)
        runQuietly('chown', '-R', '{0}:{0}'.format(gemuser), os.path.join(parentDir,archiveDir))

        linkName = LINK_NAME
        runQuietly('ln', '-s', os.path.join(parentDir,archiveDir), os.path.join(parentDir, linkName))

        print 'installed {0}'.format( name)

    uid = None
    gid = None
    for user in pwd.getpwall():
     if user[0] == gemuser:
        uid = user[2]
        gid = user[3]
        break

    if uid is None or gid is None:
     sys.exit('could not find user: ' + gemuser)

    userDir = '/home/{0}'.format(gemuser)
    m2Dir = os.path.join(userDir,'.m2')
    if not os.path.exists(m2Dir):
      os.mkdir(m2Dir)
      os.chown(m2Dir,uid,gid)

    shutil.copy('settings.xml', m2Dir)

    os.chown(os.path.join(m2Dir,'settings.xml'), uid, gid)
    print 'configured maven settings for ' + gemuser
