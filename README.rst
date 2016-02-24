Google i18n address
===========================================================================================

|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons|

This package contains a copy of `Google's i18n
address <http://i18napis.appspot.com/address>`_ metadata repository
that contains great data but comes with no uptime guarantees.

Contents of this package will allow you to programatically build address
forms that adhere to rules of a particular region or country, validate
local addresses and format them to produce a valid address label for
delivery.

The package also contains a Python interface for address validation.

Addresses validation
--------------------

Method ``validate_areas`` returns two objects, first one is a dict with
errors, second one in tuple with validation data.

Errors dict
~~~~~~~~~~~

Address validation with only country code:

.. code:: python

    >>> from i18naddress import validate_areas
    >>> errors_dict, validation = validate_areas(country_code='US')
    >>> errors_dict
    {'city': 'required',
     'country_area': 'required',
     'postal_code': 'required',
     'street_address': 'required'}

With correct address:

.. code:: python

    >>> from i18naddress import validate_areas
    >>> errors_dict, validation = validate_areas(
        country_code='US',
        country_area="CA",
        city="Mountain View",
        city_area=None,
        postal_code="94043",
        street_address="1600 Amphitheatre Pkwy")
    >>> errors_dict
    {}

Incorrect postal code for California state:

.. code:: python

    >>> from i18naddress import validate_areas
    >>> errors_dict, validation = validate_areas(
        country_code='US',
        country_area="CA",
        city="Mountain View",
        city_area=None,
        postal_code="74043",
        street_address="1600 Amphitheatre Pkwy")
    >>> errors_dict
    {'postal_code': 'invalid'}

Validation tuple
~~~~~~~~~~~~~~~~

Second returned value is ``namedtuple`` with keys: ``require``,
``country_area_keys``, ``country_area_choices``, ``city_keys``,
``city_choices``, ``city_area_keys``, ``city_area_choices``,
``postal_code_regexp``, ``postal_code_example``.

.. code:: python

    >>> from i18naddress import validate_areas
    >>> errors_dict, validation = validate_areas(country_code='US')
    >>> validation
    ValidationData(
     require=('street_address', 'city', 'country_area', 'postal_code'),
     country_area_keys=['AL', ... 'WY'],
     country_area_choices=[('AL', 'Alabama'), ... ('WY', 'Wyoming')],
     city_keys=None,
     city_choices=None,
     city_area_keys=None,
     city_area_choices=None,
     postal_code_regexp=re.compile('(\\d{5})(?:[ \\-](\\d{4}))?'),
     postal_code_example='95014,22162-1010')

Raw Google's i18n data
----------------------

All raw data are stored in ``I18nCountryData`` dict like object:

.. code:: python

    >>> from i18naddress import I18nCountryData
    >>> i18n_country_data = I18nCountryData()
    >>> i18n_country_data['US']
    {'fmt': '%N%n%O%n%A%n%C, %S %Z',
     'id': 'data/US',
     'key': 'US',
     'lang': 'en',
     'languages': 'en',
     'name': 'UNITED STATES',
     'posturl': 'https://tools.usps.com/go/ZipLookupAction!input.action',
     'require': 'ACSZ',
     'state_name_type': 'state',
     'sub_keys': 'AL~AK~AS~AZ~AR~AA~AE~AP~CA~CO~CT~DE~DC~FL~GA~GU~HI~ID~IL~IN~IA~KS~KY~LA~ME~MH~MD~MA~MI~FM~MN~MS~MO~MT~NE~NV~NH~NJ~NM~NY~NC~ND~MP~OH~OK~OR~PW~PA~PR~RI~SC~SD~TN~TX~UT~VT~VI~VA~WA~WV~WI~WY',
     'sub_names': 'Alabama~Alaska~American Samoa~Arizona~Arkansas~Armed Forces (AA)~Armed Forces (AE)~Armed Forces (AP)~California~Colorado~Connecticut~Delaware~District of Columbia~Florida~Georgia~Guam~Hawaii~Idaho~Illinois~Indiana~Iowa~Kansas~Kentucky~Louisiana~Maine~Marshall Islands~Maryland~Massachusetts~Michigan~Micronesia~Minnesota~Mississippi~Missouri~Montana~Nebraska~Nevada~New Hampshire~New Jersey~New Mexico~New York~North Carolina~North Dakota~Northern Mariana Islands~Ohio~Oklahoma~Oregon~Palau~Pennsylvania~Puerto Rico~Rhode Island~South Carolina~South Dakota~Tennessee~Texas~Utah~Vermont~Virgin Islands~Virginia~Washington~West Virginia~Wisconsin~Wyoming',
     'sub_zipexs': '35000,36999~99500,99999~96799~85000,86999~71600,72999~34000,34099~09000,09999~96200,96699~90000,96199~80000,81999~06000,06999~19700,19999~20000,20099:20200,20599:56900,56999~32000,33999:34100,34999~30000,31999:39800,39899:39901~96910,96932~96700,96798:96800,96899~83200,83999~60000,62999~46000,47999~50000,52999~66000,67999~40000,42799~70000,71599~03900,04999~96960,96979~20600,21999~01000,02799:05501:05544~48000,49999~96941,96944~55000,56799~38600,39799~63000,65999~59000,59999~68000,69999~88900,89999~03000,03899~07000,08999~87000,88499~10000,14999:06390:00501:00544~27000,28999~58000,58999~96950,96952~43000,45999~73000,74999~97000,97999~96940~15000,19699~00600,00799:00900,00999~02800,02999~29000,29999~57000,57999~37000,38599~75000,79999:88500,88599:73301:73344~84000,84999~05000,05999~00800,00899~20100,20199:22000,24699~98000,99499~24700,26999~53000,54999~82000,83199:83414',
     'sub_zips': '3[56]~99[5-9]~96799~8[56]~71[6-9]|72~340~09~96[2-6]~9[0-5]|96[01]~8[01]~06~19[7-9]~20[02-5]|569~3[23]|34[1-9]~3[01]|398|39901~969([1-2]\\d|3[12])~967[0-8]|9679[0-8]|968~83[2-9]~6[0-2]~4[67]~5[0-2]~6[67]~4[01]|42[0-7]~70|71[0-5]~039|04~969[67]~20[6-9]|21~01|02[0-7]|05501|05544~4[89]~9694[1-4]~55|56[0-7]~38[6-9]|39[0-7]~6[3-5]~59~6[89]~889|89~03[0-8]~0[78]~87|88[0-4]~1[0-4]|06390|00501|00544~2[78]~58~9695[0-2]~4[3-5]~7[34]~97~969(39|40)~1[5-8]|19[0-6]~00[679]~02[89]~29~57~37|38[0-5]~7[5-9]|885|73301|73344~84~05~008~201|2[23]|24[0-6]~98|99[0-4]~24[7-9]|2[56]~5[34]~82|83[01]|83414',
     'upper': 'CS',
     'zip': '(\\d{5})(?:[ \\-](\\d{4}))?',
     'zip_name_type': 'zip',
     'zipex': '95014,22162-1010'}
    >>> i18n_country_data['US', 'CA']
    {'id': 'data/US/CA',
     'key': 'CA',
     'lang': 'en',
     'name': 'California',
     'zip': '9[0-5]|96[01]',
     'zipex': '90000,96199'}

Used with Django form
---------------------

.. code:: python

    from collections import defaultdict

    from i18naddress import validate_areas
    from django import forms
    from django.utils.translation import ugettext as _


    class AddressForm(forms.Form):

        COUNTRY_CHOICES = [
            ('CN', 'China'),
            ('US', 'United States of America')]

        name = forms.CharField(required=True)
        company_name = forms.CharField(required=False)
        address = forms.CharField(required=False)
        city = forms.CharField(required=False)
        city_area = forms.CharField(required=False)
        country = forms.ChoiceField(required=True, choices=COUNTRY_CHOICES)
        country_area = forms.CharField(required=False)
        postal_code = forms.CharField(required=False)

        def clean(self):
            clean_data = super(AddressForm, self).clean()
            if 'country' in clean_data:
                self.validate_areas(
                    clean_data['country'], clean_data.get('country_area'),
                    clean_data.get('city'), clean_data.get('city_area'),
                    clean_data.get('postal_code'),
                    clean_data.get('address'))
            return clean_data

        def validate_areas(self, country_code, country_area,
                           city, city_area, postal_code, street_address):
            error_messages = defaultdict(
                lambda: _('Invalid value'), self.fields['country'].error_messages)
            errors, validation = validate_areas(
                country_code, country_area, city,
                city_area, postal_code, street_address)

            if 'country' in errors:
                self.add_error('country', _(
                    '%s is not supported country code.' % country_code))
            if 'street_address' in errors:
                error = error_messages[errors['street_address']] % {
                    'value': street_address}
                self.add_error('street_address_1', error)
            if 'city' in errors:
                error = error_messages[errors['city']] % {
                    'value': city}
                self.add_error('city', error)
            if 'city_area' in errors:
                error = error_messages[errors['city_area']] % {
                    'value': city_area}
                self.add_error('city_area', error)
            if 'country_area' in errors:
                error = error_messages[errors['country_area']] % {
                    'value': country_area}
                self.add_error('country_area', error)
            if 'postal_code' in errors:
                if errors['postal_code'] == 'invalid':
                    postal_code_example = validation.postal_code_example
                    if postal_code_example:
                        error = _(
                            'Invalid postal code. Ex. %(example)s') % {
                                        'example': postal_code_example}
                    else:
                        error = _('Invalid postal code.')
                else:
                    error = error_messages[errors['postal_code']] % {
                        'value': postal_code}
                self.add_error('postal_code', error)

.. image:: https://ga-beacon.appspot.com/UA-10159761-14/mirumee/google-i18n-address?pixel

.. |codecov.io| image:: https://img.shields.io/codecov/c/github/mirumee/google-i18n-address.svg
   :target: https://codecov.io/github/mirumee/google-i18n-address?branch=master
.. |Circle CI| image:: https://img.shields.io/circleci/project/mirumee/google-i18n-address.svg
   :target: https://circleci.com/gh/mirumee/google-i18n-address/tree/master
.. |PyPi downloads| image:: https://img.shields.io/pypi/dm/google-i18n-address.svg
   :target: https://pypi.python.org/pypi/google-i18n-address
.. |PyPi pythons| image:: https://img.shields.io/pypi/pyversions/google-i18n-address.svg
   :target: https://pypi.python.org/pypi/google-i18n-address
.. |PyPi version| image:: https://img.shields.io/pypi/v/google-i18n-address.svg
   :target: https://pypi.python.org/pypi/google-i18n-address
.. |GitHub| image:: https://img.shields.io/github/stars/mirumee/google-i18n-address.svg?style=social
   :target: https://github.com/mirumee/google-i18n-address
.. |requires.io| image:: https://img.shields.io/requires/github/mirumee/google-i18n-address.svg
   :target: https://requires.io/github/mirumee/google-i18n-address/requirements/?branch=master
