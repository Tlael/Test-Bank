import random


class DepositRule:
    MIN_DEPOSIT_AMOUNT = 1000
    MAX_DEPOSIT_AMOUNT = 9000

    @staticmethod
    def generate_valid_deposit_amount() -> int:
        return random.randint(
            DepositRule.MIN_DEPOSIT_AMOUNT + 1,
            DepositRule.MAX_DEPOSIT_AMOUNT
        )

    @staticmethod
    def generate_invalid_deposit_amount() -> int:
        return random.randint(
            1,
            DepositRule.MIN_DEPOSIT_AMOUNT
        )
