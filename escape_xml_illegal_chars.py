import re

_illegal_xml_chars_RE = re.compile(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')
XML_PREDEFINED_ENTITIES = {
    "<": "&#60;",
    "&": "&#38;",
    ">": "&#62;",
    "'": "&#39;",
    '"': "&#34;",
}


def escape_xml_illegal_chars(val, replacement='?'):
    """Filter out characters that are illegal in XML.

    Looks for any character in val that is not allowed in XML
    and replaces it with replacement ('?' by default).

    >>> escape_xml_illegal_chars("foo \x0c bar")
    'foo ? bar'
    >>> escape_xml_illegal_chars("foo \x0c\x0c bar")
    'foo ?? bar'
    >>> escape_xml_illegal_chars("foo \x1b bar")
    'foo ? bar'
    >>> escape_xml_illegal_chars(u"foo \uFFFF bar")
    u'foo ? bar'
    >>> escape_xml_illegal_chars(u"foo \uFFFE bar")
    u'foo ? bar'
    >>> escape_xml_illegal_chars(u"foo bar")
    u'foo bar'
    >>> escape_xml_illegal_chars(u"foo bar", "")
    u'foo bar'
    >>> escape_xml_illegal_chars(u"foo \uFFFE bar", "BLAH")
    u'foo BLAH bar'
    >>> escape_xml_illegal_chars(u"foo \uFFFE bar", " ")
    u'foo   bar'
    >>> escape_xml_illegal_chars(u"foo \uFFFE bar", "\x0c")
    u'foo \x0c bar'
    >>> escape_xml_illegal_chars(u"foo \uFFFE bar", replacement=" ")
    u'foo   bar'
    """
    return _illegal_xml_chars_RE.sub(replacement, val)
