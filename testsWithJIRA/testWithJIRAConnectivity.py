import sys
import unittest
from Simulator.ProgramIncrement import ProgramIncrement
from Simulator.JIRAUtilities import JIRAUtilities

class TestWithJIRAConnectivity(unittest.TestCase):
    small_sprint_params = {
        "Sprint1": {
            "sprint_id": 0, # This will be updated on sprint creation in JIRA
            "sprint_size": 5,
            "sprint_index" : 1
        },
    }

    sprint_params = {
        "Sprint1": {
            "sprint_id": 0, # This will be updated on sprint creation in JIRA
            "sprint_size": 5,
            "sprint_index" : 1
        },
        "Sprint2": {
            "sprint_id": 0, # This will be updated on sprint creation in JIRA
            "sprint_size": 5,
            "sprint_index" : 2
       }
    }

    small_train_params = {
        "Dev Team 1": {
            "num_epics_per_PI" : 2,
            "num_stories_per_epic" : 3,
            "user_stories_board_id": 2,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 5,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person1A", "Person1B", "Person1C"]
        }
    }

    train_params = {
        "Dev Team 1": {
            "num_epics_per_PI" : 3,
            "num_stories_per_epic" : 7,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 7,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person1A", "Person1B", "Person1C"]
        },
        "Dev Team 2": {
            "num_epics_per_PI" : 3,
            "num_stories_per_epic" : 7,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 10,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person2A", "Person2B", "Person2C", "Person2D", "Person2E"]
        },
        "Dev Team 3": {
            "num_epics_per_PI" : 5,
            "num_stories_per_epic" : 4,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 5,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person3A", "Person3B", "Person3C"]
        }
    }

    def summarize_one_sprint_one_team(self, team_sprint):
        print("\nTeam %s" % team_sprint.team.name)

        print('Sprint issues')
        print(team_sprint.curr_sprint_all_content_keys)

        print('\nTransition table')
        for day_idx in range(team_sprint.sprint_size):
            print(team_sprint.transition_table.transitions[day_idx])

        stories_in_prog = []
        stories_done = []
        stories_todo = []

        for person in team_sprint.team.team_members:
            stories_done.extend(person.stories_done)
            for story in person.stories_in_progress:
                stories_in_prog.append(story.key)

        for story in team_sprint.curr_sprint_backlog.list_of_issues:
            stories_todo.append(story.key)

        print('\n%d stories done, %d in progress, %d todo' % (len(stories_done), len(stories_in_prog), len(stories_todo)))

        print('\nDone stories:')
        print(stories_done)
        print('In progress stories:')
        print(stories_in_prog)
        print('Todo stories:')
        print(stories_todo)

    def summarize_sprint(self, sprint):
        print('\n\nSUMMARY')
        for team_sprint in sprint.team_sprints:
            self.summarize_one_sprint_one_team(team_sprint)

    def setUp(self) -> None:
        print('setup')
        #self.stdoutcopy = sys.stdout
        #sys.stdout = open('C:\\Users\\503127335\\PycharmProjects\\HelloWorld\\log.txt', 'w')

    def tearDown(self) -> None:
        print('teardown')
        #sys.stdout.close()
        #sys.stdout = self.stdoutcopy

    def test_simple_PI(self):
        jira_utils = JIRAUtilities('cloud')

        one_pi = ProgramIncrement(self.small_train_params, self.small_sprint_params, jira_utils)

        one_pi.train.initialize_backlogs()

        for day_idx, sprint in enumerate(one_pi.sprints):
            print('\n\n\nSprint %s' % sprint.sprint_name)
            sprint.run_one_sprint()
            self.summarize_sprint(sprint)
            sprint.update_jira_for_sprint()

    def test_complex_PI(self):
        jira_utils = JIRAUtilities('cloud')

        one_pi = ProgramIncrement(self.train_params, self.sprint_params, jira_utils)

        one_pi.train.initialize_backlogs()

        for day_idx, sprint in enumerate(one_pi.sprints):
            print('\n\n\nSprint %s' % sprint.sprint_name)
            sprint.run_one_sprint()
            self.summarize_sprint(sprint)
            sprint.update_jira_for_sprint()


if __name__ == '__main__':
    unittest.main()