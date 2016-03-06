import os.path as op

from ...people.contact import ATTENDEE_TYPE as roles

# declaring folder paths
module_dir          = op.abspath(op.dirname(__file__))

templates_dir       = op.join(module_dir,    'templates')
badge_templates_dir = op.join(templates_dir, 'with_cut_marks')
pythonpower_dir     = op.join(templates_dir, 'python_power')
dailypasses_dir     = op.join(templates_dir, 'daily_passes')

# badges types
keynote_badge_file     = op.join(badge_templates_dir, 'keynote_2.svg'  )
organizer_badge_file   = op.join(badge_templates_dir, 'organizer_2.svg')
trainer_badge_file     = op.join(badge_templates_dir, 'trainer_2.svg'  )
speaker_badge_file     = op.join(badge_templates_dir, 'speaker_2.svg'  )
participant_badge_file = op.join(badge_templates_dir, 'attendee_2.svg' )

badge_files = {roles.keynote:     keynote_badge_file,
               roles.organizer:   organizer_badge_file,
               roles.trainer:     trainer_badge_file,
               roles.speaker:     speaker_badge_file,
               roles.participant: participant_badge_file,
               }

badge_color = {roles.keynote:   'e37500',
               roles.organizer: 'bc445c',
               roles.trainer:   '5e9e90',
               roles.speaker:   'a98700', #'e2b000',
               roles.attendee:  'a3150e'}

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

# positions in the badges
coordinates = {'qrcode_x': 217.4,
               'qrcode_y': 337, #336.4
               'qrcode_size': 0.985 * 60,
               'stars_x': 190.866,
               'stars_y': 120.8,
               'stars_scale': 0.8,
               'badge_text_maxlength': 33,
               }
