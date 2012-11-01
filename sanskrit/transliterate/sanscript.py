# -*- coding: utf-8 -*-
"""
sanskrit.transliterate.sanscript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transliteration functions for Sanskrit.

:license: MIT and BSD
"""

from __future__ import unicode_literals

BENGALI = 'bengali'
DEVANAGARI = 'devanagari'
GUJARATI = 'gujarati'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TELUGU = 'telugu'

HK = 'hk'
IAST = 'iast'
SLP1 = 'slp1'

SCHEMES = {}

class Scheme(dict):
    """Represents all of the data associated with a given scheme. In addition
    to storing whether or not a scheme is roman, :class:`Scheme` partitions
    a scheme's characters into important functional groups.

    :param data: a :class:`dict` of initial values.
    :param is_roman: `True` if the scheme is a romanization and `False`
                     otherwise.
    """

    def __init__(self, data=None, is_roman=True, ):
        super(Scheme, self).__init__(data or {})
        self.is_roman = is_roman


class SchemeMap(object):
    """Maps one :class:`Scheme` to another. This class grabs the metadata and
    character data required to run transliteration.

    :param from_scheme: the source scheme
    :param to_scheme: the destination scheme
    """

    def __init__(self, from_scheme, to_scheme):
        """Create a mapping from `from_scheme` to `to_scheme`."""
        self.marks = {}
        self.virama = {}
        self.consonants = {}
        self.other = {}
        self.from_roman = from_scheme.is_roman
        self.to_roman = to_scheme.is_roman

        for group in from_scheme:
            if group not in to_scheme:
                continue
            sub_map = {k: v for (k, v) in zip(from_scheme[group],
                                              to_scheme[group])}
            if group.endswith('marks'):
                self.marks.update(sub_map)
            elif group == 'virama':
                self.virama = sub_map
            else:
                self.other.update(sub_map)
                if group.endswith('consonants'):
                    self.consonants.update(sub_map)


def _roman(data, scheme_map):
    """Transliterate `data` with the given `scheme_map`. This function is used
    when the source scheme is not a Brahmic scheme.

    :param data: the data to transliterate
    :param scheme_map: a dict that maps between characters in the old scheme
                       and characters in the new scheme
    """
    buf = []
    return ''.join(buf)

def _brahmic(data, scheme_map):
    """Transliterate `data` with the given `scheme_map`. This function is used
    when the source scheme is a Brahmic scheme.

    :param data: the data to transliterate
    :param scheme_map: a dict that maps between characters in the old scheme
                       and characters in the new scheme
    """
    other = scheme_map.other
    marks = scheme_map.marks
    consonants = scheme_map.consonants
    virama = scheme_map.virama
    to_roman = scheme_map.to_roman

    buf = []
    had_consonant = False
    append = buf.append

    for L in data:
        if L in marks:
            append(marks[L])
        elif L in virama:
            append(virama[L])
        else:
            if had_consonant:
                append('a')
            append(other.get(L, L))
        had_consonant = to_roman and L in consonants

    if had_consonant:
        append('a')
    return ''.join(buf)

def transliterate(data, _from=None, _to=None, scheme_map=None):
    """Transliterate `data` with the given parameters::

        output = transliterate('idam adbhutam', HK, DEVANAGARI)

    Each time the function is called, a new :class:`SchemeMap` is created
    to map the input scheme to the output scheme. This operation is fast
    enough for most use cases. But for higher performance, you can pass a
    pre-computed :class:`SchemeMap` instead::

        scheme_map = SchemeMap(SCHEMES[HK], SCHEMES[DEVANAGARI])
        output = transliterate('idam adbhutam', scheme_map=scheme_map)

    :param data: the data to transliterate
    :param _from: the name of a source scheme
    :param _to: the name of a destination scheme
    :param scheme_map: the :class:`SchemeMap` to use. If specified, ignore
                       `_from` and `_to`. If unspecified, create a
                       :class:`SchemeMap` from `_from` to `_to`.
    """
    if scheme_map is None:
        from_scheme = SCHEMES[_from]
        to_scheme = SCHEMES[_to]
        scheme_map = SchemeMap(from_scheme, to_scheme)

    if scheme_map.from_roman:
        return _roman(data, scheme_map)
    else:
        return _brahmic(data, scheme_map)

def _setup():
    """Add a variety of default schemes."""
    s = unicode.split

    SCHEMES.update({
        BENGALI: Scheme({
            'vowels': s("""অ আ ই ঈ উ ঊ ঋ ৠ ঌ ৡ এ ঐ ও ঔ"""),
            'marks': s("""া ি ী ু ূ ৃ ৄ ৢ ৣ ে ৈ ো ৌ"""),
            'virama': s('্'),
            'other': s('ং ঃ ঁ'),
            'consonants': s("""
                            ক খ গ ঘ ঙ
                            চ ছ জ ঝ ঞ
                            ট ঠ ড ঢ ণ
                            ত থ দ ধ ন
                            প ফ ব ভ ম
                            য র ল ব
                            শ ষ স হ
                            ळ ক্ষ জ্ঞ
                            """),
            'symbols': s("""
                       ॐ ঽ । ॥
                       ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯
                       """)
        }, is_roman=False),
        DEVANAGARI: Scheme({
            'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ"""),
            'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ"""),
            'virama': s('्'),
            'other': s('ं ः ँ'),
            'consonants': s("""
                            क ख ग घ ङ
                            च छ ज झ ञ
                            ट ठ ड ढ ण
                            त थ द ध न
                            प फ ब भ म
                            य र ल व
                            श ष स ह
                            ळ क्ष ज्ञ
                            """),
            'symbols': s("""
                       ॐ ऽ । ॥
                       ० १ २ ३ ४ ५ ६ ७ ८ ९
                       """)
        }, is_roman=False),
        GUJARATI: Scheme({
            'vowels': s("""અ આ ઇ ઈ ઉ ઊ ઋ ૠ ઌ ૡ એ ઐ ઓ ઔ"""),
            'marks': s("""ા િ ી ુ ૂ ૃ ૄ ૢ ૣ ે ૈ ો ૌ"""),
            'virama': s('્'),
            'other': s('ં ઃ ઁ'),
            'consonants': s("""
                            ક ખ ગ ઘ ઙ
                            ચ છ જ ઝ ઞ
                            ટ ઠ ડ ઢ ણ
                            ત થ દ ધ ન
                            પ ફ બ ભ મ
                            ય ર લ વ
                            શ ષ સ હ
                            ળ ક્ષ જ્ઞ
                            """),
            'symbols': s("""
                       ૐ ઽ ૤ ૥
                       ૦ ૧ ૨ ૩ ૪ ૫ ૬ ૭ ૮ ૯
                       """)
        }, is_roman=False),
        HK: Scheme({
            'vowels': s("""a A i I u U R RR lR lRR e ai o au"""),
            'marks': s("""A i I u U R RR lR lRR e ai o au"""),
            'virama': [''],
            'other': s('M H ~'),
            'consonants': s("""
                            k kh g gh G
                            c ch j jh J
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            z S s h
                            L kS jJ
                            """),
            'symbols': s("""
                       OM ' | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }),
        IAST: Scheme({
            'vowels': s("""a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"""),
            'marks': s("""ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"""),
            'virama': [''],
            'other': s('ṃ ḥ m̐'),
            'consonants': s("""
                            k kh g gh ṅ
                            c ch j jh ñ
                            ṭ ṭh ḍ ḍh ṇ
                            t th d dh n
                            p ph b bh m
                            y r l v
                            ś ṣ s h
                            ḻ kṣ jñ
                            """),
            'symbols': s("""
                       oṃ ' । ॥
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }),
        KANNADA: Scheme({
            'vowels': s("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ"""),
            'marks': s("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೇ ೈ ೋ ೌ"""),
            'virama': s('್'),
            'other': s('ಂ ಃ ँ'),
            'consonants': s("""
                            ಕ ಖ ಗ ಘ ಙ
                            ಚ ಛ ಜ ಝ ಞ
                            ಟ ಠ ಡ ಢ ಣ
                            ತ ಥ ದ ಧ ನ
                            ಪ ಫ ಬ ಭ ಮ
                            ಯ ರ ಲ ವ
                            ಶ ಷ ಸ ಹ
                            ಳ ಕ್ಷ ಜ್ಞ
                            """),
            'symbols': s("""
                       ಓಂ ऽ । ॥
                       ೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯
                       """)
        }, is_roman=False),
        MALAYALAM: Scheme({
            'vowels': s("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ"""),
            'marks': s("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ േ ൈ ോ ൌ"""),
            'virama': s('്'),
            'other': s('ം ഃ ँ'),
            'consonants': s("""
                            ക ഖ ഗ ഘ ങ
                            ച ഛ ജ ഝ ഞ
                            ട ഠ ഡ ഢ ണ
                            ത ഥ ദ ധ ന
                            പ ഫ ബ ഭ മ
                            യ ര ല വ
                            ശ ഷ സ ഹ
                            ള ക്ഷ ജ്ഞ
                            """),
            'symbols': s("""
                       ഓം ഽ । ॥
                       ൦ ൧ ൨ ൩ ൪ ൫ ൬ ൭ ൮ ൯
                       """)
        }, is_roman=False),
        SLP1: Scheme({
            'vowels': s("""a A i I u U f F x X e E o O"""),
            'marks': s("""A i I u U f F x X e E o O"""),
            'virama': [''],
            'other': s('M H ~'),
            'consonants': s("""
                            k K g G N
                            c C j J Y
                            w W q Q R
                            t T d D n
                            p P b B m
                            y r l v
                            S z s h
                            L kz jY
                            """),
            'symbols': s("""
                       oM ' . ..
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }),
        TELUGU: Scheme({
            'vowels': s("""అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ"""),
            'marks': s("""ా ి ీ ు ూ ృ ౄ ౢ ౣ ే ై ో ౌ"""),
            'virama': s('్'),
            'other': s('ం ః ఁ'),
            'consonants': s("""
                            క ఖ గ ఘ ఙ
                            చ ఛ జ ఝ ఞ
                            ట ఠ డ ఢ ణ
                            త థ ద ధ న
                            ప ఫ బ భ మ
                            య ర ల వ
                            శ ష స హ
                            ళ క్ష జ్ఞ
                            """),
            'symbols': s("""
                       ఓం ఽ । ॥
                       ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯
                       """)
        }, is_roman=False)
    })

_setup()