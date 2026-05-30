import webbrowser

from worlds.LauncherComponents import Component, Type, components, icon_paths


def run_client(*args: str) -> None:
    from urllib.parse import urlencode

    from CommonClient import get_base_parser, handle_url_arg

    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    query = ""
    if launch_args.name and launch_args.connect:
        query = "?" + urlencode({
            "player": launch_args.name,
            "server": f"{launch_args.url.hostname}:{launch_args.url.port}",
            "password": launch_args.password,
        })

    webbrowser.open("https://starwort.github.io/suikapelago/" + query)

icon_paths["Suikapelago"] = "ap:worlds.suikapelago/icon.png"

components.append(
    Component(
        "Suikapelago Client",
        func=run_client,
        game_name="Suikapelago",
        icon="Suikapelago",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
