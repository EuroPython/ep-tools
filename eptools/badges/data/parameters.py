
from eptools.config import conference
from eptools.people.contact import AttendeeType

if conference in ('ep2016', 'ep2015'):
    qrcode_color = {
        AttendeeType.keynote:   '87173B',
        AttendeeType.organizer: '96770B',
        AttendeeType.trainer:   '7B7D11',
        AttendeeType.speaker:   'BA6104',
        AttendeeType.attendee:  '04587D'
    }

    badge_color = {
        AttendeeType.keynote:   'b58695',
        AttendeeType.organizer: 'e2b000',
        AttendeeType.trainer:   'a0a319',
        AttendeeType.speaker:   'e47400',
        AttendeeType.attendee:  '0095d6'
    }

    # max number of chars for each line type
    maxlengths = {
        'name':    13,
        'surname': 18,
        'tagline': 26,
        'company': 26,
        'title':   26,
    }

    # positions in the badges
    coordinates = {
        'qrcode'   : (755, -100),
        'pypower'  : (642,  180),
        'epsmember': (750,  200),
        'volunteer': (695,  200),
    }

    scales = {
        'qrcode': 1.1 * 60,
        'pypower': 0.8,
     }

elif conference == 'ep2017':

    import os

    module_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    templates_dir = os.path.join(module_dir, conference, "templates")
    pythonpower_dir = os.path.join(templates_dir, "python_power")

    qrcode_color = {
        AttendeeType.keynote: "169ec9",
        AttendeeType.organizer: "575756",
        AttendeeType.trainer: "ef7918",
        AttendeeType.speaker: "005a9b",
        AttendeeType.attendee: "cb8d05",
    }

    badge_color = {
        AttendeeType.keynote: "40c1ea",
        AttendeeType.organizer: "575756",
        AttendeeType.trainer: "ef7918",
        AttendeeType.speaker: "005a9b",
        AttendeeType.attendee: "f9b00f",
    }

    # max number of chars for each line type
    maxlengths = {"name": 16, "surname": 20, "tagline": 30, "company": 30, "title": 30}

    # positions in the badges
    coordinates = {"qrcode": (275, 42), "pypower": (160, 390), "epsmember": (265, 420), "volunteer": (205, 420)}

    scales = {"qrcode": 1.4 * 60, "pypower": 1}

    # python power stars
    pythonpower_svg_0 = os.path.join(pythonpower_dir, "0.svg")
    pythonpower_svg_1 = os.path.join(pythonpower_dir, "1.svg")
    pythonpower_svg_2 = os.path.join(pythonpower_dir, "2.svg")
    pythonpower_svg_3 = os.path.join(pythonpower_dir, "3.svg")
    pythonpower_svg_4 = os.path.join(pythonpower_dir, "4.svg")
    pythonpower_svg_5 = os.path.join(pythonpower_dir, "5.svg")

    pythonpower_svg = {
        0: pythonpower_svg_0,
        1: pythonpower_svg_1,
        2: pythonpower_svg_2,
        3: pythonpower_svg_3,
        4: pythonpower_svg_4,
        5: pythonpower_svg_5,
    }

elif conference == 'ep2018':

    badge_color = {
        AttendeeType.keynote: "0065bd",
        AttendeeType.organizer: "a12a5e",
        AttendeeType.trainer: "017351",
        AttendeeType.speaker: "03c383",
        AttendeeType.attendee: "faae13",
        AttendeeType.trainee: "ed5919",
    }

    qrcode_color = {
        AttendeeType.keynote: "0065bd",
        AttendeeType.organizer: "a12a5e",
        AttendeeType.trainer: "017351",
        AttendeeType.speaker: "03c383",
        AttendeeType.attendee: "faae13",
        AttendeeType.trainee: "ed5919",
    }

    # max number of chars for each line type
    maxlengths = {
        "name": 16,
        "surname": 20,
        "tagline": 30,
        "company": 30,
        "title": 30
    }

    # positions in the badges
    coordinates = {
        "qrcode": (262, 42),
        "epsmember": (265, 385),
        "volunteer": (325, 385)
    }

    scales = {"qrcode": 1.62 * 60}
