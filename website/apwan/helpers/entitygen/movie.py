import pprint
import pythemoviedb.api.methods
from website.apwan.helpers.entitygen import search_strip
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

__author__ = 'Dean Gardiner'


class MovieEntityGenerator():
    @staticmethod
    def lookup(title, year):
        results = pythemoviedb.api.methods.search_movie(title, year=year)

        if len(results['results']) > 0:
            return pythemoviedb.api.methods.get_movie(results['results'][0]['id'])
        return None

    @staticmethod
    def create(title, year):
        l_movie = MovieEntityGenerator.lookup(title, year)
        if l_movie is None:
            return None

        e_movie_ref, e_movie, e_movie_created = MovieEntityGenerator.create_entity(l_movie)
        if e_movie_created:
            print "Movie Created"

            for company in l_movie['production_companies']:
                e_company_ref, e_company, e_company_created = MovieEntityGenerator.create_recipient(company)
                e_movie.recipient.add(e_company)

        return e_movie

    @staticmethod
    def create_entity(movie):
        print "create_entity"

        reference_filter = EntityReference.objects.filter(
            type=EntityReference.TYPE_THEMOVIEDB,
            key=movie['id']
        )
        reference_exists = len(reference_filter) == 1
        if reference_exists:
            print "reference exists", movie['id']
            return reference_filter[0], reference_filter[0].entity, False

        # Create Entity
        entity = Entity.objects.create(
            title=movie['title'],
            s_title=search_strip(movie['title']),
            type=Entity.TYPE_MOVIE
        )

        # Create Reference
        reference = EntityReference.objects.create(
            entity=entity,
            type=EntityReference.TYPE_THEMOVIEDB,
            key=movie['id']
        )

        return reference, entity, True

    @staticmethod
    def create_recipient(company):
        if 'id' not in company or 'name' not in company:
            return None, None, False
        # Search for id in recipient references
        reference_filter = RecipientReference.objects.filter(
            type=RecipientReference.TYPE_THEMOVIEDB,
            key=company['id']
        )
        reference_exists = len(reference_filter) == 1
        if reference_exists:
            return reference_filter[0], reference_filter[0].recipient, False

        # Create Recipient
        recipient = Recipient.objects.create(
            title=company['name'],
            type=Recipient.TYPE_MOVIE_PRODUCTION_COMPANY
        )

        # Create Reference
        reference = RecipientReference.objects.create(
            recipient=recipient,
            type=RecipientReference.TYPE_THEMOVIEDB,
            key=company['id']
        )

        return reference, recipient, True