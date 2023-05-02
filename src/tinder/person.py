import datetime


class Person:
    def __init__(self, data, api):
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
