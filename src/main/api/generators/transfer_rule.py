import random

class TransferRule:
    MIN_TRANSFER_AMOUNT = 500
    MAX_TRANSFER_AMOUNT = 10000



    @staticmethod
    def generate_valid_transfer_amount(balance: float) -> int:
        max_amount = min(int(balance), TransferRule.MAX_TRANSFER_AMOUNT)

        if balance <= TransferRule.MIN_TRANSFER_AMOUNT:
            raise ValueError("Денег на счете недостаточно для минимального перевода")
        return random.randint(TransferRule.MIN_TRANSFER_AMOUNT + 1, max_amount)

    @staticmethod
    def generate_invalid_transfer_amount() -> int:
        return random.randint(1, TransferRule.MIN_TRANSFER_AMOUNT)