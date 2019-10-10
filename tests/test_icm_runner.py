from unittest import TestCase
from unittest.mock import patch
from icm_runner import Runner


@patch('icm_runner.requests')
class TestRunner(TestCase):
    """
    Test cases for icm_runner.py
    """

    def test_get_token(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.post.return_value.json.return_value = {'token': 'blah'}
        mock_req.post.return_value.status_code = 200
        Runner().get_token('', '')

    def test_build_header(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        fixture_header = {'authorization': 'bearer ', 'model': 'fake_model', 'content-type': 'application/json'}
        header = Runner().build_header('fake_model')
        self.assertEqual(fixture_header, header)

    def test_get_process_id(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'activation': 'Enabled',
              'childScheduleItems': [],
              'id': 1,
              'lastRun': '2019-02-01T12:10:33.757Z',
              'lastRunStatus': 'Success',
              'name': 'test1',
              'nextRun': '0001-01-01T00:00:00',
              'order': 1,
              'scheduleItemType': 'Folder',
              'settings': {'emailOnFailure': True,
                           'emailOnSuccess': True,
                           'enableRetries': False,
                           'externalToolTimeout': 0,
                           'failEmails': ['test@test.com'],
                           'isGlobal': False,
                           'overrideChildSettings': False,
                           'scheduleItemId': 1,
                           'schedulerSettingsId': 7,
                           'stopOnFailure': True,
                           'stopToolOnTimeout': False,
                           'successEmails': ['test@test.com'],
                           'version': {'rowVersion': 1}},
              'version': {'rowVersion': 1}}, ]
        mock_req.get.return_value.status_code = 200
        activity_id = Runner().get_process_id('test', 'test1')
        self.assertEqual(int(activity_id), 1)

    def test_run_process_by_id(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.post.return_value.json.return_value = \
            {'completedactivities': 'api/v1/completedactivities/1',
              'liveactivities': 'api/v1/liveactivities/1'}
        mock_req.post.return_value.status_code = 200
        activity_id = Runner().run_process_by_id('test', '1')
        self.assertEqual(int(activity_id), 1)

    def test_run_process_by_name(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.post.return_value.json.return_value = \
            {'completedactivities': 'api/v1/completedactivities/1',
              'liveactivities': 'api/v1/liveactivities/1'}
        mock_req.post.return_value.status_code = 200
        mock_req.get.return_value.json.return_value = \
            [{'activation': 'Enabled',
              'childScheduleItems': [],
              'id': 1,
              'lastRun': '2019-02-01T12:10:33.757Z',
              'lastRunStatus': 'Success',
              'name': 'test1',
              'nextRun': '0001-01-01T00:00:00',
              'order': 1,
              'scheduleItemType': 'Folder',
              'settings': {'emailOnFailure': True,
                           'emailOnSuccess': True,
                           'enableRetries': False,
                           'externalToolTimeout': 0,
                           'failEmails': ['test@test.com'],
                           'isGlobal': False,
                           'overrideChildSettings': False,
                           'scheduleItemId': 1,
                           'schedulerSettingsId': 7,
                           'stopOnFailure': True,
                           'stopToolOnTimeout': False,
                           'successEmails': ['test@test.com'],
                           'version': {'rowVersion': 1}},
              'version': {'rowVersion': 1}}, ]
        mock_req.get.return_value.status_code = 200
        activity_id = Runner().run_process_by_name('test', 'test1')
        self.assertEqual(int(activity_id), 1)

    def test_get_live_activity_status(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 1,
              'userId': 'test',
              'type': 'Calculation',
              'status': 'Running',
              'percent': 99}, ]
        mock_req.get.return_value.status_code = 200
        mock_res = {'message': 'Running', 'value': 99, 'IsUnitTest': False}
        res = Runner().get_live_activity_status('test', '1')
        self.assertEqual(mock_res, res)

    def test_get_all_completed_activities(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 1,
              'status': 'Completed',
              'message': 'Test Successful'}, ]
        mock_req.get.return_value.status_code = 200
        mock_res = \
            [{'progressId': 1,
              'status': 'Completed',
              'message': 'Test Successful'}, ]
        res = Runner().get_all_completed_activities('test')
        self.assertEqual(mock_res, res)

    def test_get_completed_activity_status(self, mock_req):
        """
        :param mock_req:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 1,
              'type': 'Calculation',
              'status': 'Completed',
              'message': 'Test Successful'}, ]
        mock_req.get.return_value.status_code = 200
        mock_res = {'message': 'Test Successful', 'value': 'Completed', 'IsUnitTest': False}
        res = Runner().get_completed_activity_status('test', '1')
        self.assertEqual(mock_res, res)

    def test_monitor_activity_complete(self, mock_req):
        """"
        :param mock_req:
        :return:
        """
        mock_req.get.return_value.status_code = 200
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 1,
              'status': 'Completed',
              'message': 'Test Completed successfully',
              'percent': 100}, ]
        res = Runner().monitor_activity('test', '1')
        self.assertEqual(1, res)

    def test_monitor_activity_live(self, mock_req):
        """"
        :param mock_req:
        :return:
        """
        mock_req.get.return_value.status_code = 200
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 2,
              'status': 'Completed',
              'message': 'Test Completed successfully',
              'type': 'Test',
              'percent': 100,
              'IsUnitTest': True}, ]
        res = Runner().monitor_activity('test', '1')
        self.assertEqual(1, res)


if __name__ == '__main__':
    import unittest as ut
    ut.main()

