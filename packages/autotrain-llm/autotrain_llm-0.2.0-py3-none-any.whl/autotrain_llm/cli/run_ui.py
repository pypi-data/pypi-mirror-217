from argparse import ArgumentParser

from . import BaseCommand


def run_app_command_factory(args):
    return RunUICommand(args.port, args.host)


class RunUICommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        run_ui_parser = parser.add_parser(
            "ui",
            description="✨ Run autotrain-llm ui",
        )
        run_ui_parser.add_argument(
            "--port",
            type=int,
            default=7860,
            help="Port to run the app on",
            required=False,
        )
        run_ui_parser.add_argument(
            "--host",
            type=str,
            default="127.0.0.1",
            help="Host to run the app on",
            required=False,
        )
        run_ui_parser.set_defaults(func=run_app_command_factory)

    def __init__(self, port, host):
        self.port = port
        self.host = host

    def run(self):
        from ..ui.app import main

        demo = main()
        demo.launch()
