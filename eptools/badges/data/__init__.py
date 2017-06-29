import os.path as op

from ...people.contact import ATTENDEE_TYPE as roles

conference = 'ep2017'

# declaring folder paths
module_dir          = op.join(op.abspath(op.dirname(__file__)))

templates_dir       = op.join(module_dir, conference, 'templates')
badge_templates_dir = op.join(templates_dir, 'with_cut_marks')
pythonpower_dir     = op.join(templates_dir, 'python_power')
dailypasses_dir     = op.join(templates_dir, 'daily_passes')

# badges types
keynote_badge_file     = op.join(badge_templates_dir, 'keynote.svg'  )
organizer_badge_file   = op.join(badge_templates_dir, 'organizer.svg')
trainer_badge_file     = op.join(badge_templates_dir, 'trainer.svg'  )
speaker_badge_file     = op.join(badge_templates_dir, 'speaker.svg'  )
participant_badge_file = op.join(badge_templates_dir, 'participant.svg' )

# additional medals to put on the badges
medal_files = {'epsmember': op.join(templates_dir, 'epsmember.svg'),
               'volunteer': op.join(templates_dir, 'volunteer.svg'),
              }

badge_files = {roles.keynote:     keynote_badge_file,
               roles.organizer:   organizer_badge_file,
               roles.trainer:     trainer_badge_file,
               roles.speaker:     speaker_badge_file,
               roles.attendee:    participant_badge_file,
               }

# ep2016
# qrcode_color = {roles.keynote:   '87173B',
#                 roles.organizer: '96770B',
#                 roles.trainer:   '7B7D11',
#                 roles.speaker:   'BA6104',
#                 roles.attendee:  '04587D'}
#
#
# badge_color = {roles.keynote:   'b58695',
#                roles.organizer: 'e2b000',
#                roles.trainer:   'a0a319',
#                roles.speaker:   'e47400',
#                roles.attendee:  '0095d6'}
# # max number of chars for each line type
# maxlengths = {'name':    13,
#               'surname': 18,
#               'tagline': 26,
#               'company': 26,
#               'title':   26,
#               }
#
# # positions in the badges
# coordinates = {'qrcode'   : (755, -100),
#                'pypower'  : (642,  180),
#                'epsmember': (750,  200),
#                'volunteer': (695,  200),
#                }
#
#
# scales = {'qrcode': 1.1 * 60,
#           'pypower': 0.8,
#          }

# ep2017
qrcode_color = {roles.keynote:   '169ec9',
                roles.organizer: '575756',
                roles.trainer:   'ef7918',
                roles.speaker:   '005a9b',
                roles.attendee:  'cb8d05'}

badge_color = {roles.keynote:   '40c1ea',
               roles.organizer: '575756',
               roles.trainer:   'ef7918',
               roles.speaker:   '005a9b',
               roles.attendee:  'f9b00f'}

# max number of chars for each line type
maxlengths = {'name':    13,
              'surname': 18,
              'tagline': 26,
              'company': 26,
              'title':   26,
              }

# positions in the badges
coordinates = {'qrcode'   : (275, 42),
               'pypower'  : (160, 390),
               'epsmember': (265, 420),
               'volunteer': (205, 420),
               }


scales = {'qrcode': 1.4 * 60,
          'pypower': 1,
         }

# python power stars
pythonpower_svg_0 = op.join(pythonpower_dir, '0.svg')
pythonpower_svg_1 = op.join(pythonpower_dir, '1.svg')
pythonpower_svg_2 = op.join(pythonpower_dir, '2.svg')
pythonpower_svg_3 = op.join(pythonpower_dir, '3.svg')
pythonpower_svg_4 = op.join(pythonpower_dir, '4.svg')
pythonpower_svg_5 = op.join(pythonpower_dir, '5.svg')

pythonpower_svg = {0: pythonpower_svg_0,
                   1: pythonpower_svg_1,
                   2: pythonpower_svg_2,
                   3: pythonpower_svg_3,
                   4: pythonpower_svg_4,
                   5: pythonpower_svg_5,}
