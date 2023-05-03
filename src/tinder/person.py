import datetime
from typing import Dict


class PlainPerson:
    def __init__(self, data: Dict, api):
        from .tinder_api import TinderAPI
        self._api: TinderAPI = api

        self.id = data['_id']
        self.name = data.get('name', 'Unknown')
        self.bio = data.get('bio', '')
        self.city = data.get('city', dict()).get('name', 'Unknown')
        self.relationship_intent = data.get('relationship_intent', dict()).get('body_text', '')
        selected_descriptors = data.get('selected_descriptors', list())
        self.selected_descriptors = list()
        for selected_descriptor in selected_descriptors:
            if selected_descriptor.get('prompt'):
                self.selected_descriptors.append(
                    f"{selected_descriptor.get('prompt')} {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}"
                )
            else:
                self.selected_descriptors.append(
                    f"{selected_descriptor.get('name')}: {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}"
                )

        self.distance_mile = data.get('distance_mi', -1)
        self.distance_km = round(self.distance_mile * 1.609344, 3) if self.distance_mile != -1 else -1

        self.birth_date = datetime.datetime.strptime(data['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            'birth_date', False) else 'Unknown'
        self.gender = ['Male', 'Female', 'Unknown'][data.get('gender', 2)]

        self.images = list(map(lambda photo: photo['url'], data.get('photos', list())))

        self.jobs = list(
            map(lambda job: {'title': job.get('title', dict()).get('name'),
                             'company': job.get('company', dict()).get('name')},
                data.get('jobs', list())))
        self.schools = list(map(lambda school: school['name'], data.get('schools', list())))

    def infos(self):
        return {
            'name': self.name,
            'bio': self.bio,
            'city': self.city,
            'relationship_intent': self.relationship_intent,
            'selected_descriptors': self.selected_descriptors,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'jobs': self.jobs,
            'schools': self.schools
        }

    def __repr__(self) -> str:
        if self.birth_date == 'Unknown':
            birth_date_str = self.birth_date
        else:
            birth_date_str = self.birth_date.strftime('%Y.%m.%d')
        s = f"Person: {self.id} - {self.name} ({self.city}, {int(round(self.distance_km))} km) ({birth_date_str})"

        return s


class Person(PlainPerson):
    GENDER_DICT = {
        0: 'Male',
        1: 'Female',
        -1: 'Unknown',
    }

    def __init__(self, data: Dict, api):
        """
        data is the "results" object from https://api.gotinder.com/user/

        :param data: Dict
        :param api:
        """
        from .tinder_api import TinderAPI
        assert isinstance(api, TinderAPI)
        self._api: TinderAPI = api

        self.id = data['_id']
        self.name = data.get('name', 'Unknown')
        self.bio = data.get('bio', '')
        self.city = data.get('city', dict()).get('name', 'Unknown')
        self.relationship_intent = data.get('relationship_intent', dict()).get('body_text', '')

        self.selected_descriptors = list()
        selected_descriptors = data.get('selected_descriptors', list())
        for selected_descriptor in selected_descriptors:
            if selected_descriptor.get('prompt'):
                self.selected_descriptors.append(
                    f"{selected_descriptor.get('prompt')} {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}"
                )
            else:
                self.selected_descriptors.append(
                    f"{selected_descriptor.get('name')}: {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}"
                )

        self.selected_interests = list()
        selected_interests = data.get('user_interests', dict()).get('selected_interests', list())
        for selected_interest in selected_interests:
            self.selected_interests.append(selected_interest.get('name'))

        self.spotify_top_artists = data.get('spotify_top_artists', list())
        self.spotify_theme_track = data.get('spotify_theme_track', dict())
        self.common_connections = data.get('common_connections', list())
        self.is_travelling = data.get('is_travelling', 'Unknown')
        self.teasers = data.get('teasers', list())
        self.common_likes = data.get('common_likes', list())
        self.common_interests = data.get('common_interests', list())

        self.distance_mile = data.get('distance_mi', -1)
        self.distance_km = round(self.distance_mile * 1.609344, 3) if self.distance_mile != -1 else -1

        self.gender = self.GENDER_DICT[data.get('gender', -1)]
        self.birth_date = datetime.datetime.strptime(data['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            'birth_date', False) else 'Unknown'

        self.images = list(map(lambda photo: photo['url'], data.get('photos', list())))

        self.jobs = list(
            map(
                lambda job: {
                    'title': job.get('title', dict()).get('name'),
                    'company': job.get('company', dict()).get('name')}, data.get('jobs', list())
            )
        )
        self.schools = list(map(lambda school: school['name'], data.get('schools', list())))

        sexual_orientations = data.get('sexual_orientations', list())
        self.sexual_orientations = [so.get('name') for so in sexual_orientations]

        self.badges = data.get('badges', list())
        self.selfie_verified = False
        for badges in self.badges:
            if badges.get('type', '') == 'selfie_verified':
                self.selfie_verified = True

        self.is_tinder_u = data.get('is_tinder_u', 'Unknown')

    def info(self) -> Dict:
        return {
            'name': self.name,
            'bio': self.bio,
            'city': self.city,
            'relationship_intent': self.relationship_intent,
            'selected_descriptors': self.selected_descriptors,
            'selected_interests': self.selected_interests,
            'spotify_top_artists': self.spotify_top_artists,
            'spotify_theme_track': self.spotify_theme_track,
            'common_connections': self.common_connections,
            'is_travelling': self.is_travelling,
            'teasers': self.teasers,
            'common_likes': self.common_likes,
            'common_interests': self.common_interests,
            'distance_mile': self.distance_mile,
            'distance_km': self.distance_km,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'images': self.images,
            'jobs': self.jobs,
            'schools': self.schools,
            'sexual_orientations': self.sexual_orientations,
            'badges': self.badges,
            'selfie_verified': self.selfie_verified,
            'is_tinder_u': self.is_tinder_u
        }
