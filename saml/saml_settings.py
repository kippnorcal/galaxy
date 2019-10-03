from os import getenv

from onelogin.saml2.settings import OneLogin_Saml2_Settings

saml_settings = {
    "strict": True,
    "debug": True,
    "sp": {
        "entityId": f"{getenv('APP_DOMAIN')}/metadata/",
        "assertionConsumerService": {
            "url": f"{getenv('APP_DOMAIN')}/acs/",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
        },
        "singleLogoutService": {
            "url": f"{getenv('APP_DOMAIN')}/sls/",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
        "x509cert": "",
        "privateKey": "",
    },
    "idp": {
        "entityId": getenv("SAML_ENTITY_ID"),
        "singleSignOnService": {
            "url": getenv("SAML_URL"),
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
        },
        "singleLogoutService": {
            "url": getenv("SAML_SLO"),
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
        },
        "x509cert": getenv("SAML_CERT"),
    },
}

SAML_SETTINGS = OneLogin_Saml2_Settings(settings=saml_settings)
