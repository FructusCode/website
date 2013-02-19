# pylint: disable=W0403
# pylint: disable=C0111

USERAGENT_NAME = "Fruct.us"
USERAGENT_VERSION = "0.1"
USERAGENT_CONTACT = "team@fruct.us"

# Initialize Payment Platforms
import core.payment
import core.payment.braintree
import core.payment.wepay

# Initialize Entity Generators
import core.entitygen
import core.entitygen.movie
import core.entitygen.music


assert core
