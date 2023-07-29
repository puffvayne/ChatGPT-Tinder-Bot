from .person import PlainPerson


class Profile(PlainPerson):
    def __init__(self, data, api):
        super().__init__(data['user'], api)
        self.email = data['account'].get('email')
        self.phone_number = data['account'].get('account_phone_number')

        self.age_min = data['user']['age_filter_min']
        self.age_max = data['user']['age_filter_max']
        user_interests = data['user'].get('user_interests', dict()).get('selected_interests', list())
        self.user_interests = list()
        for user_interest in user_interests:
            self.user_interests.append(user_interest.get('name'))

        self.max_distance = data['user']['distance_filter']
        self.gender_filter = ['Male', 'Female'][data['user']['gender_filter']]

    def __repr__(self) -> str:
        if self.birth_date == 'Unknown':
            birth_date_str = self.birth_date
        else:
            birth_date_str = self.birth_date.strftime('%Y.%m.%d')
        s = f"Profile: {self.id} - {self.name} ({self.city}) ({birth_date_str})"

        return s
