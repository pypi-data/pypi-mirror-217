from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch

from cloudshell.networking.juniper.command_actions.system_actions import SystemActions


class TestSystemActions(TestCase):
    def setUp(self):
        self._cli_service = create_autospec("cloudshell.cli.cli_service.CliService")
        self._logger = Mock()
        self._instance = SystemActions(self._cli_service)

    def test_init(self):
        self.assertIs(self._instance._cli_service, self._cli_service)

    @patch(
        "cloudshell.networking.juniper.command_actions."
        "system_actions.command_template"
    )
    @patch(
        "cloudshell.networking.juniper.command_actions."
        "system_actions.CommandTemplateExecutor"
    )
    def test_reboot(self, command_template_executor, command_template):
        output = Mock()
        execute_command = Mock()
        command_template_executor.return_value = execute_command
        execute_command.execute_command.return_value = output
        timeout = Mock()
        self.assertIs(self._instance.reboot(timeout), output)
        command_template_executor.assert_called_once_with(
            self._cli_service, command_template.REBOOT, timeout=timeout
        )
        execute_command.execute_command.assert_called_once_with()

    @patch(
        "cloudshell.networking.juniper.command_actions."
        "system_actions.command_template"
    )
    @patch(
        "cloudshell.networking.juniper.command_actions."
        "system_actions.CommandTemplateExecutor"
    )
    def test_shutdown(self, command_template_executor, command_template):
        output = Mock()
        execute_command = Mock()
        command_template_executor.return_value = execute_command
        execute_command.execute_command.return_value = output
        self.assertIs(self._instance.shutdown(), output)
        command_template_executor.assert_called_once_with(
            self._cli_service, command_template.SHUTDOWN
        )
        execute_command.execute_command.assert_called_once_with()

    @patch(
        "cloudshell.networking.juniper.command_actions."
        "system_actions.command_template"
    )
    @patch(
        "cloudshell.networking.juniper.command_actions."
        "system_actions.CommandTemplateExecutor"
    )
    def test_load_firmware(self, command_template_executor, command_template):
        output = Mock()
        execute_command = Mock()
        command_template_executor.return_value = execute_command
        execute_command.execute_command.return_value = output
        src_path = Mock()
        self.assertIs(self._instance.load_firmware(src_path), output)
        command_template_executor.assert_called_once_with(
            self._cli_service, command_template.FIRMWARE_UPGRADE, timeout=600
        )
        execute_command.execute_command.assert_called_once_with(src_path=src_path)
