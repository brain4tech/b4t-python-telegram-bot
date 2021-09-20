# classes for polls

from .messages import User


class Poll:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.question = data_['question']
        self.options = [PollOption(option) for option in data_['options']]
        self.total_voter_count = data_['total_voter_count']
        self.is_closed = data_['is_closed']
        self.is_anonymous = data_['is_anonymous']
        self.type = data_['type']
        self.allows_multiple_answers = data_['allows_multiple_answers']
        self.correct_option_id = data_[
            'correct_option_id'] if 'correct_option_id' in data_ else None
        self.explanation = data_[
            'explanation'] if 'explanation' in data_ else None
        self.open_period = data_[
            'open_period'] if 'open_period' in data_ else None
        self.closed_data = data_[
            'closed_data'] if 'closed_data' in data_ else None


class PollOption:
    def __init__(self, data_: dict):
        self.text = data_['text']
        self.voter_count = data_['voter_count']


class PollAnswer:
    def __init__(self, data_: dict):
        self.poll_id = data_['poll_id']
        self.user = User(data_['user'])
        self.options_ids = data_['option_ids']
