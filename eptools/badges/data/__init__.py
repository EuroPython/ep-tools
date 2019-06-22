import os

from eptools.config import conference
from eptools.people.contact import AttendeeType
from eptools.badges.data.parameters import (
    qrcode_color,
    coordinates,
    badge_color,
    maxlengths,
    scales
)

# declaring folder paths
module_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

templates_dir = os.path.join(module_dir, conference, "templates")
badge_templates_dir = os.path.join(templates_dir, "with_cut_marks")
pythonpower_dir = os.path.join(templates_dir, "python_power")
dailypasses_dir = os.path.join(templates_dir, "daily_passes")

# TO make this work for all previous conference, I should add an 'if' here
# here is where I decide that this is the branch 'ep2018', forget the past
keynote_badge_file = os.path.join(badge_templates_dir, "keynote.svg")
organizer_badge_file = os.path.join(badge_templates_dir, "organizer.svg")
trainer_badge_file = os.path.join(badge_templates_dir, "trainer.svg")
speaker_badge_file = os.path.join(badge_templates_dir, "speaker.svg")
participant_badge_file = os.path.join(badge_templates_dir, "conference_participant.svg")
trainee_badge_file = os.path.join(badge_templates_dir, "trainings_participant.svg")

# additional medals to put on the badges
medal_files = {
    "epsmember": os.path.join(templates_dir, "epsmember.svg"),
    "volunteer": os.path.join(templates_dir, "volunteer.svg"),
}

badge_files = {
    AttendeeType.keynote: keynote_badge_file,
    AttendeeType.organizer: organizer_badge_file,
    AttendeeType.trainer: trainer_badge_file,
    AttendeeType.speaker: speaker_badge_file,
    AttendeeType.attendee: participant_badge_file,
    AttendeeType.trainee: trainee_badge_file,
}

