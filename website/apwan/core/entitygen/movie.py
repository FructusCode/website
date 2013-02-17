from __future__ import absolute_import

from django.conf import settings
import pythemoviedb.api.methods
from website.apwan.core.entitygen import EntityGenerator, registry
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

__author__ = 'Dean Gardiner'


class MovieEntityGenerator(EntityGenerator):
    class Meta:
        key = 'movie'
        recipient_types = [Recipient.TYPE_MOVIE_PRODUCTION_COMPANY]

    @staticmethod
    def entity_lookup(title, year, limit=1):
        result = pythemoviedb.api.methods.search_movie(title, year=year)
        results_len = len(result['results'])

        movies = []

        if results_len > 0:
            end_range = limit if limit < results_len else results_len
            for index in range(end_range):
                movies.append(pythemoviedb.api.methods.get_movie(
                    result['results'][index]['id']
                ))

        return movies

    @staticmethod
    def recipient_lookup(title, limit=1):
        result = pythemoviedb.api.methods.search_company(title)
        results_len = len(result['results'])

        companies = []

        if results_len > 0:
            end_range = limit if limit < results_len else results_len
            for index in range(end_range):
                companies.append(pythemoviedb.api.methods.get_company(
                    result['results'][index]['id']
                ))

        return companies

    @staticmethod
    def entity_create(title, year):
        # TODO: Support creating multiple movies
        l_movie = MovieEntityGenerator.entity_lookup(title, year)
        if len(l_movie) == 1:
            l_movie = l_movie[0]
        else:
            return None

        if 'release_date' not in l_movie:
            print "'release'_date not found"
            return None

        date = l_movie['release_date'].split('-')
        if len(date) != 3 or len(date[0]) != 4:
            print "'release_date' unexpected value"
            return None

        year = None
        try:
            year = int(date[0])
        except ValueError:
            print "'release_date' unexpected value"
            return None

        _, e_movie, e_movie_created = EntityGenerator.db_create_entity(
            l_movie['id'],
            EntityReference.TYPE_THEMOVIEDB, Entity.TYPE_MOVIE,
            title=l_movie['title'],
            year=year
        )
        if e_movie_created:
            print "Movie Created"

            for company in l_movie['production_companies']:
                e_company = MovieEntityGenerator._create_company_recipient(company)
                e_movie.recipient.add(e_company)

        return e_movie

    @staticmethod
    def recipient_create(title, limit=1):
        l_companies = MovieEntityGenerator.recipient_lookup(title, limit=limit)
        e_companies = []

        for company in l_companies:
            e_companies.append(MovieEntityGenerator._create_company_recipient(company))

        return e_companies

    @staticmethod
    def _create_company_recipient(company):
        (_, e_company, _) = \
            MovieEntityGenerator.db_create_recipient(
                company['id'], company['name'],
                RecipientReference.TYPE_THEMOVIEDB,
                Recipient.TYPE_MOVIE_PRODUCTION_COMPANY
            )
        return e_company

if settings.FRUCTUS_KEYS:
    registry.register(MovieEntityGenerator())
