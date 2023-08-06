import time
from os.path import abspath, join, dirname

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from project_center.models import User, Company
from sqlalchemy import create_engine
from sqlalchemy import text


def full_path(filename):
    return abspath(join(dirname(__file__), filename))


class Command(BaseCommand):
    help = """Imports users without regard for activities from a legacy database."""

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', action='store', dest='limit', default=None,
            help="Import Limit"
        )
        parser.add_argument(
            '--order', action='store', dest='order', default=None,
            help="Import Order"
        )
        parser.add_argument(
            '--reset', action='store_true', dest='reset', default=False,
            help="Clear all projects before importing"
        )

        parser.add_argument(
            '--offset', action='store', dest='offset', default=None,
            help="Number of records to offset when beginning import sequence"
        )
    def import_legacy_users(self, engine, file):
        company, created = Company.objects.update_or_create(name=settings.PROJECT_CENTER_DEFAULT_COMPANY_NAME)
        usergroup, created = Group.objects.get_or_create(name=settings.PROJECT_CENTER_USER_GROUP_NAME)
        admin_usergroup, created = Group.objects.get_or_create(name=settings.PROJECT_CENTER_ADMINISTRATOR_GROUP_NAME)
        company_admin_usergroup, created = Group.objects.get_or_create(
            name=settings.PROJECT_CENTER_COMPANY_ADMINISTRATOR_GROUP_NAME
        )

        with engine.connect() as conn:
            with open(file) as file:
                query = text(file.read())
                result = conn.execute(query)
                for row in result:
                    user, created = User.objects.update_or_create(
                        username=row.email,
                    defaults={
                        'first_name':row.first_name,
                        'last_name': row.last_name,
                        'email': row.email,
                        'company':company,
                        'title': row.title,
                        'address_1': row.address_1
                    })
                    # if created or not user.companies:
                    #     user.companies.add(company)
                    #     user.save()
                    if row.enabled == 1:
                        user.is_staff = True
                    else:
                        user.is_staff = False
                    if row.email_notify == 1:
                        user.email_notify = True
                    else:
                        user.email_notify = False
                    if created or user.groups.filter(name=settings.PROJECT_CENTER_USER_GROUP_NAME).exists() is False:
                        user.set_password(row.password)
                        user.groups.add(usergroup)
                    user.save()

    def handle(self, *args, **options):
        engine = create_engine(settings.PROJECT_CENTER_IMPORT_DATABASE_URL)
        limit = options['limit']
        order = options['order']
        reset = options['reset']
        offset = options['offset']
        tic = time.perf_counter()
        print(f'Begin Import. Limit: {limit}. Offset: {offset}. Order: {order}. Reset: {reset}.'.format(
            limit=limit,
        offset=offset,
        order=order,
        reset=reset))

        self.import_legacy_users(engine, full_path('../../sql/list_users.sql'))
        toc = time.perf_counter()
        print(toc - tic)
        # if user:
        #     user.delete()

        # for x in (get_candidate_data_rest(candidate_id).keys()):
        #     print(x)