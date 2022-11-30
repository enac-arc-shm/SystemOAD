from __future__ import annotations

from importlib_metadata import version
from pathlib import Path

from rich import box
from rich.console import RenderableType
from rich.json import JSON
from rich.markdown import Markdown
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive, watch
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Footer,
    Header,
    Input,
    Static,
    TextLog,
)
from System import (
    constrant, 
    get_services_enabled, 
    get_services_disabled, 
    get_status_dhcpd, 
    get_document_dhcp_confi, 
    get_status_dns, 
    get_document_dns_confi,
    get_list_users,
    get_scan_ports,
)

#Obtation data
constrant()
services_enabled = get_services_enabled()
services_disabled = get_services_disabled()
status_service_dhcp = get_status_dhcpd()
status_service_dns = get_status_dns()
document_dhcp_confi = get_document_dhcp_confi()
document_dns_confi = get_document_dns_confi()
list_users = get_list_users()
Info_scan_ports = get_scan_ports()

from_markup = Text.from_markup

services_enable_table = Table(
    show_edge=False,
    show_header=True,
    expand=True,
    row_styles=["none", "dim"],
    box=box.SIMPLE,
)
services_enable_table.add_column(from_markup("[white]Service"), style="white", no_wrap=True)
services_enable_table.add_column(from_markup("[green]Status"), style="green")
services_enable_table.add_column(
    from_markup("[green]Vendor"),
    style="green",
    justify="right",
    no_wrap=True,
)

for service in services_enabled:
    services_enable_table.add_row(
    service["service"],
    "{data}".format(data = service["status"]),
    "{data}".format(data = service["Vendor"]),
    )


services_disabled_table = Table(
    show_edge=False,
    show_header=True,
    expand=True,
    row_styles=["none", "dim"],
    box=box.SIMPLE,
)
services_disabled_table.add_column(from_markup("[white]Service"), style="white", no_wrap=True)
services_disabled_table.add_column(from_markup("[red]Status"), style="red")
services_disabled_table.add_column(
    from_markup("[red]Vendor"),
    style="red",
    justify="right",
    no_wrap=True,
)

for service in services_disabled:
    services_disabled_table.add_row(
    service["service"],
    "{data}".format(data = service["status"]),
    "{data}".format(data = service["Vendor"]),
    )

ports_status_table = Table(
    show_edge=False,
    show_header=True,
    expand=True,
    row_styles=["none", "dim"],
    box=box.SIMPLE,
)
ports_status_table.add_column(from_markup("[white]Service"), style="white", no_wrap=True)
ports_status_table.add_column(from_markup("[green]Status"), style="green")


for port, status in Info_scan_ports['Ports'].items():
    ports_status_table.add_row(
    str(port),
    status
    )


WELCOME_MD = """

## SystemOAD

**System Of Analysis Devices**  es un sistema de analisis de dispositivos linux que te muestra aspectos relevantes de dispositivos basados en linux, dirigido principalmente hacia servidores.

"""

DOCUMEN_DHCP = document_dhcp_confi

DOCUMENT_DNS = document_dns_confi


SERVICE_MD = """

Los servicios no instalados de forma predeterminada, principalmente aquellos servicios escenciales 
como los son los protocolos **DHCP**, **SSH**, **DNS**, entre otros.


"""

PORTS_MD = """

Nmap (Network Mapper) es un escáner de seguridad, originalmente escrito por Gordon Lyon (también conocido por su seudónimo Fyodor Vaskovich), y se usa para descubrir hosts y servicios en una red informática, Nmap envía paquetes especialmente diseñados a los hosts de destino y luego analiza sus respuestas.

Algunas de las características útiles de Nmap incluyen:

- **Host Discovery**: esto permite identificar hosts en cualquier red. Por ejemplo, enumerar los hosts que responden a las solicitudes de TCP y/o ICMP o que tienen abierto un puerto en particular.
- **Escaneo de puertos**: enumerar (contar y enumerar uno por uno) todos los puertos abiertos en los hosts de destino.
- **Detección de versión**: interrogar a los servicios de red en dispositivos remotos para determinar el nombre de la aplicación y el número de versión.
- **Detección del sistema operativo**: determinación del sistema operativo y las características del hardware de los dispositivos de red.
- Interacción mediante secuencias de comandos con el objetivo: con el motor de secuencias de comandos Nmap (NSE) y el lenguaje de programación Lua, podemos escribir fácilmente secuencias de comandos para realizar operaciones en los dispositivos de red.

"""
DATA = {
    "DHCP-Conf": get_document_dhcp_confi(),
}

USERS_MB = """

La mayoria de usuarios implementan el interprete **bin/bash** de caso contrario son usurios especiales creados por el sistema

Aquí una lista de los usuarios actuales del servidor
"""

SECTION_TITLE_MD = " {host} -> {state}".format(host = Info_scan_ports["Host"], state = Info_scan_ports["State"])


MESSAGE = """
SystemOAD analiza la información relevante de servicios y puertos en tu servidor.

La información recolectada es almacenada en un servidor online, puedes consultarlo en el siguiente enlace
[@click="app.open_link('https://console.firebase.google.com/u/0/project/api-redes-366215/firestore/data/~2Fregistros_2022~2F06Hz9jpnVV6KV0fhBP45?hl=es')"]Fire - Database[/]

Puedes consultar este proyecto en nuestro repositorio de GitHUb
[@click="app.open_link('https://github.com/enac-arc-shm/SystemOAD')"]SystemOAD GitHub Repository[/]


Nuestra página ♥ [@click="app.open_link('https://www.asage.site')"]ASAGE.site[/]

"""


class Body(Container):
    pass


class Title(Static):
    pass


class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Checkbox(value=self.app.dark)
        yield Static("Dark mode", classes="label")

    def on_mount(self) -> None:
        watch(self.app, "dark", self.on_dark_change, init=False)

    def on_dark_change(self, dark: bool) -> None:
        self.query_one(Checkbox).value = self.app.dark

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        self.app.dark = event.value


class Welcome(Container):
    def compose(self) -> ComposeResult:
        yield Static(Markdown(WELCOME_MD))
        yield Button("Start", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.add_note("[b magenta]Iniciado")
        self.app.query_one(".location-first").scroll_visible(duration=0.5, top=True)


class OptionGroup(Container):
    pass


class SectionTitle(Static):
    pass


class Message(Static):
    pass


class Version(Static):
    def render(self) -> RenderableType:
        return f"[b]v 1.0.1"


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Title("SystemOAD")
        yield OptionGroup(Message(MESSAGE), Version())
        yield DarkSwitch()


class AboveFold(Container):
    pass


class Section(Container):
    pass


class Column(Container):
    pass


class TextContent(Static):
    pass


class QuickAccess(Container):
    pass


class LocationLink(Static):
    def __init__(self, label: str, reveal: str) -> None:
        super().__init__(label)
        self.reveal = reveal

    def on_click(self) -> None:
        self.app.query_one(self.reveal).scroll_visible(top=True, duration=0.5)
        self.app.add_note(f"Sección [b]{self.reveal}[/b]")


class LoginForm(Container):
    def compose(self) -> ComposeResult:
        yield Static("Username", classes="label")
        yield Input(placeholder="Username")
        yield Static("Password", classes="label")
        yield Input(placeholder="Password", password=True)
        yield Static()
        yield Button("Login", variant="primary")


class Window(Container):
    pass


class SubTitle(Static):
    pass


class Notification(Static):
    def on_mount(self) -> None:
        self.set_timer(3, self.remove)

    def on_click(self) -> None:
        self.remove()

class DemoApp(App):
    CSS_PATH = "style.css"
    TITLE = "SystemOAD"
    BINDINGS = [
        ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+t", "app.toggle_dark", "Dark mode"),
        ("ctrl+s", "app.screenshot()", "Screenshot"),
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]

    show_sidebar = reactive(False)

    def add_note(self, renderable: RenderableType) -> None:
        self.query_one(TextLog).write(renderable)

    def compose(self) -> ComposeResult:
        example_css = "\n".join(Path(self.css_path[0]).read_text().splitlines()[:50])
        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=True),
            TextLog(classes="-hidden", wrap=False, highlight=True, markup=True),
            Body(
                QuickAccess(
                    LocationLink("Inicio", ".location-top"),
                    LocationLink("Users", ".location-users"),
                    LocationLink("Servicios", ".location-services"),
                    LocationLink("Puertos", ".location-ports"),
                ),
                AboveFold(Welcome(), classes="location-top"),
                Column(
                    Section(
                        LoginForm(),
                    ),
                    classes="location-login location-first",
                ),
                Column(
                    Section(
                        SectionTitle("Users"),
                        TextContent(Markdown(USERS_MB)),
                        DataTable(), 
                    ),
                    classes="location-users",
                ),
                Column(
                    Section(
                        SectionTitle("Servicios"),
                        TextContent(Markdown(SERVICE_MD)),
                        SectionTitle("Servicio DHCP - archivo de configuración"),
                        SubTitle(from_markup(f"[{status_service_dhcp['color']}]{status_service_dhcp['status']}", style = f"{status_service_dhcp['color']}")),
                        TextContent(Text(DOCUMEN_DHCP)),
                        SectionTitle("Servicio DNS - archivos de configuración"),
                        SubTitle(from_markup(f"[{status_service_dns['color']}]{status_service_dns['status']}", style = f"{status_service_dns['color']}")),
                        TextContent(Text(DOCUMENT_DNS)),
                        SubTitle("Services - enabled"),
                        Static(services_enable_table, classes="table pad"),
                        SubTitle("Services - disabled"),
                        Static(services_disabled_table, classes="table pad"),
                    ),
                    classes="location-services",
                ),
                Column(
                    Section(
                        SectionTitle("Analisis de puertos"),
                        TextContent(Markdown(PORTS_MD)),
                        SectionTitle(SECTION_TITLE_MD),
                        SubTitle(from_markup(f"{Info_scan_ports['Protocol']}", style = f"GREEN")),
                        Static(ports_status_table, classes="table pad"),
                    ),
                    classes="location-ports",
                ),
            ),
        )
        yield Footer()

    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser

        webbrowser.open(link)

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")

    def on_mount(self) -> None:
        self.add_note("Servicio SystemOAD iniciado")
        table = self.query_one(DataTable)
        table.add_column("Usuario", width=20)
        table.add_column("ID", width=20)
        table.add_column("ID Grupo", width=20)
        table.add_column("Directorio", width=20)
        table.add_column("Interprete", width=20)
        table.zebra_stripes = True
        for user in list_users:
            #table.add_row(*[info for info in user])
            table.add_row(user[0], user[2], user[3], user[5], user[6])
        self.query_one("Welcome Button", Button).focus()

    def action_screenshot(self, filename: str | None = None, path: str = "./") -> None:
        """Save an SVG "screenshot". This action will save an SVG file containing the current contents of the screen.

        Args:
            filename (str | None, optional): Filename of screenshot, or None to auto-generate. Defaults to None.
            path (str, optional): Path to directory. Defaults to "./".
        """
        self.bell()
        path = self.save_screenshot(filename, path)
        message = Text.assemble("Captura de pantalla guardada en ", (f"'{path}'", "bold green"))
        self.add_note(message)
        self.screen.mount(Notification(message))


app = DemoApp()
if __name__ == "__main__":
    app.run()
