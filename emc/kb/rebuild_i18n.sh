#!/bin/sh
PRODUCTNAME='eisoo.topic'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
/home/panlei/plone41/bin/i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --merge locales/${PRODUCTNAME}-manual.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
/home/panlei/plone41/bin/i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po


