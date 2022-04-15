from src.infra.orm.factories.products import ProductsFactory
from src.infra.orm.factories.user import UserFactory

__all__ = ["ProductsFactory","UserFactory"]

"""
    Como usar os factories:

        Criando uma entity populada de src.app.modules.catalogs.entities
            provider = ProviderFactory() #'Não sera persistido no bando'
            provider = ProviderFactory(name='Nome do Provider', document='31123456100023') #'Não sera persistido no bando'

        Criando uma entity populada de src.app.modules.catalogs.entities e persistindo no banco
            provider = ProviderFactory.create()
            provider = ProviderFactory.create(name='Nome do Provider', document='31123456100023')

        Criando uma lista de entities populadas de src.app.modules.catalogs.entities
            providers = ProviderFactory.batch_build(4) #'Não sera persistido no bando'

        Criando uma lista de entities populadas de src.app.modules.catalogs.entities e persistindo no banco
            providers = ProviderFactory.batch_create(7)
"""
