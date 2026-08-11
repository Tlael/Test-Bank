import random


class CreditRule:
    MIN_CREDIT_AMOUNT = 1
    MIN_WORKING_CREDIT_AMOUNT = 5000
    MAX_CREDIT_AMOUNT = 15000

    MIN_TERM_MONTHS = 1
    MAX_TERM_MONTHS = 60

    @staticmethod
    def generate_working_credit_amount() -> int:
        return random.randint(
            CreditRule.MIN_WORKING_CREDIT_AMOUNT,
            CreditRule.MAX_CREDIT_AMOUNT
        )

    @staticmethod
    def generate_invalid_credit_amount() -> int:
        return CreditRule.MAX_CREDIT_AMOUNT + 1

    @staticmethod
    def get_contract_valid_but_rejected_amount() -> int:
        return CreditRule.MIN_WORKING_CREDIT_AMOUNT - 1

    @staticmethod
    def generate_valid_term_months() -> int:
        return random.randint(
            CreditRule.MIN_TERM_MONTHS,
            CreditRule.MAX_TERM_MONTHS
        )