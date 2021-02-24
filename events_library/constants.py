class Service():
    ACCOUNTS = 'accounts'
    ORDERS = 'orders'
    PAYMENTS = 'payments'
    PROFILES = 'profiles'
    REPORTS = 'reports'
    SELFDECODE = 'selfdecode'

    @classmethod
    def not_a_service_option(cls, service_name: str):
        return service_name not in [
            cls.ACCOUNTS,
            cls.ORDERS,
            cls.PAYMENTS,
            cls.PROFILES,
            cls.REPORTS,
            cls.SELFDECODE,
        ]
