import datetime
import pytest
from freezegun import freeze_time

from xword.lib.xword_etl import extract, transform, load, etl
from xword.models.xwords import Xwords
from xword.models.sunday_titles import SundayTitles


@pytest.mark.vcr()
@freeze_time('2018-04-29 01:00:00')
def test_extract_and_transform():
    response = extract()
    content = transform(response)

    assert content['title'] == u'MIS-UNABBREVIATED'

    assert content['across_clues'] == [
        u' Projects', u' Nowhere close', u' First name on the Supreme Court',
        u' Delight', u' Supercollider bit', u' Online tracker',
        u' Country whose capital lent its name to a fabric',
        u' "___ reading too much into this?"', u' Meadows filled with loos?',
        u' Originally', u' Bar that might be dangerous', u' Ax', u' Be agreeable',
        u' Negligent', u' Old letter opener', u' Blotto',
        u' Where sailors recover from their injuries?', u' No longer edible',
        u' Square figure', u' Actor Paul of "There Will Be Blood"',
        u' Lead-in to -tainment', u' Quashes', u' Chart again',
        u' Checkpoint offense, for short', u' Gusto',
        u' Goings-on in accelerated classes?', u' "My man"',
        u' Subject for The Source magazine', u' Sch. of 30,000+ on the Mississippi',
        u" Bill's support",
        u" It dethroned Sophia as the #1 baby girl's name in the U.S. in 2014",
        u' Home for a Roman emperor', u' Onetime Bond girl ___ Wood', u' "So obvious!"',
        u' Common core?', u' Like', u' Prime-time time',
        u" Dog that doesn't offend people?", u' Come down hard, as hail',
        u' Barnyard male', u' First name on the Supreme Court',
        u' Dreyfus Affair figure', u' Subject for Ken Burns, briefly', u' Burg',
        u' Went by air?', u' Dorm monitors',
        u' Cry of devotion from a non-academy student?',
        u' Source of the line "They shall beat their swords into plowshares"',
        u' Things that may be rolled or wild', u' Soprano Tebaldi', u' Some fasteners',
        u' They aid in diagnosing A.C.L. tears', u' Funny face?',
        u' Old White House nickname', u' Morning zoo programming?',
        u' Panama City state: Abbr.', u' Substantive', u' "Don\'t doubt me!"', u' Clue',
        u' Divinity sch.', u' Chatty bird', u' Provider of aerial football views',
        u' Actress Kendrick'
    ]

    assert content['across_answers'] == [
        u'JUTS', u'FAROFF', u'RUTH', u'JOY', u'ATOM', u'COOKIE', u'SYRIA', u'AMI',
        u'WATERCLOSETFIELDS', u'NEE', u'SHOAL', u'FIRE', u'SITWELL', u'REMISS',
        u'SIRS', u'LOOPED', u'PHYSICALTHERAPYBOATS', u'BAD', u'STATUE', u'DANO',
        u'EDU', u'ENDS', u'REMAP', u'DWI', u'ELAN', u'ADVANCEDPLACEMENTNEWS',
        u'DADDYO', u'RAP', u'LSU', u'YEA', u'EMMA', u'VILLA', u'LANA', u'AHA', u'EMS',
        u'ALA', u'NINEPM', u'POLITICALLYCORRECTLAB', u'PELT', u'TOM', u'SONIA',
        u'ZOLA', u'NAM', u'TOWN', u'WAFTED', u'RAS', u'PUBLICSCHOOLILOVEYOU',
        u'ISAIAH', u'OATS', u'RENATA', u'LATCHES', u'MRIS', u'EMOJI', u'ABE',
        u'ANTEMERIDIEMRADIO', u'FLA', u'MEATY', u'ICANSO', u'HINT', u'SEM', u'MYNA',
        u'SKYCAM', u'ANNA'
    ]

    assert content['down_clues'] == [
        u' Best Picture nominee with three sequels',
        u" Pac-12 school that's not really near the Pacific",
        u' Completely, after "in"', u' Like wet makeup', u' Media watchdog grp.',
        u' Parent co. of HuffPost',
        u' Hundred Acre Wood denizen', u' Agrees to', u" Lord's domain",
        u' Fixation', u' Slice for a Reuben',
        u' Things that have slashes', u' With nothing out of place',
        u' "What other explanation is there?!"',
        u' Former "Today" show host', u' Word before pan or after Spanish',
        u' Investment figures', u' GMC truck',
        u" Like poor months for oysters, it's said", u' Mentally wiped', u' Stiff',
        u' Sch. with an annual Mystery Hunt', u' Words of compassion',
        u' Stuffed', u' Weak period',
        u' "Fifty Shades of Grey" subject, briefly', u' Symbol of China',
        u' Onetime Blu-ray rival', u' Blue-green',
        u" Albright's successor as secretary of state", u' Craft shop item',
        u' "The Sweetest Taboo" singer, 1985',
        u' Combo bets', u' Absolutely harebrained', u' Astonishment', u' Cryptanalysis org.',
        u' Queens player, for short', u' Pledge', u' ___ Poly', u' Green org.',
        u' Caesar dressing?', u' Some neckwear',
        u" Italy's ___ d'Orcia", u' Laid up',
        u' Second U.S. feature-length computer-animated movie, after "Toy Story"',
        u' Modern subject of reviews', u' Row maker', u' Elite court group',
        u' Ecuadorean coastal province known for its gold', u' Micronesian land',
        u' Some future execs',
        u' Inclined to stress?', u' Bygone gas brand with a torch in its logo',
        u" Druid's head cover", u' Studio sign',
        u' Ransack', u' Boca ___',
        u' 2007 female inductee into the National Soccer Hall of Fame', u' Hex',
        u' Our, in Tours', u' "Uncle Tom\'s Cabin" girl', u' Stave off', u' Rice dishes',
        u' Of service',
        u" Gore's successor as vice president", u' Green-skinned god of the underworld',
        u' Harley-Davidson competitor',
        u' "___ Against Evil" (IFC series)', u' Totally awesome, in slang',
        u' Role in "Thor," 2011',
        u' Islamic spirit', u' Second letter after 118-Down', u' Second letter before 115-Down',
        u' Word with camp or care', u' L.L.C. alternative', u' That: Sp.', u' Dr. ___'
    ]

    assert content['down_answers'] == [
        u'JAWS', u'UTAH', u'TOTO', u'SMEARY', u'FCC', u'AOL', u'ROO', u'OKS', u'FIEF',
        u'FETISH', u'RYE', u'URLS', u'TIDILY', u'HASTOBE', u'JANEPAULEY', u'OMELET',
        u'YIELDS', u'SIERRA', u'RLESS', u'FRIED', u'WOODEN', u'MIT', u'ICARE', u'SATED',
        u'SLUMP', u'SANDM', u'PANDA', u'HDDVD', u'TEAL', u'POWELL', u'BEAD', u'SADE',
        u'PARLAYS', u'INSANE', u'AWE', u'NSA', u'NYMET', u'COMMIT', u'CAL', u'EPA',
        u'TUNIC', u'ASCOTS', u'VAL', u'ILL', u'ANTZ', u'APP', u'HOE', u'ALLNBATEAM',
        u'ELORO', u'PALAU', u'MBAS', u'ITALIC', u'AMOCO', u'COWL', u'ONAIR', u'RIFLE',
        u'RATON', u'MIAHAMM', u'WHAMMY', u'NOTRE', u'EVA', u'DETER', u'PILAFS',
        u'USABLE', u'CHENEY', u'OSIRIS', u'YAMAHA', u'STAN', u'SICK', u'ODIN', u'JINN',
        u'IOTA', u'ETA', u'DAY', u'INC', u'ESA', u'MOM'
    ]

    assert content['debut_words'] == [
        u'PUBLICSCHOOLILOVEYOU', u'PHYSICALTHERAPYBOATS', u'POLITICALLYCORRECTLAB',
        u'WATERCLOSETFIELDS', u'ANTEMERIDIEMRADIO', u'HDDVD', u'ADVANCEDPLACEMENTNEWS',
        u'JANEPAULEY', u'HASTOBE'
    ]


@pytest.fixture()
def content():
    return dict(
        title='',
        across_answers=[],
        across_clues=[],
        down_answers=[],
        down_clues=[],
        debut_words=[],
    )


@freeze_time('2018-05-05 01:00:00')
def test_load_title(content):
    test_title = 'test_title'
    content['title'] = test_title

    load(content)
    title_entry = SundayTitles.get_all()[0]
    assert title_entry.date == datetime.date.today()
    assert title_entry.title == test_title


@freeze_time('2018-05-05 01:00:00')
def test_load_clues_and_answers(content):
    test_clue = 'test_clue'
    test_answer = 'test_answer'
    content['across_answers'].append('{}_across'.format(test_answer))
    content['down_answers'].append('{}_down'.format(test_answer))
    content['across_clues'].append('{}_across'.format(test_clue))
    content['down_clues'].append('{}_down'.format(test_clue))

    load(content)
    across_entry = Xwords.query.filter(Xwords.orientation == 'across').first()
    down_entry = Xwords.query.filter(Xwords.orientation == 'down').first()

    assert across_entry.clue == '{}_across'.format(test_clue)
    assert across_entry.answer == '{}_across'.format(test_answer)

    assert down_entry.clue == '{}_down'.format(test_clue)
    assert down_entry.answer == '{}_down'.format(test_answer)

    assert SundayTitles.get_all()[:] == []


@freeze_time('2018-05-05 01:00:00')
def test_load_debut_words(content):
    # TODO: Write me.
    debut_answer = 'debut_answer'
    non_debut_answer = 'non_debut_answer'
    test_clue = 'test_clue'
    content['debut_words'].append(debut_answer)
    content['across_answers'].extend([debut_answer, non_debut_answer])
    content['across_clues'].extend([test_clue] * 2)

    for entry in Xwords.get_all():
        if entry.answer == debut_answer:
            assert entry.debut
        else:
            assert not entry.debut
