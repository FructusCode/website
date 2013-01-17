import pprint
import pythemoviedb.api.methods
from website.apwan.helpers.entitygen import search_strip, EntityGenerator
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

__author__ = 'Dean Gardiner'


class MovieEntityGenerator(EntityGenerator):
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

        e_movie_ref, e_movie, e_movie_created = EntityGenerator.create_entity(
            l_movie['id'],
            EntityReference.TYPE_THEMOVIEDB, Entity.TYPE_MOVIE,
            title=l_movie['title']
        )
        if e_movie_created:
            print "Movie Created"

            for company in l_movie['production_companies']:
                e_company_ref, e_company, e_company_created = MovieEntityGenerator.create_recipient(
                    company['id'], company['name'],
                    RecipientReference.TYPE_THEMOVIEDB,
                    Recipient.TYPE_MOVIE_PRODUCTION_COMPANY
                )
                e_movie.recipient.add(e_company)

        return e_movie