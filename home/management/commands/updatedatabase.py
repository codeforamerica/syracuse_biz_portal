from django.core.management.base import BaseCommand, CommandError
from syracuse_bizport.settings.base import *
import subprocess
import sys


class Command(BaseCommand):
    help = ('Pulls the database from production so that you can keep your'
            'dev environment content up-to-date.')

    def handle(self, *args, **options):
        confirmation = input(
            ('WARNING: This will overwrite the contents of your dev'
                'database with production. Do you wish to continue? (Y/n)'))

        if confirmation == 'Y':
            self.stdout.write(
                '== Creating Backup of Heroku Production Database ==')
            subprocess.call((
                'heroku pg:backups:capture DATABASE_URL'
                '--app=syracuse-bizport'), shell=True)

            self.stdout.write(
                '== Downloading Backup of Heroku Production Database ==')
            subprocess.call(
                ('heroku pg:backups:download --app=syracuse-bizport'),
                shell=True)

            self.stdout.write(
                ('== Restoring Backup of Heroku Production Database'
                    ' Over Local Dev =='))
            subprocess.call(
                ('pg_restore --verbose --clean --no-acl --no-owner -h '
                    'localhost -d syracuse_biz_portal '
                    ' latest.dump'), shell=True)

            self.stdout.write('== Deleting Dump File ==')

            if sys.platform.startswith(('darwin', 'os')):
                subprocess.call('rm ' + BASE_DIR + '/latest.dump', shell=True)
            elif sys.platform.startswith(('win', 'cygwin')):
                subprocess.call('del ' + BASE_DIR + '/latest.dump', shell=True)

        else:
            self.stdout.write('Error! Local Database Dump Unsuccessful')
