import unittest
from datetime import datetime
from datetime import timedelta

from Simulator.JIRAUtilities import JIRAUtilities

class TestJIRAUtilities(unittest.TestCase):
    _jira_inst_type = 'cloud'
    #_jira_inst_type = 'virtual_local'

    _sprint_name = "Sprint A"
    _sprint_size = 7
    _board_id = 106

    def setUp(self) -> None:
        self.jira_utils = JIRAUtilities(self._jira_inst_type)

    def tearDown(self) -> None:
        del self.jira_utils

    def test_create_sprint(self):
        start_date = datetime.now()
        sprint = self.jira_utils.create_sprint(self._board_id, self._sprint_name, start_date, self._sprint_size)

        self.assertIsNotNone(sprint)
        self.assertEqual(sprint.name, self._sprint_name)

        end_date = start_date + timedelta(days=self._sprint_size)

        start_date_str = start_date.strftime("%d/%b/%y %#I:%M %p")
        end_date_str = end_date.strftime("%d/%b/%y %#I:%M %p")

        self.assertEqual(sprint.startDate, start_date_str)
        self.assertEqual(sprint.endDate, end_date_str)

    def test_create_epic(self):
        epic = self.jira_utils.create_epic('Test Epic 1')
        self.assertEqual(epic.fields.summary, 'Test Epic 1')
        self.assertEqual(epic.fields.issuetype.name, 'Epic')

    def test_create_user_story_without_epic(self):
        story = self.jira_utils.create_user_story_with_epic('Test Story')
        self.assertEqual(story.fields.summary, 'Test Story')
        self.assertEqual(story.fields.issuetype.name, 'Story')

    def test_create_user_story_with_epic(self):
        epic = self.jira_utils.create_epic('Test Epic 2')

        story = self.jira_utils.create_user_story_with_epic('Test Story E', epic.key)

        # 10118 is the Epic Link
        self.assertEqual(story.fields.customfield_10118, epic.key)


if __name__ == '__main__':
    unittest.main()