# class for dices

class Dice:
    DICE = "🎲"
    BULLSEYE = "🎯"
    BASKETBALL = "🏀"
    SOCCER = "⚽",
    BOWLING = "🎳"
    SLOTMACHINE = "🎰"

    def __init__(self, data_: dict):
        self.emoji = data_['emoji']
        self.value = data_['value']

